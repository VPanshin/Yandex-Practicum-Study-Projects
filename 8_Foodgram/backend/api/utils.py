from django.db.models import Sum
from django.http import HttpResponse

from recipes.models import RecipeIngredient


def download_shopping_cart(user):
    """Метод реализующий скачивание списка продуктов."""
    sum_ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user).values(
        'ingredient__name', 'ingredient__measurement_unit').annotate(
        amount=Sum('amount')).order_by(
        'ingredient__name', 'amount')
    ingredients_dict = [
        f"{ingredient['ingredient__name']}"
        f"({ingredient['ingredient__measurement_unit']})"
        f"- {ingredient['amount']}"
        for ingredient in sum_ingredients
    ]
    content = '\n'.join(ingredients_dict)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shoping_cart.txt"'
    return response
