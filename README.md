# Телеграм-бот @memimgbot

Бот получает от пользователя картинку, запрашивает текст для подписи и рисует её на картинке пользователя. Полученную картинку бот отправляет пользователю и предлагает ею поделиться в публичном канале.

## Использование

Клонируем репозиторий
```
git clone https://github.com/alminin/memimgbot.git
```
Переходим в рабочий каталог
```
cd memimgbot
```
Устанавливаем виртуальное окружение
```
python3 -m venv venv
```
Активируем его
```
source venv/bin/activate
```
Устанавливаем зависимости
```
pip install -r requirements.txt
```
Создайте файл .env и сохраните в нем значение переменных, необходимых для работы бота:
- **TOKEN** - токен вашего бота
- **IMAGES_DIR** - каталог с изображениями пользователей
- **FONT** - файл шрифта
- **REPOST_CHANNEL** - идентификатор канала для репостов(отрицательное число)