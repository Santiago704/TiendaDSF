class Item:
    #inicializa los atributos de la instancia con los valores que se le pasan.
    def __init__(self, cantidad, producto, cupon_code=None):
        self.cantidad = cantidad
        self.producto = producto
        self.cupon_code = cupon_code
    #Le pasa al manejador de reglas los datos para calcular los valores
    def calcular_total(self, manejador_reglas) -> float:
        return manejador_reglas.calcular_total(
            sku=self.producto.sku,
            cantidad=self.cantidad,
            precio_unitario=self.producto.precio_unitario,
            cupon_code=self.cupon_code,
        )
