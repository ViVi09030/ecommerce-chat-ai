"""
Modelos ORM de la capa de infraestructura.

Este módulo define las tablas de base de datos para productos y
memoria de chat usando SQLAlchemy.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from src.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM para la tabla de productos.

    Atributos:
        id (Column): Identificador único del producto.
        name (Column): Nombre del producto.
        brand (Column): Marca del producto.
        category (Column): Categoría del producto.
        size (Column): Talla del producto.
        color (Column): Color del producto.
        price (Column): Precio del producto.
        stock (Column): Cantidad disponible.
        description (Column): Descripción del producto.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class ChatMemoryModel(Base):
    """
    Modelo ORM para la tabla del historial de chat.

    Atributos:
        id (Column): Identificador único del mensaje.
        session_id (Column): Identificador de la sesión de conversación.
        role (Column): Rol del emisor del mensaje.
        message (Column): Texto del mensaje.
        timestamp (Column): Fecha y hora del mensaje.
    """

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )