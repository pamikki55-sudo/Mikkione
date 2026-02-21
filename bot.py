import asyncio, sqlite3, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiohttp import web

TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"
ADMIN_ID = 1771702671 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем базу данных
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER DEFAULT 0)')
    cur.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, reward INTEGER, link TEXT)')
    conn.commit()
    conn.close()

@dp.message(CommandStart())
async def start(message: types.Message):
    user_id, name = message.from_user.id, message.from_user.first_name
    conn = sqlite3.connect('database.db'); cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))
    conn.commit(); conn.close()
    
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=f"{APP_URL}?u={user_id}"))]]
    await message.answer(f"Привет, {name}! Нажми кнопку ниже:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@dp.message(Command("add_task"))
async def add_task(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, title, reward, link = message.text.split("|")
        conn = sqlite3.connect('database.db'); cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, reward, link) VALUES (?, ?, ?)", (title.strip(), int(reward), link.strip()))
        conn.commit(); conn.close()
        await message.answer("✅ Задание добавлено!")
    except: await message.answer("Ошибка! Пример: /add_task | Подписка | 100 | https://t.me/mikkione")

async def handle(request):
    user_id = request.query.get('u', '0')
    conn = sqlite3.connect('database.db'); cur = conn.cursor()
    cur.execute("SELECT name, balance FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone() or ("Гость", 0)
    cur.execute("SELECT title, reward, link FROM tasks"); tasks = cur.fetchall()
    conn.close()

    tasks_html = "".join([f'<div class="task-card"><div><b>{t[0]}</b><br><small>{t[1]} ₽</small></div><a href="{t[2]}" class="btn">Выполнить</a></div>' for t in tasks])
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read().replace("{NAME}", str(user[0])).replace("{BALANCE}", str(user[1])).replace("{TASKS}", tasks_html)
    return web.Response(text=html, content_type='text/html')

async def main():
    init_db()
    app = web.Application(); app.router.add_get('/', handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
