from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import RecipeFilter
from api.mixins import FavoriteShoppingCartMixin
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    CreateRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
    UserSerializer,
)
from api.utils import download_shopping_cart
from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)
from users.models import User


class UserViewSet(UserViewSet):
    """"Вьюсет для модели Пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')
    lookup_field = 'id'

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Создание и удаление подписки."""
        following = get_object_or_404(User, id=id)
        user = self.request.user
        if request.method == 'POST':
            data = {'following': following.id, 'user': user.id}
            serializer = SubscribeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(following=following, user=user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = get_object_or_404(
                Follow,
                user=user,
                following=following
            )
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """"Вьюсет для модели Тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """"Вьюсет для модели Ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet, FavoriteShoppingCartMixin):
    """"Вьюсет для модели Рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    lookup_field = 'id'

    def get_serializer_class(self):
        """
        Метод определяющий способ сериализации данных
        в зависимости от запроса.
        """
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            )
    def favorite(self, request, id):
        """Метод для добавления и удаления из избранного."""
        return self.favorite_shopping_cart(
            request,
            id,
            Favorite,
            'Рецепт успешно добавлен в избранное'
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated]
            )
    def shopping_cart(self, request, id):
        """Метод для добавления и удаления из списка покупок."""
        return self.favorite_shopping_cart(
            request,
            id,
            ShoppingCart,
            'Рецепт успешно добавлен в корзину'
        )

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated]
            )
    def download_shopping_cart(self, request):
        """Вызов метода для скачивания списка покупок."""
        return download_shopping_cart(request.user)
