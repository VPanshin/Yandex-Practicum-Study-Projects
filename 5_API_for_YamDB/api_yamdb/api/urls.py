from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .v1.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UserSignupViewSet, UserViewSet, get_token,
)


router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')


auth_patterns = [
    path('auth/signup/',
         UserSignupViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('auth/token/', get_token, name='token')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_patterns))
]
