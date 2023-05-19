<h2>Foodgram Service</h2>

<h3>Сервис с рецептами</h3>

## Возможности
- Делись своими рецептами
- Просматривай чужие
- Подписывайся на понравившихся авторов, добавляй рецепты в избранное, а главное: ты можешь скачать список покупок, в котором будут записаны ВСЕ ингредиенты из рецептов в твоей корзине

## Технологии
[![My Skills](https://skillicons.dev/icons?i=python,django,sqlite,bootstrap&theme=light)](https://skillicons.dev)


## Наполнение env файла
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres

### Здесь Вам надо указать свой пароль ###
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

## Запуск проекта в контейнере:
Клонировать образ с DockerHub:
docker pull foodgram_backend
docker pull foodgram_frontend

Сборка контейнера и его запуск:
docker-compose up -d --build

Выполнение миграций:
docker-compose exec backend python manage.py migrate 

Создание суперпользователя:
docker-compose exec backend python manage.py createsuperuser

Загрузка статики:
docker-compose exec backend python manage.py collectstatic --no-input

## Остановка контейнера:
docker-compose down -v


## Запуск проекта локально:
Клонировать репозиторий и перейти в него в командной строке:

```
either HTTPS:
git@github.com:ZukoLordofFire/foodgram_project_react.git
```
```
or SSH:
git clone git@github.com:ZukoLordofFirefoodgram_project_react.git
```

```
cd foodgram_project_react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

cd backend

```
python manage.py makemigrations
python manage.py migrate
```

python manage.py createsuperuser


Запустить проект:

```
python manage.py runserver
```

### Документация:
После запуска на localhost доступна [документация].

## Примеры:

### Регистрация:
* POST: http://127.0.0.1:8000/api/auth/signup/ 
```
{
    "email": "string",
    "username": "string",
    "password": "string",
    "last_name": "string",
    "first_name": "string"
}
```

### Получение токена: 
* POST: http://127.0.0.1:8000/api/auth/token/ 
```
{
    "email": "string",
    "password": "string"
}
```
RESPONSE:
```
{
    "token": "string"
}
```

Для добавления/изменения данных через API необходимо добавить в header 
к запросу параметр 'Authorization' со значением 'token TOKEN'.

### Получение рецептов (постранично): 
* GET: http://127.0.0.1:8000/api/recipes/

RESPONSE:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

### Получение конкретного рецепта: 
* GET: http://127.0.0.1:8000/api/recipes/1/

RESPONSE:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
### скачивание списка покупок: 
* GET: http://127.0.0.1:8000/api/recipes/download_shopping_cart/



### Автор

Валентин Веселов [Telegram](https://t.me/bothat) [GitHub](https://github.com/ZukoLordofFire)

[документация]: <http://127.0.0.1:8000/redoc/>

