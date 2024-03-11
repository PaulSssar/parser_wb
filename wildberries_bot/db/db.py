import logging
import os

from sqlalchemy import Integer, MetaData, String, select, func, DateTime
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

engine = create_async_engine(
    f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}'
    f':{os.getenv("POSTGRES_PASSWORD")}'
    f'@{os.getenv("DB_HOST")}/{os.getenv("POSTGRES_DB")}')

metadata = MetaData()

Base = declarative_base()

session = async_sessionmaker(engine,
                             class_=AsyncSession,
                             expire_on_commit=False)


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(150))
    article: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(Integer)
    count_on_stocks: Mapped[int] = mapped_column(Integer)
    price: Mapped[str] = mapped_column(String(15))
    user_id: Mapped[int] = mapped_column(Integer)
    time_request: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now())


async def save_data_to_postgres(name,
                                article,
                                rating,
                                count_on_stocks,
                                price,
                                user_id):
    async with engine.connect() as connect:
        await connect.execute(Product.__table__.insert().values(
            name=name,
            article=article,
            rating=rating,
            count_on_stocks=count_on_stocks,
            price=price,
            user_id=user_id
        ))
        await connect.commit()


async def get_data_from_db(count, user_id):
    query = select(Product).filter(
        Product.user_id == user_id).order_by(
        Product.id.desc()).limit(count)
    async with session.begin() as connection:
        result = await connection.execute(query)
        products = result.scalars().all()
        logging.info(f'res {products}')
        return products


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
