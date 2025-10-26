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