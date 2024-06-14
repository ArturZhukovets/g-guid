import logging
import asyncio

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

from src.config import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()


#####################################################################

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    text = (
        f"Привет, {message.from_user.first_name}.\n"
        f"Я расскажу тебе всё о составе продуктов, которые я знаю.\n"
        f"Для начала работы просто напиши название интересующего тебя"
        f" продукта на русском языке и, если я найду его в своей базе знаний, я расскажу всё что о нём знаю!"
    )
    await message.answer(text=text)

#####################################################################

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = (
        "Этот бот предназачен для быстрого подсчёта каллорий и БЖУ.\n\n"
        "Для того чтобы узнать о составе интересующего продукта - просто введите название этого продукта.\n\n"
        "Если необходимо получить полную информацию об комбинации продуктов порционно - введите '/*****'.\n\n"
        "Если необходимо получить полноценный рацион питания на длительный срок - введите '/*****'."
    )
    await message.answer(text=text)

#####################################################################

@dp.message()
async def handle_product(message: types.Message):
    return await message.send_copy(
        chat_id=message.chat.id,
    )

#####################################################################

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
