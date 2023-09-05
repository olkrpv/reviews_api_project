import sqlite3

from csv import DictReader

from django.core.management import BaseCommand


table_dict = {
    'reviews_category': 'category.csv',
    'reviews_genre': 'genre.csv',
    'reviews_title': 'titles.csv',
    'reviews_title_genre': 'genre_title.csv',
    'users_user': 'users.csv',
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            print('Подключение к SQLite')

            for table_name, file_name  in table_dict.items():
                with open(f'static\data\{file_name}', encoding='utf-8') as csvfile:
                    reader = DictReader(csvfile)
                    for row in reader:
                        colomns = tuple(row.keys())
                        values = tuple(row.values())
                        insert_query = f'INSERT INTO {table_name}{colomns} VALUES {values};'
                        cursor.execute(insert_query)
                        try:
                            connection.commit()
                            print(f'Запись успешно вставлена ​​в таблицу {table_name}', cursor.rowcount)
                        except Exception as error:
                            print(f'Ошибка при добавлении строки в таблицу {table_name}', error)
            cursor.close()

        except sqlite3.Error as error:
            print('Ошибка при работе с SQLite', error)
        finally:
            if connection:
                connection.close()
                print('Соединение с SQLite закрыто')



        # for file_name, model_name in loading.items():

        #     for row in DictReader(open(f'static\data\{file_name}', encoding='utf-8')):
        #         ex_model = model_name(**row)
        #         ex_model.save()
