from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer

console = Console()

def mostrar_menu_admin(user_info):
  """Muestra el menú interactivo para el rol de Administrador."""
  
  # Bucle principal del menú
  while True:
    console.print(Panel(f"[bold white]Menú Principal de Administrador[/bold white]",
      title=f"Bienvenido, {user_info.get('nombre', 'Admin')}", expand=False))

    opcion = inquirer.select(
      message="Tareas de Administración:",
      choices=[
        "Gestión de Usuarios (Empleados)",
        "Gestión de Servicios y Productos",
        "Ver Reportes de Ventas",
        "Cerrar Sesión"
      ]
    ).execute()

    if opcion == "Gestión de Usuarios (Empleados)":
      # Aquí llamarías a una función o clase para gestionar usuarios
      console.print("[yellow]--- Accediendo a Gestión de Usuarios ---[/yellow]")
      pass
    
    elif opcion == "Gestión de Servicios y Productos":
      # Aquí llamarías a la lógica de CRUD para Servicios/Productos
      console.print("[yellow]--- Accediendo a Gestión de Servicios/Productos ---[/yellow]")
      pass

    elif opcion == "Cerrar Sesión":
      console.print("[bold cyan]Cerrando sesión de Administrador.[/bold cyan]")
      break # Sale del bucle While y regresa a main.py (que luego hace exit())

    # Puedes añadir una pausa entre acciones si lo deseas
    # console.input("\n[dim]Presiona Enter para continuar...[/dim]")