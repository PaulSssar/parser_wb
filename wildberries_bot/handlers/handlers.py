import asyncio
import logging

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from config import URL, TIME_NOTIFICATION
from db.db import get_data_from_db
from handlers.fsm import SUBSCRIBE
from handlers.utils import parse_data, request_get
from keyboards.keyboard import build_keyboard_inline

router = Router()


@router.message(F.text == '/db')
async def get_last_data(message: Message):
    products = await get_data_from_db(5, message.from_user.id)
    for product in products:
        logging.info(f'1prod{product}')
        await message.answer(
            text=f'Название: {product.name}\nАртикул: {product.article}\n'
                 f'Рейтинг: {product.rating}\n'
                 f'Количество на складах: {product.count_on_stocks}\n'
                 f'Цена: {product.price}',
            reply_markup=await build_keyboard_inline(
                'Подписаться',
                f'/subscribe, {product.article}'),
        )


@router.callback_query(F.data.startswith('/subscribe'))
async def subscribe(callback_data: CallbackQuery, bot: Bot):
    article_of_product = callback_data.data.split(', ')[-1]
    chat_id = callback_data.from_user.id
    SUBSCRIBE[f'chat_id {article_of_product}'] = True

    await bot.send_message(
        chat_id,
        text='Вы успешно подписались на товар')
    while SUBSCRIBE.get(f'chat_id {article_of_product}'):
        for key in SUBSCRIBE.keys():
            article_url = key.split(' ')[-1]
            data = await request_get(URL + article_url)
            name, article, rating, count, price = await parse_data(
                data, callback_data.from_user.id)
            products = await get_data_from_db(
                1,
                callback_data.from_user.id,
                int(article))
            logging.info(f'PROD {products}')
            product = products[0]
            logging.info(product.name)
            logging.info(f'{price} {product.price}')
            if price < product.price:
                await bot.send_message(chat_id=callback_data.from_user.id,
                                       text=f'Цена снижена с {product.price} до {price}'
                                            f'Название: {name}\nАртикул: {article}\n'
                                            f'Рейтинг: {rating}\nКоличество на складах: {count}\n'
                                            f'Цена: {price}',
                                       reply_markup=await build_keyboard_inline(
                                           'Подписаться',
                                           f'/subscribe, {article}'
                                       )
                                       )
        await asyncio.sleep(TIME_NOTIFICATION)


@router.message(F.text == '/stop')
async def unsubscribe(message: Message):
    SUBSCRIBE.clear()
    await message.answer('Вы успешно отписались')
