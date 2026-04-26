"""
Pruebas unitarias para las entidades del dominio.

Este módulo valida el comportamiento de Product, ChatMessage y
ChatContext, incluyendo reglas de negocio y utilidades de contexto.
"""

from datetime import datetime, timezone
import pytest

from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:
    """
    Conjunto de pruebas para la entidad Product.
    """

    def test_create_valid_product(self):
        """
        Verifica que un producto válido se cree correctamente.
        """
        product = Product(
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

        assert product.name == "Nike Air Zoom Pegasus"
        assert product.price == 120.0
        assert product.stock == 5

    def test_product_price_must_be_positive(self):
        """
        Verifica que el precio deba ser mayor a 0.
        """
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            Product(
                id=None,
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=0,
                stock=5,
                description="Zapato ideal para correr"
            )

    def test_product_stock_must_not_be_negative(self):
        """
        Verifica que el stock no pueda ser negativo.
        """
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            Product(
                id=None,
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=-1,
                description="Zapato ideal para correr"
            )

    def test_product_name_must_not_be_empty(self):
        """
        Verifica que el nombre no pueda estar vacío.
        """
        with pytest.raises(ValueError, match="El nombre del producto no puede estar vacío"):
            Product(
                id=None,
                name="   ",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=5,
                description="Zapato ideal para correr"
            )

    def test_is_available_returns_true_when_stock_greater_than_zero(self):
        """
        Verifica que is_available retorne True cuando hay stock.
        """
        product = Product(
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

        assert product.is_available() is True

    def test_is_available_returns_false_when_stock_is_zero(self):
        """
        Verifica que is_available retorne False cuando el stock es 0.
        """
        product = Product(
            id=None,
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=0,
            description="Zapato ideal para correr"
        )

        assert product.is_available() is False

    def test_reduce_stock_successfully(self):
        """
        Verifica que el stock pueda reducirse correctamente.
        """
        product = Product(
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

        product.reduce_stock(2)

        assert product.stock == 3

    def test_reduce_stock_quantity_must_be_positive(self):
        """
        Verifica que no se pueda reducir stock con cantidad no positiva.
        """
        product = Product(
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

        with pytest.raises(ValueError, match="La cantidad a reducir debe ser mayor a 0"):
            product.reduce_stock(0)

    def test_reduce_stock_must_have_enough_stock(self):
        """
        Verifica que no se pueda reducir más stock del disponible.
        """
        product = Product(
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

        with pytest.raises(ValueError, match="No hay suficiente stock disponible"):
            product.reduce_stock(10)

    def test_increase_stock_successfully(self):
        """
        Verifica que el stock pueda aumentarse correctamente.
        """
        product = Product(
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

        product.increase_stock(3)

        assert product.stock == 8

    def test_increase_stock_quantity_must_be_positive(self):
        """
        Verifica que no se pueda aumentar stock con cantidad no positiva.
        """
        product = Product(
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

        with pytest.raises(ValueError, match="La cantidad a aumentar debe ser mayor a 0"):
            product.increase_stock(0)


class TestChatMessage:
    """
    Conjunto de pruebas para la entidad ChatMessage.
    """

    def test_create_valid_chat_message(self):
        """
        Verifica que un mensaje válido se cree correctamente.
        """
        message = ChatMessage(
            id=None,
            session_id="user123",
            role="user",
            message="Hola",
            timestamp=datetime.now(timezone.utc)
        )

        assert message.session_id == "user123"
        assert message.role == "user"
        assert message.message == "Hola"

    def test_role_must_be_user_or_assistant(self):
        """
        Verifica que el rol sea únicamente 'user' o 'assistant'.
        """
        with pytest.raises(ValueError, match="El rol debe ser 'user' o 'assistant'"):
            ChatMessage(
                id=None,
                session_id="user123",
                role="admin",
                message="Hola",
                timestamp=datetime.now(timezone.utc)
            )

    def test_message_must_not_be_empty(self):
        """
        Verifica que el mensaje no pueda estar vacío.
        """
        with pytest.raises(ValueError, match="El mensaje no puede estar vacío"):
            ChatMessage(
                id=None,
                session_id="user123",
                role="user",
                message="   ",
                timestamp=datetime.now(timezone.utc)
            )

    def test_session_id_must_not_be_empty(self):
        """
        Verifica que el session_id no pueda estar vacío.
        """
        with pytest.raises(ValueError, match="El session_id no puede estar vacío"):
            ChatMessage(
                id=None,
                session_id="   ",
                role="user",
                message="Hola",
                timestamp=datetime.now(timezone.utc)
            )

    def test_is_from_user(self):
        """
        Verifica que is_from_user identifique correctamente un mensaje del usuario.
        """
        message = ChatMessage(
            id=None,
            session_id="user123",
            role="user",
            message="Hola",
            timestamp=datetime.now(timezone.utc)
        )

        assert message.is_from_user() is True
        assert message.is_from_assistant() is False

    def test_is_from_assistant(self):
        """
        Verifica que is_from_assistant identifique correctamente un mensaje del asistente.
        """
        message = ChatMessage(
            id=None,
            session_id="user123",
            role="assistant",
            message="Hola, ¿en qué puedo ayudarte?",
            timestamp=datetime.now(timezone.utc)
        )

        assert message.is_from_assistant() is True
        assert message.is_from_user() is False


class TestChatContext:
    """
    Conjunto de pruebas para el objeto de valor ChatContext.
    """

    def test_get_recent_messages_returns_last_n_messages(self):
        """
        Verifica que se retornen los últimos N mensajes del historial.
        """
        messages = [
            ChatMessage(
                id=i,
                session_id="user123",
                role="user" if i % 2 == 0 else "assistant",
                message=f"Mensaje {i}",
                timestamp=datetime.now(timezone.utc)
            )
            for i in range(8)
        ]

        context = ChatContext(messages=messages, max_messages=6)
        recent_messages = context.get_recent_messages()

        assert len(recent_messages) == 6
        assert recent_messages[0].message == "Mensaje 2"
        assert recent_messages[-1].message == "Mensaje 7"

    def test_format_for_prompt(self):
        """
        Verifica que el historial se formatee correctamente para el prompt.
        """
        messages = [
            ChatMessage(
                id=1,
                session_id="user123",
                role="user",
                message="Busco zapatos para correr",
                timestamp=datetime.now(timezone.utc)
            ),
            ChatMessage(
                id=2,
                session_id="user123",
                role="assistant",
                message="Tengo varias opciones disponibles",
                timestamp=datetime.now(timezone.utc)
            ),
            ChatMessage(
                id=3,
                session_id="user123",
                role="user",
                message="Talla 42",
                timestamp=datetime.now(timezone.utc)
            ),
        ]

        context = ChatContext(messages=messages)
        formatted = context.format_for_prompt()

        expected = (
            "Usuario: Busco zapatos para correr\n"
            "Asistente: Tengo varias opciones disponibles\n"
            "Usuario: Talla 42"
        )

        assert formatted == expected