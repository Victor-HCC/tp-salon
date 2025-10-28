from modelos.modelo_base import ModeloBase

class Turno(ModeloBase):
  TABLA = "Turno"

  @classmethod
  def crear(cls, cliente_id, fecha_hora, total=0.0):
    """Crea un nuevo turno pendiente."""
    query = f"""
      INSERT INTO {cls.TABLA} (cliente_id, fecha_hora, total)
      VALUES (%s, %s, %s)
    """
    return cls.ejecutar(query, (cliente_id, fecha_hora, total), last_id=True)

  @classmethod
  def listar(cls, estado=None, cliente_id=None):
    """Devuelve una lista de turnos con filtros opcionales."""
    base_query = f"""
      SELECT t.id, t.fecha_hora, t.estado, t.pagado, t.total,
        u1.nombre AS cliente_nombre, u1.apellido AS cliente_apellido
      FROM {cls.TABLA} t
      JOIN Usuario u1 ON t.cliente_id = u1.id
    """
    filtros = []
    params = []

    if estado:
      filtros.append("t.estado = %s")
      params.append(estado)

    if cliente_id:
      filtros.append("t.cliente_id = %s")
      params.append(cliente_id)

    if filtros:
      base_query += " WHERE " + " AND ".join(filtros)

    base_query += " ORDER BY t.fecha_hora DESC"

    return cls.ejecutar(base_query, params, fetch=True, dict_cursor=True)

  @classmethod
  def listar_para_cliente(cls, cliente_id):
    # Devuelve la lista de turnos pendientes del cliente
    query = f'''SELECT T.id, T.fecha_hora, T.total, GROUP_CONCAT(S.nombre SEPARATOR ', ') AS servicios
      FROM {cls.TABLA} T JOIN Turno_Servicio TS ON T.id = TS.turno_id
      JOIN Servicio S ON TS.servicio_id = S.id
      WHERE T.cliente_id = %s
      GROUP BY T.id, T.fecha_hora, T.total
      ORDER BY T.fecha_hora ASC'''
      
    return cls.ejecutar(query, (cliente_id,), fetch=True, dict_cursor=True)

  @classmethod
  def actualizar_estado(cls, turno_id, nuevo_estado):
    """Actualiza el estado de un turno."""
    query = f"UPDATE {cls.TABLA} SET estado = %s WHERE id = %s"
    return cls.ejecutar(query, (nuevo_estado, turno_id))

  @classmethod
  def marcar_pagado(cls, turno_id):
    """Marca el turno como pagado."""
    query = f"UPDATE {cls.TABLA} SET pagado = TRUE WHERE id = %s"
    return cls.ejecutar(query, (turno_id,))

  @classmethod
  def actualizar_total(cls, turno_id, total):
    """Actualiza el total del turno."""
    query = f"UPDATE {cls.TABLA} SET total = %s WHERE id = %s"
    return cls.ejecutar(query, (total, turno_id))

  @classmethod
  def eliminar(cls, turno_id):
    """Elimina un turno (también elimina relaciones en Turno_Servicio por ON DELETE CASCADE)."""
    query = f"DELETE FROM {cls.TABLA} WHERE id = %s"
    return cls.ejecutar(query, (turno_id,))
