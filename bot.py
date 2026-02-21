import asyncio, sqlite3, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
# Твой точный URL из панели Bothost
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# База данных для баланса
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)')
    conn.commit()
    conn.close()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Кнопка, которая открывает Mini App
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=APP_URL))]]
    await message.answer("Приложение готово! Нажми на кнопку ниже:", 
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

# Твой дизайн сайта (вместо index.html)
async def handle_webapp(request):
    html_content = """
    <!DOCTYPE html><html><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; padding: 20px; text-align: center; }
        .card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; }
        .btn { display: inline-block; padding: 15px 30px; background: #34a853; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; margin-top: 20px; }
    </style>
    </head><body>
        <div class="card">
            <h1>Биржа Труда ⚒️</h1>
            <p>Добро пожаловать!</p>
            <div style="font-size: 24px;">Баланс: <b>0 ₽</b></div>
            <a href="https://t.me/ONMIKKI" class="btn">Вывод средств</a>
        </div>
    </body></html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def main():
    init_db()
    # Создаем веб-сервер
    app = web.Application()
    app.router.add_get('/', handle_webapp)
    
    runner = web.AppRunner(app)
    await runner.setup()
    # Bothost ВСЕГДА слушает порт 8080
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    print("Бот и Веб-сайт запущены на Bothost!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
