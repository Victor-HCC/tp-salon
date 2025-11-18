from rich.console import Console
from InquirerPy import inquirer
from rich.rule import Rule
from rich.table import Table
from decimal import Decimal

from modelos.modelo_turno import Turno
from modelos.modelo_usuario import Usuario
from modelos.modelo_turno_servicio import TurnoServicio

from .auxiliares import obtener_entrada_valida, validar_email, validar_duracion
from .gestion_servicios import listar_servicios
from .generador_pdf import generar_ticket_pdf

console = Console()


def gestion_turnos():
  """
  Permite al recepcionista buscar y confirmar la llegada de un cliente (cambiar estado a 'confirmado').
  """
  console.print(Rule(title="Confirmación de Turnos", style="bold blue"))
  
  opcion = None
  
  try:
    opcion = inquirer.select(
      message="Buscar turno por:",
      choices=["ID del Turno", "Email del Cliente"]
    ).execute()
  except KeyboardInterrupt:
    console.print("[yellow]Operación cancelada. Volviendo al menú.[/yellow]")
    return
  
  turno_a_confirmar = None
  
  # --- Búsqueda por ID del Turno ---
  if opcion == "ID del Turno":
    try:
      turno_id_str = obtener_entrada_valida(
        message="Ingresa el ID del Turno:",
        validator_func=validar_duracion, # Reutilizamos esta función ya que valida un numero entero positivo
        error_message="El ID debe ser un número entero válido."
      )
      turno_id = int(turno_id_str)
      
      # Obtener el turno y verificar estado
      turno_a_confirmar = Turno.obtener_por_id((turno_id))
      
      if not turno_a_confirmar or turno_a_confirmar.get('estado') != 'pendiente':
        console.print(f"[bold red]❌ Turno con ID {turno_id} no encontrado, no está pendiente o ya pasó.[/bold red]")
        return
    except ValueError as e:
      console.print(f"[yellow][ERROR]Error en la base de datos: {e}[/yellow]")
    except KeyboardInterrupt:
      console.print("[yellow]Operación cancelada por el usuario.[/yellow]")

  # --- Búsqueda por Email del Cliente ---
  elif opcion == "Email del Cliente":
    email = ""
    try:
      email = obtener_entrada_valida(
        message="Ingresa el Email del Cliente:",
        validator_func=validar_email,
        error_message="Email inválido. Asegúrate de usar un formato correcto (ej: usuario@dominio.com)."
      )
      
      user_info = None
      try:
        user_info = Usuario.obtener_por_email(email)
        
        if not user_info: 
          console.print(f"[bold yellow]No existe un usuario registrado con ese email.[/bold yellow]")
          return
        
        turnos_pendientes = Turno.listar('pendiente', user_info.get('id'),True) 
      except Exception as e:
        console.print(f"[bold red][ERROR]Error al acceder a la base de datos: {e}[/bold red]")
        return

      if not turnos_pendientes:
        console.print(f"[bold red]❌ No hay turnos pendientes o futuros registrados para el email: {email}[/bold red]")
        return

      # Si hay múltiples, se despliega el selector
      choices = []
      opciones_mapeadas = {}
      
      for t in turnos_pendientes:
        fecha_str = t['fecha_hora'].strftime("%A %d/%m/%Y a las %H:%M")
        label = f"ID {t['id']} | {fecha_str} | Servicios: {t['servicios']}"
        choices.append(label)
        opciones_mapeadas[label] = t # Mapeamos a todo el objeto turno
          
      turno_seleccionado_str = inquirer.select(
        message=f"Selecciona el turno pendiente para {email}:",
        choices=choices
      ).execute()
      
      turno_a_confirmar = opciones_mapeadas.get(turno_seleccionado_str)
    except KeyboardInterrupt:
        console.print()
        console.print(f"[yellow]Operación de confirmación cancelada.[/yellow]")
        console.print()
        return
  # --- PASO FINAL: Confirmar el Turno Encontrado ---
  if turno_a_confirmar:
    # print(turno_a_confirmar)
    
    fecha_hora_str = turno_a_confirmar['fecha_hora'].strftime("%d/%m/%Y a las %H:%M")
    
    console.print()
    console.print(Rule(style="green"))
    console.print(f"[bold yellow]**Turno a confirmar:**[/bold yellow] ID [bold yellow]{turno_a_confirmar['id']}[/bold yellow] | Hora: [bold cyan]{fecha_hora_str}[/bold cyan]")
    console.print(f"Servicios: {turno_a_confirmar['servicios']}")
    console.print(f"Total: ${float(turno_a_confirmar['total']):.2f}")
    
    try:
      confirmacion = inquirer.confirm(
        message="¿Desea confirmar la llegada de este cliente? (Estado: Pendiente -> Confirmado)"
      ).execute()
      
      if confirmacion:
        # Llama a la función del modelo para actualizar el estado
        Turno.actualizar_estado(turno_a_confirmar['id'], 'confirmado') 
        console.print(f"\n[bold green]✅ Turno ID {turno_a_confirmar['id']} CONFIRMADO exitosamente. Cliente listo para ser atendido.[/bold green]")
      else:
        console.print("[yellow]Operación de confirmación cancelada.[/yellow]")
    except KeyboardInterrupt:
      console.print("[yellow]Confirmación interrumpida.[/yellow]")
  
