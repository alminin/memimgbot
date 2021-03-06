import logging
from decouple import config
import os

from aiogram import Bot, Dispatcher, executor, types
from PIL import Image, ImageDraw, ImageFont


API_TOKEN = config('TOKEN')
IMAGES_DIR = config('IMAGES_DIR')
FONT = config('FONT')
REPOST_CHANNEL = config('REPOST_CHANNEL')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def make_caption(filepath, text):
    '''Make caption on received photo'''
    image = Image.open(filepath)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT, size=70, encoding="utf-8")
    width_image, height_image = image.size
    width_text, height_text = draw.textsize(text, font=font)
    draw.text(
        ((width_image - width_text) / 2 + 1, ((height_image / 10) * 8.5) + 5),
        text,
        font=font,
        fill=(0, 0, 0, 0)
    )
    draw.text(
        ((width_image - width_text) / 2, ((height_image / 10) * 8.5)),
        text,
        font=font,
        fill=(255, 255, 255, 0)
    )
    image.save(filepath)

def save_text(user_id, message_id, text):
    with open('mems.txt', 'a') as f:
        f.write(f'{user_id}-{message_id}:-:{text} \n')

def get_text(user_id, message_id):
    with open('mems.txt', 'r') as f:
        for line in f:
            if f'{user_id}-{message_id}' in line:
                return line.strip('\n').split(':-:')[1]

def get_user_img(user_id):
    '''
    Return file path of the last downloaded image of the user
    '''
    for file in os.listdir(IMAGES_DIR):
        if file.startswith(f"{user_id}"):
            return os.path.join(IMAGES_DIR, file)

def gen_kb():
    '''Generate inline keyboard for share image'''
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("Поделиться", callback_data="share_this"))
    return kb

async def on_startup(_):
    print('Bot is online')

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` 
    command
    """
    await message.reply("Привет!\nДавай сделаем мем из твоего фото!\nВышли мне фото, введи текст для подписи и получи свой мем.")

@dp.message_handler(content_types=['photo'])
async def save_image(message: types.Message):
    '''
    This handler will be called when user sends image.
    Bot download the image for further processing and asks user to input text for caption.
    '''
    file_name = f"{message.from_user.id}_{message.message_id}.jpg"
    file_path = os.path.join(IMAGES_DIR, file_name)
    await message.photo[-1].download(file_path)
    #await message.reply('What text would you like to add?')
    await message.answer('Какой текст ты хочешь добавить?')

@dp.message_handler()
async def change_image(message: types.Message):
    '''
    Processing image and send new image to user
    '''
    save_text(message.from_user.id, message.message_id, message.text)
    await message.answer('Делаю магию!')
    user_id = message.from_user.id
    caption = get_text(user_id, message.message_id)
    img_path = get_user_img(user_id)
    make_caption(img_path, caption)
    with open(img_path, 'rb') as f:
        await message.answer_photo(f, reply_markup=gen_kb())
    os.remove(img_path)

@dp.callback_query_handler(lambda callback_query: True)
async def share_callback_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'share_this':
        await bot.answer_callback_query(callback_query.id, 'Сделано!')
        await bot.forward_message(REPOST_CHANNEL, callback_query.from_user.id, callback_query.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)