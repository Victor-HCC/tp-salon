from rich.console import Console
from rich.panel import Panel
from InquirerPy import inquirer


from menus.menu_admin import mostrar_menu_admin
from menus.menu_cliente import mostrar_menu_cliente
from menus.menu_recepcionista import mostrar_menu_recepcionista

from funciones.login import autenticar

console = Console()
console.print()
console.print(Panel("Bienvenido a la aplicación de Salon ✂ ✂ ✂", 
  title="Salon",
  expand=False
))

# --- Bucle principal para el menú de inicio de sesión ---
while True:
  try:
    opcion = inquirer.select(
      message="Selecciona una opción:",
      choices=["Acceder", "Salir"]
    ).execute()
  except KeyboardInterrupt:
    # Si presionan Ctrl+C en el menú principal
      console.print("\n[bold cyan]Saliendo del sistema... ¡Adiós! 👋[/bold cyan]")
      break # Sale del bucle while True
    
  if opcion == "Acceder":
    
    user_info = autenticar()
    
    if user_info:
      rol = user_info.get('rol') # Obtener el rol del diccionario retornado
      console.print()
      console.print(f"[bold green]Acceso concedido. Rol: {rol.upper()}[/bold green]")
      
      if rol == 'admin':
        mostrar_menu_admin(user_info) # Llama a la función del menú de admin
      elif rol == 'recepcionista':
        mostrar_menu_recepcionista(user_info) # Llama al menú de recepcionista
      elif rol == 'cliente':
        mostrar_menu_cliente(user_info)
      else:
        console.print("[bold yellow]Rol no reconocido o menú no implementado.[/bold yellow]")
    else:
      console.print()
      console.print("[bold red]Error de autenticación. Email o contraseña incorrectos.[/bold red]")
      console.print()
  if opcion == "Salir":
    console.print()
    console.print(Panel("[bold cyan]Hasta luego! 👋\nGracias por usar el sistema[/bold cyan]", 
      title="¡Adiós!", 
      subtitle="Vuelve pronto", 
      expand=False))
    console.print()
    exit()