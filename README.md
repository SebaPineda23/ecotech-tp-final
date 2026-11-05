# TP FINAL - EcoTech Solutions

Trabajo práctico final de Python. Abajo están las consignas tal cual las recibí y, después, explico con mis palabras qué hice en cada ejercicio, cómo está armado el proyecto y cómo correrlo.

---

## Consignas

### Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores (20 puntos)

Los microcontroladores de EcoTech Solutions transmiten lecturas térmicas en formato heterogéneo con espacios indeseados, textos mezclados con unidades de medida y atributos incompletos. Se necesita un componente que normalice estos registros individuales y genere un reporte consolidado para la toma de decisiones.

**Punto A: Normalización de Lecturas (`limpiar_registro_sensor`).** Diseñar la función `limpiar_registro_sensor(registro_raw)` encargada de procesar un diccionario con datos crudos de un sensor (por ejemplo: `{"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"}`). La función debe transformar la información para retornar un nuevo diccionario estandarizado, garantizando que el identificador quede sin espacios sobrantes, la temperatura sea un valor numérico de tipo float sin sufijos de unidad, y la ubicación posea un valor por defecto seguro en caso de no haberse registrado.

**Punto B: Monitoreo y Mapeo Estadístico (`generar_resumen_sensores`).** Desarrollar la función `generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura)` que tome una colección de registros sanitizados previamente con la función del Punto A y un valor límite. Debe retornar una tupla `(lista_sensores_alerta, promedio_temperatura)` conteniendo los IDs de los dispositivos que superan el umbral estipulado y el promedio térmico global de la planta. Incluir un bloque de ejecución que demuestre el flujo completo desde la limpieza de registros crudos hasta la impresión formateada del reporte final.

### Ejercicio 2 - Modelo de Productos, Excepciones y Persistencia (40 puntos)

Para la división de equipamiento sustentable de EcoTech Solutions, se requiere un módulo de software que gestione los productos del catálogo, impida inconsistencias en el inventario mediante validaciones de negocio y garantice la persistencia del stock en disco.

**Punto A: Dominio del Catálogo y Reglas de Inventario.** Construir la jerarquía orientada a objetos para los productos ecológicos. Diseñar una clase de excepción personalizada `StockInvalidoError` y aplicarla dentro de la clase base `DispositivoEcológico` para impedir que el stock tome valores negativos mediante encapsulamiento explícito. Desarrollar la clase especializada `PanelSolar`, incorporando sus atributos específicos mediante herencia y aplicando polimorfismo para personalizar la emisión de su ficha técnica comercial.

**Punto B: Persistencia y Gestión del Catálogo.** Implementar la clase `GestorInventario` con el método `guardar_catalogo_json(lista_dispositivos, ruta_archivo)` capaz de serializar y almacenar en `catalogo_ecotech.json` las instancias creadas en el Punto A. Incluir un bloque de prueba donde se verifique la captura controlada de `StockInvalidoError` ante un intento de asignación de stock erróneo, finalizando con la exportación exitosa de los productos válidos al archivo JSON.

### Ejercicio 3 - Auditoría con Tests Unitarios e Integración Web (40 puntos)

Previo a la puesta en producción, EcoTech Solutions debe certificar la precisión del algoritmo de cálculo de huella de carbono industrial. Tras auditar su comportamiento mediante pruebas automatizadas, dicho algoritmo debe integrarse en la tubería de datos que alimenta la interfaz web administrativa de la empresa.

**Punto A: Auditoría de Algoritmo de Emisiones (`unittest`).** A partir de la función `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)` (la cual eleva `ValueError` si el consumo es negativo), implementar la clase de prueba `TestCalculoEmisiones(unittest.TestCase)`. Diseñar los casos de prueba necesarios para validar tanto la exactitud numérica del cálculo ante valores nominales como la correcta elevación de la excepción ante consumos fuera de rango.

**Punto B: Procesamiento de Métricas y Renderizado Web.** Incorporar la función `calcular_emisiones_carbono` en la función `obtener_metricas_consumo(registros)`, procesando un historial de consumos por planta industrial para determinar el total global de emisiones y la planta de mayor consumo. Por último, diseñar la función de vista en Django `vista_panel_sustentabilidad(request)` que invoque dicho procesamiento y proporcione el diccionario de contexto listo para ser renderizado en la plantilla `sustentabilidad/panel.html`.

---

## Qué hice

Trabajé con Python 3.13 y Django 6.1, dentro de un entorno virtual (`venv`) y usando VS Code. Fui haciendo un ejercicio por vez y probando cada uno antes de pasar al siguiente.

### Ejercicio 1: sensores

Está todo en `ejercicio1/sensores.py`.

- **`limpiar_registro_sensor`**: recibe el diccionario crudo y devuelve uno nuevo, sin tocar el original. Al ID le saco los espacios con `strip()`. Para la temperatura uso una expresión regular que busca el número dentro del texto, así funciona con `"24.5C"`, `" 31.2 °C"` o `"28,7C"` (con coma). Después lo convierto a `float`. Si la temperatura no trae ningún número, lanzo un `ValueError`, porque no tiene sentido inventar un dato de temperatura. Si la ubicación no viene o está vacía (o solo tiene espacios), le pongo `"Sin ubicación"` como valor por defecto.
- **`generar_resumen_sensores`**: recorre los sensores ya limpios y arma la lista de IDs que superan el umbral. También calcula el promedio. Contemplé el caso de lista vacía para que no divida por cero y devuelva `0.0`.
- **Bloque de ejecución** (`if __name__ == "__main__"`): tengo 4 registros crudos con distintos problemas (espacios, coma decimal, ubicación faltante, ubicación en blanco), los limpio, genero el resumen con un umbral de 30 °C e imprimo el reporte formateado.

