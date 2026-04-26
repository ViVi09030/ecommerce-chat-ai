"""
Repositorio concreto para el historial de chat usando SQLAlchemy.

Este módulo implementa la interfaz IChatRepository de la capa de dominio.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación concreta del repositorio de chat usando SQLAlchemy.

    Atributos:
        db (Session): Sesión activa de base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en la base de datos.

        Args:
            message (ChatMessage): Entidad de dominio a persistir.

        Returns:
            ChatMessage: Mensaje persistido.
        """
        model = ChatMemoryModel(
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._model_to_entity(model)

    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Límite opcional de mensajes.

        Returns:
            List[ChatMessage]: Mensajes de la sesión en orden cronológico.
        """
        query = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.asc())
        )

        if limit is not None:
            query = query.limit(limit)

        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id)
        count = query.count()
        query.delete()
        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los mensajes más recientes de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número máximo de mensajes recientes.

        Returns:
            List[ChatMessage]: Mensajes recientes en orden cronológico.
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )

        models.reverse()

        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM en una entidad del dominio.

        Args:
            model (ChatMemoryModel): Modelo ORM del mensaje.

        Returns:
            ChatMessage: Entidad del dominio equivalente.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )