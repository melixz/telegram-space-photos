# Космический Телеграм

Проект позволяет автоматически скачивать фотографии космоса с различных источников (NASA, SpaceX и др.) и публиковать их в Telegram-канал с заданной периодичностью. 

### Как установить

1. Скачайте репозиторий с проектом:
    ```sh
    git clone https://github.com/melixz/telegram-space-photos
    ```

2. Создайте файл `.env` в корневой директории проекта и добавьте следующие строки:
    ```env
    TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_Telegram
    TELEGRAM_CHANNEL_ID=ваш_идентификатор_канала_Telegram
    NASA_API_TOKEN=ваш_токен_от_NASA_API
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

### Использование

1. Загрузите изображения с NASA APOD:
    ```sh
    python fetch_nasa_apod_images.py --count 50
    ```

2. Запустите скрипт для публикации изображений в Telegram-канал:
    ```sh
    python image_post_to_telegram.py images --delay 14400
    ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
