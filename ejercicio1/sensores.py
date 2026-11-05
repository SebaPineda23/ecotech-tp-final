import re

UBICACION_POR_DEFECTO = "Sin ubicación"


def limpiar_registro_sensor(registro_raw):
    """Normaliza un registro crudo de sensor y devuelve un nuevo diccionario."""
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    temperatura_raw = str(registro_raw.get("temperatura", ""))
    coincidencia = re.search(r"-?\d+(?:[.,]\d+)?", temperatura_raw)
    if not coincidencia:
        raise ValueError(f"Temperatura inválida: {temperatura_raw!r}")
    temperatura = float(coincidencia.group().replace(",", "."))

    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion else ""
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve (lista_ids_en_alerta, promedio_temperatura)."""
    sensores_alerta = [
        s["sensor_id"]
        for s in lista_sensores_limpios
        if s["temperatura"] > umbral_temperatura
    ]
    if lista_sensores_limpios:
        promedio = sum(s["temperatura"] for s in lista_sensores_limpios) / len(
            lista_sensores_limpios
        )
    else:
        promedio = 0.0
    return sensores_alerta, promedio


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002  ", "temperatura": " 31.2 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "28,7C"},  # sin ubicación
        {"sensor_id": "SENSOR-004", "temperatura": "35C", "ubicacion": "  "},
    ]
    UMBRAL = 30.0

    limpios = []
    for crudo in registros_crudos:
        try:
            limpios.append(limpiar_registro_sensor(crudo))
        except ValueError as e:
            print(f"Registro descartado: {e}")

    alertas, promedio = generar_resumen_sensores(limpios, UMBRAL)

    print("=" * 45)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("=" * 45)
    for s in limpios:
        print(f"{s['sensor_id']:<12} {s['temperatura']:>6.1f} °C  {s['ubicacion']}")
    print("-" * 45)
    print(f"Umbral de alerta     : {UMBRAL:.1f} °C")
    print(f"Sensores en alerta   : {', '.join(alertas) if alertas else 'Ninguno'}")
    print(f"Temperatura promedio : {promedio:.2f} °C")