from __future__ import annotations
from typing import List, Optional
from Producto import Producto
from Usuario import Usuario
from manejador_reglas import ManejadorReglas

class Tienda:
    """La Tienda mantiene su catálogo y finaliza todas las compras que realicen los clientes.
    el Agregar y eliminar los items ya es responsabilidad de los clientes quienes son los dueños de sus Carritos.
    luego de realizar un analisis a la clase encontramos a manera personal y sin desmeritar el diseño inicial que es-
    totalmente funcional, que la clase tienda tiene responsabilidades que no son de su competencia, relacionadas al-
    manejo del carrito, usamos solid para establecer realmente las responsabilidades de la tienda, con esta nueva version
    la tienda solo se encarga del catalogo y de finalizar compras, la gestion del carrito como tal, pasa a manos del usuario pues-
    este es su real dueño.
    """
    def __init__(self, total_ventas: float = 0.0, manejador_reglas: Optional[ManejadorReglas] = None):
        self.total_ventas = float(total_ventas)
        self.manejador_reglas = manejador_reglas or ManejadorReglas()
        self.productos: List[Producto] = []   # Asociación con Producto (catálogo)

    # Se Gestiona el catálogo
    def registrar_producto(self, producto: Producto) -> None:
        self.productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        return self.productos

    def buscar_producto_por_sku(self, sku: str) -> Optional[Producto]:
        key = sku.strip()
        for p in self.productos:
            if p.sku == key:
                return p
        return None

    #Compra finalizada
    def finalizar_compra(self, usuario: Usuario) -> float:
        total = usuario.carrito.calcular_total(self.manejador_reglas)
        self.total_ventas += total
        usuario.carrito.items.clear()
        return total
