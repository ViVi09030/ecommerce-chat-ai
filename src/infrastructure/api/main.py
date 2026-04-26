"""
Aplicación principal FastAPI del sistema.

Este módulo define el punto de entrada de la API REST, configura CORS,
la inicialización de base de datos y los endpoints principales.
"""

from datetime import datetime, timezone
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from src.application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
)
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.domain.exceptions import ProductNotFoundError, ChatServiceError
from src.infrastructure.db.database import get_db, init_db, SessionLocal
from src.infrastructure.db.init_data import load_initial_data
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.

    Al iniciar la aplicación:
    - crea las tablas de base de datos
    - carga datos iniciales si la tabla de productos está vacía

    Args:
        app (FastAPI): Instancia de la aplicación FastAPI.

    Yields:
        None
    """
    init_db()

    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="E-commerce Chat AI API",
    description="API REST para e-commerce de zapatos con chat inteligente usando Gemini",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Retorna información básica de la API.

    Returns:
        dict: Mensaje de bienvenida, versión y lista de endpoints.
    """
    return {
        "message": "Bienvenido a la API de E-commerce Chat AI",
        "version": "1.0.0",
        "endpoints": [
            "/docs",
            "/products",
            "/products/{product_id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health"
        ]
    }


@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos.

    Args:
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ProductDTO]: Lista de productos registrados.
    """
    product_repo = SQLProductRepository(db)
    product_service = ProductService(product_repo)
    return product_service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto por su identificador.

    Args:
        product_id (int): ID del producto.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        ProductDTO: Producto encontrado.

    Raises:
        HTTPException: Si el producto no existe.
    """
    product_repo = SQLProductRepository(db)
    product_service = ProductService(product_repo)

    try:
        return product_service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario y genera una respuesta con IA.

    Args:
        request (ChatMessageRequestDTO): Cuerpo de la petición con
            session_id y mensaje.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        ChatMessageResponseDTO: Respuesta generada por el asistente.

    Raises:
        HTTPException: Si ocurre un error al procesar el chat.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    chat_service = ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        ai_service=ai_service
    )

    try:
        return await chat_service.process_message(request)
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(session_id: str, limit: Optional[int] = 10, db: Session = Depends(get_db)):
    """
    Obtiene el historial de mensajes de una sesión.

    Args:
        session_id (str): Identificador de la sesión.
        limit (Optional[int]): Cantidad máxima de mensajes a retornar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[ChatHistoryDTO]: Historial de mensajes de la sesión.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    chat_service = ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        ai_service=ai_service
    )

    return chat_service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina el historial completo de una sesión.

    Args:
        session_id (str): Identificador de la sesión.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje indicando cuántos mensajes fueron eliminados.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    chat_service = ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        ai_service=ai_service
    )

    deleted_count = chat_service.clear_session_history(session_id)

    return {
        "message": f"Se eliminaron {deleted_count} mensajes de la sesión '{session_id}'"
    }


@app.get("/health")
def health_check():
    """
    Verifica el estado general de la API.

    Returns:
        dict: Estado de salud y timestamp en UTC.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }