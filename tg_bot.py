import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token, user_id
from main import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["All news", "Last 5 news", "Fresh news"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("News feed", reply_markup=keyboard)


@dp.message_handler(Text(equals="All news"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(v['article_title'])}\n" \
               f"Author - {hunderline(v['article_author'])}\n" \
               f"{v['article_date']}\n" \
               f"{v['article_url']}"
        await message.answer(news)


@dp.message_handler(Text(equals="Last 5 news"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(v['article_title'])}\n" \
               f"Author - {hunderline(v['article_author'])}\n" \
               f"{v['article_date']}\n" \
               f"{v['article_url']}"
        await message.answer(news)


@dp.message_handler(Text(equals="Fresh news"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(v['article_title'])}\n" \
                   f"Author - {hunderline(v['article_author'])}\n" \
                   f"{v['article_date']}\n" \
                   f"{v['article_url']}"
            await message.answer(news)
    else:
        await message.answer("No news yet =(")


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(v['article_title'])}\n" \
                       f"Author - {hunderline(v['article_author'])}\n" \
                       f"{v['article_date']}\n" \
                       f"{v['article_url']}"
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, "No news yet =(", disable_notification=True)
        await asyncio.sleep(20)

if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #loop.create_task(news_every_minute())
    executor.start_polling(dp)

