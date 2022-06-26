# Бекенд для веб-сервиса сравнения цен. 
## Описание задачи
В данном задании вам предлагается реализовать бэкенд для веб-сервиса сравнения цен, аналогичный сервису [Яндекс Товары](https://yandex.ru/products). Обычно взаимодействие с такими сервисами происходит следующим образом:
1. Представители магазинов загружают информацию о своих товарах и категориях. Также можно изменять и удалять информацию о ранее загруженных товарах и категориях.
2. Покупатели, пользуясь веб-приложением, могут искать предложения разных магазинов, сравнивать цены и следить за их динамикой и историей.

Ваша задача - разработать REST API сервис, который позволяет магазинам загружать и обновлять информацию о товарах, а пользователям - смотреть какие товары были обновлены за последние сутки, а также следить за динамикой цен товара или категории за указанный интервал времени.

## Используемые технологии
Более подробно можно посмотреть в файле requirements.txt.
- Web services : starlette
- Database: postgresql
- PostgreSQL database adapter: psycopg2 
- ASGI web server implementation for Python: uvicorn
- Database schema migration tool: yoyo-migrations
- Data validation and settings management: pydantic
- Python testing tool: pytest
## Реализованные возможности
## Запуск
По заданию требовалось развертывать сервис в контейнере,но есть возможность запустить без контейнера.
### Запуск в контейнере
Для запуска в контейнере нужно выполнить следующие действия:
1. Создать файл docker-compose.yaml 
2. Рядом с ним положить .env с указанием названия,пароля,имени пользователя базы данных.

Шаблон .env
```
POSTGRES_DB="{db name}"
POSTGRES_USER="{username}"
POSTGRES_PASSWORD="{password}"

```
Если база данных используется не та,которая развертывается в контейнере,то тогда еще нужно в docker-compose.yaml файле в сервисе megamarket изменить environment поля host,port.
### Запуск без контейнера
Для запуска без контейнера нужно выполнить следующие действия:
1. Склонировать репозиторий.
2. Выполнить команду pip freeze > requierments.txt.
3. В директории в которой находится файл main.py создать файл .env и указать там данные для подключения к базе данных(Шаблон будет ниже).
4. Выполнить команду python3 main.py

При этом нужно иметь доступ к базе данных postgres.Опять же можно развернуть в контейре или просто подключиться к какой-то существующей.

Шаблон .env
```
PG_ADDRESS='host={hostname} port={port} user={username} dbname={db name} password={password}'
PG_DSN='postgres://{username}:{password}@{hostname}:{port}/{db name}'
```