def consulta_clientes():
  """
  Permite al recepcionista buscar clientes por nombre similar, seleccionar uno, 
  y ver sus datos.
  """
  console.print("[bold cyan]--- Consulta Rápida de Clientes ---[/bold cyan]")
  
  try:
    nombre_busqueda = inquirer.text(
      message="Ingresa parte del nombre o apellido del cliente:",
      qmark="🔍"
    ).execute().strip()
  except KeyboardInterrupt:
    console.print("[yellow]Operación cancelada.[/yellow]")
    return

  if not nombre_busqueda:
    console.print("[yellow]Búsqueda cancelada: No se ingresó texto.[/yellow]")
    return
  
  # 1. Buscar clientes con nombre similar
  clientes_coincidentes = Usuario.buscar_por_nombre_similar(nombre_busqueda)
  
  if not clientes_coincidentes:
    console.print(f"[bold red]❌ No se encontraron clientes con nombre similar a '{nombre_busqueda}'.[/bold red]")
    return

  # 2. Preparar la lista para la selección
  opciones_mapeadas = {}
  choices = []
  
  for cliente in clientes_coincidentes:
    label = f"ID {cliente['id']} | {cliente['nombre']} {cliente['apellido']}"
    choices.append(label)
    opciones_mapeadas[label] = cliente # Mapeamos la etiqueta al diccionario del cliente

  # 3. Seleccionar un cliente
  try:
    opcion_seleccionada_str = inquirer.select(
      message="Selecciona el cliente para ver sus datos:",
      choices=choices,
      qmark="👤"
    ).execute()
    
    cliente_seleccionado = opciones_mapeadas[opcion_seleccionada_str]

    # 4. Mostrar datos del cliente seleccionado
    console.print("\n--- [bold green]Datos del Cliente[/bold green] ---")
    console.print(f"ID: [yellow]{cliente_seleccionado['id']}[/yellow]")
    console.print(f"Nombre: [cyan]{cliente_seleccionado['nombre']} {cliente_seleccionado['apellido']}[/cyan]")
    console.print(f"Email: [cyan]{cliente_seleccionado['email']}[/cyan]")
    console.print(f"Activo: {'[bold green]SÍ[/bold green]' if cliente_seleccionado['activo'] else '[bold red]NO[/bold red]'}")
    console.print("--------------------------------------\n")
    
  except KeyboardInterrupt:
    console.print("[yellow]Selección cancelada.[/yellow]")

