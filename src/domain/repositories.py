"""
Interfaces de repositorio del dominio.

Este módulo define los contratos abstractos para acceder a productos
y mensajes de chat sin acoplar la lógica de negocio a una tecnología
concreta de persistencia.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.

    Las implementaciones concretas de esta interfaz se encuentran en la
    capa de infraestructura, por ejemplo usando SQLAlchemy.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos registrados.

        Returns:
            List[Product]: Lista completa de productos.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su identificador.

        Args:
            product_id (int): ID del producto a consultar.

        Returns:
            Optional[Product]: Producto encontrado o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand (str): Marca a consultar.

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        Args:
            category (str): Categoría a consultar.

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto.

        Si el producto ya tiene ID, normalmente se interpreta como una
        actualización. Si no lo tiene, se considera un nuevo registro.

        Args:
            product (Product): Producto a guardar.

        Returns:
            Product: Producto persistido.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su identificador.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones.

    Define las operaciones necesarias para guardar y recuperar mensajes
    de chat asociados a una sesión específica.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial.

        Args:
            message (ChatMessage): Mensaje a persistir.

        Returns:
            ChatMessage: Mensaje guardado con su información persistida.
        """
        pass

    @abstractmethod
    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Cantidad máxima de mensajes a retornar.

        Returns:
            List[ChatMessage]: Historial de la sesión en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los mensajes más recientes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Cantidad de mensajes recientes requeridos.

        Returns:
            List[ChatMessage]: Mensajes recientes en orden cronológico.
        """
        pass