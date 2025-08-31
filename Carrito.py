from Item import Item
#inicia el carrito vacio
class Carrito:
    def __init__(self):
        self.items = []
#agrega un item
    def agregar_item(self, producto, cantidad, cupon_code=None):
        item = Item(cantidad, producto, cupon_code=cupon_code)
        self.items.append(item)
        return item
#calcula el total de la compra
    def calcular_total(self, manejador_reglas) -> float:
        return sum(i.calcular_total(manejador_reglas) for i in self.items)
#elimina un item del carrito
    def borrar_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False
