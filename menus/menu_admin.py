from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

from funciones.gestion_usuarios import menu_gestion_usuarios
from funciones.gestion_reportes import menu_reportes
from funciones.gestion_servicios import menu_gestion_servicios

console = Console()

def mostrar_menu_admin(user_info):
  """Muestra el menú interactivo para el rol de Administrador."""
  
  # Bucle principal del menú
  while True:
    console.print(Panel(f"[bold white]Menú Principal de Administrador[/bold white]",
      title=f"Bienvenido/a, {user_info.get('nombre')}", expand=False))

    opcion = inquirer.select(
      message="Tareas de Administración:",
      choices=[
        "👥 Gestión de Usuarios",
        "💇 Gestión de Servicios",
        "📊 Ver Reportes de Facturación",
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
