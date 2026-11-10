from menus.menuUsuario import solicitar_login
from menus.menuPrincipal import menu_autenticado
from persistencia.crear_bd import crear_tablas
from semilla_bd import sembrar_datos_iniciales

def main():
    crear_tablas()
    sembrar_datos_iniciales()

    while True:
        print("\n" + "="*35)
        print("   BIENVENIDO A ECOTECH SOLUTIONS")
        print("="*35)
        print("1. Iniciar sesion")
        print("0. Salir del programa")
        
        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            usuario_actual = solicitar_login()
            if usuario_actual is not None:
                menu_autenticado(usuario_actual)
        elif opcion == "0":
            print("\nGracias por utilizar EcoTech Solutions! Saliendo...")
            break
        else:
            print("\nOpcion no valida. Intente nuevamente.")

if __name__ == "__main__":
    main()