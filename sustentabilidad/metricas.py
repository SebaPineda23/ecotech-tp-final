from .emisiones import calcular_emisiones_carbono


def obtener_metricas_consumo(registros):
    """
    registros: dict {planta: [consumos_kwh, ...]}
    Devuelve totales de emisiones y la planta de mayor consumo.
    """
    emisiones_por_planta = {}
    consumo_por_planta = {}

    for planta, consumos in registros.items():
        consumo_total = sum(consumos)
        consumo_por_planta[planta] = consumo_total
        emisiones_por_planta[planta] = calcular_emisiones_carbono(consumo_total)

    total_emisiones = sum(emisiones_por_planta.values())
    planta_mayor_consumo = (
        max(consumo_por_planta, key=consumo_por_planta.get)
        if consumo_por_planta
        else None
    )

    return {
        "consumo_por_planta": consumo_por_planta,
        "emisiones_por_planta": emisiones_por_planta,
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo,
    }