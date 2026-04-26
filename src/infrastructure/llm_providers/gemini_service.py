"""
Servicio de integración con Google Gemini AI.

Este módulo encapsula la comunicación con el proveedor de IA para
mantener la infraestructura desacoplada de la capa de aplicación.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

from src.domain.entities import Product, ChatContext


class GeminiService:
    """
    Servicio para interactuar con Google Gemini AI.

    Atributos:
        model: Instancia del modelo generativo de Gemini.
    """

    def __init__(self):
        """
        Inicializa el cliente de Gemini usando la API key del entorno.

        Raises:
            ValueError: Si no existe la variable GEMINI_API_KEY.
        """
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró la variable GEMINI_API_KEY en el archivo .env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def format_products_info(self, products: list[Product]) -> str:
        """
        Convierte la lista de productos en un bloque de texto para el prompt.

        Args:
            products (list[Product]): Productos disponibles en el catálogo.

        Returns:
            str: Texto formateado con información de productos.
        """
        if not products:
            return "No hay productos disponibles en este momento."

        lines = []
        for product in products:
            lines.append(
                f"- {product.name} | Marca: {product.brand} | "
                f"Categoría: {product.category} | Talla: {product.size} | "
                f"Color: {product.color} | Precio: ${product.price} | "
                f"Stock: {product.stock} | Descripción: {product.description}"
            )

        return "\n".join(lines)

    async def generate_response(
        self,
        user_message: str,
        products: list[Product],
        context: ChatContext
    ) -> str:
        """
        Genera una respuesta de Gemini usando productos y contexto conversacional.

        Args:
            user_message (str): Mensaje actual del usuario.
            products (list[Product]): Lista de productos disponibles.
            context (ChatContext): Historial reciente de la conversación.

        Returns:
            str: Respuesta generada por Gemini.
        """
        products_info = self.format_products_info(products)
        conversation_context = context.format_for_prompt()

        prompt = f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes información, sé honesto
- Responde en español

HISTORIAL DE CONVERSACIÓN:
{conversation_context}

MENSAJE ACTUAL DEL USUARIO:
Usuario: {user_message}

RESPUESTA DEL ASISTENTE:
"""

        response = await self.model.generate_content_async(prompt)
        return response.text.strip()