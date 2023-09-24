from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError

from recipes.models import (
    Favorite,
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class RecipeIngredientForm(BaseInlineFormSet):

    def clean(self):
        super(RecipeIngredientForm, self).clean()
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            if (data.get('DELETE')):
                raise ValidationError('Нельзя удалить все ингредиенты')


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    formset = RecipeIngredientForm
    extra = 0
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, )
    list_display = ('id', 'author', 'name', 'times_added',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags',)

    def times_added(self, obj):
        return obj.favorite_recipe.all().count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following',)
    list_filter = ('following',)
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user',)
    search_fields = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user',)
    search_fields = ('user',)
