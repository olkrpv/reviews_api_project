"""Импорт csv-файлов из папки static/data/."""

import sqlite3

from csv import DictReader

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title
from users.models import User

FILES_MODELS = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'users.csv': User,
    # 'review.csv': Review,
    # 'comments.csv': Coment,
    'genre_title.csv': (Genre, Title)
}
FIELDS = {
    'category': Category,
    'title': Title,
    'genre': Genre,
    'author': User,
    # 'review': Review,
}

def change_foreign_keys(data_csv):
    """Изменяет значения внешних ключей при загрузке"""
    change_data = data_csv.copy()
    for key, value in data_csv.items():
        if key in FIELDS.keys():
            change_data[key] = FIELDS[key].objects.get(pk=value)
    return change_data

class Command(BaseCommand):

    def handle(self, *args, **options):

        for file_name, model_name in FILES_MODELS.items():
            with open(
                f'static/data/{file_name}', encoding='utf-8'
            ) as csvfile:
                for data_csv in DictReader(csvfile):
                    data = change_foreign_keys(data_csv)
                    try:
                        if file_name != 'genre_title.csv':
                            ex_model = model_name(**data)
                            ex_model.save()
                        else:
                            title_obj = get_object_or_404(
                                Title, 
                                id=data_csv['title_id']
                            )
                            genre_obj = get_object_or_404(
                                Genre,
                                id=data_csv['genre_id']
                            )
                            title_obj.genre.add(genre_obj)
                            title_obj.save()
                    except Exception as error:
                        self.stderr.write(self.style.WARNING(f'{error}'))
                        raise Exception(error)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully load {file_name}')
                )
