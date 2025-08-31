from Carrito import Carrito
#El usuario ya tiene la responsabilidad de gestionar su carrito, eliminando esa responsabilidad de tienda.
#Con esto cada clase hace lo que realmente le corresponde

class Usuario:
    def __init__(self):
        self.carrito = Carrito()

    def agregar_item_a_carrito(self, producto, cantidad, cupon_code=None):
        return self.carrito.agregar_item(producto, cantidad, cupon_code=cupon_code)

    def borrar_item_de_carrito(self, item):
        return self.carrito.borrar_item(item)