### Ejercicio 2: productos, excepciones y persistencia

Está en la carpeta `ejercicio2/`, separado en módulos:

- **`excepciones.py`**: define `StockInvalidoError`, mi excepción personalizada.
- **`dispositivos.py`**: tiene la clase base `DispositivoEcológico` y la clase hija `PanelSolar`.
  - El stock está encapsulado: el atributo real es privado (`__stock`) y se accede con una propiedad. El `setter` valida que sea un entero y que no sea negativo; si no cumple, lanza `StockInvalidoError`. Como el constructor también asigna el stock a través de la propiedad, la validación se aplica al crear el objeto y también cuando se modifica después.
  - `PanelSolar` hereda de la clase base y agrega `potencia_w` y `eficiencia`. Sobrescribe `ficha_tecnica()` (polimorfismo) para mostrar sus datos propios además de los generales, y también extiende `to_dict()` para que el JSON incluya esos campos.
- **`gestor.py`**: `GestorInventario.guardar_catalogo_json` convierte cada dispositivo a diccionario y lo guarda en un archivo JSON con `indent=4` y `ensure_ascii=False`, para que se lean bien los acentos.
- **`demo.py`**: intenta crear tres productos, uno de ellos con stock `-5` a propósito. Ese error lo capturo y lo informo. También pruebo asignar un stock negativo a un producto que ya existe. Los productos válidos se muestran por pantalla y se exportan a `catalogo_ecotech.json`.

### Ejercicio 3: tests y web con Django

Está en la app `sustentabilidad/`.

- **`emisiones.py`**: la función `calcular_emisiones_carbono`, que multiplica el consumo por el factor de emisión (0.4 por defecto) y lanza `ValueError` si el consumo es negativo.
- **`test_emisiones.py`**: la clase `TestCalculoEmisiones` con 6 tests: cálculo con el factor por defecto, con un factor personalizado, con consumo cero, con decimales, y dos tests para el `ValueError` (uno chequea que se lance y el otro que el mensaje contenga la palabra "negativo"). Para comparar floats usé `assertAlmostEqual`.
- **`metricas.py`**: `obtener_metricas_consumo` recibe un diccionario `{planta: [consumos]}`, suma el consumo de cada planta, calcula sus emisiones con la función del Punto A, y devuelve el total global de emisiones y la planta de mayor consumo (más los detalles por planta). Contempla el caso de que no haya datos.
- **`views.py`**: `vista_panel_sustentabilidad` llama a `obtener_metricas_consumo` con datos de ejemplo y arma el contexto. Para que la plantilla quede simple, la vista le pasa una lista de `filas` ya preparadas (planta, consumo y emisiones) en vez de dejar que la plantilla cruce dos diccionarios.
- **`templates/sustentabilidad/panel.html`**: muestra el total de emisiones, la planta de mayor consumo y una tabla con el detalle por planta.
- **`urls.py`** y la configuración en `config/`: conectan la vista con la ruta `/sustentabilidad/panel/`.

Separé la lógica (`emisiones.py` y `metricas.py`) de la vista a propósito: esos dos archivos no dependen de Django, así que los tests corren con `unittest` solo, sin configurar el framework.

## Estructura del proyecto

```
ecotech_Tp_Final/
├── manage.py
├── requirements.txt
├── catalogo_ecotech.json
├── config/
│   ├── settings.py
│   └── urls.py
├── ejercicio1/
│   └── sensores.py
├── ejercicio2/
│   ├── __init__.py
│   ├── excepciones.py
│   ├── dispositivos.py
│   ├── gestor.py
│   └── demo.py
└── sustentabilidad/
    ├── emisiones.py
    ├── metricas.py
    ├── views.py
    ├── urls.py
    ├── test_emisiones.py
    └── templates/
        └── sustentabilidad/
            └── panel.html
```

## Cómo correrlo

Todos los comandos se ejecutan desde la raíz del proyecto.

**Instalación (una sola vez):**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Ejercicio 1:**

```bash
python ejercicio1/sensores.py
```

**Ejercicio 2:** (se corre con `-m` por los imports relativos entre módulos)

```bash
python -m ejercicio2.demo
```

Genera el archivo `catalogo_ecotech.json`.

**Ejercicio 3, tests:**

```bash
python -m unittest sustentabilidad.test_emisiones -v
```

**Ejercicio 3, panel web:**

```bash
python manage.py runserver
```

Después abrir `http://127.0.0.1:8000/sustentabilidad/panel/`. Con los datos de ejemplo tiene que mostrar un total de 4500.00 kg CO₂ y a Planta Este como la de mayor consumo.

## Resultados que obtuve

- Ejercicio 1: reporte con 4 sensores, 2 en alerta (SENSOR-002 y SENSOR-004) y un promedio de 29.85 °C.
- Ejercicio 2: 2 productos válidos exportados al JSON y los 2 intentos de stock negativo capturados.
- Ejercicio 3: los 6 tests pasan y el panel web se renderiza con los valores correctos.
