import math
import requests

def obtener_datos():
    respuesta = requests.get(
        "https://open.er-api.com/v6/latest/USD",
        timeout=(3, 5),
    )
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_tasa(datos: dict, moneda: str = "CLP"):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    rates = datos.get("rates")
    if not isinstance(rates, dict) or moneda not in rates:
        raise ValueError(f"No se encontro el valor de la moneda '{moneda}'.")

    valor = rates[moneda]

    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador invalido.")

    fecha = datos.get("time_last_update_utc", "Fecha no disponible")

    return fecha, valor

try:
    datos = obtener_datos()
    fecha, valor = extraer_tasa(datos, "CLP")
    print(f"Dólar observado: {valor:.2f} CLP por USD")
    print(f"Fecha del registro: {fecha}")

except requests.exceptions.RequestException:
    print("No pudimos consultar el servicio. Reintente.")

except (ValueError, KeyError, TypeError):
    print("La respuesta no contiene un indicador valido.")