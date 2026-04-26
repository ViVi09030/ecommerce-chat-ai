"""
Servicio de aplicación para productos.

Este módulo orquesta los casos de uso relacionados con el catálogo
de productos, utilizando el repositorio abstracto definido en el dominio.
"""

from typing import List

from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError
from .dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para gestionar productos.

    Atributos:
        product_repository (IProductRepository): Repositorio de productos.
    """

    def __init__(self, product_repository: IProductRepository):
        """
        Inicializa el servicio con un repositorio de productos.

        Args:
            product_repository (IProductRepository): Implementación del
                repositorio de productos.
        """
        self.product_repository = product_repository

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles en el sistema.

        Returns:
            List[ProductDTO]: Lista de productos convertidos a DTO.
        """
        products = self.product_repository.get_all()
        return [ProductDTO.model_validate(p) for p in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Obtiene un producto por su ID.

        Args:
            product_id (int): Identificador del producto.

        Returns:
            ProductDTO: Producto encontrado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError(product_id)

        return ProductDTO.model_validate(product)

    def get_products_by_brand(self, brand: str) -> List[ProductDTO]:
        """
        Obtiene productos filtrados por marca.

        Args:
            brand (str): Marca a consultar.

        Returns:
            List[ProductDTO]: Lista de productos de la marca indicada.
        """
        products = self.product_repository.get_by_brand(brand)
        return [ProductDTO.model_validate(p) for p in products]

    def get_products_by_category(self, category: str) -> List[ProductDTO]:
        """
        Obtiene productos filtrados por categoría.

        Args:
            category (str): Categoría a consultar.

        Returns:
            List[ProductDTO]: Lista de productos de la categoría indicada.
        """
        products = self.product_repository.get_by_category(category)
        return [ProductDTO.model_validate(p) for p in products]

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene únicamente los productos con stock disponible.

        Returns:
            List[ProductDTO]: Lista de productos disponibles.
        """
        products = self.product_repository.get_all()
        available = [p for p in products if p.is_available()]
        return [ProductDTO.model_validate(p) for p in available]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto.

        Args:
            product_dto (ProductDTO): Datos del producto a crear.

        Returns:
            ProductDTO: Producto creado con sus datos persistidos.
        """
        product = Product(**product_dto.model_dump())
        saved_product = self.product_repository.save(product)
        return ProductDTO.model_validate(saved_product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza un producto existente.

        Args:
            product_id (int): ID del producto a actualizar.
            product_dto (ProductDTO): Nuevos datos del producto.

        Returns:
            ProductDTO: Producto actualizado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        existing_product = self.product_repository.get_by_id(product_id)

        if not existing_product:
            raise ProductNotFoundError(product_id)

        updated_data = product_dto.model_dump()
        updated_data["id"] = product_id

        updated_product = Product(**updated_data)
        saved_product = self.product_repository.save(updated_product)

        return ProductDTO.model_validate(saved_product)

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
        """
        return self.product_repository.delete(product_id)