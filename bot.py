import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# ДАННЫЕ ТВОЕГО БОТА
TOKEN = "8258676796:AAEqzSr3tpWeN3QxrFwORN4RIu4ZMaFIDfU"
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    # Кнопка для открытия Mini App
    kb = [[types.InlineKeyboardButton(text="Открыть Биржу 💰", web_app=types.WebAppInfo(url=APP_URL))]]
    await message.answer(f"Привет, {user_name}! 👋\nБиржа запущена и готова к работе.", 
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

async def handle(request):
    # Читаем файл index.html и отдаем его в Telegram
    try:
        with open('/app/index.html', 'r', encoding='utf-8') as f:
            html = f.read()
        return web.Response(text=html, content_type='text/html')
    except Exception as e:
        return web.Response(text=f"Ошибка: {e}", status=500)

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Обязательный порт 8080 для Bothost
    await web.TCPSite(runner, '0.0.0.0', 8080).start()
    print("ВЕБ-СЕРВЕР ЗАПУЩЕН")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
