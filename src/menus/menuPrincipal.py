from servicios.autenticacion import autenticar
from servicios.mi_cuenta import mi_ficha, mis_registros
from menus.menuEmpleado import gestionar_empleados
from menus.menuDepartamento import gestionar_departamentos
from menus.menuProyecto import gestionar_proyectos
from menus.menuRegistroTiempo import gestionar_registros
from menus.menuUsuario import gestionar_usuarios
from menus.menuIndicador import gestionar_indicadores

def menu_autenticado(usuario_actual):
    while True:
        rol_str = usuario_actual['rol'].upper()
        print(f"\n***** Menu EcoTech | Usuario: {usuario_actual['nombre_usuario']} ({rol_str}) *****")
        
        # Opciones accesibles por ambos roles (Administrador y Funcionario)
        print("1. Consultar mi ficha")
        print("2. Consultar mis registros de tiempo")
        print("3. Consultar Indicadores Economicos (API / BD)")

        # Opciones exclusivas del Administrador
        if usuario_actual["rol"] == "admin":
            print("\n--- Panel de Administracion ---")
            print("4. Administrar empleados")
            print("5. Administrar departamentos")
            print("6. Administrar proyectos")
            print("7. Administrar registros de tiempo")
            print("8. Administrar usuarios del sistema")

        print("\n9. Cerrar sesion")
        print("0. Salir del programa")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            try:
                ficha = mi_ficha(usuario_actual)
                print("\n--- DATOS DE MI FICHA ---")
                if ficha:
                    print(ficha.mostrar_datos() if hasattr(ficha, "mostrar_datos") else ficha)
                else:
                    print("No hay ficha asociada a tu cuenta.")
            except Exception as error:
                print(f"Error: {error}")

        elif opcion == "2":
            try:
                registros = mis_registros(usuario_actual)
                print("\n--- MIS REGISTROS DE TIEMPO ---")
                if registros:
                    for r in registros:
                        print(r.mostrar_registro() if hasattr(r, "mostrar_registro") else r)
                else:
                    print("No posees registros de tiempo.")
            except Exception as error:
                print(f"Error: {error}")

        elif opcion == "3":
            gestionar_indicadores(usuario_actual)

        elif opcion == "4" and usuario_actual["rol"] == "admin":
            gestionar_empleados()

        elif opcion == "5" and usuario_actual["rol"] == "admin":
            gestionar_departamentos()

        elif opcion == "6" and usuario_actual["rol"] == "admin":
            gestionar_proyectos()

        elif opcion == "7" and usuario_actual["rol"] == "admin":
            gestionar_registros()

        elif opcion == "8" and usuario_actual["rol"] == "admin":
            gestionar_usuarios(usuario_actual)

        elif opcion == "9":
            print("\nSesion cerrada con exito.")
            break

        elif opcion == "0":
            print("\nHasta luego!")
            exit()

        else:
            print("\nOpcion no valida o no permitida para su rol.")
