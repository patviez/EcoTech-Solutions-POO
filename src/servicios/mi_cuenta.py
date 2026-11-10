from servicios.permisos import exigir_sesion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.proyecto_dao import ProyectoDAO
from dominio.empleado import Empleado

def formatear_horas(valor):
    try:
        cant_horas = float(valor)
        horas = int(cant_horas)
        minutos = int(round((cant_horas - horas) * 60))
        return f"{horas:02d}:{minutos:02d} hrs"
    except (ValueError, TypeError):
        return f"{valor} hrs"

def mi_ficha(sesion):
    exigir_sesion(sesion)
    emp_id = sesion.get("empleado_id")
    if not emp_id:
        return None
    return EmpleadoDAO.buscar_por_id(emp_id)

def mis_registros(sesion):
    exigir_sesion(sesion)
    emp_id = sesion.get("empleado_id")
    if not emp_id:
        return []
    
    registros = RegistroTiempoDAO.listar_por_empleado(emp_id)
    resultado_formateado = []
    
    for r in registros:
        if hasattr(r, "mostrar_registro"):
            resultado_formateado.append(r.mostrar_registro())
        else:
            nombre_proyecto = "Proyecto General"
            if hasattr(r, "id_proyecto"):
                proy = ProyectoDAO.buscar_por_id(r.id_proyecto)
                if proy:
                    nombre_proyecto = proy.nombre
            
            fecha = getattr(r, "fecha", "Sin fecha")
            horas_raw = getattr(r, "horas", getattr(r, "horasTrabajadas", 0))
            horas_texto = formatear_horas(horas_raw)
            
            resultado_formateado.append(f"Fecha: {fecha} | Proyecto: {nombre_proyecto} | Horas: {horas_texto}")
            
    return resultado_formateado

def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)
    emp_id = sesion.get("empleado_id")
    if not emp_id:
        raise ValueError("No hay un empleado asociado a la sesion actual.")
        
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    
    empleado = EmpleadoDAO.buscar_por_id(emp_id)
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    
    empleado.nombre = nombre
    empleado.correo = correo
    return EmpleadoDAO.actualizar(empleado)