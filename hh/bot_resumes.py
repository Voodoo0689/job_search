import json
import requests
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

token = '5511994135:AAE6m4QleaGKJv1XCcZKDK15uOjJyu5_o7s'
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Здесь вам нужно вставить id вашей телеги
your_id = '1089473312'


def get_resumes(input_city: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36"
    }
    url_city = f"https://career.habr.com/api/frontend/suggestions/locations?term={input_city}"
    r = requests.get(url=url_city, headers=headers)
    try:
        id_city = r.json()['list'][0]['value']
        url = f"https://career.habr.com/api/frontend/resumes?order=last_visited&currency=RUR&city_ids[]={id_city}"
        r = requests.get(url=url, headers=headers)
        resumes = r.json()
        city_name = resumes['list'][0].get('location').get('title')
        with open(f"resumes_{city_name}.json", "w", encoding='utf-8') as file:
            json.dump(resumes, file, indent=4, ensure_ascii=False)
    except:
        pass


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Введи мне название города,"
                         "а я тебе создам json файл с резюмешечками")


@dp.message_handler()
async def get(message: types.Message):
    city = message.__getattribute__('text')
    get_resumes(str(city))
    try:
        await bot.send_document(your_id, open(f"resumes_{city}.json", 'rb'))
    except:
        await message.answer("Скорее всего такого города нет")


if __name__ == '__main__':
    executor.start_polling(dp)
