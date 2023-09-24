from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    """Фильтр для Тегов и страниц с Рецептами."""
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_favorited_and_cart(self, queryset, filter_name, value):
        if self.request.user.is_authenticated and value:
            filter_parameters = {f'{filter_name}__user': self.request.user}
            return queryset.filter(**filter_parameters)
        return queryset

    def get_is_favorited(self, queryset, name, value):
        return self.get_favorited_and_cart(queryset, 'favorite_recipe', value)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return self.get_favorited_and_cart(queryset, 'shopping_cart', value)
