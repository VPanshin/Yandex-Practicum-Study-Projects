import csv
import os

import django
from recipes.models import Ingredient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()


def load_csv_data():
    with open('../data/ingredients.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, measurement_unit = row
            Ingredient.objects.create(
                name=name,
                measurement_unit=measurement_unit
            )


if __name__ == '__main__':
    load_csv_data()
