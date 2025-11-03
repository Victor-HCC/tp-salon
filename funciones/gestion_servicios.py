from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer
from modelos.modelo_servicio import Servicio
from decimal import Decimal
from rich.rule import Rule

from .auxiliares import obtener_entrada_valida, validar_nombre_servicio, validar_precio, validar_duracion

console = Console()

def crear_servicio():
  console.print("[bold green]--- Crear nuevo servicio ---[/bold green]")
  
  # Obtener y validar nombre
  nombre = obtener_entrada_valida(
    message="Nombre:",
    validator_func=validar_nombre_servicio,
    error_message="Nombre inválido"
  )
  
  # Obtener y validar descripcion
  descripcion = obtener_entrada_valida(
    message="Descripción (opcional):",
    validator_func=lambda x: True,
    error_message="Descripción inválida."
  )
  
  # Obtener y validar precio
  precio = obtener_entrada_valida(
    message="Precio:",
    validator_func=validar_precio,
    error_message="Ingresa un precio válido."
  )
  
  # Obtener y validar duracion_estimada
  duracion_estimada = obtener_entrada_valida(
    message="Duración estimada (min):",
    validator_func=validar_duracion,
    error_message="Ingresa una duración válida, debe ser mayor a cero."
  )
  
  precio = Decimal(precio)
  duracion_estimada = int(duracion_estimada)
  
  console.print((nombre, descripcion, precio, duracion_estimada))
  
  try:
    nuevo_id = Servicio.crear(nombre, descripcion, precio, duracion_estimada)
    console.print(f"[green]Servicio creado exitosamente con ID: {nuevo_id}[/green]")
  except Exception as e:
    console.print(f"[red]Error al crear servicio:[/red] {e}")
    
def obtener_servicio_a_editar():
  """
  Muestra una lista de todos los servicios disponibles y permite al usuario 
  seleccionar uno para su edición.
  
  Returns:
    dict | None: El diccionario del servicio seleccionado o None si se cancela o no hay servicios.
  """
  
  # 1. Obtener todos los servicios del modelo
  servicios = Servicio.listar_todos()
  
  if not servicios:
    console.print("[bold yellow]No hay servicios registrados para editar.[/bold yellow]")
    return None
    
  console.print(Rule(title="Seleccionar Servicio para Edición", style="bold magenta"))

  # 2. Preparar las opciones para InquirerPy
  opciones_mapeadas = {} # Mapea la etiqueta de display al objeto servicio original
  choices = []
  
  for servicio in servicios:
    # Crear una etiqueta clara para la CLI, incluyendo el ID
    display_label = (
      f"[ID: {servicio['id']}] {servicio['nombre']} "
      f"(💰 ${servicio['precio']:.2f} - ⏳ {servicio['duracion_estimada']} min)"
    )
    choices.append(display_label)
    # Mapear la etiqueta a todo el objeto servicio
    opciones_mapeadas[display_label] = servicio 
    
  try:
    # 3. Pedir al usuario que seleccione un servicio
    opcion_seleccionada_str = inquirer.select(
      message="Elige el servicio a editar:",
      choices=choices,
      qmark="✏️" # Un emoji de lápiz para el prompt
    ).execute()
    
    # 4. Retornar el objeto servicio completo
    return opciones_mapeadas[opcion_seleccionada_str]
    
  except KeyboardInterrupt:
    console.print("[bold yellow]Operación de selección cancelada por el usuario.[/bold yellow]")
    return None
  
