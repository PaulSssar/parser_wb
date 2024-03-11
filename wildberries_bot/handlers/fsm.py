from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import URL
from handlers.utils import parse_data, request_get
from keyboards.keyboard import build_keyboard_inline


class Article(StatesGroup):
    article = State()


router_fsm = Router()
SUBSCRIBE = {}


@router_fsm.message(CommandStart())
async def get_article(message: Message, state: FSMContext):
    await message.reply(
        'Введите артикул товара, чтобы получить информацию по нему'
    )
    await state.set_state(Article.article)


@router_fsm.message(Article.article)
async def get_data(message: Message, state: FSMContext):
    try:
        await state.set_data({'url': message.text})
        data = await request_get(URL + message.text)
        name, article, rating, count, price = await parse_data(
            data, message.from_user.id)
        await message.answer(
            f'Название: {name}\nАртикул: {article}\n'
            f'Рейтинг: {rating}\nКоличество на складах: {count}\n'
            f'Цена: {price}',
            reply_markup=await build_keyboard_inline(
                    'Подписаться',
                    f'/subscribe, {article}'
                )
            )
    except IndexError:
        await message.answer('Неверный артикул, введите заново')
        await state.clear()
