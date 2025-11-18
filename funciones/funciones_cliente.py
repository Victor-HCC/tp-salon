from rich.console import Console
from rich.table import Table
from rich.rule import Rule
from InquirerPy import inquirer
from decimal import Decimal
from datetime import datetime

from modelos.modelo_servicio import Servicio
from modelos.modelo_usuario import Usuario
from modelos.modelo_turno import Turno
from modelos.modelo_turno_servicio import TurnoServicio
from .auxiliares import validar_email, validar_password, validar_nombre, obtener_entrada_valida, mostrar_tabla, seleccionar_dia_y_hora

console = Console()

def cambiar_contraseña(user_id):
  while True:
    try:
      password = obtener_entrada_valida(
        message="Contraseña nueva:",
        validator_func=validar_password,
        error_message="La contraseña debe tener al menos 6 caracteres, una mayúscula y un número.",
        is_secret=True
      )
      
      check_password = obtener_entrada_valida( 
        message="Repite la contraseña:",
        validator_func=lambda x: len(x) > 0,
        error_message="Debe repetir la contraseña.",
        is_secret=True
      )
      
      if password == check_password:
        hash_password = Usuario._hash_password(password)
        try:
          Usuario.cambiar_password(hash_password, user_id)
          console.print("[bold green]Se cambio la contraseña con éxito.[/bold green]")
          break
        except Exception as e:
          console.print(f"[red]Error al cambiar la contraseña:[/red] {e}")
      else:
        # Se repite el bucle
        console.print("[yellow]Las contraseñas con coinciden.[/yellow]")
    except KeyboardInterrupt:
      console.print("[yellow]Operación interrumpida por el usuario.[/yellow]")
      break
    
def seleccionar_servicios(servicios: list) -> list:
  """
  Permite al usuario seleccionar múltiples servicios de una lista.
  
  Args:
    servicios: Una lista de diccionarios de servicios 
    (e.g., [{'id': 1, 'nombre': 'Corte', 'precio': 800.00, ...}, ...]).
                  
  Returns:
    list: Una lista de los diccionarios de servicios seleccionados.
    Retorna una lista vacía si no selecciona nada o si cancela.
  """
  if not servicios:
    console.print("[yellow]No hay servicios disponibles para seleccionar.[/yellow]")
    return []

  # 1. Preparar las opciones para InquirerPy
  # Creamos un mapeo entre la etiqueta mostrada al usuario y el objeto servicio original.
  opciones_mapeadas = {}
  choices = []
  
  for servicio in servicios:
    # Formato de presentación: "Corte de Pelo Caballero ($800.00 - 30 min)"
    display_label = (
      f"{servicio['nombre']} (💰 ${servicio['precio']:.2f} - "
      f"⏳ {servicio['duracion_estimada']} min)"
    )
    choices.append(display_label)
    opciones_mapeadas[display_label] = servicio

  try:
    # 2. Usar inquirer.checkbox para selección múltiple
    nombres_seleccionados = inquirer.select(
      message="Selecciona uno o más servicios:",
      choices=choices,
      multiselect=True,
      # Instrucciones útiles al pie del prompt
      long_instruction="(Usa ESPACIO para marcar/desmarcar, ENTER para confirmar)"
    ).execute()

  except KeyboardInterrupt:
    console.print("[yellow]Selección de servicios cancelada.[/yellow]")
    return []

  # 3. Mapear los nombres seleccionados de vuelta a los objetos de servicio
  servicios_seleccionados = []
  for nombre in nombres_seleccionados:
    servicios_seleccionados.append(opciones_mapeadas[nombre])
      
  if not servicios_seleccionados:
    console.print("[yellow]No se seleccionó ningún servicio. Proceso cancelado.[/yellow]")
    return []
  
  return servicios_seleccionados

