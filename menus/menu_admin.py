from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

from funciones.gestion_usuarios import menu_gestion_usuarios

console = Console()

def mostrar_menu_admin(user_info):
  """Muestra el menú interactivo para el rol de Administrador."""
  
  # Bucle principal del menú
  while True:
    console.print(Panel(f"[bold white]Menú Principal de Administrador[/bold white]",
      title=f"Bienvenido, {user_info.get('nombre')}", expand=False))

    opcion = inquirer.select(
      message="Tareas de Administración:",
      choices=[
        "👥 Gestión de Usuarios",
        "💇 Gestión de Servicios",
        "📊 Ver Reportes de Ventas",
        "🚪 Cerrar Sesión"
      ]
    ).execute()

    if opcion.startswith("👥"):
      menu_gestion_usuarios()
    elif opcion.startswith("💇"):
      menu_gestion_servicios()
    elif opcion.startswith("📊"):
      menu_reportes()
    elif opcion.startswith("🚪"):
      console.print("[bold cyan]Cerrando sesión de Administrador...[/bold cyan]")
      break # Sale del bucle While y regresa a main.py (que luego hace exit())

    # Puedes añadir una pausa entre acciones si lo deseas
    # console.input("\n[dim]Presiona Enter para continuar...[/dim]")