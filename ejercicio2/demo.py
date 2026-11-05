from .dispositivos import DispositivoEcológico, PanelSolar
from .excepciones import StockInvalidoError
from .gestor import GestorInventario

if __name__ == "__main__":
    catalogo = []

    # Intentos de crear productos (uno inválido a propósito)
    intentos = [
        lambda: PanelSolar("PS-001", "Panel Monocristalino 450W", 320.50, 25, 450, 21.5),
        lambda: DispositivoEcológico("CB-010", "Cargador Solar Portátil", 45.0, 100),
        lambda: PanelSolar("PS-002", "Panel Policristalino 300W", 210.0, -5, 300, 17.8),
    ]

    for crear in intentos:
        try:
            catalogo.append(crear())
        except StockInvalidoError as e:
            print(f"[ERROR CONTROLADO] StockInvalidoError: {e}")

    # Verificar también la asignación posterior de stock
    try:
        catalogo[0].stock = -10
    except StockInvalidoError as e:
        print(f"[ERROR CONTROLADO] Asignación rechazada: {e}")

    print(f"\nProductos válidos: {len(catalogo)}\n")
    for d in catalogo:
        print(d.ficha_tecnica(), end="\n\n")

    GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print("Catálogo exportado a catalogo_ecotech.json")