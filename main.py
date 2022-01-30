import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import numpy as np
import matplotlib.pyplot as plt


API_TOKEN = os.environ.get('TOKEN')

logging.basicConfig(level=logging.INFO)
lines_num = 50
lines_amp = 5
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    await message.reply(
        "Здравствуй, этот бот сделает, из отправленной тобой картинки, изображение из 50 линий"
    )


@dp.message_handler(content_types=['photo'])
async def photo_hadler(message: Message):
    file_name = f'{message.from_user.id}.png'
    await message.photo[-1].download(file_name)
    await edit_photo(file_name)
    with open(file_name, 'rb') as photo:
        await message.answer_photo(photo)
    os.remove(f'./{file_name}')

def decel(x):
  return 1 - (x-1)*(x-1)

async def edit_photo(file_name: str):
    inp_img = plt.imread(file_name, format='jpeg')
    inp_shape = inp_img.shape
    out_img = np.ones(inp_shape)
    for line in range(0, lines_num):
        l=0
        y = int(line*inp_shape[0]/lines_num)
        for x in range(0, inp_shape[1]):
        # m = 1-"the most intense color". It can be particular color only (e.g. red - inp_img[y, x, 0])
            m = np.max(inp_img[y, x])
            if m < 1: # *.png
                m = 1 - m
            else: #*.jpeg
                m = 1 - m/255 

            for s in range(0, lines_amp + 1):      
                out_img[min(y + int(np.sin(l * np.pi/2.) * lines_amp * decel(m)), inp_shape[0] - 1), x] = 0
                l+=m/lines_amp
    plt.imsave(file_name, out_img)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
