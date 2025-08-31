
#Ejecuta el programa
from Tienda import Tienda
from Usuario import Usuario
from Producto import Producto
from manejador_reglas import ManejadorReglas
from reglas import Cupon

def mostrar_menu():
    print("\n--- MENÚ TIENDA ---")
    print("1. Ver productos")
    print("2. Agregar producto al carrito (por SKU)")
    print("3. Ver carrito")
    print("4. Eliminar producto del carrito")
    print("5. Finalizar compra")
    print("0. Salir (sin comprar)")

def seed_tienda(tienda: Tienda):
    # Cupones/reglas
    tienda.manejador_reglas.registrar_cupon(Cupon(codigo="DESC10", tipo="percent", valor=0.10))
    tienda.manejador_reglas.registrar_cupon(Cupon(codigo="ARROZ-5K", tipo="fixed", valor=5.0, skus_validos={"KG-ARROZ"}))
    # Catálogo
    tienda.registrar_producto(Producto("A001", "Galletas", "Paquete 12 und", 100, 2.5))
    tienda.registrar_producto(Producto("ESP123", "Bebida Promo", "Lata 355ml", 200, 3.0))
    tienda.registrar_producto(Producto("KG-ARROZ", "Arroz granel", "Precio por kg", 50000, 4.0))

def main():
    tienda = Tienda(manejador_reglas=ManejadorReglas())
    usuario = Usuario()
    seed_tienda(tienda)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                print("\n--- CATÁLOGO DE PRODUCTOS ---")
                if not tienda.listar_productos():
                    print("(vacío)")
                else:
                    for p in tienda.listar_productos():
                        print(f"{p.sku}: {p.nombre} - {p.descripcion} - ${p.precio_unitario} (Disp: {p.unidades_disponibles})")

            case "2":
                sku = input("Ingrese SKU del producto: ").strip()
                try:
                    cantidad = float(input("Ingrese cantidad (unidades o gramos): "))
                    cupon = input("Ingrese código de cupón (o Enter si no aplica): ").strip() or None
                    prod = tienda.buscar_producto_por_sku(sku)
                    if not prod:
                        print("❌ SKU no encontrado.")
                        continue
                    if not prod.tiene_unidades(cantidad):
                        print("❌ No hay unidades suficientes.")
                        continue
                    # Usuario gestiona su carrito
                    usuario.agregar_item_a_carrito(prod, cantidad, cupon_code=cupon)
                    prod.descontar_unidades(cantidad)
                    print("✅ Producto agregado al carrito.")
                except ValueError:
                    print("❌ Cantidad inválida.")

            case "3":
                print("\n--- CARRITO ---")
                if not usuario.carrito.items:
                    print("Carrito vacío.")
                else:
                    for idx, item in enumerate(usuario.carrito.items, start=1):
                        total = item.calcular_total(tienda.manejador_reglas)
                        cupon = f" (Cupón: {item.cupon_code})" if item.cupon_code else ""
                        print(f"{idx}. {item.producto.nombre} [{item.producto.sku}] x {item.cantidad} -> ${total:.2f}{cupon}")
                    print(f"Total parcial: ${usuario.carrito.calcular_total(tienda.manejador_reglas):.2f}")

            case "4":
                if not usuario.carrito.items:
                    print("Carrito vacío.")
                else:
                    for idx, item in enumerate(usuario.carrito.items, start=1):
                        print(f"{idx}. {item.producto.nombre} [{item.producto.sku}] x {item.cantidad}")
                    try:
                        i = int(input("Número del item a eliminar: ")) - 1
                        if 0 <= i < len(usuario.carrito.items):
                            eliminado = usuario.carrito.items[i]
                            usuario.borrar_item_de_carrito(eliminado)  # Usuario borra
                            print("✅ Item eliminado.")
                        else:
                            print("❌ Número inválido.")
                    except ValueError:
                        print("❌ Entrada inválida.")

            case "5":
                total = tienda.finalizar_compra(usuario)
                print(f"\n💰 COMPRA FINALIZADA. Total: ${total:.2f}")
                print(f"Ventas acumuladas de la tienda: ${tienda.total_ventas:.2f}")
                break

            case "0":
                print("👋 Saliendo sin comprar...")
                break

            case _:
                print("❌ Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