def solicitar_turno(user_id):
  # Selecciona dia y hora
  dia_hora_ocupados = Turno.listar_ocupados(estado='pendiente')
  
  turno_final = seleccionar_dia_y_hora(dia_hora_ocupados)
  if not turno_final:
    console.print("[red]Proceso de turno abortado.[/red]")
    print()
    return
  
  console.print()
  console.print(f"[green]Turno:[/green] {turno_final.strftime('%A %d/%m/%Y a las %H:%M')}")
  console.print()
  
  # Seleccionar servicios
  servicios = Servicio.listar_todos(solo_activos=True)
  servicios_seleccionados = seleccionar_servicios(servicios)
  
  if not servicios_seleccionados:
    console.print("[yellow]No seleccionaste ningún servicio. Operación cancelada.[/yellow]")
    return
  
  # Tabla para mostrar los servicios seleccionados
  tabla = Table(title="Servicios Seleccionados", show_lines=True)
  tabla.add_column("ID", justify="center")
  tabla.add_column("Nombre")
  tabla.add_column("Precio", justify="right")
  tabla.add_column("Duración (min)", justify="center")
  
  total = Decimal("0.00")
  duracion_total = 0
  
  for s in servicios_seleccionados:
    tabla.add_row(str(s["id"]), s["nombre"], f"$ {s['precio']:.2f}", str(s["duracion_estimada"]))
    total += s["precio"]
    duracion_total += s["duracion_estimada"]

  console.print(tabla)
  console.print(f"[bold cyan]Total a pagar: $ {total:.2f}[/bold cyan]")
  console.print(f"[bold]Duración estimada total: {duracion_total} minutos[/bold]")
  console.print()
  
  # Confirmar o cancelar
  try:
    confirmar = inquirer.confirm(
      message="¿Deseas confirmar el turno?",
      default=True
    ).execute()
  except KeyboardInterrupt:
    console.print("[yellow]Operación cancelada por el usuario.[/yellow]")
    return
  
  if not confirmar:
    console.print("[yellow]Turno cancelado por el usuario.[/yellow]")
    return
  
  # Guardar en la base de datos
  try:
    if Turno.verificar_disponibilidad(turno_final):
      turno_id = Turno.crear(user_id, turno_final, total)
    else:
      # La capacidad está al máximo
      console.print()
      console.print("[bold red]❌ Lo sentimos, el horario seleccionado ya está lleno (3 turnos). Por favor, elige otra hora.[/bold red]")
      return

    for s in servicios_seleccionados:
      TurnoServicio.agregar_servicio(turno_id, s["id"], s["precio"])
  except Exception as e:
    console.print(f"[ERROR] Error al guardar en la base de datos: {e}")
    return
    
  # Resumen final
  console.print()
  console.print(f"[green]✅ Turno confirmado exitosamente![/green]")
  console.print(f"ID Turno: [bold cyan]{turno_id}[/bold cyan]")
  console.print(f"Fecha: [bold]{turno_final.strftime('%d/%m/%Y %H:%M')}[/bold]")
  console.print(f"Total: [bold cyan]$ {total:.2f}[/bold cyan]")
  
def listar_turnos_cliente(user_id):
  turnos = Turno.listar_para_cliente(user_id)
  
  if not turnos:
    console.print("[bold yellow]No tienes turnos registrados.[/bold yellow]")
    return
      
  tabla = Table(
    title="📋 Mis Turnos Solicitados", 
    show_header=True, 
    header_style="bold blue",
    padding=(0, 1) # Reduce un poco el padding horizontal
  )
  
  # 1. Definir Columnas
  tabla.add_column("ID", style="bold cyan", justify="center")
  tabla.add_column("📅 Fecha y Hora", style="cyan", justify="left")
  tabla.add_column("Servicios", style="white", justify="left")
  tabla.add_column("💰 Total", style="green", justify="right")
  
  # 2. Agregar Filas de Datos
  for turno in turnos:
    # Formatear la Fecha y Hora
    fecha_str = turno['fecha_hora'].strftime("%d/%m/%Y %H:%M")
    
    # Formatear el Total (Asegurarse de que sea una cadena con 2 decimales)
    # Usamos float() por seguridad si Decimal causa problemas de formato
    total_str = f"$ {float(turno['total']):.2f}"
    
    # Agregar la fila a la tabla
    tabla.add_row(
      str(turno['id']),
      fecha_str,
      turno['servicios'], # Esto viene como cadena de GROUP_CONCAT
      total_str
    )

  console.print() 
  console.print(tabla)
  console.print() 
  
def cancelar_turno(user_id):
  # Obtener todos los turnos del cliente
  turnos = Turno.listar_para_cliente(user_id)
  
  if not turnos:
    console.print("[bold yellow]No tienes turnos registrados.[/bold yellow]")
    return
  
  console.print(Rule(title="Selecciona Turno a Cancelar", style="bold red"))
  
  # Preparar opciones para InquirerPy
  opciones_mapeadas = {} # Mapea la etiqueta de display al ID del turno
  choices = []
  
  for turno in turnos:
    fecha_str = turno['fecha_hora'].strftime("%A %d/%m/%Y a las %H:%M")
    
    # Etiqueta de presentación: Fecha, Servicios (truncado) y Total
    servicios_resumen = turno['servicios'].split(', ')[0] # Solo el primer servicio para brevedad
    display_label = f"{fecha_str} | {servicios_resumen} | Total: ${float(turno['total']):.2f}"
    
    choices.append(display_label)
    opciones_mapeadas[display_label] = turno['id'] # Guardamos el ID del turno
      
  try:
    # Seleccionar el turno
    turno_seleccionado_str = inquirer.select(
      message="Elige el turno que deseas cancelar:",
      choices=choices
    ).execute()
    
    turno_id_a_cancelar = opciones_mapeadas[turno_seleccionado_str]
    
    # Pedir confirmación
    console.print()
    confirmacion = inquirer.confirm(
      message=f"¿Estás seguro de que deseas cancelar el turno:\n{turno_seleccionado_str}?"
    ).execute()
    
    if confirmacion:
      # Cambiar estado en la base de datos
      Turno.actualizar_estado(turno_id_a_cancelar, 'cancelado') 
      console.print(f"\n[bold green]✅ Turno #{turno_id_a_cancelar} cancelado con éxito.[/bold green]")
      console.print()
    else:
      console.print("\n[bold yellow]Operación de cancelación abortada por el usuario.[/bold yellow]")
      console.print()

  except KeyboardInterrupt:
    console.print("\n[yellow]Operación interrumpida por el usuario.[/yellow]")
    return
