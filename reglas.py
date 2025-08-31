from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Set
#Se implementa como una clase abstracta para que las demás reglas la hereden y se vean obligadas a utilizarla.
class ReglaPrecio(ABC):
    @abstractmethod
    def es_aplicable(self, sku: str) -> bool: ...
    @abstractmethod
    def calcular_total(self, cantidad: int | float, precio_unitario: float) -> float: ...
#Esta regla aplica únicamente cuando ninguna de las demás reglas definidas se cumple.
class ReglaPrecioNormal(ReglaPrecio):
    def es_aplicable(self, sku: str) -> bool:
        return True
    def calcular_total(self, cantidad: int | float, precio_unitario: float) -> float:
        return float(cantidad) * float(precio_unitario)
#Esta regla aplica cuando el producto se comercializa por peso y no por unidad.
class ReglaPrecioPorPeso(ReglaPrecio):
    def es_aplicable(self, sku: str) -> bool:
        s = sku.upper()
        return s.startswith("KG") or s.endswith("-KG") or s.endswith("-G")
    def calcular_total(self, cantidad: int | float, precio_unitario: float) -> float:
        kg = float(cantidad) / 1000.0
        return kg * float(precio_unitario)
#Esta regla aplica cuando el producto tiene un cálculo especial. Por ejemplo, si se compran más de 10 unidades, se otorga un 10% de descuento sobre el valor total.
class ReglaPrecioEspecial(ReglaPrecio):
    def es_aplicable(self, sku: str) -> bool:
        return sku.upper().startswith("ESP")
    def calcular_total(self, cantidad: int | float, precio_unitario: float) -> float:
        subtotal = float(cantidad) * float(precio_unitario)
        return subtotal * 0.90 if float(cantidad) >= 10 else subtotal
#Quisimos implementar esta clase para verificar la flexibilidad del diseño. Se implementa siguiendo el patrón Decorator, lo que nos permite modificar el resultado calculado por otra clase. Por ejemplo, se puede calcular un precio especial para 10 productos y, si además se aplica un cupón, se otorga un descuento adicional. De esta manera, se utiliza el patrón Decorator y se demuestra que el diseño ofrece la flexibilidad necesaria para agregar nuevas formas de calcular precios.
@dataclass(frozen=True)
class Cupon:
    codigo: str
    tipo: str
    valor: float
    skus_validos: Optional[Set[str]] = None

    def aplica_a(self, sku: str) -> bool:
        return (self.skus_validos is None) or (sku in self.skus_validos)

    def aplicar_descuento(self, subtotal: float, sku: str) -> float:
        if not self.aplica_a(sku):
            return subtotal
        if self.tipo.lower() == "percent":
            return max(0.0, subtotal * (1.0 - float(self.valor)))
        if self.tipo.lower() == "fixed":
            return max(0.0, subtotal - float(self.valor))
        return subtotal
