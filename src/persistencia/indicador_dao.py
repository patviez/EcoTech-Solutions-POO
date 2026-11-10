import pymysql
from persistencia.conexion import abrir_conexion
from dominio.indicador import Indicador

class IndicadorDAO:
    @classmethod
    def guardar_o_actualizar(cls, indicador):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad, verificado_en)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                    ON DUPLICATE KEY UPDATE
                        valor = VALUES(valor),
                        unidad = VALUES(unidad),
                        verificado_en = NOW()
                """
                cursor.execute(sql, (
                    indicador.fuente,
                    indicador.codigo,
                    indicador.fecha,
                    indicador.valor,
                    indicador.unidad
                ))
                conexion.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al guardar indicador en BD: {e}")
            return False
        finally:
            conexion.close()

    @classmethod
    def obtener_ultimo(cls, codigo="dolar"):
        conexion = abrir_conexion()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT fecha, valor, fuente, codigo, unidad, verificado_en FROM indicador_api WHERE codigo = %s ORDER BY fecha DESC LIMIT 1"
                cursor.execute(sql, (codigo,))
                row = cursor.fetchone()
                if row:
                    if isinstance(row, dict):
                        return Indicador(
                            fecha=str(row['fecha']),
                            valor=float(row['valor']),
                            fuente=row['fuente'],
                            codigo=row['codigo'],
                            unidad=row['unidad'],
                            verificado_en=row['verificado_en']
                        )
                    else:
                        return Indicador(
                            fecha=str(row[0]),
                            valor=float(row[1]),
                            fuente=row[2],
                            codigo=row[3],
                            unidad=row[4],
                            verificado_en=row[5]
                        )
                return None
        finally:
            conexion.close()

    @classmethod
    def listar_historial(cls, codigo="dolar"):
        conexion = abrir_conexion()
        historial = []
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT fecha, valor, fuente, codigo, unidad, verificado_en FROM indicador_api WHERE codigo = %s ORDER BY fecha DESC"
                cursor.execute(sql, (codigo,))
                rows = cursor.fetchall()
                for row in rows:
                    if isinstance(row, dict):
                        ind = Indicador(
                            fecha=str(row['fecha']),
                            valor=float(row['valor']),
                            fuente=row['fuente'],
                            codigo=row['codigo'],
                            unidad=row['unidad'],
                            verificado_en=row['verificado_en']
                        )
                    else:
                        ind = Indicador(
                            fecha=str(row[0]),
                            valor=float(row[1]),
                            fuente=row[2],
                            codigo=row[3],
                            unidad=row[4],
                            verificado_en=row[5]
                        )
                    historial.append(ind)
                return historial
        finally:
            conexion.close()