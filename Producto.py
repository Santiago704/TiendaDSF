#La clase Producto es la más importante, ya que permite identificar los productos, verificar la disponibilidad según la cantidad solicitada y actualizar el inventario al finalizar la venta.
class Producto:
    def __init__(self, sku, nombre, descripcion, unidades_disponibles, precio_unitario):
        self.sku = sku
        self.nombre = nombre
        self.descripcion = descripcion
        self.unidades_disponibles = unidades_disponibles
        self.precio_unitario = precio_unitario

    def tiene_unidades(self, cantidad):
        return self.unidades_disponibles >= cantidad

    def descontar_unidades(self, cantidad):
        if self.tiene_unidades(cantidad):
            self.unidades_disponibles -= cantidad
            return True
        return False
