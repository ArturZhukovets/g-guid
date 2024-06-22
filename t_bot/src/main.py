import json
import logging
import asyncio

from aiogram import types
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from cache_service import MemCacher
from src.api_service import ProductCompositionAPIService
from src.config import settings
from src.utils import product_to_pretty_str

dp = Dispatcher()
cacher = MemCacher()


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

@dp.message(~F.text)
async def handle_no_text_message(message: types.Message):
    """Handling all non-text messages"""
    await message.answer(
        text="Бот поддерживает только текстовый формат ввода.\n"
        "Пожалуйста введите запрос в виде текста."
    )

#####################################################################

@dp.message()
async def handle_product(message: types.Message):
    await message.answer(text="Подождите пару секунд...")
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )

    product_service = ProductCompositionAPIService()
    response_json = await product_service.find_products(product_title=message.text)
    items = response_json['items']
    count = response_json['count']
    if count == 0:
        return await message.answer(
            "К сожалению по вашему запросу не найдено ни одного продукта 😟."
        )
    if count == 1:
        return await message.answer(product_to_pretty_str(items[0]))

    keyboard = InlineKeyboardBuilder()
    for product in items:
        keyboard.button(
            text=product['ru_title'],
            callback_data=f"product_{product['id']}"
        )
    keyboard.adjust(1)
    cacher.set_products_data(chat_id=message.chat.id, data=items)
    text = f"Всего найдено продуктов по запросу: {response_json['count']}\n"
    return await message.answer(text=text, reply_markup=keyboard.as_markup(resize_keyboard=True))


@dp.callback_query(lambda c: c.data.startswith('product_'))
async def process_callback(callback_query: types.CallbackQuery):
    message = callback_query.message
    product_id = callback_query.data.split("_")[-1]
    if not product_id.isdigit():
        return await message.answer(text="Что-то пошло не так. Попробуйте ещё раз.")
    product_id = int(product_id)
    product = cacher.get_product(chat_id=message.chat.id, product_id=product_id)
    if not product:
        # TODO Think how to implement it the best way.
        #  For example in this case generate a new query to productDetail
        return await message.answer(
            "Информации больше нет или она больше не актуальна.\n"
            "Возможно запрос был сделан слишком давно."
            "Попробуйте ввести название продукта ещё раз."
        )
    product_str = product_to_pretty_str(product)
    return await message.answer(text=product_str)

#####################################################################

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
