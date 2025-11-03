from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from InquirerPy import inquirer

from menus.menu_admin import mostrar_menu_admin
from menus.menu_cliente import mostrar_menu_cliente
from menus.menu_recepcionista import mostrar_menu_recepcionista
from funciones.login import autenticar

console = Console()

def mostrar_banner():
  console.print()
  banner = """
  💈✨  Bienvenido a  ✨💈
    ███████╗ █████╗ ██╗      ██████╗ ███╗   ██╗
    ██╔════╝██╔══██╗██║     ██╔═══██╗████╗  ██║
    ███████╗███████║██║     ██║   ██║██╔██╗ ██║
    ╚════██║██╔══██║██║     ██║   ██║██║╚██╗██║
    ███████║██║  ██║███████╗╚██████╔╝██║ ╚████║
    ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
    ✂  Sistema de Gestión de Salón  ✂
  """
  panel = Panel(
    Align.center(banner),
    title="[bold magenta]Salon App[/bold magenta]",
    border_style="bright_magenta",
    expand=False
  )
  console.print(panel)

def mostrar_menu_inicio():
  while True:
    try:
      opcion = inquirer.select(
        message="Selecciona una opción:",
        choices=["Acceder", "Salir"],
        pointer="👉",
        default="Acceder"
      ).execute()
    except KeyboardInterrupt:
      console.print("\n[bold cyan]Saliendo del sistema... ¡Adiós! 👋[/bold cyan]")
      break

    if opcion == "Acceder":
      user_info = autenticar()
      console.print()
      if user_info:
        rol = user_info.get("rol", "").lower()
        console.print(f"[bold green]✅ Acceso concedido[/bold green] — Rol: [yellow]{rol.upper()}[/yellow]\n")

        if rol == "admin":
          mostrar_menu_admin(user_info)
        elif rol == "recepcionista":
          mostrar_menu_recepcionista(user_info)
        elif rol == "cliente":
          mostrar_menu_cliente(user_info)
        else:
          console.print("[bold yellow]Rol no reconocido o menú no implementado.[/bold yellow]")
      else:
          console.print("[bold red]❌ Error de autenticación. Email o contraseña incorrectos.[/bold red]\n")

    elif opcion == "Salir":
      despedida = Panel(
        Align.center("[bold cyan]Hasta luego! 👋\nGracias por usar el sistema[/bold cyan]"),
        title="💫 ¡Adiós!",
        subtitle="Vuelve pronto 💇‍♀️",
        border_style="cyan",
        expand=False
      )
      console.print(despedida)
      console.print()
      break

if __name__ == "__main__":
  console.clear()
  mostrar_banner()
  mostrar_menu_inicio()
