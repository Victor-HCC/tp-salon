import re
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table

console = Console()

def validar_nombre(texto: str) -> bool:
  """
  Valida si una cadena de texto (nombre o apellido) es válida.
  
  Criterios:
  1. Mínimo 2 caracteres de longitud.
  2. SOLO permite letras (mayúsculas, minúsculas y acentuadas).
  3. NO permite espacios, números o símbolos.
      
  Args:
    texto: El nombre o apellido individual a validar.
      
  Returns:
    True si la cadena es válida, False en caso contrario.
  """

  regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]{2,}$"
  
  if re.fullmatch(regex, texto):
    return True
  else:
    return False


def validar_email(email: str) -> bool:
  """
  Valida el formato de una cadena como dirección de correo electrónico 
  utilizando una expresión regular estándar.
  
  Args:
    email: La cadena de texto a validar.
      
  Returns:
    True si el formato es válido, False en caso contrario.
  """
  regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
  
  # re.fullmatch() intenta hacer coincidir el patrón con TODA la cadena.
  # Si encuentra una coincidencia, devuelve un objeto match (True en contexto booleano).
  if re.fullmatch(regex, email):
    return True
  else:
    return False


import re

def validar_password(password: str) -> bool:
  """
  Valida una contraseña para asegurar que cumpla con:
  1. Mínimo 6 caracteres de longitud.
  2. Al menos una letra mayúscula (A-Z).
  3. Al menos un dígito numérico (0-9).
  
  Args:
    password: La cadena de texto de la contraseña a validar.
      
  Returns:
    True si la contraseña es válida, False en caso contrario.
  """
  
  regex = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
  
  if re.fullmatch(regex, password):
    return True
  else:
    return False

# def obtener_entrada_valida(message, validator_func, error_message, is_secret=False):
  """
  Bucle genérico para solicitar entrada al usuario hasta que la validación pase.
  """
  while True:
    # Usa inquirer.secret para contraseñas o inquirer.text por defecto
    if is_secret:
      entrada = inquirer.secret(message=message).execute().strip()
    else:
      entrada = inquirer.text(message=message).execute().strip()

    # Validación específica
    if validator_func(entrada):
      return entrada
    else:
      console.print(f"[red]{error_message}[/red]")
      
def obtener_entrada_valida(message, validator_func, error_message, is_secret=False, default=None):
  """
  Bucle genérico para solicitar entrada al usuario hasta que la validación pase.

  El valor por defecto (default) permite al usuario presionar Enter para aceptarlo.
  """
  
  while True:
    # 1. Determinar el prompt a usar (secret o text) y aplicar el default.
    if is_secret:
      entrada = inquirer.secret(message=message, default=default).execute().strip()
    else:
      entrada = inquirer.text(message=message, default=default).execute().strip()
        
    # 2. Lógica de Manejo de la Entrada
    
    # ESCENARIO A: MODO EDICIÓN (Se presionó Enter para usar el default)
    # Si hay un valor default Y la entrada es idéntica al default (o si ambos son None, aunque default debe tener un valor aquí si se proporciona)
    # O si la entrada está vacía PERO se proporcionó un default (significa que el usuario aceptó el default).
    if default is not None and entrada == default:
      return entrada

    # ESCENARIO B: MODO CREACIÓN o EDICIÓN (Se ingresó un nuevo valor o no hay default)

    # Si la entrada está completamente vacía y NO estamos en modo edición (default es None), esto es un error.
    # Nota: Usamos la función de validación para manejar si la entrada vacía es válida o no.
    
    # 3. Validación
    # La validación se aplica a la entrada. Si la validación falla, se muestra el error.
    if validator_func(entrada):
      return entrada
    else:
      # Si estamos en modo edición Y la entrada está vacía, asumimos que el usuario no quiere cambiarlo 
      # (pero esto ya lo maneja InquirerPy devolviendo el default, así que nos enfocamos en el fallo de la validación)
      
      console.print(f"[red]{error_message}[/red]")
      
def mostrar_tabla(titulo, data):
  """Genera y muestra una tabla Rich a partir de una lista de diccionarios."""
  if not data:
    console.print(f"[bold yellow]No se encontraron usuarios para {titulo}.[/bold yellow]")
    return
      
  # Crear una tabla Rich
  tabla = Table(title=titulo, show_header=True, header_style="bold magenta")
  
  # Obtener nombres de columnas de la primera fila
  columnas = data[0].keys()
  for col in columnas:
    tabla.add_column(col.replace('_', ' ').title(), style="dim" if col == 'id' else "white")

  # Agregar filas de datos
  for fila in data:
    # Se convierte cada valor a string antes de agregarlo a la fila
    tabla.add_row(*[str(v) for v in fila.values()])

  console.print(tabla)