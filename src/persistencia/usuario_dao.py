from dominio.usuario import Usuario
from persistencia.base_dao import BaseDAO


class UsuarioDAO(BaseDAO):
    TABLA = "usuario"
    COLUMNAS = "id, id_empleado, nombre, contraseña, rol"
    NOMBRE = "el usuario"

    @staticmethod
    def _convertir(fila):
        return Usuario.desde_bd(
            id=fila[0],
            id_empleado=fila[1],
            nombre=fila[2],
            contraseña_cifrada=fila[3],
            rol=fila[4],
        )

    @classmethod
    def buscar_por_nombre(cls, nombre):
def buscar_por_nombre(cls, nombre):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT id, nombre, contraseña, id_empleado, rol FROM usuario WHERE nombre = %s"
                cursor.execute(sql, (nombre,))
                row = cursor.fetchone()
                if row:                    
                    if isinstance(row, dict):
                        return Usuario(
                            id=row['id'],
                            nombre=row['nombre'],
                            contraseña=row['contraseña'],
                            empleado_id=row['id_empleado'],
                            rol=row['rol']
                        )
                    else:
                        return Usuario(
                            id=row[0],
                            nombre=row[1],
                            contraseña=row[2],
                            empleado_id=row[3],
                            rol=row[4]
                        )
                return None
        finally:
            conexion.close()

    @classmethod
    def insertar(cls, usuario):
        sql = "INSERT INTO usuario (id_empleado, nombre, contraseña, rol) VALUES (?, ?, ?, ?)"
        parametros = (usuario.id_empleado, usuario.nombre, usuario.contraseña, usuario.rol)
        nuevo_id = cls._insertar(sql, parametros, "insertar el usuario")
        if nuevo_id is None:
            return None
        usuario.id = nuevo_id
        return usuario

    @classmethod
    def actualizar(cls, usuario):
        sql = "UPDATE usuario SET id_empleado = ?, nombre = ?, contraseña = ?, rol = ? WHERE id = ?"
        parametros = (usuario.id_empleado, usuario.nombre, usuario.contraseña, usuario.rol, usuario.id)
        return cls._ejecutar(sql, parametros, "actualizar el usuario") > 0


