from django.urls import include, path
from djoser.urls import authtoken, base
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register('ingredients', IngredientViewSet)

authpatterns = [
    path('auth/', include(base)),
    path('auth/', include(authtoken)),
]

urlpatterns = [
    path('', include(authpatterns)),
    path('', include(router_v1.urls)),
]
