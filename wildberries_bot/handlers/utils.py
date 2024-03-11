from aiogram.client.session import aiohttp
from db.db import save_data_to_postgres


async def request_get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        return data
    except ConnectionError:
        print('Ошибка соединения')


async def count_on_stocks(stocks):
    count = 0
    for stock in stocks:
        count += stock['qty']
    return count


async def parse_data(data, user_id):
    name = data['data']['products'][0]['name']
    article = data['data']['products'][0]['id']
    rating = data['data']['products'][0]['reviewRating']
    price = str(data['data']['products'][0]['salePriceU'])[:-2:]
    stocks = data['data']['products'][0]['sizes'][0]['stocks']
    count = await count_on_stocks(stocks)
    user_id = user_id
    await save_data_to_postgres(name,
                                article,
                                rating,
                                count,
                                price,
                                user_id
                                )
    return name, article, rating, count, price
