import logging
from decouple import config

from aiogram import Bot, Dispatcher, executor, types
from PIL import Image, ImageDraw, ImageFont


API_TOKEN = config("TOKEN")

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
    font = ImageFont.truetype('Lobster-Regular.ttf', size=40, encoding="utf-8")
    width_image, height_image = image.size
    width_text, height_text = draw.textsize(text, font=font)
    draw.text(
        ((width_image - width_text) / 2 + 1, ((height_image / 10) * 9) + 1),
        text,
        font=font,
        fill=(0, 0, 0, 0)
    )
    draw.text(
        ((width_image - width_text) / 2, ((height_image / 10) * 9)),
        text,
        font=font,
        fill=(255, 0, 0, 0)
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


async def on_startup(_):
    print('Bot is omline')

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` 
    command
    """
    await message.reply("Hi!\nLet's make a meme out of your photo!\nSend me a photo, type a text and get your mem image.")

@dp.message_handler(content_types=['photo'])
async def ask_caption_text(message: types.Message):
    '''
    This handler will be called when user sends image.
    Bot asks user to input text for caption.
    '''
    #await message.reply('What text would you like to add?')
    await message.answer('What text would you like to add?')

@dp.message_handler()
async def change_image(message: types.Message):
    '''
    Processing image and send new image to user
    '''
    save_text(message.from_user.id, message.message_id, message.text)
    await message.answer('Doing my magic!')
    caption = get_text(message.from_user.id, message.message_id)
    await message.answer(f'Your caption: {caption}') # debug

# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)

#     await message.answer(message.text)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)