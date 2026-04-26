"""
Carga de datos iniciales para la base de datos.

Este módulo inserta productos de ejemplo cuando la tabla de productos
está vacía, con el fin de facilitar pruebas y demostraciones.
"""

from sqlalchemy.orm import Session
from src.infrastructure.db.models import ProductModel


def load_initial_data(db: Session):
    """
    Carga productos iniciales si la base de datos está vacía.

    Args:
        db (Session): Sesión activa de base de datos.

    Returns:
        None
    """
    existing_products = db.query(ProductModel).count()

    if existing_products > 0:
        return

    products = [
        ProductModel(
            name="Nike Air Zoom Pegasus",
            brand="Nike",
            category="Running",
            size="35",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato ideal para correr con gran amortiguación"
        ),
        ProductModel(
            name="Adidas Ultraboost 21",
            brand="Adidas",
            category="Running",
            size="36",
            color="Blanco",
            price=150.0,
            stock=3,
            description="Máxima comodidad y retorno de energía"
        ),
        ProductModel(
            name="Puma Suede Classic",
            brand="Puma",
            category="Casual",
            size="40",
            color="Azul",
            price=80.0,
            stock=10,
            description="Diseño clásico para uso diario"
        ),
        ProductModel(
            name="Nike Air Force 1",
            brand="Nike",
            category="Casual",
            size="39",
            color="Blanco",
            price=110.0,
            stock=7,
            description="Ícono urbano atemporal"
        ),
        ProductModel(
            name="Adidas Stan Smith",
            brand="Adidas",
            category="Casual",
            size="42",
            color="Verde",
            price=95.0,
            stock=6,
            description="Minimalismo y estilo clásico"
        ),
        ProductModel(
            name="Puma RS-X",
            brand="Puma",
            category="Running",
            size="37",
            color="Rojo",
            price=130.0,
            stock=4,
            description="Tecnología moderna y diseño audaz"
        ),
        ProductModel(
            name="Nike ZoomX Vaporfly",
            brand="Nike",
            category="Running",
            size="41",
            color="Verde",
            price=200.0,
            stock=2,
            description="Alto rendimiento para competencia"
        ),
        ProductModel(
            name="Adidas Forum Low",
            brand="Adidas",
            category="Casual",
            size="40",
            color="Negro",
            price=90.0,
            stock=8,
            description="Inspirado en el baloncesto clásico"
        ),
        ProductModel(
            name="Puma Future Rider",
            brand="Puma",
            category="Casual",
            size="39",
            color="Amarillo",
            price=85.0,
            stock=5,
            description="Ligero y cómodo para el día a día"
        ),
        ProductModel(
            name="Nike Revolution 6",
            brand="Nike",
            category="Running",
            size="38",
            color="Gris",
            price=70.0,
            stock=12,
            description="Opción económica para running"
        ),
    ]

    db.add_all(products)
    db.commit()