def editar_servicio():
  """
  Guía al usuario para seleccionar un servicio y editar sus atributos.
  """
  console.print("[bold yellow]--- Editar Servicio ---[/bold yellow]")
  
  # Identificar y Obtener Datos
  servicio_actual = obtener_servicio_a_editar()
  if not servicio_actual:
    return

  # Muestra la información del servicio
  console.print(f"[cyan]Editando servicio:[/cyan] ID {servicio_actual['id']} | {servicio_actual['nombre']}")

  # Inicializar la conversión del valor 'precio' y 'activo' para defaults
  precio_actual_decimal = servicio_actual['precio'] # Asumimos que viene como Decimal
  activo_actual_bool = bool(servicio_actual['activo']) # Conversión a booleano para el select

  # Datos que se recopilarán para la actualización
  datos_nuevos = {}
  
  # --- Solicitud y Autocompletado de Campos ---
  
  # 1. Nombre
  nuevo_nombre = obtener_entrada_valida(
    message="Nombre:",
    validator_func=validar_nombre_servicio,
    error_message="Nombre inválido. Debe contener al menos 2 caracteres y solo letras/espacios/números.",
    default=servicio_actual['nombre']
  )
  if nuevo_nombre != servicio_actual['nombre']:
    datos_nuevos['nombre'] = nuevo_nombre

  # 2. Descripción (Opcional)
  nueva_descripcion = obtener_entrada_valida(
    message="Descripción (Opcional):",
    validator_func=lambda x: True,
    error_message="Descripción inválida. Solo caracteres alfanuméricos y puntuación básica.",
    default=servicio_actual.get('descripcion', '') or '' # Usamos .get por si es NULL y aseguramos un string
  )
  # Si la descripción ingresada es vacía, guardamos un NULL 
  descripcion_a_guardar = nueva_descripcion.strip() or None
  if descripcion_a_guardar != servicio_actual.get('descripcion'):
    datos_nuevos['descripcion'] = descripcion_a_guardar

  # 3. Precio
  precio_str_validado = obtener_entrada_valida(
    message=f"Precio (Actual: ${precio_actual_decimal:.2f}):",
    validator_func=validar_precio,
    error_message="Precio inválido. Debe ser un número positivo (ej: 15.00 o 15,00).",
    default=str(precio_actual_decimal) # El default debe ser una CADENA del valor
  )
  # Conversión y verificación del cambio
  nuevo_precio_decimal = Decimal(precio_str_validado)
  if nuevo_precio_decimal is not None and nuevo_precio_decimal != precio_actual_decimal:
    datos_nuevos['precio'] = nuevo_precio_decimal

  # 4. Duración Estimada
  duracion_actual_int = servicio_actual['duracion_estimada']
  duracion_str_validada = obtener_entrada_valida(
    message=f"Duración (minutos - Actual: {duracion_actual_int} min):",
    validator_func=validar_duracion,
    error_message="Duración inválida. Debe ser un número entero positivo de minutos.",
    default=str(duracion_actual_int)
  )
  # Conversión y verificación del cambio
  try:
    nueva_duracion_int = int(duracion_str_validada)
    if nueva_duracion_int != duracion_actual_int:
      datos_nuevos['duracion_estimada'] = nueva_duracion_int
  except ValueError:
      # No debería pasar si validar_duracion es robusto, pero sirve como seguro
      pass

  # 5. Estado Activo (Booleano)
  opcion_activo = inquirer.select(
    message="Estado:",
    choices=[
      {"name": "Activo (Visible y disponible)", "value": True},
      {"name": "Inactivo (Oculto)", "value": False}
    ],
    default=activo_actual_bool
  ).execute()
  
  if opcion_activo != activo_actual_bool:
    datos_nuevos['activo'] = opcion_activo
      
  # --- Actualizar ---
  
  if not datos_nuevos:
    console.print("[bold yellow]No se detectaron cambios. No se realizó ninguna actualización.[/bold yellow]")
    return
  
  # Como el método 'actualizar' requiere *todos* los campos, debemos rellenar los no modificados.
  datos_finales = {
    'nombre': datos_nuevos.get('nombre', servicio_actual['nombre']),
    'descripcion': datos_nuevos.get('descripcion', servicio_actual.get('descripcion', None)),
    'precio': datos_nuevos.get('precio', precio_actual_decimal),
    'duracion_estimada': datos_nuevos.get('duracion_estimada', duracion_actual_int),
    'activo': datos_nuevos.get('activo', activo_actual_bool)
  }
      
  try:
    # Llamar a la función 'actualizar' con el ID y los datos finales
    Servicio.actualizar(
      servicio_actual['id'],
      **datos_finales
    )
    console.print("[bold green]✅ Servicio actualizado exitosamente.[/bold green]")
      
  except Exception as e:
    console.print(f"[bold red]❌ Error al actualizar servicio:[/bold red] {e}")

def listar_servicios():
  console.print("[bold yellow]--- Listado de Servicios ---[/bold yellow]")
  
  try:
    # 1. Obtener la lista completa de servicios
    data = Servicio.listar_todos()
  except Exception as e:
    console.print(f"[bold red]Error al obtener servicios:[/bold red] {e}")
    return

  if not data:
    console.print("[yellow]No hay servicios registrados en el sistema.[/yellow]")
    return
      
  # 2. Configurar la tabla
  tabla = Table(
    title="📋 Servicios del Salón", 
    show_header=True, 
    header_style="bold magenta",
    padding=(0, 1)
  )
  
  # Definir Columnas
  tabla.add_column("ID", style="dim", justify="center")
  tabla.add_column("Nombre", style="cyan", justify="left")
  tabla.add_column("Descripción", justify="left", max_width=40)
  tabla.add_column("💰 Precio", justify="right")
  tabla.add_column("⏳ Duración", justify="center")
  tabla.add_column("✅ Activo", justify="center")
  
  # 3. Agregar Filas con Formato Condicional
  for servicio in data:
    # Conversiones de datos
    servicio_activo = bool(servicio['activo'])
    precio_str = f"${float(servicio['precio']):.2f}"
    duracion_str = f"{servicio['duracion_estimada']} min"
    estado_str = "[bold green]SÍ[/bold green]" if servicio_activo else "[bold red]NO[/bold red]"
    
    # Aplicar el estilo de toda la fila si el servicio está inactivo
    fila_style = None
    if not servicio_activo:
      # Color rojo tenue para diferenciarlo
      fila_style = "dim red" 

    # Agregar la fila
    tabla.add_row(
      str(servicio['id']),
      servicio['nombre'],
      servicio['descripcion'] if servicio['descripcion'] else '[italic dim]Sin descripción[/italic dim]',
      precio_str,
      duracion_str,
      estado_str,
      style=fila_style  # Aplica el estilo condicional a toda la fila
    )

  console.print()
  console.print(tabla)
  console.print()

def menu_gestion_servicios():
  """Menú para que el administrador gestione los servicios del salón."""
  console.print()
  
  while True:
    try:
      opcion = inquirer.select(
        message="Gestión de Servicios - Selecciona una acción:",
        choices=[
          "➕ Crear nuevo servicio",
          "✏️ Editar servicio",
          "📋 Listar servicios",
          "⬅️ Volver al menú principal"
        ]
      ).execute()
    except KeyboardInterrupt:
      console.print("[yellow]Volviendo al menú principal.[/yellow]")
      break # Vuelve al menu de admin

    if opcion.startswith("➕"):
      crear_servicio()
    elif opcion.startswith("✏️"):
      editar_servicio()
    elif opcion.startswith("📋"):
      listar_servicios()
    elif opcion.startswith("⬅️"):
      break
