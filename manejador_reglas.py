#La clase ManejadorReglas es el cerebro del sistema de precios, se encarga de elegir qué estrategia de cálculo usar (Strategy Pattern) y de aplicar cupones (Decorator) 
from typing import List, Dict, Optional
from reglas import (
    ReglaPrecio, ReglaPrecioNormal, ReglaPrecioPorPeso, ReglaPrecioEspecial, Cupon
)
#Administra las políticas de precio y sabe cuáles reglas existen y qué cupones están activos.
class ManejadorReglas:
    def __init__(
        self,
        reglas: Optional[List[ReglaPrecio]] = None,
        cupones: Optional[Dict[str, Cupon]] = None,
    ):
        self._reglas: List[ReglaPrecio] = reglas or [
            ReglaPrecioEspecial(),
            ReglaPrecioPorPeso(),
            ReglaPrecioNormal(),
        ]
        self._cupones: Dict[str, Cupon] = cupones or {}
    #recorre todas las reglas, preunta cual aplica, devuelve la que aplique, si ninguna aplica usa precio normal
    def obtener_regla(self, sku: str) -> ReglaPrecio:
        for r in self._reglas:
            if r.es_aplicable(sku):
                return r
        return ReglaPrecioNormal()
    #encuentra la regla que aplica,calcula el subtotal, si hay cupon valido lo aplica,devuelve el total final
    def calcular_total(
        self, sku: str, cantidad: int | float, precio_unitario: float, cupon_code: Optional[str] = None
    ) -> float:
        base = self.obtener_regla(sku).calcular_total(cantidad, precio_unitario)
        if cupon_code:
            cup = self._cupones.get(cupon_code.upper())
            if cup and cup.aplica_a(sku):
                return cup.aplicar_descuento(base, sku)
        return base
    #Registra nuevos cupones
    def registrar_cupon(self, cupon: Cupon):
        self._cupones[cupon.codigo.upper()] = cupon
