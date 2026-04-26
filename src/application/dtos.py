"""
DTOs de la capa de aplicación.

Este módulo define los objetos de transferencia de datos utilizados
para comunicar la capa de aplicación con la infraestructura y la API,
incluyendo validaciones con Pydantic.
"""

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.

    Atributos:
        id (Optional[int]): Identificador del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto.
        stock (int): Cantidad disponible en inventario.
        description (str): Descripción del producto.
    """

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        """
        Valida que el precio sea mayor a 0.

        Args:
            v (float): Valor del precio.

        Returns:
            float: Precio validado.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
        """
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @field_validator("stock")
    @classmethod
    def stock_must_be_non_negative(cls, v):
        """
        Valida que el stock no sea negativo.

        Args:
            v (int): Valor del stock.

        Returns:
            int: Stock validado.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el endpoint de chat.

    Atributos:
        session_id (str): Identificador de la sesión.
        message (str): Texto del mensaje enviado por el usuario.
    """

    session_id: str
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v):
        """
        Valida que el mensaje no esté vacío.

        Args:
            v (str): Contenido del mensaje.

        Returns:
            str: Mensaje validado.

        Raises:
            ValueError: Si el mensaje está vacío o contiene solo espacios.
        """
        if not v or not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v

    @field_validator("session_id")
    @classmethod
    def session_id_not_empty(cls, v):
        """
        Valida que el identificador de sesión no esté vacío.

        Args:
            v (str): Session ID.

        Returns:
            str: Session ID validado.

        Raises:
            ValueError: Si el session_id está vacío o contiene solo espacios.
        """
        if not v or not v.strip():
            raise ValueError("El session_id no puede estar vacío")
        return v


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar la respuesta del chat al cliente.

    Atributos:
        session_id (str): Identificador de la sesión.
        user_message (str): Mensaje enviado por el usuario.
        assistant_message (str): Respuesta generada por el asistente.
        timestamp (datetime): Momento en que se generó la respuesta.
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para representar mensajes del historial de una sesión.

    Atributos:
        id (int): Identificador del mensaje.
        role (str): Rol del emisor del mensaje.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    id: int
    role: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)