# Сервис для оценивания произведений

### Описание
Данный API сервис предназначен для оценивания различных произведений, таких как фильмы, книги, игры и многое другое. С помощью данного сервиса пользователи могут оставлять свои оценки и отзывы на произведения, комментировать их, а также просматривать оценки и отзывы других пользователей.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:olkrpv/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать виртуальное окружение:

```
python3.9 -m venv venv
```

Активировать виртуальное окружение:
```
source venv/bin/activate
```

Обновить pip:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Перейти в папку с настройками проекта:

```
cd api_yamdb/
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Загрузить данные из файла csv:

```
python3 manage.py importcsv
```

### Документация API

После запуска проекта документация к API будет доступна по адресу:
http://127.0.0.1:8000/redoc/

### Стек технологий:
- Python
- Django Framework
- Django Rest Framework
- Djoser/Simple JWT

### Дополнительная информация
Над проектом работали:
- Ольга Карпова (@olkrpv)
- Дарья Фёдорова (@FedorovaDasha)
- Наталья Любимова (@hadge13)
