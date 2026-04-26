"""
Configuración de base de datos para la capa de infraestructura.

Este módulo define el motor de SQLAlchemy, la sesión de base de datos,
la clase base para modelos ORM y funciones auxiliares para FastAPI.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Proporciona una sesión de base de datos para una petición.

    Esta función está pensada para usarse como dependencia de FastAPI.
    Abre una sesión, la entrega al endpoint y luego la cierra.

    Yields:
        Session: Sesión activa de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando las tablas definidas.

    Esta función importa los modelos ORM para registrarlos en el metadata
    de SQLAlchemy y luego crea las tablas correspondientes.

    Returns:
        None
    """
    from src.infrastructure.db.models import ProductModel, ChatMemoryModel
    Base.metadata.create_all(bind=engine)