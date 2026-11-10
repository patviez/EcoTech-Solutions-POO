import bcrypt
from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72

def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Maximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")

def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    
    datos = clave.encode("utf-8")
    if not (0 < len(datos) <= MAX_BYTES_BCRYPT):
        return None
        
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None:
        return None
        
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
        
    return {
        "id": cuenta.id,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
        "rol": cuenta.rol
    }

def registrar_usuario(empleado_id, nombre, clave, rol="empleado"):
    nombre = Usuario.normalizar_usuario(nombre)
    rol = Usuario.validar_rol(rol)
    
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    
    hash_guardado = crear_hash(clave)

    usuario = Usuario(
        nombre_usuario=nombre,
        password_hash=hash_guardado,
        empleado_id=empleado_id,
        rol=rol
    )
    
    return UsuarioDAO.insertar(usuario)