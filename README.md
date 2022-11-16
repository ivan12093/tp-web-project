# Запуск проекта
**Необходимые пакеты**:
python3, pip,  postgresql
- 1. Создайте виртуальное окружение
```shell
$ python3 -m venv venv
```
- 2. Активируйте venv и установите зависимости
```shell
$ source venv/bin/activate
$ pip install -r requirements.txt
```

- 3. Поднимите локально `postgres`. 
Подробнее по ссылке: https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html

- 4. По умолчанию подключение к базе настроено таким образом:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'askme',
        'USER': 'web',
        'PASSWORD': 'pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
Поменять настройки подключения к бд можно в файле `askme/setting.py`

- 5. Примените миграции к бд.
```shell
$ python3 manage.py migrate
```

- 6. Заполните таблицу тестовыми данными командой:
```shell
$ python3 manage.py fill_db [ratio] 
```
Где `[ratio]` относительное кол-во данных

- 7. Поднимите веб-сервер
```shell
$ python3 manage.py runserver
```
