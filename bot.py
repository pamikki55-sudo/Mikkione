import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"
CHANNEL_ID = -1003496001891  # Твой ID из скриншота
ADMIN_ID = 1771702671 # Твой ID (подставь свой точный из бота)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ ---
def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users 
                   (id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0, referrer INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, reward INTEGER, link TEXT)''')
    conn.commit()
    conn.close()

# --- ЛОГИКА БОТА ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cur.fetchone():
        # Реферальная система
        referrer = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
        cur.execute("INSERT INTO users (id, referrer) VALUES (?, ?)", (user_id, referrer))
        if referrer:
            cur.execute("UPDATE users SET balance = balance + 10 WHERE id = ?", (referrer,))
        conn.commit()
    
    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=f"{APP_URL}?user_id={user_id}"))
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\nВаш баланс: 0 ₽\nПриглашай друзей и получай бонусы!",
        reply_markup=kb.as_markup()
    )
    conn.close()

# --- АДМИН-ПАНЕЛЬ (Добавление заданий) ---
@dp.message(Command("add_task"))
async def add_task(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, title, reward, link = message.text.split("|")
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, reward, link) VALUES (?, ?, ?)", (title.strip(), int(reward), link.strip()))
        conn.commit()
        await message.answer("✅ Задание добавлено!")
    except:
        await message.answer("Ошибка! Формат: /add_task | Название | 100 | ссылка")

# --- СЕРВЕР ДЛЯ WEB APP ---
async def handle(request):
    user_id = request.query.get('user_id')
    # Здесь логика отдачи index.html с подстановкой баланса из БД
    path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return web.Response(text=f.read(), content_type='text/html')
    return web.Response(text="Ошибка 404", status=404)

async def main():
    init_db()
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
