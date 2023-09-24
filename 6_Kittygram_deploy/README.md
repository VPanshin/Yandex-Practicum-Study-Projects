# <p align="center">KittyGramYP</p>

KittyGramYP - это веб-приложение для обмена милыми фотографиями котов с друзьями и сообществом. Пользователи могут загружать, делиться, указывать достижения для фотографий котов. Проект размещен по адресу [https://kittygramyp.servegame.com/](https://kittygramyp.servegame.com/).

## Возможности

- Регистрация и аутентификация пользователей
- Загрузка и обмен фотографиями котов
- Присвоение достижений для своих любимцев

## Используемые технологии

![Python](https://img.shields.io/badge/Python-3.9.10-blue)

![Django](https://img.shields.io/badge/Django-3.2-blue)

![Django Rest Framework](https://img.shields.io/badge/DjangoRestFramework-3.12.4-blue)

![Nginx](https://img.shields.io/badge/Nginx-1.18.0-blue)

![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-blue)


## Установка
Используйте python3 для MacOS и Linux

1. Клонируйте репозиторий:

   ```python
   git clone git@github.com:VPanshin/Yandex-Practicum-Study-Projects.git
   ```

2. Cоздайте и активировайте виртуальное окружение:

   ```python
   $ cd Yandex-Practicum-Study-Projects/6_Kittygram_deploy
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
   cd backend/
   python manage.py migrate
   ```

5. Запустите проект:

   ```bash
   python manage.py runserver
   ```

6. Откройте веб-браузер и перейдите по адресу [http://localhost:8000/](http://localhost:8000/), чтобы увидеть KittyGramYP в действии.

## Развертывание

Чтобы развернуть KittyGramYP на производственной среде, следуйте этим шагам:

- Создайте сервер с установленным Nginx.

- Настройте Nginx для обслуживания приложения и обработки SSL-сертификатов.

- Обновите соответствующие файлы конфигурации (например, settings.py, конфигурацию Nginx) с настройками вашего сервера, включая параметры подключения к базе данных, разрешенные хосты и пути к статическим файлам.

- Установите Gunicorn и настройте его для запуска приложения Django.

- Запустите приложение с помощью Gunicorn и Nginx.

*Для получения более подробных инструкций обратитесь к официальной документации Django и Nginx.*

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)
