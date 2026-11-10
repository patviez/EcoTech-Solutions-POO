class Indicador:
    def __init__(self, fecha, valor, fuente="api_dolar_curso", codigo="dolar", unidad="CLP/USD", verificado_en=None, id=None):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("El valor del indicador debe ser un numero positivo.")
        
        self.id = id
        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = codigo
        self.unidad = unidad
        self.verificado_en = verificado_en

    def mostrar_indicador(self):
        return f"Dolar: ${self.valor:.2f} {self.unidad} | Fecha: {self.fecha} | Fuente: {self.fuente}"