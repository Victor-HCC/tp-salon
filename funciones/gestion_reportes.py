from rich.console import Console
from rich.panel import Panel
from rich.box import DOUBLE_EDGE # Importa un estilo de borde

console = Console()

def menu_reportes():
  contenido = (
    "[bold yellow]🔒 ACCESO RESTRINGIDO 🔒[/bold yellow]\n\n"
    "Esta sección de Reportes y Análisis Avanzados\n"
    "solo está disponible para usuarios con la "
    "[bold magenta]Suscripción Premium[/bold magenta] 🌟.\n\n"
    "[italic bright_white]¡Gracias por tu comprensión! 😉[/italic bright_white]"
  )
  
  console.print()
  console.print(
    Panel(
      contenido,
      title="[bold red]💸 Reportes de Facturación 💸[/bold red]",
      subtitle="[bold red]¡Actualiza tu cuenta hoy mismo![/bold red]",
      border_style="yellow",
      box=DOUBLE_EDGE, # Utiliza un borde doble para que se destaque
      padding=(1, 4), # Relleno vertical y horizontal para más espacio
      width=75
    )
  )
  console.print()
  
