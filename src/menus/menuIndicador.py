from servicios.indicadores import consultar_indicador_servicio, obtener_historial_servicio

def gestionar_indicadores(sesion):
    while True:
        print("\n--- CONSULTA DE INDICADORES ECONOMICOS ---")
        print("1. Consultar valor del DOlar (API / Respaldo)")
        print("2. Ver historial guardado en BD local")
        print("8. Volver al menU principal")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            resultado = consultar_indicador_servicio(sesion)
            print(f"\n[{resultado['origen'].upper()}] - {resultado['mensaje']}")
            if resultado['indicador']:
                print(resultado['indicador'].mostrar_indicador())

        elif opcion == "2":
            historial = obtener_historial_servicio(sesion)
            print("\n--- HISTORIAL EN BASE DE DATOS LOCAL ---")
            if historial:
                for ind in historial:
                    print(f"Fecha: {ind.fecha} | Valor: ${ind.valor:.2f} {ind.unidad} | Fuente: {ind.fuente}")
            else:
                print("No hay registros guardados en el historial local.")

        elif opcion == "8":
            break
        else:
            print("\nOpcion no valida.")