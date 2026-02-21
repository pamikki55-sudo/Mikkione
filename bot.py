import asyncio, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# ТВОИ ДАННЫЕ
TOKEN = "8258676796:AAEqzSr3tpWeN3QxrFwORN4RIu4ZMaFIDfU"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ФУНКЦИЯ ДЛЯ ОТРИСОВКИ ДИЗАЙНА (КАК НА СКРИНШОТАХ)
def get_html(user_name):
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; padding: 15px; color: #1c1e21; }}
            .header {{ background: white; padding: 20px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
            .balance {{ background: #e7f3ff; padding: 8px 16px; border-radius: 25px; color: #1877f2; font-weight: bold; font-size: 18px; }}
            .task-card {{ background: white; padding: 20px; border-radius: 15px; margin-top: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
            .btn {{ background: #1877f2; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; }}
            .withdraw {{ display: block; text-align: center; background: #42b72a; color: white; padding: 18px; border-radius: 15px; margin-top: 30px; text-decoration: none; font-weight: bold; font-size: 18px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div style="font-weight: bold; font-size: 20px;">Привет, {user_name}! 👋</div>
            <div class="balance">⭐️ 0 ₽</div>
        </div>
        <h3 style="margin-top: 30px; color: #606770;">ДОСТУПНЫЕ ЗАДАНИЯ</h3>
        
        <div class="task-card">
            <div><b>Подписаться на канал</b><br><small style="color:green;">+ 150 ₽</small></div>
            <a href="https://t.me/mikkione" class="btn">Выполнить</a>
        </div>

        <div class="task-card">
            <div><b>Поставить лайки</b><br><small style="color:green;">+ 100 ₽</small></div>
            <a href="#" class="btn">Выполнить</a>
        </div>

        <a href="https://t.me/ONMIKKI" class="withdraw">Вывод средств</a>
    </body>
    </html>
    """

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    # Используем твою новую ссылку
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=APP_URL))]]
    await message.answer(f"Привет, {user_name}! 👋\nБиржа запущена и готова к работе.", 
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

async def handle(request):
    return web.Response(text=get_html("Пользователь"), content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # СТРОГО ПОРТ 8080
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    print("ВЕБ-СЕРВЕР ЗАПУЩЕН НА ПОРТУ 8080")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
