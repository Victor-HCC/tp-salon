from modelos.modelo_base import ModeloBase

from rich.console import Console
from InquirerPy import inquirer

console = Console()

def autenticar():
  console.print("[bold]Ingresa tus credenciales: [/bold]")
  try:
    email = input("Email: ")
    password = inquirer.secret(message="Contraseña:").execute().strip()
  except KeyboardInterrupt:
    console.print()
    console.print("\n[bold yellow]Operación cancelada por el usuario.[/bold yellow]")
    console.print()
    return None
  
  return ModeloBase.autenticar(email, password)