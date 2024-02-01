### Сервис для оценивания произведений
Данный API сервис предназначен для оценивания различных произведений, таких как фильмы, книги, игры и многое другое. С помощью данного сервиса пользователи могут оставлять свои оценки и отзывы на произведения, а также просматривать оценки и отзывы других пользователей.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:olkrpv/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать виртуальное окружение:

(Windows)
```
python -m venv venv
```

(MacOs, Linux)
```
python3 -m venv venv
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

(Windows)
```
python manage.py migrate
```

(MacOs, Linux)
```
python3 manage.py migrate
```

Запустить проект:

(Windows)
```
python manage.py runserver
```

(MacOs, Linux)
```
python3 manage.py runserver
```
