from .excepciones import StockInvalidoError


class DispositivoEcológico:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock  # pasa por el setter, que valida

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise StockInvalidoError(valor, "El stock debe ser un entero")
        if valor < 0:
            raise StockInvalidoError(valor)
        self.__stock = valor

    def ficha_tecnica(self):
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"Precio: ${self.precio:,.2f} | Stock: {self.stock} u."
        )

    def to_dict(self):
        return {
            "tipo": type(self).__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcológico):
    def __init__(self, codigo, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  # porcentaje, ej. 21.5

    def ficha_tecnica(self):  # polimorfismo: sobrescribe el método base
        base = super().ficha_tecnica()
        return (
            f"=== PANEL SOLAR ===\n{base}\n"
            f"Potencia: {self.potencia_w} W | Eficiencia: {self.eficiencia}%"
        )

    def to_dict(self):
        datos = super().to_dict()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos