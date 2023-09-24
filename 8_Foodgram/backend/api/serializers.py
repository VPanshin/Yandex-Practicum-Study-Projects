import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Пользователя."""
    is_subscribed = serializers.SerializerMethodField(
        method_name='user_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def user_is_subscribed(self, obj: User):
        request = self.context.get("request")
        if request is None:
            return False
        user = request.user
        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(following=obj).exists()


class FollowSerializer(UserSerializer):
    """Сериалайзер для модели Подписок."""
    first_name = serializers.StringRelatedField(
        source='following.first_name'
    )
    last_name = serializers.StringRelatedField(
        source='following.last_name'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta(UserSerializer.Meta):
        model = Follow
        fields = (
            'recipes',
            'recipes_count',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def get_recipes(self, obj):
        """
        Метод реализующий способ получения рецептов для пользователей,
        на которых подписан текущий пользователь.
        """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.following)
        if limit:
            limit = int(limit)
            recipes = recipes[:limit]
        recipes_serializer = RecipeForFollowSerializer(recipes, many=True)
        return recipes_serializer.data

    def get_recipes_count(self, obj):
        """Метод для подсчета количества рецептов."""
        return Recipe.objects.filter(author=obj.following).count()


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)

    def validate_color(self, data):
        """Метод для валидации цвета."""
        if data['color'] == data['name']:
            raise serializers.ValidationError(
                'Имя не может совпадать с цветом!'
            )
        return data


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер связывающий модели Рецептов и Ингредиентов."""
    id = serializers.SlugRelatedField(
        source='ingredient.id'
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class CreateIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для отоборажения Игредиентов в поле при создании Рецепта."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Рецептов."""
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True)
    author = UserSerializer()
    image = Base64ImageField(
        required=False,
        allow_null=True
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='recipe_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='recipe_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def check_recipe_status(self, obj, model):
        """Вспомогательный метод для добавления рецептов."""
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def recipe_is_favorited(self, obj):
        """Метод проверяющий добавление рецепта в изранное."""
        return self.check_recipe_status(obj, Favorite)

    def recipe_is_in_shopping_cart(self, obj):
        """Метод проверяющий добавление рецепта в список покупок."""
        return self.check_recipe_status(obj, ShoppingCart)


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для страницы создания Рецептов."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    ingredients = CreateIngredientSerializer(many=True)
    image = Base64ImageField(max_length=None)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'ingredients',
            'cooking_time',
            'text',
            'image',
            'author',
        )

    def to_representation(self, instance):
        """Метод для представления данных в поля рецепта."""
        serializer = RecipeSerializer(instance)
        return serializer.data

    def create_ingredients_and_tags(self, ingredients, tags, model):
        """Метод для добавления игредиентов и тэгов при создании рецепта."""
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = ingredient['id']
            ingredients, created = RecipeIngredient.objects.get_or_create(
                recipe=model,
                ingredient=ingredient,
                amount=amount
            )
        model.tags.set(tags)

    def create(self, validated_data):
        """Метод для создания рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.create_ingredients_and_tags(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Метод для редактирования рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.create_ingredients_and_tags(ingredients, tags, instance)
        return super().update(instance, validated_data)


class RecipeForFollowSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для обображения Рецептов у пользователей,
    на которых подписан текущий пользователь.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания Подписки."""
    class Meta:
        model = Follow
        fields = ('user', 'following',)

    def to_representation(self, instance):
        """Метод для отображения """
        request = self.context.get('request')
        return FollowSerializer(
            instance,
            context={'request': request}).data

    def validate_following(self, data):
        """Метод для валидации подписки на себя."""
        if self.context['request'].user == data:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data
