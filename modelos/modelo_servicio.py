from modelos.modelo_base import ModeloBase

class Servicio(ModeloBase):
  TABLA = "Servicio"

  @classmethod
  def crear(cls, nombre, descripcion, precio, duracion_estimada):
    """Crea un nuevo servicio en la base de datos."""
    query = f"""
      INSERT INTO {cls.TABLA} (nombre, descripcion, precio, duracion_estimada)
      VALUES (%s, %s, %s, %s)
    """
    return cls.ejecutar(query, (nombre, descripcion, precio, duracion_estimada), last_id=True)

  @classmethod
  def listar_todos(cls):
    """Obtiene todos los servicios."""
    query = f"SELECT * FROM {cls.TABLA}"
    return cls.ejecutar(query, fetch=True, dict_cursor=True)

  @classmethod
  def obtener_por_id(cls, servicio_id):
    """Obtiene un servicio por su ID."""
    query = f"SELECT * FROM {cls.TABLA} WHERE id = %s"
    rows = cls.ejecutar(query, (servicio_id,), fetch=True, dict_cursor=True)
    return rows[0] if rows else None

  @classmethod
  def actualizar(cls, servicio_id, nombre, descripcion, precio, duracion_estimada, activo):
    """Edita los datos de un servicio."""
    query = f"""
      UPDATE {cls.TABLA}
      SET nombre = %s, descripcion = %s, precio = %s, duracion_estimada = %s, activo = %s
      WHERE id = %s
    """
    return cls.ejecutar(query, (nombre, descripcion, precio, duracion_estimada, activo, servicio_id))

  @classmethod
  def desactivar(cls, servicio_id):
    query = f"UPDATE {cls.TABLA} SET activo = FALSE WHERE id = %s"
    return cls.ejecutar(query, (servicio_id,))

