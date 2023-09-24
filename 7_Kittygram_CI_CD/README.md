# <p align="center"> CI/CD для проекта KittyGramYP</p>

KittyGramYP - это веб-приложение для обмена милыми фотографиями котов с друзьями и сообществом. Пользователи могут загружать, делиться, указывать достижения для фотографий котов. Проект размещен по адресу [https://kittygramyp.servegame.com/](https://kittygramyp.servegame.com/).

## Возможности

CI/CD API сервиса Kittygram.Workflow включает в себя последовательность автоматических действий, таких как запуск тестов, обновление образа проекта на DockerHub, автоматический деплой на боевой сервер и запуск сервиса. Кроме того, при выполнении команды push, происходит отправка уведомления в Телеграм о успешном завершении workflow.

## Используемые технологии

![Python](https://img.shields.io/badge/Python-3.9.10-blue)

![Django](https://img.shields.io/badge/Django-3.2-blue)

![Django Rest Framework](https://img.shields.io/badge/DjangoRestFramework-3.12.4-blue)

![Nginx](https://img.shields.io/badge/Nginx-1.18.0-blue)

![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-blue)


## Подготовка к деплою проекта
1. Создать директорию kittygram/ в домашней директории сервера.

2. Установить Nginx и настроить конфигурацию так, чтобы все запосы шли в докер на порт 9000.

    ```bash
    sudo apt install nginx -y 
    sudo nano etc/nginx/sites-enabled/default
    ```
    Конфигурация nginx
    ```bash
    server {
        server_name kittygramyp.servegame.com;
        server_tokens off;
        client_max_body_size 20M;
    
        location / {
            proxy_set_header Host $http_host;
            proxy_pass http://127.0.0.1:9000;
    }
    ```

3. Установите docker-compose:
    ```bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin    
    ``` 
4. Добавите в Secrets GitHub Actions данного репозитория на GitHub переменные окружения:
    ```bash
    DOCKER_USERNAME=<имя пользователя DockerHub>
    DOCKER_PASSWORD=<пароль от DockerHub>
    
    USER=<username для подключения к удаленному серверу>
    HOST=<ip сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш приватный SSH-ключ>
    
    TELEGRAM_TO=<id вашего Телеграм-аккаунта>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)
