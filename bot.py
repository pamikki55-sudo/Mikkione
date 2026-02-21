import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web
import os

TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=APP_URL))]]
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\nБиржа готова к работе.", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# ЭТОТ БЛОК ЛЕЧИТ ОШИБКУ 404
async def handle(request):
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return web.Response(text=f.read(), content_type='text/html')
    return web.Response(text="Файл index.html не найден!", status=404)

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080) # Bothost ждет сайт на порту 8080
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
