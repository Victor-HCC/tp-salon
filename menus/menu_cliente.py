from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

from funciones.funciones_cliente import cambiar_contraseña, solicitar_turno, listar_turnos_cliente, cancelar_turno

console = Console()

def mostrar_menu_cliente(user_info):
  """Menú principal del cliente"""
  while True:
    console.print(Panel(
      f"[bold white]Menú de Cliente[/bold white]",
      title=f"Bienvenido, {user_info.get('nombre')}",
      expand=False
    ))

    opcion = inquirer.select(
      message="¿Qué deseas hacer?",
      choices=[
        "📅 Solicitar turno",
        "👀 Ver mis turnos",
        "❌ Cancelar un turno",
        "🔒 Cambiar contraseña",
        "⬅️ Cerrar sesión"
      ]
    ).execute()

    if opcion.startswith("📅"):
      solicitar_turno(user_info["id"])
    elif opcion.startswith("👀"):
      listar_turnos_cliente(user_info["id"])
    elif opcion.startswith("❌"):
      cancelar_turno(user_info["id"])
    elif opcion.startswith("🔒"):
      cambiar_contraseña(user_info["id"])
    elif opcion.startswith("⬅️"):
      console.print("[bold cyan]Cerrando sesión...[/bold cyan]")
      break
