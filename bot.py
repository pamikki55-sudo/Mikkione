import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Твой проверенный токен и адрес
TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = [[types.InlineKeyboardButton(
        text="Открыть Биржу 💰", 
        web_app=types.WebAppInfo(url=APP_URL)
    )]]
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nБиржа запущена. Если видишь белый экран — открой ссылку в браузере один раз.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb)
    )

# Исправленный обработчик сайта (отдает index.html)
async def handle(request):
    path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            return web.Response(text=content, content_type='text/html')
    else:
        return web.Response(text=f"Ошибка: файл index.html не найден по пути {path}", status=404)

async def main():
    # Настройка веб-сервера на порту 8080 для Bothost
    app = web.Application()
    app.router.add_get('/', handle)
    
    # Запуск сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    
    print("--- СИСТЕМА ЗАПУЩЕНА ---")
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
