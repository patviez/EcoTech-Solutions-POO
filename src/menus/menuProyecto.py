from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from menus.menuEmpleado import pedir_texto, pedir_entero, pedir_fecha, mostrar_lista

def pedir_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si"):
            return True
        elif respuesta in ("n", "no"):
            return False
        print("Respuesta no valida. Ingrese 's' para si o 'n' para no.")

def gestionar_proyectos():
    while True:
        print("\n--- GESTION DE PROYECTOS ---")
        print("1. Crear proyecto")
        print("2. Editar proyecto")
        print("3. Eliminar proyecto")
        print("4. Listar proyectos")
        print("5. Buscar proyecto por id")
        print("6. Asignar empleado al proyecto")
        print("7. Quitar empleado del proyecto")
        print("8. Listar empleados del proyecto")
        print("9. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            crear_proyecto()
        elif opcion == "2":
            editar_proyecto()
        elif opcion == "3":
            eliminar_proyecto()
        elif opcion == "4":
            listar_proyectos()
        elif opcion == "5":
            buscar_proyecto_por_id()
        elif opcion == "6":
            asignar_empleado_proyecto()
        elif opcion == "7":
            quitar_empleado_proyecto()
        elif opcion == "8":
            listar_empleados_proyecto()
        elif opcion == "9":
            break
        else:
            print("\nOpcion no valida.")

def pedir_proyecto_existente(mensaje):
    idProyecto = pedir_entero(mensaje)
    proyecto = ProyectoDAO.buscar_por_id(idProyecto)
    if proyecto is None:
        print("\nNo existe un proyecto con ese id")
    return proyecto

def crear_proyecto():
    nombre = pedir_texto("\nNombre del proyecto: ")
    descripcion = pedir_texto("Descripcion: ")
    fechaInicio = pedir_fecha("Fecha de inicio (DD-MM-AAAA): ")

    proyecto = Proyecto(nombre, descripcion, fechaInicio)
    if ProyectoDAO.insertar(proyecto) is not None:
        print(f"\nProyecto '{proyecto.nombre}' creado correctamente con id {proyecto.id}")
    else:
        print("\nNo fue posible crear el proyecto")

def editar_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea editar: ")
    if proyecto is None:
        return

    print("\nDatos actuales:")
    print(f"Id: {proyecto.id} | Nombre: {proyecto.nombre} | Inicio: {proyecto.fechaInicio}")
    print(f"Descripcion: {proyecto.descripcion}")

    nombre = input(f"\nNuevo nombre (Enter para mantener '{proyecto.nombre}'): ").strip()
    if nombre:
        proyecto.nombre = nombre

    descripcion = input("Nueva descripcion (Enter para mantener la actual): ").strip()
    if descripcion:
        proyecto.descripcion = descripcion

    if pedir_confirmacion("Desea cambiar la fecha de inicio? (s/n): "):
        proyecto.fechaInicio = pedir_fecha("Nueva fecha de inicio (DD-MM-AAAA): ")

    if ProyectoDAO.actualizar(proyecto):
        print("\n----------------------------------------")
        print("  PROYECTO ACTUALIZADO CON EXITO")
        print("----------------------------------------")
        print(f"ID          : {proyecto.id}")
        print(f"Nombre      : {proyecto.nombre}")
        print(f"Fecha Inicio: {proyecto.fechaInicio}")
        print(f"Descripcion : {proyecto.descripcion}")
        print("----------------------------------------")
    else:
        print("\nNo fue posible actualizar el proyecto")

def eliminar_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea eliminar: ")
    if proyecto is None:
        return

    if RegistroTiempoDAO.listar_por_proyecto(proyecto.id):
        print("\nNo se puede eliminar un proyecto que tiene horas registradas")
        return

    for empleado in EmpleadoDAO.listar_por_proyecto(proyecto.id):
        ProyectoDAO.quitar_empleado(proyecto.id, empleado.id)

    if ProyectoDAO.eliminar(proyecto.id):
        print("\nProyecto eliminado correctamente")
    else:
        print("\nNo fue posible eliminar el proyecto")

def listar_proyectos():
    proyectos = ProyectoDAO.listar_todos()
    if not proyectos:
        print("\nNo hay proyectos registrados.")
        return
    print("\n--- LISTADO GENERAL DE PROYECTOS ---")
    for proyecto in proyectos:
        cant_emp = len(EmpleadoDAO.listar_por_proyecto(proyecto.id))
        print(f"ID {proyecto.id}, Nombre: {proyecto.nombre}, Inicio: {proyecto.fechaInicio} | Empleados asignados: {cant_emp}")

def buscar_proyecto_por_id():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto que desea buscar: ")
    if proyecto is None:
        return

    empleados = EmpleadoDAO.listar_por_proyecto(proyecto.id)
    horas = sum(float(r.horas) for r in RegistroTiempoDAO.listar_por_proyecto(proyecto.id))
    print(f"\nProyecto {proyecto.nombre} (ID {proyecto.id})")
    print(f"Descripcion: {proyecto.descripcion}")
    print(f"Inicio: {proyecto.fechaInicio} | Empleados: {len(empleados)} | Horas registradas: {horas:g}")

def asignar_empleado_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea asignar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return
    if any(e.id == empleado.id for e in EmpleadoDAO.listar_por_proyecto(proyecto.id)):
        print("\nEl empleado ya esta asignado a este proyecto")
        return

    if ProyectoDAO.asignar_empleado(proyecto.id, empleado.id):
        print(f"\nEmpleado {empleado.nombre} asignado al proyecto '{proyecto.nombre}'")
    else:
        print("\nNo fue posible asignar el empleado al proyecto")

def quitar_empleado_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    idEmpleado = pedir_entero("Ingrese el id del empleado que desea quitar: ")
    if ProyectoDAO.quitar_empleado(proyecto.id, idEmpleado):
        print(f"\nEmpleado quitado del proyecto '{proyecto.nombre}'")
    else:
        print("\nEse empleado no esta asignado a este proyecto")

def listar_empleados_proyecto():
    proyecto = pedir_proyecto_existente("Ingrese el id del proyecto: ")
    if proyecto is None:
        return

    mostrar_lista(EmpleadoDAO.listar_por_proyecto(proyecto.id))
