import json


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)