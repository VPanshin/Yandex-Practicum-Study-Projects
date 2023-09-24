# <p align="center">Foodgram. Ваш продуктовый помощник на каждый день</p>

Foodgram - бесплатный сервис для обмена, публикации и просмотра рецептов кулинарны блюд.

Проект размещен по адресу [http://foodgramyp.servegame.com:9080/](http://foodgramyp.servegame.com:9080)

## Возможности

- Регистрация и аутентификация пользователей
- Публикация своих собственных рецептов
- Просмотр рецептов других пользователей
- Возможность подписаться на публикации конкретных пользователей, чтоб следить за рецептами отдельных понравившихся авторов
- Возможность добавлять полюбившиеся или любые другие рецепты в список покупок, чтобы составить для себя покупательскую корзину с необходимы ингредиентами как для одного, так и для нескольких блюд сразу
- У сервиса есть свое собственное API

## Используемые технологии

![Python](https://img.shields.io/badge/Python-3.9.10-blue)

![Django](https://img.shields.io/badge/Django-3.2-blue)

![Django Rest Framework](https://img.shields.io/badge/DjangoRestFramework-3.12.4-blue)

![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

![PostreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

## Установка и деплой на Ваш боевой сервер

Чтобы начать работу с Foodgram, выполните следующие шаги:

1. Клонируйте репозиторий:

   ```bash
   git clone git@github.com:Savichx/foodgram-project-react.git
   ```
 
2. Установите на сервере Docker, Docker Compose:

   ```bash
   sudo apt install curl                                   - установка утилиты для скачивания файлов
   curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
   sh get-docker.sh                                        - запуск скрипта
   sudo apt-get install docker-compose-plugin              - последняя версия docker compose
   ```

3. В корневой папке создайте папку foodgram и создайте файл .env, после укажите в нем следующие данные:
   ```bash
   mkdir foodgram && cd foodgram/
   touch .env
   nano .env
   ```
   ```bash
   POSTGRES_DB= #название вашей базы данных
   POSTGRES_USER= #логин базы данных
   POSTGRES_PASSWORD= #пароль
   DB_NAME=foodgram-db
   DB_PORT=  #укажите порт (стандартное значение 5432)
   SECRET_KEY=  #укажите секретные ключ Django
   ALLOWED_HOSTS=  #введите список доступных хостов 
   DEBUG=  #значение Fasle либо True
   ```
4. Находясь на локальной машине скопируйте файлы на сервер и запустите докер:
   ```bash
   scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
   docker compose -f docker-compose.production.yml up -d
   ```
5. Соберите статику и сделайте миграции:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
   docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
   docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   ```

6. Не забудьте создать суперпользователя и наполнить базу данных ингредиентами:
   ```bash
   sudo docker exec -it foodgram-backend bash
   python manage.py createsuperuser
   python manage load_data_csv <путь_к_файлу>
   ```

7. Откройте веб-браузер и перейдите по адресу [http://foodgramyp.servegame.com:9080](http://foodgramyp.servegame.com:9080), чтобы увидеть Foodgram в действии.


## Вот список некоторых эндпоинтов API для работы с ними:
```py
- /api/users/ Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя. Доступно без токена.

- /api/users/{id} GET-запрос – персональная страница пользователя с указанным id (доступно без токена).

- /api/users/me/ GET-запрос – страница текущего пользователя. PATCH-запрос – редактирование собственной страницы. Доступно авторизированным пользователям.

- /api/users/set_password POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям.

- /api/auth/token/login/ POST-запрос – получение токена. Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.

- /api/auth/token/logout/ POST-запрос – удаление токена.

- /api/tags/ GET-запрос — получение списка всех тегов. Доступно без токена.

- /api/tags/{id} GET-запрос — получение информации о теге о его id. Доступно без токена.

- /api/ingredients/ GET-запрос – получение списка всех ингредиентов. Подключён поиск по частичному вхождению в начале названия ингредиента. Доступно без токена.

- /api/ingredients/{id}/ GET-запрос — получение информации об ингредиенте по его id. Доступно без токена.

- /api/recipes/ GET-запрос – получение списка всех рецептов. Возможен поиск рецептов по тегам и по id автора (доступно без токена). POST-запрос – добавление нового рецепта (доступно для авторизированных пользователей).

- /api/recipes/?is_favorited=1 GET-запрос – получение списка всех рецептов, добавленных в избранное. Доступно для авторизированных пользователей.

- /api/recipes/is_in_shopping_cart=1 GET-запрос – получение списка всех рецептов, добавленных в список покупок. Доступно для авторизированных пользователей.

- /api/recipes/{id}/ GET-запрос – получение информации о рецепте по его id (доступно без токена). PATCH-запрос – изменение собственного рецепта (доступно для автора рецепта). DELETE-запрос – удаление собственного рецепта (доступно для автора рецепта).

- /api/recipes/{id}/favorite/ POST-запрос – добавление нового рецепта в избранное. DELETE-запрос – удаление рецепта из избранного. Доступно для авторизированных пользователей.

- /api/recipes/{id}/shopping_cart/ POST-запрос – добавление нового рецепта в список покупок. DELETE-запрос – удаление рецепта из списка покупок. Доступно для авторизированных пользователей.

- /api/recipes/download_shopping_cart/ GET-запрос – получение текстового файла со списком покупок. Доступно для авторизированных пользователей.

- /api/users/{id}/subscribe/ GET-запрос – подписка на пользователя с указанным id. POST-запрос – отписка от пользователя с указанным id. Доступно для авторизированных пользователей

- /api/users/subscriptions/ GET-запрос – получение списка всех пользователей, на которых подписан текущий пользователь Доступно для авторизированных пользователей.
```

## Автор

Vsevolod Panshin 

[![Telegram Badge](https://img.shields.io/badge/-vsevolod.panshin-blue?style=social&logo=telegram&link=https://t.me/VPanshin)](https://t.me/VPanshin)

[![Gmail Badge](https://img.shields.io/badge/vsevolodpanshin@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:vsevolodpanshin.mv@gmail.com)](mailto:vsevolodpanshin@gmail.com)

