# EcoTech Solutions - Sistema de Gestion de Empleados y Proyectos



Aplicacion de consola en Python para gestionar empleados, departamentos, proyectos, registros de horas, usuarios e indicadores economicos (API del Dolar con respaldo local) en EcoTech Solutions. Desarrollada bajo el paradigma de Programacion Orientada a Objetos (POO) y arquitectura en capas con persistencia en MySQL / SQLite.



Proyecto grupal de la asignatura Programacion Orientada a Objeto Seguro (TI3021).



================================================================================



1. REQUISITOS DEL SISTEMA



- Python 3.10 o superior

- Servidor MySQL o base de datos SQLite local

- Librerias especificadas en requirements.txt (pymysql, bcrypt, requests, python-dotenv)



================================================================================



2. INSTALACION Y CONFIGURACION



Clonar el repositorio y preparar el entorno virtual:



   git clone https://github.com/patviez/EcoTech-Solutions-POO.git

   cd EcoTech-Solutions-POO

   python -m venv .venv

   source .venv/Scripts/activate      # Git Bash en Windows

   # .venv\Scripts\activate            # CMD o PowerShell

   pip install -r requirements.txt



La conexion a la base de datos se gestiona mediante el archivo .env en la raiz del proyecto:



   DB_ENGINE   : Motor de base de datos (sqlite o mysql)

   DB_NAME     : Nombre de la base de datos o archivo local

   DB_HOST     : Host del servidor MySQL (ej. localhost)

   DB_PORT     : Puerto de conexion MySQL (ej. 3306 o 3308)

   DB_USER     : Usuario de MySQL (ej. root)

   DB_PASSWORD : Password de MySQL



* Nota: Las credenciales sensibles se mantienen protegidas en el archivo .env y nunca se exponen en el codigo fuente.



================================================================================



3. EJECUCION DEL SISTEMA



1) Creacion e inicializacion de tablas y cuenta administrador (Semilla):

   python src/semilla_bd.py



2) Ejecucion principal del programa:

   python src/main.py



Credenciales por Defecto (Administrador):

- Usuario: admin

- Clave  : Admin123!



================================================================================



4. FUNCIONALIDADES PRINCIPALES



- Cuenta / Perfil: Consultar ficha personal, consultar registros de tiempo (formato HH:MM hrs) y actualizar datos.

- Indicadores Economicos: Consultar valor actual del Dolar desde servicio API REST externa con fallback a BD local e historial.

- Empleados: Registrar, actualizar, eliminar, listar, listar por departamento, buscar por ID y buscar por nombre.

- Departamentos: Crear, editar (nombre y gerente), eliminar, agregar/quitar empleados, listar empleados y ver cantidad.

- Proyectos: Crear, editar, eliminar, listar con contadores, buscar por ID, asignar/quitar empleados y listar equipo.

- Registros de Tiempo: Registrar horas, editar, eliminar, listar (todos, por empleado, por proyecto) y exportar informe a .txt.

- Usuarios del Sistema: Registrar usuarios, gestionar roles (admin / empleado), cambiar claves y asociar a ficha de empleado.



================================================================================



5. ESTRUCTURA DEL PROYECTO



src/

├── main.py                    Punto de entrada: inicializa la aplicacion y los menus

├── main_prueba.py             Script de verificacion para el modulo de consumo de la API

├── semilla_bd.py              Script de poblado inicial (usuario admin y tablas base)

├── entradas.py                Validaciones globales de entrada de datos por consola

├── dominio/                   Clases del modelo de dominio (UML)

│   ├── departamento.py

│   ├── empleado.py

│   ├── indicador.py

│   ├── proyecto.py

│   ├── registroTiempo.py

│   └── usuario.py

├── persistencia/              Capa de acceso a datos (Patron DAO)

│   ├── base_dao.py            Clase base generica para operacion CRUD

│   ├── conexion.py            Conexion dinamica a MySQL/SQLite mediante .env

│   ├── crear_bd.py            Script DDL para creacion de tablas e indices

│   ├── departamento_dao.py

│   ├── empleado_dao.py

│   ├── indicador_dao.py       Persistencia e historial de indicadores economicos

│   ├── proyecto_dao.py

│   ├── registroTiempo_dao.py

│   └── usuario_dao.py

├── servicios/                 Logica de negocio y servicios externos

│   ├── api_dolar.py           Consumo de la API externa del dolar

│   ├── autenticacion.py       Gestion de login y hashing seguro con bcrypt

│   ├── deserializador_indicador.py Deserializacion de JSON a objetos de dominio

│   ├── gestion_empleados.py

│   ├── indicadores.py         Servicio de indicadores con estrategia de respaldo (fallback)

│   ├── mi_cuenta.py           Servicio de gestion para perfil autenticado

│   └── permisos.py            Control de acceso y verificacion de roles

└── menus/                     Capa de presentacion e interfaz de usuario de consola

    ├── menuDepartamento.py

    ├── menuEmpleado.py

    ├── menuIndicador.py

    ├── menuPrincipal.py

    ├── menuProyecto.py

    ├── menuRegistroTiempo.py

    └── menuUsuario.py

docs/

└── uml_grupal.png             Diagrama de clases del sistema



================================================================================



6. SEGURIDAD Y MANEJO DE ERRORES



- Prevencion de Inyeccion SQL: Todas las consultas en la capa DAO utilizan sentencias preparadas y consultas parametrizadas.

- Cifrado de Contraseñas: Uso de la libreria bcrypt para hashing seguro con sal aleatoria de contraseñas.

- Manejo de Errores en Espanol: Control estricto de excepciones (pymysql.err.OperationalError, IntegrityError y ValueError) evitando la exposicion de trazas en ingles o del motor de BD al usuario final.

- Estrategia Fallback (API Dolar): Ante caidas de red o fallas del servicio web externo, el sistema conmuta automaticamente a la lectura del ultimo registro en la base de datos local.

- Validacion Estricta de Entradas: Sanitizacion de entradas mediante Expresiones Regulares, limites salariales, rangos de fechas reales y confirmaciones explicitas (s/n).



================================================================================



7. DECLARACION DE USO DE HERRAMIENTAS DE IA (ASISTENCIA Y DEPURACION)



En el desarrollo del sistema EcoTech Solutions, la Inteligencia Artificial fue utilizada exclusivamente como una herramienta de apoyo tecnico para la resolucion de casos de borde, refactorizacion de consultas y validacion de errores de consola. La arquitectura en capas, el diseño de clases UML y la estructura de datos fueron concebidos integralmente por el equipo.



Puntos clave de asistencia tecnica:

1. Optimizacion de Expresiones Regulares: Apoyo en el diseño del patron Regex para la sanitizacion y validacion de correos electronicos corporativos.

2. Refactorizacion de Mapeos DAO: Asistencia en la resolucion de descalces de indices en tuplas devueltas por MySQL para instanciar objetos mediante parametros nominales (IndicadorDAO).

3. Estrategia Fallback en Servicios: Apoyo en el patron de contingencia para la API del dolar, garantizando la continuidad operativa del sistema ante la falta de conexion a Internet.

4. Formateo de Consola: Asistencia en la logica de formateo de tiempo a cadenas estandarizadas (HH:MM hrs) y limpieza de caracteres no ASCII en salidas de consola.
