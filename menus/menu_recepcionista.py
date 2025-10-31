from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

from funciones.funciones_recepcionista import gestion_turnos, consulta_clientes, cobrar_turno, listar_servicios_recepcion

console = Console()

def mostrar_menu_recepcionista(user_info):
  """Muestra el menú interactivo para el rol de Recepcionista."""
  
  # Bucle principal del menú
  while True:
    console.print()
    console.print(Panel(f"[bold white]Menú Principal de Recepcionista[/bold white]",
      title=f"Bienvenido/a, {user_info.get('nombre')}", expand=False))

    try:
      opcion = inquirer.select(
        message="Tareas Operativas:",
        choices=[
          "📅 Gestión de Turnos",
          "👤 Consulta Rápida de Clientes",
          "💸 Cobro de Turnos confirmados",
          "💇 Consultar Servicios y Precios",
          "🚪 Cerrar Sesión"
        ]
      ).execute()
    except KeyboardInterrupt:
      console.print("[yellow]Operación cancelada por el usuario. Cerrando la aplicación...[/yellow]")
      return

    if opcion.startswith("📅"):
      # Lógica para ver turnos pendientes, confirmar llegada (Pendiente -> Confirmado), etc.
      gestion_turnos() 
    elif opcion.startswith("👤"):
      # Lógica para buscar cliente por ID/Email y ver su información básica.
      consulta_clientes()
    elif opcion.startswith("💸"):
      # Lógica para listar los turnos confirmados y seleccionar uno para cobrar y cambiar a realizado
      cobrar_turno()
    elif opcion.startswith("💇"):
      # Usar la función que ya creaste para listar servicios con sus detalles
      listar_servicios_recepcion() 
    elif opcion.startswith("🚪"):
      console.print("[bold cyan]Cerrando sesión de Recepcionista...[/bold cyan]")
      break # Sale del bucle While