from aiogram.types import BotCommand

COMMANDS = [BotCommand(command='/start',
                       description='Получить информацию по товару'),
            BotCommand(command='/stop',
                       description='Отключить подписку'),
            BotCommand(command='/db',
                       description='Получить информацию из БД')
            ]

URL = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm='
