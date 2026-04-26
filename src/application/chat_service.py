"""
Servicio de aplicación para el chat con IA.

Este módulo coordina la interacción entre productos, historial de chat
y el servicio externo de inteligencia artificial.
"""

from datetime import datetime, timezone
from typing import List, Optional

from src.domain.entities import ChatMessage, ChatContext
from src.domain.repositories import IProductRepository, IChatRepository
from src.domain.exceptions import ChatServiceError
from .dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO


class ChatService:
    """
    Servicio de aplicación para gestionar el chat con IA.

    Atributos:
        product_repository (IProductRepository): Repositorio de productos.
        chat_repository (IChatRepository): Repositorio de mensajes de chat.
        ai_service: Servicio externo encargado de generar respuestas.
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service
    ):
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repository (IProductRepository): Repositorio de productos.
            chat_repository (IChatRepository): Repositorio de historial de chat.
            ai_service: Servicio de IA para generar respuestas.
        """
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta usando IA.

        Flujo general:
        1. Obtiene productos disponibles
        2. Recupera historial reciente
        3. Construye el contexto conversacional
        4. Solicita una respuesta al servicio de IA
        5. Guarda mensaje del usuario y respuesta del asistente
        6. Retorna un DTO de respuesta

        Args:
            request (ChatMessageRequestDTO): Mensaje enviado por el usuario.

        Returns:
            ChatMessageResponseDTO: Respuesta generada por el asistente.

        Raises:
            ChatServiceError: Si ocurre un error en el procesamiento.
        """
        try:
            products = self.product_repository.get_all()

            recent_history = self.chat_repository.get_recent_messages(
                request.session_id,
                6
            )

            context = ChatContext(messages=recent_history)

            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context
            )

            user_chat_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=datetime.now(timezone.utc)
            )

            assistant_chat_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=datetime.now(timezone.utc)
            )

            self.chat_repository.save_message(user_chat_message)
            self.chat_repository.save_message(assistant_chat_message)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=datetime.now(timezone.utc)
            )

        except Exception as e:
            raise ChatServiceError(f"Error al procesar el mensaje: {str(e)}")

    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar.

        Returns:
            List[ChatHistoryDTO]: Historial de la sesión en formato DTO.
        """
        messages = self.chat_repository.get_session_history(session_id, limit)
        return [ChatHistoryDTO.model_validate(message) for message in messages]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id (str): Identificador de la sesión.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        return self.chat_repository.delete_session_history(session_id)