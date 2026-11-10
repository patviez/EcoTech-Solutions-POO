def exigir_sesion(sesion):
    if not isinstance(sesion, dict):
        raise PermissionError("Inicie sesion.")
    if sesion.get("rol") not in ("admin", "empleado"):
        raise PermissionError("Acceso no permitido.")
    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("Sesion invalida.")

def exigir_admin(sesion):
    exigir_sesion(sesion)
    if sesion["rol"] != "admin":
        raise PermissionError("Accion solo para administrador.")
