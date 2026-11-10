from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.empleado import Empleado
from servicios.autenticacion import registrar_usuario

def sembrar_datos_iniciales():
    correo_admin = "admin@ecotech.cl"

    empleado = EmpleadoDAO.buscar_por_correo(correo_admin)
    emp_id = None

    if empleado is None:
        nuevo_emp = Empleado(
            nombre="Admin General",
            correo=correo_admin,
            direccion="Oficina Central",
            telefono="123456789",
            salario=500000,
            inicioContrato="2026-01-01"
        )
        emp_id = EmpleadoDAO.insertar(nuevo_emp)
    else:
        if hasattr(empleado, 'id'):
            emp_id = empleado.id
        elif isinstance(empleado, (list, tuple)):
            emp_id = empleado[0]
        elif isinstance(empleado, dict):
            emp_id = empleado.get('id')

    if not emp_id:
        print("Error: No se pudo obtener ni generar el ID para el empleado administrador.")
        return

    usuario = UsuarioDAO.buscar_por_nombre("admin")
    if usuario is None:
        registrar_usuario(empleado_id=emp_id, nombre="admin", clave="Admin123!", rol="admin")
        print("Semilla ejecutada: Cuenta admin creada exitosamente con rol admin.")
    else:
        if usuario.rol != "admin":
            usuario.rol = "admin"
            UsuarioDAO.actualizar(usuario)
            print("Semilla verificada: Rol de la cuenta admin actualizado a admin.")
        else:
            print("Semilla verificada: La cuenta admin ya existe.")

if __name__ == "__main__":
    sembrar_datos_iniciales()