from modelo_base import ModeloBase


class Empleado(ModeloBase):
  TABLA = "Empleado"
  
  @classmethod
  def crear(cls, nombre, apellido, email, password_hash, rol):
    query = f"""
    INSERT INTO {cls.TABLA} (nombre, apellido, email, password_hash, rol)
    VALUES (?, ?, ?, ?, ?)
    """
    return cls.ejecutar(query, (nombre, apellido, email, password_hash, rol), last_id=True)

  @classmethod
  def listar(cls, solo_activos=True):
    query = f"SELECT * FROM {cls.TABLA}"
    if solo_activos:
        query += " WHERE activo = TRUE"
    return cls.ejecutar(query, fetch=True, dict_cursor=True)

  @classmethod
  def obtener_por_id(cls, id_empleado):
    query = f"SELECT * FROM {cls.TABLA} WHERE id = ?"
    result = cls.ejecutar(query, (id_empleado,), fetch=True, dict_cursor=True)
    return result[0] if result else None

  @classmethod
  def actualizar(cls, id_empleado, nombre=None, apellido=None, email=None, rol=None, activo=None):
    campos = []
    valores = []
    if nombre: campos.append("nombre = ?"); valores.append(nombre)
    if apellido: campos.append("apellido = ?"); valores.append(apellido)
    if email: campos.append("email = ?"); valores.append(email)
    if rol: campos.append("rol = ?"); valores.append(rol)
    if activo is not None: campos.append("activo = ?"); valores.append(activo)

    if not campos:
      print("[INFO] No hay campos para actualizar.")
      return 0

    query = f"UPDATE {cls.TABLA} SET {', '.join(campos)} WHERE id = ?"
    valores.append(id_empleado)
    return cls.ejecutar(query, tuple(valores))

  @classmethod
  def eliminar(cls, id_empleado):
    query = f"DELETE FROM {cls.TABLA} WHERE id = ?"
    return cls.ejecutar(query, (id_empleado,))