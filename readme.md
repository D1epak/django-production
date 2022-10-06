### Django контейнер для выгрузки на прод
Что включено в контейнер?
+ Проверка кода на ошибки с помощью fluke8
+ Связка nginx + gunicorn для проксирования веб сервера
+ База данных на postgresql с подлючением в .env
+ Подключение сертификата certbot-ом
+ Установка requirements.txt автоматически и сборка в wheels
***
## Инструкция по выгрузке на сервер
### Шаг 1 - Установка зависимостей и прочих ПО
В папке с проектом есть Makefile, который поможет вам собрать образ на сервере,
что бы начать установка всех важных зависимостей и софта напишите команду:
```code 
# make install
```
* Требуются root права, в рекомендациях докера описано почему, докер настоятельно просит запускать контейнеры от имени администратора, и забрать доступы у другиз пользователей кроме root!

### Шаг 2 - Сборка контейнера и запуск на сервере
С помощью того же Makefile выполняем команду, которая запустит сборку нашего
сайта на сервере, заранее требуется подготовить проект к выгрузке, это описано ниже.
Для сборки введите команду:
```code
# make build
```
* Требуются root права, в рекомендациях докера описано почему, докер настоятельно просит запускать контейнеры от имени администратора, и забрать доступы у другиз пользователей кроме root!
### Шаг 3 - Тестирование работоспособности и остановка контейнера
* Шаг не обязательный, расписан просто для удобства управления контейнерами.

С помощью Makefile-а написанного мною, можно удобно останавливать контейнеры и даже удалять их в случае переборки.

Остановка запущенных контейнеров:
```code
# make down
```

Остановка и удаление всех контейнеров, изображений, чистка системы от всех не используемых контейнеров, удобная штука при переборке контейнеров.
```code
# make rm
```

Просмотр всех запущенных контейнеров:
```code
# make ps
```

Просмотр всех images внутри докера:
```code
# make im
```
***
## Подготовка к выгрузке своего приложения на сервер
Это обязательный пункт перед деплоем, перенесен ниже для удобства, некоторые кто сюда приходят, уже знают что нужно сделать.
Нам потребуется создать файл .env в корне рядом с docker-compose.yml файлом, с содержанием:
```dotenv
SECRET_KEY="Ваш скретный ключ"
#Database setings
POSTGRES_DB="Имя базы данных"
POSTGRES_USER="Никнейм пользователя"
POSTGRES_PASSWORD="Пароль пользователя"
```
### Шаг 1.1 - Сборка приложения и подготовка настроек.
Откройте settings.py и измените поля указанные у меня в инструкции на такие же

```python
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['*']
```
Мы отключаем режим DEBUG, и разрешаем django принимать любой урл, ведь за проксирование будет отвечать nginx.

Так как мы используем postgresql базу данных нам нужно сменить database в настройках.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': 'db',
        'PORT': '5432',
    }
}
```
Далее требуется научить django понимать где у нее статика, и где media:
```python
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```
### Шаг 1.2 - Конфигурируем docker-compose на новый сайт
Как вы поняли, вам требуется перенести содержимое своего проекта перенести в папку app
и название папки с settings.py и wsgi.py является главной с помощью нее мы и будем запускать весь продукт.

После переноса, откройте docker-compose.yml и замените в backend название projectname на название вашей папки.

```docker-compose
  backend:
    build: ./app
    command: gunicorn projectname.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/home/app/web/static
      - media_volume:/home/app/web/media
    env_file:
      - ./.env
    expose:
      - '8000'
    depends_on:
      - db
```
Потом требуется заменить exampleemail@yandex.ru в поле CERTBOT_EMAIL для генерации сертификата, в блоке nginx
```
  nginx:
    restart: unless-stopped
    image: staticfloat/nginx-certbot
    ports:
        - 80:80/tcp
        - 443:443/tcp
    environment:
        CERTBOT_EMAIL: examplemail@yandex.ru
    volumes:
      - ./conf.d:/etc/nginx/user.conf.d:ro
      - letsencrypt:/etc/letsencrypt
      - static_volume:/home/app/web/static
      - media_volume:/home/app/web/media
```
Отлично docker-compose файл готов к сборке, далее требуется настроить сам конфиг nginx и приступать к прочтению инструкции выгрузка на сервер.
### Шаг 1.3 - Конфигурирование nginx на работу с django backend
Что бы все работало, требуется настроить nginx на работу с беком django,
в папке с проектом есть conf.d в нем лежит стандартный конфиг default.conf,
откройте его и замените доменное имя на ваше, важно указать домен с www и без.

в server_name напишите ваш домен, например example.com, так же в ssl_certificate и ssl_certificate_key,
исправьте путь, укажите верный домен, по примеру как ниже.
```
  listen 443 ssl;
  listen [::]:443 ssl;
  server_name example.com www.example.com;
  ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
```
Должен получиться вот такой конфиг:
```
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=STATIC:10m inactive=7d use_temp_path=off;

upstream backend_upstream {
  server backend:8000;
}
server {
  listen 443 ssl;
  listen [::]:443 ssl;
  server_name example.com www.example.com;
  ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;


  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection 'upgrade';
  proxy_set_header Host $host;
  proxy_cache_bypass $http_upgrade;

  location /static/ {
        alias /home/app/web/static/;
  }

  location /media/ {
        alias /home/app/web/media/;
  }

  location / {
    proxy_pass http://backend_upstream;
  }
}
```
Теперь продукт готов, можете начать читать инструкцию по выгрузке на сервер.