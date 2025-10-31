from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from decimal import Decimal
import os # Necesario para manejar rutas de archivos
from rich.console import Console

console = Console()

# --- Constantes y Configuración ---
PDF_PATH = os.path.join(os.getcwd(), 'tickets')

# Asegúrate de que el directorio exista
if not os.path.exists(PDF_PATH):
  os.makedirs(PDF_PATH)
    
def generar_ticket_pdf(turno_info: dict, detalle_servicios: list):
  """Genera y guarda el detalle de cobro como un archivo PDF (Ticket)."""
  
  # 1. Preparar la información
  turno_id = turno_info['id']
  cliente = f"{turno_info['cliente_nombre']} {turno_info['cliente_apellido']}"
  fecha_hora_str = turno_info['fecha_hora'].strftime("%d/%m/%Y %H:%M")
  total_decimal = turno_info['total'] if isinstance(turno_info['total'], Decimal) else Decimal(str(turno_info['total']))
  
  filename = os.path.join(PDF_PATH, f"Ticket_{turno_id}_{turno_info['cliente_apellido']}.pdf")
  
  c = canvas.Canvas(filename, pagesize=letter)
  width, height = letter # 612x792 puntos (puntos = 1/72 pulgada)
  
  y = height - 50 # Posición inicial vertical (cerca de la parte superior)
  line_height = 20
  
  # 2. Encabezado del Ticket
  c.setFont("Helvetica-Bold", 16)
  c.drawString(inch, y, "SALÓN DE BELLEZA [NOMBRE DEL SALÓN]")
  y -= line_height * 1.5
  
  c.setFont("Helvetica-Bold", 12)
  c.drawString(inch, y, f"RECIBO DE PAGO - TURNO ID: {turno_id}")
  y -= line_height
  
  # 3. Datos del Cliente y Fecha
  c.setFont("Helvetica", 10)
  c.drawString(inch, y, f"Cliente: {cliente}")
  y -= line_height
  c.drawString(inch, y, f"Fecha y Hora: {fecha_hora_str}")
  y -= line_height * 2
  
  # 4. Detalle de Servicios (Tabla simple)
  c.setFont("Helvetica-Bold", 10)
  c.drawString(inch, y, "SERVICIO")
  c.drawString(inch * 4, y, "PRECIO")
  y -= line_height / 2
  c.line(inch, y, inch * 6, y) # Línea divisoria
  y -= line_height
  
  c.setFont("Helvetica", 10)
  for servicio in detalle_servicios:
      precio_str = f"${servicio['precio_cobrado']:.2f}"
      
      c.drawString(inch, y, servicio['nombre'])
      c.drawString(inch * 4, y, precio_str)
      y -= line_height
      
  y -= line_height / 2
  c.line(inch, y, inch * 6, y) # Línea divisoria
  y -= line_height
  
  # 5. Total
  c.setFont("Helvetica-Bold", 12)
  c.drawString(inch, y, "TOTAL COBRADO:")
  c.drawString(inch * 4, y, f"${total_decimal:.2f}")
  y -= line_height * 2
  
  # 6. Mensaje Final
  c.setFont("Helvetica-Oblique", 10)
  c.drawString(inch, y, "¡Gracias por su preferencia!")
  
  # 7. Finalizar y Guardar
  c.showPage()
  c.save()
  
  console.print(f"[bold green]✅ Ticket generado en:[/bold green] [yellow]{filename}[/yellow]")
    