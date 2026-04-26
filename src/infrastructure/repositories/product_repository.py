"""
Repositorio concreto de productos usando SQLAlchemy.

Este módulo implementa la interfaz IProductRepository de la capa
de dominio utilizando modelos ORM y una sesión de base de datos.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación concreta del repositorio de productos usando SQLAlchemy.

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

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            List[Product]: Lista de entidades Product.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            Optional[Product]: Producto encontrado o None si no existe.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos filtrados por marca.

        Args:
            brand (str): Marca a consultar.

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos filtrados por categoría.

        Args:
            category (str): Categoría a consultar.

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto.

        Args:
            product (Product): Entidad de dominio a persistir.

        Returns:
            Product: Producto persistido y convertido nuevamente a entidad.
        """
        if product.id:
            model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
            if not model:
                return None
        else:
            model = ProductModel()

        model.name = product.name
        model.brand = product.brand
        model.category = product.category
        model.size = product.size
        model.color = product.color
        model.price = product.price
        model.stock = product.stock
        model.description = product.description

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (int): Identificador del producto a eliminar.

        Returns:
            bool: True si el producto se eliminó, False si no existía.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()

        if not model:
            return False

        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM en una entidad del dominio.

        Args:
            model (ProductModel): Modelo ORM de producto.

        Returns:
            Product: Entidad del dominio equivalente.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description
        )