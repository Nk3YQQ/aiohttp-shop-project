from typing import Annotated, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

int_pk = Annotated[int, mapped_column(primary_key=True)]
title_category_field = Annotated[str, mapped_column(String(100), unique=True, nullable=False)]
title_product_field = Annotated[str, mapped_column(String(100), nullable=False)]
category_id = Annotated[int, mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))]


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int_pk]
    title: Mapped[title_category_field]

    products: Mapped[List['Product']] = relationship(back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int_pk]
    title: Mapped[title_product_field]
    description: Mapped[str]
    price: Mapped[float]
    category_id: Mapped[category_id]

    category: Mapped['Category'] = relationship(back_populates='products')
