def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Devuelve las emisiones (kg CO2) = consumo * factor."""
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision