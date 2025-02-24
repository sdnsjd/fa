from uuid import UUID
import sqlalchemy
from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.dbase.database import async_engine, Base, async_session_factory
from backend.dbase.schemas import CategoryEnum


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")


class SessionORM(Base):
    __tablename__ = "session"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)


class CartORM(Base):
    __tablename__ = "cart"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)


class CartItemsORM(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[str] = mapped_column(ForeignKey("cart.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    quantity: Mapped[int]


class ProductORM(Base):
    __tablename__ = "product"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name: Mapped[str]
    price: Mapped[float]
    size: Mapped[str] = mapped_column(nullable=True)
    main_image: Mapped[str]
    quantity: Mapped[int]
    total_price: Mapped[float] = mapped_column(nullable=True)
    category: Mapped[CategoryEnum]
    # Связь с таблицей изображений
    images: Mapped[list["ImageORM"]] = relationship("ImageORM", back_populates="product", cascade="all, delete-orphan")


class ImageORM(Base):
    __tablename__ = "image"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("product.id"))
    image_url: Mapped[str]
    # Обратная связь с таблицей товаров
    product: Mapped[ProductORM] = relationship("ProductORM", back_populates="images")




