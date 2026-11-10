import re
from datetime import datetime
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registroTiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.empleado import Empleado

def a_entero_positivo(valor):
    try:
        numero = int(valor)
    except ValueError:
        return None
    if numero >= 1:
        return numero
    return None

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Este campo no puede quedar vacio, intente de nuevo.")

def pedir_nombre_persona(mensaje):
    while True:
        nombre = input(mensaje).strip()
        if not nombre:
            print("El nombre no puede quedar vacio, intente de nuevo.")
            continue
        if not all(c.isalpha() or c.isspace() or c == "-" for c in nombre):
            print("El nombre solo debe contener letras y espacios, intente de nuevo.")
            continue
        return nombre

def pedir_entero(mensaje, minimo=1):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Debe ingresar un numero entero, intente de nuevo.")
            continue
        if numero < minimo:
            print(f"El numero debe ser mayor o igual a {minimo}, intente de nuevo.")
            continue
        return numero

def pedir_salario(mensaje, minimo=500000, maximo=50000000):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Debe ingresar un numero entero valido, intente de nuevo.")
            continue
        if numero < minimo or numero > maximo:
            print(f"El salario debe estar entre ${minimo:,} y ${maximo:,}, intente de nuevo.")
            continue
        return numero

def pedir_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        if telefono.isdecimal() and 8 <= len(telefono) <= 12:
            return int(telefono)
        print("El telefono debe tener solo numeros (entre 8 y 12 digitos), intente de nuevo.")

def pedir_correo(mensaje):
    while True:
        correo = input(mensaje).strip()
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            return correo
        print("El correo no es valido (ejemplo: nombre@dominio.cl), intente de nuevo.")

def pedir_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
            return fecha
        except ValueError:
            print("La fecha debe tener el formato DD-MM-AAAA (ejemplo: 15-03-2024), intente de nuevo.")

def pedir_departamento(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        id_departamento = a_entero_positivo(valor)
        if id_departamento is None:
            print("El id del departamento debe ser un numero entero positivo, intente de nuevo.")
            continue
        if DepartamentoDAO.buscar_por_id(id_departamento) is None:
            print("No existe un departamento con ese id, intente de nuevo.")
            continue
        return id_departamento

def quitar_gerencias(id_empleado, excepto=None):
    for departamento in DepartamentoDAO.listar_todos():
        if departamento.id_gerente == id_empleado and departamento.id != excepto:
            departamento.id_gerente = None
            DepartamentoDAO.actualizar(departamento)
            print(f"El departamento '{departamento.nombre}' quedo sin gerente")

def ingresar_datos():
    nombre = pedir_nombre_persona("\nNombre: ")
    direccion = pedir_texto("Direccion (calle y numero): ")
    telefono = pedir_telefono("Telefono: ")
    correo = pedir_correo("Correo: ")
    salario = pedir_salario("Salario: ")
    inicioContrato = pedir_fecha("Inicio contrato (DD-MM-AAAA): ")
    id_departamento = pedir_departamento("Id del departamento (Enter para dejarlo sin departamento): ")
    return nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento

def gestionar_empleados():
    while True:
        print("\n--- GESTION DE EMPLEADOS ---")
        print("1. Registrar empleado")
        print("2. Actualizar empleado")
        print("3. Eliminar empleado")
        print("4. Listar empleados")
        print("5. Listar empleados por departamento")
        print("6. Buscar empleado por id")
        print("7. Buscar empleado por nombre")
        print("8. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            actualizar_empleado()
        elif opcion == "3":
            eliminar_empleado()
        elif opcion == "4":
            listar_empleados()
        elif opcion == "5":
            listar_empleados_por_departamento()
        elif opcion == "6":
            buscar_empleado_por_id()
        elif opcion == "7":
            buscar_empleado_por_nombre()
        elif opcion == "8":
            break
        else:
            print("\nOpcion no valida.")

def registrar_empleado():
    nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento = ingresar_datos()

    empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento)
    if EmpleadoDAO.insertar(empleado) is not None:
        print(empleado.mostrar_datos())
        print("\nEmpleado registrado correctamente.")
    else:
        print("\nNo fue posible registrar el empleado.")

def actualizar_empleado():
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea actualizar: ")
    actual = EmpleadoDAO.buscar_por_id(idEmpleado)
    if actual is None:
        print("\nNo existe un empleado con ese id")
        return

    print("\nDatos actuales:")
    print(actual.agregar_descripcion())
    nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento = ingresar_datos()

    empleado = Empleado(nombre, direccion, telefono, correo, salario, inicioContrato, id_departamento, idEmpleado)

    if EmpleadoDAO.actualizar(empleado):
        quitar_gerencias(empleado.id, excepto=id_departamento)
        print(empleado.mostrar_datos())
        print("\nEmpleado actualizado correctamente")
    else:
        print("\nNo fue posible actualizar al empleado")

def eliminar_empleado():
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea eliminar: ")
    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is None:
        print("\nNo existe un empleado con ese id")
        return

    if RegistroTiempoDAO.listar_por_empleado(empleado.id):
        print("\nNo se puede eliminar un empleado que tiene horas registradas")
        return

    for proyecto in ProyectoDAO.listar_por_empleado(empleado.id):
        ProyectoDAO.quitar_empleado(proyecto.id, empleado.id)
        print(f"Quitado del proyecto '{proyecto.nombre}'")

    quitar_gerencias(empleado.id)

    for usuario in UsuarioDAO.listar_todos():
        if usuario.id_empleado == empleado.id:
            usuario.id_empleado = None
            UsuarioDAO.actualizar(usuario)
            print(f"El usuario '{usuario.nombre}' quedo sin empleado asociado")

    if EmpleadoDAO.eliminar(idEmpleado):
        print("\nEmpleado eliminado correctamente")
    else:
        print("\nNo fue posible eliminar al empleado")

def mostrar_lista(empleados):
    if not empleados:
        print("\nNo se encontraron empleados.")
        return
    for empleado in empleados:
        print(empleado.mostrar_datos())

def listar_empleados():
    mostrar_lista(EmpleadoDAO.listar_todos())

def listar_empleados_por_departamento():
    idDepartamento = pedir_entero("Ingrese el id del departamento: ")
    mostrar_lista(EmpleadoDAO.listar_por_departamento(idDepartamento))

def buscar_empleado_por_id():
    idEmpleado = pedir_entero("Ingrese el id del empleado que desea buscar: ")

    empleado = EmpleadoDAO.buscar_por_id(idEmpleado)
    if empleado is not None:
        print("\n" + empleado.agregar_descripcion())
    else:
        print("\nNo se encontro un empleado con ese id")

def buscar_empleado_por_nombre():
    nombre = pedir_texto("Ingrese el nombre del empleado que desea buscar: ")
    mostrar_lista(EmpleadoDAO.buscar_por_nombre(nombre))
