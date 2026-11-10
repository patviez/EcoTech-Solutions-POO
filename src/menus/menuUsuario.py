import getpass

from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario, autenticar
from dominio.usuario import Usuario

def solicitar_registro():
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass.getpass)
        
        if clave != getpass.getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
            
        usuario_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        return None
        
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id

def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass.getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
        
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario

def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado ID: {usuario_actual['empleado_id']}")

def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    mostrar_indicador()

def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
        
    while True:
        print("\n--- Menú Privado ---")
        print("1. Registrar nuevo usuario")
        print("2. Ver Perfil")
        print("9. Cerrar sesión")
        print("0. Salir")
        
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
            
        if opcion == "1":
            solicitar_registro()
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
        else:
            print("Opción no válida.")

def gestionar_usuarios(usuario_actual=None):
    return menu_privado(usuario_actual)