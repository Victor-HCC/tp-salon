from modelos.modelo_base import ModeloBase

from rich.console import Console
from InquirerPy import inquirer

console = Console()

def autenticar():
  console.print("[bold]Ingresa tus credenciales: [/bold]")
  email = input("Email: ")
  password = inquirer.secret(message="Contraseña:").execute().strip()
  
  return ModeloBase.autenticar(email, password)