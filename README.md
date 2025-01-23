<h1 align="center">Бот для предложки в телеграм канал</h1>

![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fnumpy%2Fnumpy%2Fmain%2Fpyproject.toml
)
<h3>Что вообще этот бот делает?</h3>
Пользователь отправляет пост через бота, админу приходит оповещение, далее в пагинаторе будет показан пост и действия "Принять" или "Отклонить"<br>
Посты для пагинатора хранятся в отдельном json, так что переживать, что они потеряются при отключении бота не стоит.


## Установка

Создайте виртуальное окружение
```shell
python3 -m venv venv
```
Запустите виртуальное окружение
```shell
source venv/bin/activate
```
Установите зависимости
```shell
pip install -r requirements.txt
```

## Команды админа

```
admin - вызов пагинатора для просмотра предложки.
/ban [user_id] - Заблокировать пользователя.
/unban [user_id] - Разблокировать пользователя
/blocked - список заблокированных пользователей.
```

## Конфиг

Удалите `.template` в файла `.env` и укажите там токен бота

Файл `config/config.py`
```
BOT_TOKEN = os.getenv("BOT_TOKEN")                  # токен бота
POSTS_FILE = "data_json/posts.json"                 # тут хранятся все посты из предложки
PENDING_POSTS_FILE = "data_json/pending_posts.json" # временное хранение постов для пагинатора
BLOCKED_USERS_FILE = "data_json/blocked_users.json" # заблокированные пользователи
IMAGE_FOLDER = "images"                             # директория для хранения картинок
DELAY_HOURS = 1                                     # задержка для предложения постов
LOG_FILE = "logs/bot.log"                           # файл логов
POSTS_PER_PAGE = 1                                  # начальная страница пагинатора
ADMIN_ID =                                          # айди админа
CHANNEL_ID =                                        # айди канала
```

Основные сообщения изменяются в файле `config/messages_list.py`
