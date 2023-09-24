# <p align="center">Социальная сеть Yatube</p>

Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам.

## Возможности

- Можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора
- Автор может выбрать имя и уникальный адрес для своей страницы
- Пользователи смогут заходить на чужие страницы, подписываться на авторов и комментировать их записи
- Записи можно отправить в сообщество и посмотреть там записи разных авторов

## Используемые технологии

![Python](https://img.shields.io/badge/Python-3.9.10-blue)

![Django](https://img.shields.io/badge/Django-2.2.9-blue)

## Установка
Используйте python3 для MacOS и Linux

1. Клонируйте репозиторий:

   ```bash
   git clone git@github.com:VPanshin/Yandex-Practicum-Study-Projects.git
   ```

2. Cоздайте и активировайте виртуальное окружение:

   ```bash
    $ cd Yandex-Practicum-Study-Projects/2_Yatube
    $ python -m venv venv

    $ source venv/Scripts/activate  #Для Windows
    $ source venv/bin/activate #Для MacOs/Linux
   ```

 3. Установите зависимости:

    ```py
    (venv) $ python -m pip install --upgrade pip
    (venv) $ pip install -r requirements.txt
    ```

4. Создайте и запустите миграции:

    ```py 
    cd yatube/
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Запустите проект:

    ```bash
    python manage.py runserver
    ```

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)