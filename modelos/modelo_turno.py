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
    """
    Devuelve una lista de turnos con filtros opcionales, incluyendo el nombre
    del cliente y los servicios asociados.
    """
    base_query = f"""
      SELECT 
        t.id, 
        t.fecha_hora, 
        t.estado, 
        t.total,
        u1.nombre AS cliente_nombre, 
        u1.apellido AS cliente_apellido,
        GROUP_CONCAT(s.nombre SEPARATOR ', ') AS servicios 
      FROM {cls.TABLA} t
      JOIN Usuario u1 ON t.cliente_id = u1.id
      LEFT JOIN Turno_Servicio ts ON t.id = ts.turno_id
      LEFT JOIN Servicio s ON ts.servicio_id = s.id
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

    # CLÁUSULA CRÍTICA: Necesaria debido a GROUP_CONCAT. 
    # Incluimos todas las columnas no agregadas.
    base_query += """ 
      GROUP BY 
        t.id, t.fecha_hora, t.estado, t.total,
        u1.nombre, u1.apellido
    """
    
    base_query += " ORDER BY t.fecha_hora ASC"

    return cls.ejecutar(base_query, params, fetch=True, dict_cursor=True)
  
  @classmethod
  def obtener_por_id(cls, turno_id):
    query = f"""SELECT T.id, T.fecha_hora, T.estado, T.total, GROUP_CONCAT(S.nombre SEPARATOR ', ') AS servicios
      FROM {cls.TABLA} T JOIN Turno_Servicio TS ON T.id = TS.turno_id
      JOIN Servicio S ON TS.servicio_id = S.id WHERE TS.turno_id = %s"""
    
    turno = cls.ejecutar(query, (turno_id,), fetch=True, dict_cursor=True)
    
    return turno[0] if turno else None

  @classmethod
  def listar_para_cliente(cls, cliente_id):
    # Devuelve la lista de turnos pendientes del cliente
    query = f'''SELECT T.id, T.fecha_hora, T.total, GROUP_CONCAT(S.nombre SEPARATOR ', ') AS servicios
      FROM {cls.TABLA} T JOIN Turno_Servicio TS ON T.id = TS.turno_id
      JOIN Servicio S ON TS.servicio_id = S.id
      WHERE T.cliente_id = %s AND T.estado = 'pendiente'
      GROUP BY T.id, T.fecha_hora, T.total
      ORDER BY T.fecha_hora ASC'''
      
    return cls.ejecutar(query, (cliente_id,), fetch=True, dict_cursor=True)

  @classmethod
  def actualizar_estado(cls, turno_id, nuevo_estado):
    """Actualiza el estado de un turno."""
    query = f"UPDATE {cls.TABLA} SET estado = %s WHERE id = %s"
    return cls.ejecutar(query, (nuevo_estado, turno_id))

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
