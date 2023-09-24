import csv
import os

from progress.bar import IncrementalBar

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


import_settings = {
    'category.csv': {
        'model': Category,
        'fieldnames': None,
    },
    'genre.csv': {
        'model': Genre,
        'fieldnames': None,
    },
    'titles.csv': {
        'model': Title,
        'fieldnames': ['id', 'name', 'year', 'category_id'],
    },
    'users.csv': {
        'model': User,
        'fieldnames': None,
    },
    'review.csv': {
        'model': Review,
        'fieldnames': [
            'id', 'title_id', 'text',
            'author_id', 'score', 'pub_date'
        ],
    },
    'comments.csv': {
        'model': Comment,
        'fieldnames': ['id', 'review_id', 'text', 'author_id', 'pub_date'],
    },
    'genre_title.csv': {
        'model': GenreTitle,
        'fieldnames': ['id', 'title_id', 'genre_id'],
    },
}


class Command(BaseCommand):
    # Show this when the user types help
    help = "Load DB from dir (../static/data/)"

    def handle(self, *args, **options):
        bar = IncrementalBar('Loading data', max=len(import_settings))
        for filename, set in import_settings.items():
            path = os.path.join(settings.BASE_DIR, "static/data/") + filename
            fieldnames = set['fieldnames']
            with open(path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames)
                if fieldnames:
                    next(reader, None)
                for row in reader:
                    set['model'].objects.get_or_create(**row)
            bar.next()
        bar.finish()
        self.stdout.write("!!! csv database has been loaded successfully !!!")
