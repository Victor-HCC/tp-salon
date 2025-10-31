import re
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

import locale

console = Console()

# --- Configuración Regional a Español ---
try:
  # Intenta establecer un locale común en sistemas Unix/Linux
  locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
  try:
    # Intenta un locale común en Windows
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
  except locale.Error:
    # Si ambos fallan, usa una opción genérica (puede ser menos confiable)
    locale.setlocale(locale.LC_TIME, 'es')
# Si la configuración regional falla en el sistema, los nombres pueden seguir en inglés.

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

def validar_nombre_servicio(texto: str) -> bool:
  """
  Valida si una cadena de texto (nombre de un servicio) es válida.
  
  Criterios:
  1. Mínimo 2 caracteres de longitud.
  2. Permite letras (mayúsculas, minúsculas, acentuadas, ñ).
  3. Permite espacios.
  4. Permite números (opcional, pero útil para servicios).
      
  Args:
    texto: El nombre del servicio a validar.
      
  Returns:
    True si la cadena es válida, False en caso contrario.
  """
  # Expresión regular:
  # ^[...]$ -> Coincidencia exacta de principio a fin.
  # [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ] -> Letras.
  # \s -> Espacios.
  # 0-9 -> Números (opcional, puedes quitarlo si no quieres números).
  # {2,} -> Mínimo 2 caracteres de longitud total.
  regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s0-9]{2,}$"

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
  
  default_str = default if default is not None else ""
  
  while True:
    # 1. Determinar el prompt a usar (secret o text) y aplicar el default.
    if is_secret:
      entrada = inquirer.secret(message=message, default=default_str).execute().strip()
    else:
      entrada = inquirer.text(message=message, default=default_str).execute().strip()
        
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
  
def seleccionar_dia_y_hora(data_horas_ocupadas=None):
  """
  Permite al usuario seleccionar un día y una hora válidos para un turno.
  
  Restricciones:
  - Próximos 5 días (excluyendo el día actual).
  - Días laborales: Lunes a Sábado (excluyendo Domingo).
  - Horario: 9:00 a 18:00 (en punto).
  
  Returns:
    datetime.datetime: La fecha y hora seleccionada, o None si se cancela.
  """
  
  # --- 1. Generar Opciones de Días Válidos ---
  
  dias_validos = {} # { "Lunes 28/10": datetime.date(2025, 10, 28), ... }
  hoy = datetime.now().date()
  
  # Iterar para obtener los próximos 5 días laborables, empezando mañana (i=1)
  count = 1 # para contar los 5 dias disponibles para elegir turno
  j = 1 # para controlar los dias
  while count < 6:
    fecha = hoy + timedelta(days=j)
  
    # 0=Lunes, 6=Domingo. Excluimos el Domingo (fecha.weekday() == 6).
    if fecha.weekday() < 6:
      # Formato de presentación: "Lunes 28/10"
      nombre_dia = fecha.strftime("%A") 
      display_fecha = fecha.strftime("%d/%m")
      
      # Formato de la opción en la CLI
      opcion_key = f"{nombre_dia} {display_fecha}"
      dias_validos[opcion_key] = fecha
      
      count += 1 # Solo contamos si el día es válido (no es domingo)
    
    j += 1 # Siempre avanzamos al siguiente día
  
  try:
    # Pide al usuario que seleccione el día
    dia_seleccionado_str = inquirer.select(
      message="Selecciona el día para el turno:",
      choices=list(dias_validos.keys())
    ).execute()
    
    # Obtener el objeto date real a partir de la selección string
    fecha_seleccionada = dias_validos[dia_seleccionado_str]
    print(fecha_seleccionada)
  except KeyboardInterrupt:
    console.print("[yellow]Selección de día cancelada.[/yellow]")
    return None


  # --- 2. Generar Opciones de Horas Válidas ---
  print(data_horas_ocupadas)
  # Obtengo 'hora' donde 'fecha' es la fecha seleccionada
  horas_ocupadas = [item['hora'] for item in data_horas_ocupadas if item['fecha'] == str(fecha_seleccionada)]
  horas_choices = []
  print(horas_ocupadas)
  # Generar horas desde las 9:00 hasta las 18:00
  for hora in range(9, 19): 
    # Si la hora está ocupada, la salto
    if hora in horas_ocupadas:
      continue
    
    # Formato de hora: "09:00", "15:00", "18:00"
    horas_choices.append(f"{hora:02d}:00")

  try:
    # Pide al usuario que seleccione la hora
    hora_seleccionada_str = inquirer.select(
      message=f"Selecciona la hora para el {dia_seleccionado_str}:",
      choices=horas_choices
    ).execute()
      
  except KeyboardInterrupt:
    console.print("[yellow]Selección de hora cancelada.[/yellow]")
    return None
      
  # --- 3. Combinar y Retornar ---
  
  # Combina la fecha (date) con la hora (time)
  hora_obj = datetime.strptime(hora_seleccionada_str, "%H:%M").time()
  fecha_hora_final = datetime.combine(fecha_seleccionada, hora_obj)
  
  return fecha_hora_final

def validar_precio(texto: str) -> bool:
  """
  Valida si una cadena de texto representa un precio válido (número positivo).
  
  Criterios:
  1. No puede estar vacío (precio obligatorio).
  2. Debe ser convertible a un número (entero o decimal).
  3. Debe ser mayor o igual a 0.
      
  Args:
    texto: La entrada de texto del usuario.
      
  Returns:
    True si es un precio válido, False en caso contrario.
  """
    
  try:
    # Intentar convertir a Decimal (para manejar precisión)
    # Reemplazamos coma por punto si se usa la notación decimal europea
    precio_decimal = Decimal(texto.replace(',', '.'))
    
    # Verificar que sea un valor no negativo
    if precio_decimal >= 0:
      return True
    else:
      return False
      
  except InvalidOperation:
    # Captura errores si el texto no es un número válido (ej: "abc", "10..0")
    return False

def validar_duracion(texto: str) -> bool:
  """
  Valida si una cadena de texto representa una duración válida en minutos.
  
  Criterios:
  1. No puede estar vacío (duración obligatoria).
  2. Debe ser convertible a un NÚMERO ENTERO.
  3. Debe ser un valor estrictamente POSITIVO (> 0).
      
  Args:
    texto: La entrada de texto del usuario.
      
  Returns:
    True si la duración es válida, False en caso contrario.
  """
    
  try:
    # Intentar convertir a ENTERO (int)
    # Esto automáticamente falla si el texto contiene decimales o caracteres no numéricos
    duracion_int = int(texto) 
    
    # Verificar que sea un valor estrictamente positivo (un servicio debe durar algo)
    if duracion_int > 0:
      return True
    else:
      return False
      
  except ValueError:
    # Captura errores si la conversión a int falla (ej: "abc", "10.5", "5,5")
    return False