from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitleFilter
from api.v1.permissions import (
    IsSuperUserOrIsStaffOrIsAdminOnly,
    IsSuperUserOrIsStaffOrIsAdminOrIsModeratorOrIsAuthor, ReadOnly,
)
from api.v1.serializers import (
    CategorySerializer, CommentSerializers, GenreSerializer,
    GetTokenSerializer, ReviewSerializers, TitleCreateSerializer,
    TitleReadSerializer, UserForAdminSerializer, UserSerializer,
    UserSignupSerializer,
)
from api.v1.utils import generating_and_sending_confirmation_code
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Общий класс для CategoryViewSet и GenreViewSet."""
    pass


class TitleCommonViewSet(CreateListDestroyViewSet):
    """
    Базовый (родительский) класс для CategoryViewSet, GenreViewSet
    """
    queryset = None
    serializer_class = None
    pagination_class = PageNumberPagination
    permission_classes = (IsSuperUserOrIsStaffOrIsAdminOnly | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(TitleCommonViewSet):
    """
    Для эндпоинта 'categories/' для любого пользователя:
    'get' - получение списка всех категорий.
    Для эндпоинта 'categories/' для пользователя с ролью 'admin':
    'post' - создать категорию.
    Для эндпоинта 'categories/{slug}/' для пользователя с ролью 'admin':
    'delete' - удалить категорию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(TitleCommonViewSet):
    """
    Для эндпоинта 'genres/' для любого пользователя:
    'get' - получение списка всех жанров.
    Для эндпоинта 'genres/' для пользователя с ролью 'admin':
    'post' - добавить жанр.
    Для эндпоинта 'genres/{slug}/' для пользователя с ролью 'admin':
    'delete' - удалить жанр.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Для эндпоинта 'titles/' для любого пользователя:
    'get' - получение списка всех произведений.
    Для эндпоинта 'titles/' для пользователя с ролью 'admin':
    'post' - добавить новое произведение.
    Для эндпоинта 'titles/{titles_id}/' для любого пользователя:
    'get' - получение информации о произведении.
    Для эндпоинта 'titles/{titles_id}/' для пользователя с ролью 'admin':
    'delete' - удалить произведение.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    pagination_class = PageNumberPagination
    permission_classes = (IsSuperUserOrIsStaffOrIsAdminOnly | ReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Для эндпоинта 'titles/{title_id}/reviews/' для любого пользователя:
    'get' - получение списка всех отзывов.
    Для эндпоинта 'titles/{title_id}/reviews/'
    для пользователя с ролью 'IsAuthenticated':
    'post' - добавить новый отзыв.
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/
    для любого пользователя:
    'get' - получение информации об отзыве.
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/
    для пользователя с ролью 'Author', 'admin', or 'Moderator':
    'patch' - частично обновить отзыв.
    'delete' - удалить отзыв.
    """
    serializer_class = ReviewSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsSuperUserOrIsStaffOrIsAdminOrIsModeratorOrIsAuthor,
                          IsAuthenticatedOrReadOnly)

    def get_title(self):
        "Получает объект произведения по id."
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/comments/'
    для любого пользователя:
    'get' - получение списка всех комментариев по конкретному отзыву.
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/comments/'
    для пользователя с ролью 'IsAuthenticated':
    'post' - добавить новый комментарий к отзыву.
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/comments/{comments_id}
    для любого пользователя:
    'get' - получение конкретного комментария в отзыве.
    Для эндпоинта 'titles/{title_id}/reviews/{review_id}/comments/{comments_id}
    для пользователя с ролью 'author', 'admin', or 'Moderator':
    'patch' - частично обновить комментарий в отзыве.
    'delete' - удалить комментарий в отзыве.
    """
    serializer_class = CommentSerializers
    pagination_class = PageNumberPagination
    permission_classes = (IsSuperUserOrIsStaffOrIsAdminOrIsModeratorOrIsAuthor,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва,
        где автором является текущий пользователь."""
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """
    Для эндпоинта 'users/' для пользователя с ролью 'admin':
    'get', 'post' - получение списка пользователей,
    создание нового пользователя.
    Для эндпоинта 'users/{username}' для пользователя с ролью 'admin':
    'get', 'patch', 'delete' - получение пользователя по username,
    изменение данных пользователя, удаление пользоователя.
    Для эндпоинта 'users/me/' для любого авторизованного пользователя:
    'get', 'patch' - получение персональных данных авторизованного
    пользователя, изменение всех своих полей кроме 'role'.
    """
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = [IsSuperUserOrIsStaffOrIsAdminOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            serializer_class=UserSerializer,
            pagination_class=None)
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignupViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            raise ValidationError('Этот email уже занят.')
        generating_and_sending_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """
    Для эндпоинта 'auth/token/' (при авторизации пользователя).
    Получаем токен.
    """
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    if serializer.data['confirmation_code'] == user.confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )

    return Response(
        {'field_name': ['Проверьте, что указанные данные верны.']},
        status=status.HTTP_400_BAD_REQUEST
    )
