from servicios.api_dolar import obtener_datos
from servicios.deserializador_indicador import DeserializadorIndicador
from persistencia.indicador_dao import IndicadorDAO
from servicios.permisos import exigir_sesion

def consultar_indicador_servicio(sesion):
    exigir_sesion(sesion)
    try:
        datos_json = obtener_datos()
        indicador = DeserializadorIndicador.desde_api(datos_json)
        IndicadorDAO.guardar_o_actualizar(indicador)
        
        return {
            "exito": True,
            "origen": "API Externa",
            "indicador": indicador,
            "mensaje": "Datos actualizados desde el servicio web."
        }
    except Exception:
        respaldo = IndicadorDAO.obtener_ultimo("dolar")
        if respaldo:
            return {
                "exito": True,
                "origen": "BD Local (Respaldo)",
                "indicador": respaldo,
                "mensaje": "Servicio web no disponible. Mostrando ultimo respaldo registrado en la base de datos."
            }
        else:
            return {
                "exito": False,
                "origen": "Ninguno",
                "indicador": None,
                "mensaje": "El servicio no esta disponible y no existen registros previos en el historial."
            }

def obtener_historial_servicio(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar_historial("dolar")