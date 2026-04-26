"""
Entidades del dominio para el sistema de e-commerce con chat inteligente.

Este módulo contiene las entidades principales del negocio:
- Product: representa un producto del catálogo
- ChatMessage: representa un mensaje dentro de una conversación
- ChatContext: encapsula el historial reciente de una conversación

Estas clases pertenecen a la capa de dominio, por lo que no deben
depender de frameworks ni detalles de infraestructura.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.

    Esta clase encapsula la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.

    Atributos:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto. Debe ser mayor a 0.
        stock (int): Cantidad disponible en inventario. No puede ser negativa.
        description (str): Descripción del producto.
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio después de crear el objeto.

        Valida que:
        - El precio sea mayor a 0
        - El stock no sea negativo
        - El nombre no esté vacío

        Raises:
            ValueError: Si alguna de las validaciones falla.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío")

    def is_available(self) -> bool:
        """
        Indica si el producto tiene stock disponible.

        Returns:
            bool: True si el stock es mayor a 0, False en caso contrario.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.

        Este método valida que la cantidad sea positiva y que haya
        suficiente inventario antes de descontarlo.

        Args:
            quantity (int): Cantidad a reducir del stock.

        Raises:
            ValueError: Si la cantidad no es positiva o si no hay
                suficiente stock disponible.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0")

        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")

        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.

        Args:
            quantity (int): Cantidad a sumar al stock.

        Raises:
            ValueError: Si la cantidad no es positiva.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser mayor a 0")

        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje del chat.

    Cada mensaje pertenece a una sesión y puede haber sido enviado por
    el usuario o por el asistente virtual.

    Atributos:
        id (Optional[int]): Identificador único del mensaje.
        session_id (str): Identificador de la sesión de conversación.
        role (str): Rol del emisor. Debe ser 'user' o 'assistant'.
        message (str): Contenido textual del mensaje.
        timestamp (datetime): Fecha y hora en que se generó el mensaje.
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio después de crear el mensaje.

        Valida que:
        - El rol sea 'user' o 'assistant'
        - El mensaje no esté vacío
        - El session_id no esté vacío

        Raises:
            ValueError: Si alguna validación falla.
        """
        if self.role not in ["user", "assistant"]:
            raise ValueError("El rol debe ser 'user' o 'assistant'")

        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío")

        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        """
        Indica si el mensaje fue enviado por el usuario.

        Returns:
            bool: True si el rol es 'user', False en caso contrario.
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Indica si el mensaje fue enviado por el asistente.

        Returns:
            bool: True si el rol es 'assistant', False en caso contrario.
        """
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto reciente de una conversación.

    Esta clase se utiliza para conservar coherencia en las respuestas
    del asistente, entregando a la IA los últimos mensajes relevantes.

    Attributes:
        messages (List[ChatMessage]): Lista de mensajes de la conversación.
        max_messages (int): Cantidad máxima de mensajes a considerar
            para el contexto. Por defecto es 6.
    """

    messages: List[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> List[ChatMessage]:
        """
        Obtiene los últimos mensajes de la conversación.

        Returns:
            List[ChatMessage]: Lista con los últimos `max_messages`
            mensajes en orden cronológico.
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Convierte el historial reciente en un texto legible para la IA.

        El formato generado distingue entre mensajes del usuario y del
        asistente, para que el modelo pueda interpretar el contexto
        correctamente.

        Returns:
            str: Historial formateado listo para incluir en el prompt.
        """
        recent_messages = self.get_recent_messages()
        formatted_messages = []

        for msg in recent_messages:
            if msg.is_from_user():
                formatted_messages.append(f"Usuario: {msg.message}")
            else:
                formatted_messages.append(f"Asistente: {msg.message}")

        return "\n".join(formatted_messages)