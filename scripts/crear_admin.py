import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelos.modelo_base import ModeloBase

from dotenv import load_dotenv

load_dotenv()

def crear_admin():
  conn = ModeloBase.conectar()
  if not conn:
    print("[ERROR] No se pudo conectar con la base de datos.")
    return
  
  cursor = conn.cursor()

  cursor.execute("SELECT COUNT(*) FROM Empleado WHERE rol = 'admin'")
  existe = cursor.fetchone()[0]
  
  if existe > 0:
    print("[INFO] Ya existe un usuario Administrador")
  else:
    admin_nombre = os.getenv("ADMIN_NOMBRE")
    admin_apellido = os.getenv("ADMIN_APELLIDO")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = ModeloBase._hash_password(os.getenv("ADMIN_PASSWORD"))

    query = """
    INSERT INTO Empleado (nombre, apellido, email, password_hash, rol)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (admin_nombre, admin_apellido, admin_email, admin_password, "admin"))
    conn.commit()
    print("[OK] Usuario administrador creado con éxito.")

    conn.close()
    
if __name__ == "__main__":
  crear_admin()