from modelos.modelo_base import ModeloBase

class TurnoServicio(ModeloBase):
  TABLA = "Turno_Servicio"

  @classmethod
  def agregar_servicio(cls, turno_id, servicio_id, precio_cobrado):
    """Asocia un servicio a un turno."""
    query = f"""
      INSERT INTO {cls.TABLA} (turno_id, servicio_id, precio_cobrado)
      VALUES (%s, %s, %s)
    """
    return cls.ejecutar(query, (turno_id, servicio_id, precio_cobrado))

  @classmethod
  def listar_por_turno(cls, turno_id):
    """Devuelve los servicios asociados a un turno."""
    query = f"""
      SELECT ts.servicio_id, s.nombre, ts.precio_cobrado
      FROM {cls.TABLA} ts
      JOIN Servicio s ON ts.servicio_id = s.id
      WHERE ts.turno_id = %s
    """
    return cls.ejecutar(query, (turno_id,), fetch=True, dict_cursor=True)

  @classmethod
  def eliminar_servicios_turno(cls, turno_id):
    """Elimina todas las relaciones de servicios de un turno (por ejemplo, al cancelar)."""
    query = f"DELETE FROM {cls.TABLA} WHERE turno_id = %s"
    return cls.ejecutar(query, (turno_id,))

  @classmethod
  def calcular_total(cls, turno_id):
    """Calcula el total sumando los precios de los servicios asociados a un turno."""
    query = f"SELECT SUM(precio_cobrado) AS total FROM {cls.TABLA} WHERE turno_id = %s"
    rows = cls.ejecutar(query, (turno_id,), fetch=True, dict_cursor=True)
    if rows and rows[0]["total"] is not None:
      return float(rows[0]["total"])
    return 0.0