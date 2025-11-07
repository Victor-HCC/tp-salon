import mariadb
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

class ModeloBase:
  CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
  }
  
  @staticmethod
  def _hash_password(password: str) -> str:
    return pwd_context.hash(password)

  @classmethod
  def _validar_config(cls):
    missing = [k for k, v in cls.CONFIG.items() if v is None]
    if missing:
      raise RuntimeError(f"Faltan variables de entorno de DB: {missing}")

  @classmethod
  def conectar(cls):
    cls._validar_config()
    try:
      conn = mariadb.connect(**cls.CONFIG)
      return conn
    except mariadb.Error as e:
      print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
      return None

  @classmethod
  def ejecutar(cls, query, params=(), fetch=False, last_id=False, dict_cursor=False):
    conn = cls.conectar()
    if not conn:
      return None

    try:
      # Crear cursor en formato diccionario si se solicita
      if dict_cursor:
        cursor = conn.cursor(dictionary=True)
      else:
        cursor = conn.cursor()

      cursor.execute(query, params)

      if fetch:
        rows = cursor.fetchall()
        return rows  # conn se cerrará en finally

      conn.commit()

      if last_id:
        return cursor.lastrowid

      # devolver número de filas afectadas
      return cursor.rowcount

    except mariadb.Error as e:
      print(f"[ERROR SQL] {e}")
      return None
    finally:
      # asegurar que la conexión se cierre siempre
      try:
        cursor.close()
      except Exception:
        pass
      conn.close()
      
  @classmethod
  def autenticar(cls, email, password):
    # obtener usuario por email
    rows = cls.ejecutar(f"SELECT * FROM Usuario WHERE email = %s AND activo = True", (email,), fetch=True, dict_cursor=True)
    if not rows:
      return None  # usuario no existe

    usuario = rows[0]
    password_hash = usuario["password_hash"]
    # verificar con passlib
    if pwd_context.verify(password, password_hash):
      return {"id": usuario["id"], "nombre": usuario["nombre"], "apellido": usuario["apellido"], "email": usuario["email"], "rol": usuario["rol"]}
    return None