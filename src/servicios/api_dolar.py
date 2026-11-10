import requests

URL_API_DOLAR = "https://mindicador.cl/api/dolar"

def obtener_datos():
    """
    Realiza la solicitud HTTP GET a la API del dolar usando la libreria oficial requests.
    Devuelve la respuesta en formato diccionario (JSON).
    """
    response = requests.get(URL_API_DOLAR, timeout=5)
    response.raise_for_status()
    return response.json()

def extraer_primero(datos):
    """
    Extrae y valida la primera observacion (fecha y valor) de la respuesta JSON.
    Reutilizado por DeserializadorIndicador segun la Clase 6.
    """
    if not isinstance(datos, dict) or "serie" not in datos:
        raise ValueError("Formato de respuesta de la API no valido.")
    
    serie = datos.get("serie", [])
    if not serie:
        raise ValueError("La API no entrego registros en la serie de datos.")
    
    primer_registro = serie[0]
    fecha_raw = primer_registro.get("fecha", "")
    fecha = fecha_raw.split("T")[0] if "T" in fecha_raw else fecha_raw
    valor = float(primer_registro.get("valor", 0))

    if valor <= 0:
        raise ValueError("El valor del indicador recibido de la API no es valido.")

    return fecha, valor