from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


class FavoriteShoppingCartMixin:
    "Миксин для добавления и удаления избранных рецептов."
    def favorite_shopping_cart(
            self,
            request,
            id,
            model_class,
            message):
        item = get_object_or_404(Recipe, id=id)
        user = self.request.user
        if request.method == 'POST':
            instance, created = model_class.objects.get_or_create(
                user=user,
                recipe=item
            )
            return Response(
                {'message': message},
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            instance = model_class.objects.get(user=user, recipe=item)
            if instance:
                instance.delete()
                return Response(
                    {'message': message},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'message': 'Рецепт не найден в корзине или избранном'},
                status=status.HTTP_404_NOT_FOUND
            )