def mostrar_detalle_cobro(turno_info: dict, detalle_servicios: list):
  """Muestra el detalle del turno cobrado."""
  
  console.print(Rule(title="[bold green]Recibo de Pago[/bold green]", style="green"))
  
  # 1. Información General del Turno
  fecha_hora_str = turno_info['fecha_hora'].strftime("%d/%m/%Y %H:%M")
  console.print(f"**Turno ID:** [bold yellow]{turno_info['id']}[/bold yellow]")
  console.print(f"**Cliente:** [cyan]{turno_info['cliente_nombre']} {turno_info['cliente_apellido']}[/cyan]")
  console.print(f"**Fecha y Hora:** {fecha_hora_str}")
  console.print(f"**Estado Final:** [bold green]REALIZADO[/bold green]")
  console.print()

  # 2. Tabla de Servicios y Precios
  tabla = Table(title="Detalle de Servicios", show_header=True, header_style="bold green")
  tabla.add_column("Servicio", style="cyan", justify="left")
  tabla.add_column("Precio Cobrado", justify="right", style="yellow")
  
  for servicio in detalle_servicios:
    precio_str = f"${servicio['precio_cobrado']:.2f}"
    tabla.add_row(
      servicio['nombre'],
      precio_str
    )
      
  console.print(tabla)
  
  # 3. Total
  total_decimal = turno_info['total'] if isinstance(turno_info['total'], Decimal) else Decimal(str(turno_info['total']))
  console.print(f"\n[bold white on green]TOTAL COBRADO: ${total_decimal:.2f}[/bold white on green]\n")

def cobrar_turno():
  """
  Permite al recepcionista seleccionar un turno 'confirmado', cambiar su estado a 
  'realizado' y mostrar el detalle del cobro.
  """
  console.print(Rule(title="[bold blue]Finalizar y Cobrar Turno[/bold blue]", style="bold blue"))
  
  try:
    # 1. Listar turnos con estado 'confirmado'
    turnos_confirmados = Turno.listar(estado='confirmado')
    
    if not turnos_confirmados:
      console.print("[yellow]No hay turnos con estado 'confirmado' listos para ser cobrados.[/yellow]")
      return

    # 2. Preparar opciones para la selección
    opciones_mapeadas = {}
    choices = []
    
    for t in turnos_confirmados:
      fecha_hora_str = t['fecha_hora'].strftime("%H:%M")
      label = (
        f"ID {t['id']} | {fecha_hora_str} | Cliente: {t['cliente_nombre']} {t['cliente_apellido']} "
        f"(Total: ${t['total']:.2f})"
      )
      choices.append(label)
      opciones_mapeadas[label] = t
        
    # 3. Seleccionar el turno a cobrar
    opcion_seleccionada_str = inquirer.select(
      message="Selecciona el turno para cobrar:",
      choices=choices,
      qmark="💰"
    ).execute()
    
    turno_a_cobrar = opciones_mapeadas.get(opcion_seleccionada_str)
    
    if not turno_a_cobrar:
      console.print("[yellow]Selección cancelada.[/yellow]")
      return
          
    # 4. Confirmar el Cobro
    confirmacion = inquirer.confirm(
      message=f"¿Confirmas el cobro de ${turno_a_cobrar['total']:.2f} para el turno ID {turno_a_cobrar['id']}?"
    ).execute()
    
    if not confirmacion:
      console.print("[yellow]Cobro cancelado por el usuario.[/yellow]")
      return
        
    # 5. Realizar el Cobro (Actualizar estado y obtener detalle)
    
    # a) Actualizar estado a 'realizado'
    Turno.actualizar_estado(turno_a_cobrar['id'], 'realizado')
    
    # b) Obtener detalle de servicios (incluye precios cobrados)
    detalle_servicios = TurnoServicio.listar_por_turno(turno_a_cobrar['id'])
    
    # c) Mostrar detalle final
    mostrar_detalle_cobro(turno_a_cobrar, detalle_servicios)
    
    #d) Generar ticket pdf
    generar_ticket_pdf(turno_a_cobrar, detalle_servicios)
      
  except KeyboardInterrupt:
    console.print("[yellow]Operación cancelada. Volviendo al menú.[/yellow]")
  except Exception as e:
    console.print(f"[bold red]❌ Ocurrió un error al procesar el cobro:[/bold red] {e}")
  
def listar_servicios_recepcion() :
  listar_servicios()
  
