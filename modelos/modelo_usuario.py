from .modelo_base import ModeloBase


class Usuario(ModeloBase):
  TABLA = "Usuario"
  
  @classmethod
  def crear(cls, nombre, apellido, email, password, rol):
    query = f"""
    INSERT INTO {cls.TABLA} (nombre, apellido, email, password_hash, rol)
    VALUES (?, ?, ?, ?, ?)
    """
    password = ModeloBase._hash_password(password)
    return cls.ejecutar(query, (nombre, apellido, email, password, rol), last_id=True)

  @classmethod
  def listar_empleados(cls, solo_activos=True):
    query = f"SELECT id, nombre, apellido, email, rol, activo FROM {cls.TABLA} WHERE rol != 'cliente'"
    if solo_activos:
      query += " AND activo = TRUE"
    return cls.ejecutar(query, fetch=True, dict_cursor=True)
  
  @classmethod
  def listar_clientes(cls, solo_activos=True):
    query = f"SELECT id, nombre, apellido, email, rol, activo FROM {cls.TABLA} WHERE rol = 'cliente'"
    if solo_activos:
      query += " AND activo = TRUE"
    return cls.ejecutar(query, fetch=True, dict_cursor=True)

  @classmethod
  def obtener_por_id(cls, id_empleado):
    query = f"SELECT id, nombre, apellido, email, rol, activo FROM {cls.TABLA} WHERE id = %s"
    result = cls.ejecutar(query, (id_empleado,), fetch=True, dict_cursor=True)
    return result[0] if result else None
  
  @classmethod
  def obtener_por_email(cls, email):
    query = f"SELECT id, nombre, apellido, email, rol, activo FROM {cls.TABLA} WHERE email = %s"
    result = cls.ejecutar(query, (email,), fetch=True, dict_cursor=True)
    return result[0] if result else None
  
  @classmethod
  def buscar_por_nombre_similar(cls, nombre_parcial, rol='cliente', solo_activos=True):
    """
    Busca usuarios por coincidencia parcial en el nombre o apellido
    para un rol específico (por defecto, 'cliente').
    
    Args:
      nombre_parcial (str): Parte del nombre o apellido a buscar.
      rol (str): El rol del usuario a buscar.
      solo_activos (bool): Si solo debe buscar usuarios activos.
        
    Returns:
      list[dict]: Lista de diccionarios de usuarios coincidentes.
    """
    
    # Usamos LOWER() y LIKE con comodines % para buscar coincidencias
    query = f"""
      SELECT id, nombre, apellido, email, rol, activo 
      FROM {cls.TABLA} 
      WHERE rol = %s
        AND (LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s)
    """
    
    # Valor para el operador LIKE: '%parte_del_nombre%'
    nombre_like = f"%{nombre_parcial.lower()}%"
    
    params = [rol, nombre_like, nombre_like]
    
    if solo_activos:
      query += " AND activo = TRUE"

    query += " ORDER BY nombre, apellido ASC"
    
    return cls.ejecutar(query, params, fetch=True, dict_cursor=True)

  @classmethod
  def actualizar(cls, id, nombre=None, apellido=None, email=None, rol=None, activo=None):
    campos = []
    valores = []
    if nombre: campos.append("nombre = %s"); valores.append(nombre)
    if apellido: campos.append("apellido = %s"); valores.append(apellido)
    if email: campos.append("email = %s"); valores.append(email)
    if rol: campos.append("rol = %s"); valores.append(rol)
    if activo is not None: campos.append("activo = %s"); valores.append(activo)

    if not campos:
      print("[INFO] No hay campos para actualizar.")
      return 0

    query = f"UPDATE {cls.TABLA} SET {', '.join(campos)} WHERE id = %s"
    valores.append(id)
    return cls.ejecutar(query, tuple(valores))

  @classmethod
  def desactivar(cls, usuario_id):
    query = "UPDATE Usuario SET activo = FALSE WHERE id = %s"
    return cls.ejecutar(query, (usuario_id,))
  
  @classmethod
  def cambiar_password(cls, password, usuario_id):
    query = "UPDATE Usuario SET password_hash = %s WHERE id = %s"
    return cls.ejecutar(query, (password, usuario_id,), last_id=True)