from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

subscribe_button = InlineKeyboardButton(
    text='Подписаться',
    callback_data='/subscribe'
)
unsubscribe_button = InlineKeyboardButton(
    text='Отписаться',
    callback_data='/unsubscribe'
)

subscribe_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[subscribe_button, unsubscribe_button], ]
)


async def build_keyboard_inline(text, data):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=data), ]])
