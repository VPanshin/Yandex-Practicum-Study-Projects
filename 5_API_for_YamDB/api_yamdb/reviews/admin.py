from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров."""
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


class GenreInline(admin.TabularInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""
    inlines = [GenreInline, ]
    list_display = ('pk', 'name', 'year', 'category')
    list_editable = ('category',)
    search_fields = ('name', 'year',)
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров, относящихся к произведениям."""
    list_display = ('title', 'genre')
    list_editable = ('genre',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""
    list_display = (
        'pk',
        'title',
        'author',
        'text',
        'score',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('text', 'score', 'author')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('author',)
    empty_value_display = '-пусто-'
