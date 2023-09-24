
# <p align="center">Бот-ассистент для проверки статуса домашнего задания от Яндекс.Практикум</p>

Этот телеграмм бот сможет проверить состояние вашего домашнего задания через [API](https://practicum.yandex.ru/api/user_api/homework_statuses/) Яндекс.Домашка и отправит следующее сообщение:

1. Работа проверена: ревьюеру всё понравилось. Ура!
2. Работа взята на проверку ревьюером.
3. Работа проверена, в ней нашлись ошибки.

## Используемые технологии

![Python](https://img.shields.io/badge/python-3.9.10-blue)

![Telegram-bot](https://img.shields.io/badge/telegram--bot-13.7-blue)

![donenv](https://img.shields.io/badge/dotevn-0.19.0-blue)

## Установка
Используйте python3 для MacOS и Linux

1. Клонируйте репозиторий:

    ```python
    git clone git@github.com:VPanshin/Yandex-Practicum-Study-Projects.git
    ```
2. Cоздайте и активировайте виртуальное окружение:
    ```python
    $ cd Yandex-Practicum-Study-Projects/3_telegram_bot
    $ python -m venv venv

    $ source venv/Scripts/activate  #Для Windows
    $ source venv/bin/activate #Для MacOs/Linux
   ```
3. Установите зависимости:
    ```python
    $ pip install -r requirements.txt
    ```
4. Запустите проект:
    ```python
    $ python homework.py 
    ```

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)