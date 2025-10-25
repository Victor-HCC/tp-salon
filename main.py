from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from InquirerPy import inquirer

from modelos.modelo_base import ModeloBase

from menus.menu_admin import mostrar_menu_admin

console = Console()

console.print(Panel("Bienvenido a la aplicación de Salon ✂ ✂ ✂", 
  title="Salon",
  expand=False
))

opcion = inquirer.select(
  message="Selecciona una opción:",
  choices=["Acceder", "Salir"]
).execute()


if opcion == "Acceder":
  console.print("[bold]Ingresa tus credenciales: [/bold]")
  email = input("Email: ")
  password = Prompt.ask("Contraseña", password=True)
  
  user_info = ModeloBase.autenticar(email, password)
  print(user_info)
  
  if user_info:
    rol = user_info.get('rol') # Obtener el rol del diccionario retornado
    console.print(f"[bold green]Acceso concedido. Rol: {rol.upper()}[/bold green]")
    
    if rol == 'admin':
      mostrar_menu_admin(user_info) # Llama a la función del menú de admin
    elif rol == 'recepcionista':
      mostrar_menu_recepcionista(user_info) # Llama al menú de recepcionista TO-DO
    # ... Añadir más 'elif' para 'cajero', 'cliente', etc.
    else:
      console.print("[bold yellow]Rol no reconocido o menú no implementado.[/bold yellow]")
      
  else:
    console.print("[bold red]Error de autenticación. Email o contraseña incorrectos.[/bold red]")
    
  exit()
  
if opcion == "Salir":
  console.print(Panel("[bold cyan]Hasta luego! 👋\nGracias por usar el sistema[/bold cyan]", 
    title="¡Adiós!", 
    subtitle="Vuelve pronto", 
    expand=False))
  exit()