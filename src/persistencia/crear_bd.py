from persistencia.conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    if obtener_motor() == "sqlite":
        sentencias = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                id_gerente INTEGER,
                FOREIGN KEY (id_gerente) REFERENCES empleado(id)
            )""",
            """CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_departamento INTEGER,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL,
                salario INTEGER NOT NULL,
                inicioContrato TEXT NOT NULL,
                FOREIGN KEY (id_departamento) REFERENCES departamento(id)
            )""",
            """CREATE TABLE IF NOT EXISTS proyecto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                fechaInicio TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                PRIMARY KEY (id_empleado, id_proyecto),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            )""",
            """CREATE TABLE IF NOT EXISTS registroTiempo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                horasTrabajadas REAL NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            )""",
            """CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER,
                nombre TEXT NOT NULL,
                clave TEXT NOT NULL,
                rol TEXT NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id)
            )""",
            """CREATE TABLE IF NOT EXISTS indicador_api (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuente TEXT NOT NULL,
                codigo TEXT NOT NULL,
                fecha TEXT NOT NULL,
                valor REAL NOT NULL,
                unidad TEXT NOT NULL,
                verificado_en TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(fuente, codigo, fecha)
            )"""
        ]
    else:
        sentencias = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                id_gerente INT
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_departamento INT,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(150) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                correo VARCHAR(150) NOT NULL,
                salario INT NOT NULL,
                inicioContrato VARCHAR(150) NOT NULL,
                FOREIGN KEY (id_departamento) REFERENCES departamento(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS proyecto (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(300) NOT NULL,
                fechaInicio VARCHAR(150) NOT NULL
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                PRIMARY KEY (id_empleado, id_proyecto),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS registroTiempo (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                fecha VARCHAR(150) NOT NULL,
                horasTrabajadas DECIMAL(4,2) NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS usuario (
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_empleado INT,
                nombre VARCHAR(100) NOT NULL,
                clave VARCHAR(100) NOT NULL,
                rol VARCHAR(100) NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado(id)
            ) ENGINE=InnoDB""",
            """CREATE TABLE IF NOT EXISTS indicador_api (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fuente VARCHAR(50) NOT NULL,
                codigo VARCHAR(20) NOT NULL,
                fecha VARCHAR(20) NOT NULL,
                valor DECIMAL(10, 2) NOT NULL,
                unidad VARCHAR(20) NOT NULL,
                verificado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uq_fuente_codigo_fecha (fuente, codigo, fecha)
            ) ENGINE=InnoDB"""
        ]

    if obtener_motor() != "sqlite":
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    for sql in sentencias:
        cursor.execute(sql)

    if obtener_motor() != "sqlite":
        cursor.execute(
            """SELECT 1 FROM information_schema.TABLE_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = DATABASE() AND TABLE_NAME = 'departamento'
            AND CONSTRAINT_NAME = 'fk_gerente'"""
        )
        if cursor.fetchone() is None:
            cursor.execute(
                """ALTER TABLE departamento
                ADD CONSTRAINT fk_gerente
                FOREIGN KEY (id_gerente) REFERENCES empleado(id)"""
            )
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
