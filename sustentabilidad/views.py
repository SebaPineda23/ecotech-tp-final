from django.shortcuts import render

from .metricas import obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    registros = {
        "Planta Norte": [1200, 1350, 1280],
        "Planta Sur": [900, 950, 870],
        "Planta Este": [1500, 1620, 1580],
    }
    metricas = obtener_metricas_consumo(registros)

    filas = [
        {
            "planta": planta,
            "consumo": metricas["consumo_por_planta"][planta],
            "emisiones": metricas["emisiones_por_planta"][planta],
        }
        for planta in metricas["consumo_por_planta"]
    ]

    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "filas": filas,
    }
    return render(request, "sustentabilidad/panel.html", contexto)