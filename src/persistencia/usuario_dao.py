import pymysql
from persistencia.conexion import abrir_conexion
from persistencia.base_dao import BaseDAO
from dominio.usuario import Usuario

class UsuarioDAO(BaseDAO):
    TABLA = "usuario"
    COLUMNAS = "id, id_empleado, nombre, clave, rol"
    NOMBRE = "el usuario"

    @staticmethod
    def _convertir(fila):
        return Usuario(
            id=fila[0],
            empleado_id=fila[1],
            nombre_usuario=fila[2],
            password_hash=fila[3],
            rol=fila[4]
        )

    @classmethod
    def buscar_por_nombre(cls, nombre):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT id, nombre, clave, id_empleado, rol FROM usuario WHERE BINARY nombre = %s"
                cursor.execute(sql, (nombre,))
                row = cursor.fetchone()
                if row:
                    if isinstance(row, dict):
                        return Usuario(
                            id=row['id'],
                            nombre_usuario=row['nombre'],
                            password_hash=row['clave'],
                            empleado_id=row['id_empleado'],
                            rol=row['rol']
                        )
                    else:
                        return Usuario(
                            id=row[0],
                            nombre_usuario=row[1],
                            password_hash=row[2],
                            empleado_id=row[3],
                            rol=row[4]
                        )
                return None
        finally:
            conexion.close()

    @classmethod
    def insertar(cls, usuario):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO usuario (nombre, clave, id_empleado, rol) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (
                    usuario.nombre_usuario,
                    usuario.password_hash,
                    usuario.empleado_id,
                    usuario.rol
                ))
                conexion.commit()
                return cursor.lastrowid
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1452:
                print(f"\nError: El empleado con ID {usuario.empleado_id} no existe en la base de datos.")
            else:
                print(f"\nError de integridad al registrar el usuario: {e.args[1]}")
            return None
        except Exception as e:
            print(f"\nError inesperado al insertar el usuario: {e}")
            return None
        finally:
            conexion.close()

    @classmethod
    def actualizar(cls, usuario):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = "UPDATE usuario SET nombre = %s, clave = %s, id_empleado = %s, rol = %s WHERE id = %s"
                cursor.execute(sql, (
                    usuario.nombre_usuario,
                    usuario.password_hash,
                    usuario.empleado_id,
                    usuario.rol,
                    usuario.id
                ))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()


