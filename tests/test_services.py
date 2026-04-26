"""
Pruebas unitarias para la capa de aplicación.

Este módulo valida el comportamiento de ProductService y ChatService
usando mocks para desacoplar los tests de la base de datos y la IA.
"""

from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock
import pytest

from src.domain.entities import Product, ChatMessage
from src.domain.exceptions import ProductNotFoundError, ChatServiceError
from src.application.dtos import ProductDTO, ChatMessageRequestDTO
from src.application.product_service import ProductService
from src.application.chat_service import ChatService


@pytest.fixture
def sample_product():
    """
    Crea un producto de ejemplo para reutilizar en múltiples pruebas.

    Returns:
        Product: Producto de prueba.
    """
    return Product(
        id=1,
        name="Nike Air Zoom Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapato ideal para correr"
    )


@pytest.fixture
def sample_chat_message():
    """
    Crea un mensaje de chat de ejemplo para reutilizar en pruebas.

    Returns:
        ChatMessage: Mensaje de prueba.
    """
    return ChatMessage(
        id=1,
        session_id="user123",
        role="user",
        message="Hola",
        timestamp=datetime.now(timezone.utc)
    )


class TestProductService:
    """
    Conjunto de pruebas unitarias para ProductService.
    """

    def test_get_all_products(self, sample_product):
        """
        Verifica que se obtengan todos los productos como DTOs.
        """
        mock_repo = Mock()
        mock_repo.get_all.return_value = [sample_product]

        service = ProductService(mock_repo)
        result = service.get_all_products()

        assert len(result) == 1
        assert isinstance(result[0], ProductDTO)
        assert result[0].name == "Nike Air Zoom Pegasus"

    def test_get_product_by_id_success(self, sample_product):
        """
        Verifica que se obtenga correctamente un producto existente por ID.
        """
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = sample_product

        service = ProductService(mock_repo)
        result = service.get_product_by_id(1)

        assert isinstance(result, ProductDTO)
        assert result.id == 1
        assert result.name == "Nike Air Zoom Pegasus"

    def test_get_product_by_id_not_found(self):
        """
        Verifica que se lance ProductNotFoundError si el producto no existe.
        """
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        service = ProductService(mock_repo)

        with pytest.raises(ProductNotFoundError, match="Producto con ID 1 no encontrado"):
            service.get_product_by_id(1)

    def test_get_available_products(self):
        """
        Verifica que solo se retornen productos con stock disponible.
        """
        available_product = Product(
            id=1,
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato ideal para correr"
        )

        unavailable_product = Product(
            id=2,
            name="Adidas Ultraboost",
            brand="Adidas",
            category="Running",
            size="41",
            color="Blanco",
            price=150.0,
            stock=0,
            description="Máxima comodidad"
        )

        mock_repo = Mock()
        mock_repo.get_all.return_value = [available_product, unavailable_product]

        service = ProductService(mock_repo)
        result = service.get_available_products()

        assert len(result) == 1
        assert result[0].name == "Nike Air Zoom Pegasus"

    def test_create_product(self):
        """
        Verifica que se cree correctamente un nuevo producto.
        """
        mock_repo = Mock()

        product_dto = ProductDTO(
            id=None,
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato ideal para correr"
        )

        saved_product = Product(
            id=1,
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato ideal para correr"
        )

        mock_repo.save.return_value = saved_product

        service = ProductService(mock_repo)
        result = service.create_product(product_dto)

        assert isinstance(result, ProductDTO)
        assert result.id == 1
        assert result.name == "Nike Air Zoom Pegasus"

    def test_update_product_not_found(self):
        """
        Verifica que no se pueda actualizar un producto inexistente.
        """
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None

        product_dto = ProductDTO(
            id=None,
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato ideal para correr"
        )

        service = ProductService(mock_repo)

        with pytest.raises(ProductNotFoundError):
            service.update_product(1, product_dto)

    def test_delete_product(self):
        """
        Verifica que delete_product delegue correctamente al repositorio.
        """
        mock_repo = Mock()
        mock_repo.delete.return_value = True

        service = ProductService(mock_repo)
        result = service.delete_product(1)

        assert result is True


class TestChatService:
    """
    Conjunto de pruebas unitarias para ChatService.
    """

    @pytest.mark.asyncio
    async def test_process_message_success(self, sample_product):
        """
        Verifica que process_message procese el mensaje y guarde ambos mensajes.
        """
        mock_product_repo = Mock()
        mock_chat_repo = Mock()
        mock_ai_service = Mock()

        mock_product_repo.get_all.return_value = [sample_product]
        mock_chat_repo.get_recent_messages.return_value = []
        mock_ai_service.generate_response = AsyncMock(return_value="Te recomiendo Nike Air Zoom Pegasus")

        service = ChatService(
            product_repository=mock_product_repo,
            chat_repository=mock_chat_repo,
            ai_service=mock_ai_service
        )

        request = ChatMessageRequestDTO(
            session_id="user123",
            message="Busco zapatos para correr"
        )

        result = await service.process_message(request)

        assert result.session_id == "user123"
        assert result.user_message == "Busco zapatos para correr"
        assert result.assistant_message == "Te recomiendo Nike Air Zoom Pegasus"
        assert mock_chat_repo.save_message.call_count == 2

    @pytest.mark.asyncio
    async def test_process_message_raises_chat_service_error(self):
        """
        Verifica que se encapsulen errores internos como ChatServiceError.
        """
        mock_product_repo = Mock()
        mock_chat_repo = Mock()
        mock_ai_service = Mock()

        mock_product_repo.get_all.side_effect = Exception("DB error")

        service = ChatService(
            product_repository=mock_product_repo,
            chat_repository=mock_chat_repo,
            ai_service=mock_ai_service
        )

        request = ChatMessageRequestDTO(
            session_id="user123",
            message="Busco zapatos"
        )

        with pytest.raises(ChatServiceError, match="Error al procesar el mensaje"):
            await service.process_message(request)

    def test_get_session_history(self):
        """
        Verifica que el historial de sesión se retorne como DTOs.
        """
        mock_product_repo = Mock()
        mock_chat_repo = Mock()
        mock_ai_service = Mock()

        messages = [
            ChatMessage(
                id=1,
                session_id="user123",
                role="user",
                message="Hola",
                timestamp=datetime.now(timezone.utc)
            ),
            ChatMessage(
                id=2,
                session_id="user123",
                role="assistant",
                message="Hola, ¿en qué puedo ayudarte?",
                timestamp=datetime.now(timezone.utc)
            ),
        ]

        mock_chat_repo.get_session_history.return_value = messages

        service = ChatService(
            product_repository=mock_product_repo,
            chat_repository=mock_chat_repo,
            ai_service=mock_ai_service
        )

        result = service.get_session_history("user123")

        assert len(result) == 2
        assert result[0].message == "Hola"
        assert result[1].role == "assistant"

    def test_clear_session_history(self):
        """
        Verifica que se elimine el historial de una sesión y se retorne el conteo.
        """
        mock_product_repo = Mock()
        mock_chat_repo = Mock()
        mock_ai_service = Mock()

        mock_chat_repo.delete_session_history.return_value = 4

        service = ChatService(
            product_repository=mock_product_repo,
            chat_repository=mock_chat_repo,
            ai_service=mock_ai_service
        )

        result = service.clear_session_history("user123")

        assert result == 4