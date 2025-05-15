import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import re

API_TOKEN = '7501320294:AAEhkJk8Z7mzMQKzohJov-bAhuTPODbCWio'  # <-- замени сюда свой токен

# Загружаем чёрный список из файла
def load_blacklist(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip()]

# Заменяем запрещённые слова на "капибара"
def replace_blacklisted_words(text: str, blacklist: list) -> str:
    def replacer(match):
        return "В рот пусть тебя ебут"
    pattern = r'\b(' + '|'.join(re.escape(word) for word in blacklist) + r')\b'
    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message()
    async def filter_bad_words(message: Message):
        if message.chat.type in ('group', 'supergroup'):
            blacklist = load_blacklist('blacklist.txt')  # перечитываем каждый раз
            new_text = replace_blacklisted_words(message.text, blacklist)
            if new_text != message.text:
                await message.reply(f"Исправлено:\n{new_text}")

    print("Бот запущен. Ожидание сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())