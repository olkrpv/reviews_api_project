"""Импорт csv-файлов из папки static/data/."""

from csv import DictReader

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


PARAMS_MODELS = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'users': User,
    'reviews': Review,
    'comments': Comment,
    'genre_title': (Genre, Title)
}

FIELDS = {
    'category': Category,
    'title': Title,
    'genre': Genre,
    'author': User,
    'review': Review,
}


def change_foreign_keys(data_csv):
    """Изменяет значения внешних ключей при загрузке"""
    change_data = data_csv.copy()
    for key, value in data_csv.items():
        if key in FIELDS.keys():
            change_data[key] = FIELDS[key].objects.get(pk=value)
    return change_data


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            action='store',
            help='Load data to "category" model',
        )
        parser.add_argument(
            '--genre',
            action='store',
            help='Load data to "genres" model',
        )
        parser.add_argument(
            '--users',
            action='store',
            help='Load data to "users" model',
        )
        parser.add_argument(
            '--reviews',
            action='store',
            help='Load data to "reviews" model',
        )
        parser.add_argument(
            '--titles',
            action='store',
            help='Load data to "title" model',
        )
        parser.add_argument(
            '--comments',
            action='store',
            help='Load data to "comments" model',
        )
        parser.add_argument(
            '--genre_title',
            action='store',
            help='Load data to "title_genre" model',
        )

    def handle(self, *args, **options):

        for parameter, model_name in PARAMS_MODELS.items():

            if options[parameter]:

                with open(
                    f'static/data/{options[parameter]}', encoding='utf-8'
                ) as csvfile:
                    for data_csv in DictReader(csvfile):
                        data = change_foreign_keys(data_csv)
                        try:
                            if options[parameter] != 'genre_title.csv':
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
                        self.style.SUCCESS(f'Successfully load {options[parameter]}')
                    )

