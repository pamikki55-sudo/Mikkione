import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Вставь сюда НОВЫЙ токен от @BotFather (после того как нажмешь Revoke)
TOKEN = "ТВОЙ_НОВЫЙ_ТОКЕН"

# Твой адрес из панели Bothost (скопируй его там)
APP_URL = "https://pamikki55-sudo-mikkione.bothost.ru" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # Текст приветствия
    text = (f"Привет, {user_name}! 👋\n\n"
            f"Твой ID: `{user_id}`\n"
            "Добро пожаловать в проект @hackmikki.\n"
            "Нажми кнопку ниже, чтобы открыть биржу!")
    
    # Кнопка открытия приложения
    kb = [[types.InlineKeyboardButton(
        text="Открыть Биржу 💰", 
        web_app=types.WebAppInfo(url=APP_URL)
    )]]
    
    await message.answer(text, reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="Markdown")

async def main():
    print("Бот @hackmikki запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
