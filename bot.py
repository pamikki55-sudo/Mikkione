import asyncio, sqlite3, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiohttp import web

TOKEN = "7963384798:AAH7Y-f0LeDxQ3vKLfJNtwOOJjlIyS20RYQ"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"
ADMIN_ID = 1771702671 

bot = Bot(token=TOKEN)
dp = Dispatcher()

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
    # Ссылка с защитой от кэша
    v = os.urandom(2).hex()
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=f"{APP_URL}?u={user_id}&v={v}"))]]
    await message.answer(f"Привет, {name}! 👋\nБиржа запущена.", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@dp.message(Command("add_task"))
async def add_task(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, title, reward, link = message.text.split("|")
        conn = sqlite3.connect('database.db'); cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, reward, link) VALUES (?, ?, ?)", (title.strip(), int(reward), link.strip()))
        conn.commit(); conn.close()
        await message.answer("✅ Задание добавлено!")
    except: await message.answer("Ошибка! Формат: /add_task | Текст | 100 | ссылка")

async def handle(request):
    user_id = request.query.get('u', '0')
    conn = sqlite3.connect('database.db'); cur = conn.cursor()
    cur.execute("SELECT name, balance FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone() or ("Гость", 0)
    cur.execute("SELECT title, reward, link FROM tasks"); tasks = cur.fetchall()
    conn.close()

    tasks_html = "".join([f'<div style="background:white;padding:15px;margin-top:10px;border-radius:10px;display:flex;justify-content:space-between;align-items:center;"><div><b>{t[0]}</b><br>{t[1]} ₽</div><a href="{t[2]}" style="background:#007bff;color:white;padding:5px 10px;text-decoration:none;border-radius:5px;">Выполнить</a></div>' for t in tasks])

    # Генерируем HTML прямо здесь (без файла index.html)
    html_content = f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>body{{font-family:sans-serif;background:#f0f2f5;padding:20px;}} .bal{{background:white;padding:15px;border-radius:15px;display:flex;justify-content:space-between;font-weight:bold;}}</style>
    </head><body>
    <div class="bal"><span>Привет, {user[0]}!</span><span>⭐️ {user[1]}</span></div>
    <h3>ЗАДАНИЯ:</h3>{tasks_html}
    <a href="https://t.me/ONMIKKI" style="display:block;text-align:center;background:#28a745;color:white;padding:15px;margin-top:20px;text-decoration:none;border-radius:10px;">Вывод средств</a>
    </body></html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def main():
    init_db()
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
