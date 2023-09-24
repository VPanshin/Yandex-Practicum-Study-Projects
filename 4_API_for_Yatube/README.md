# <p align="center">REST API для социальной сети Yatube</p>

Этот API может помочь взаимодействовать с социальной сетью Yatube и данными вокруг нее.

Все данные хранятся в формате JSON и предоставляются вам в реализации RESTish, которая позволяет программно собирать и измерять данные.

## Возможности

- Аутентификация по JWT-токену
- Получение, cоздание, обновление и удаление публикаций и комментариев
- Получение информации о сообществах
- Получение информации о существующих подписках автора
- Возможность подписываться на пользователей

## Используемые технологии

![Python](https://img.shields.io/badge/python-3.9.10-blue)

![Django Rest Framework](https://img.shields.io/badge/djangorestframework-3.12.4-blue)

![SQLite](https://img.shields.io/badge/SQLite-blue)

## Установка
Используйте python3 для MacOS и Linux

1. Клонируйте репозиторий:

    ```python
    git clone git@github.com:VPanshin/Yandex-Practicum-Study-Projects.git
    ```

2. Cоздайте и активировайте виртуальное окружение:

    ```python
    $ cd Yandex-Practicum-Study-Projects/4_API_for_Yatube
    $ python -m venv venv

    $ source venv/Scripts/activate  #Для Windows
    $ source venv/bin/activate #Для MacOs/Linux
   ```

3. Установите зависимости:

    ```py
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

4. Примените миграции базы данных:

    ```py 
    cd yatube_api/
    python manage.py migrate
    ```

5. Запустите проект:

    ```bash
    python manage.py runserver
    ```

## Примеры использования

- Вы можете [GET](http://127.0.0.1:8000/api/v1/posts/) список всех опубликованных постов. Существует возможность установить предел и смещение для лучшего вида.
- Или вы можете  [POST](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/) комментарий. Вы должны быть авторизованы для этого.
- Еще один пример для [UPDATE](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/) вашего комментария. Эта функция доступна только авторам комментариев.

Полную документацию можно найти [здесь.](http://127.0.0.1:8000/redoc/)

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)