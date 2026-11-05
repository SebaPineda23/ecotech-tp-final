class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock inválido (negativo)."""

    def __init__(self, valor, mensaje="El stock no puede ser negativo"):
        self.valor = valor
        self.mensaje = f"{mensaje}: {valor}"
        super().__init__(self.mensaje)