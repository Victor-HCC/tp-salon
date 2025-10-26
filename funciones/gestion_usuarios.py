from rich.console import Console
from InquirerPy import inquirer

from modelos.modelo_usuario import Usuario
from .auxiliares import validar_email, validar_password, validar_nombre, obtener_entrada_valida, mostrar_tabla

console = Console()

def crear_usuario():
  console.print("[bold green]--- Crear nuevo usuario ---[/bold green]")

  # Obtener y validar nombre
  nombre = obtener_entrada_valida(
    message="Nombre:",
    validator_func=validar_nombre,
    error_message="Nombre inválido. Solo debe contener letras y tener al menos 2 caracteres."
  )
  
  # Obtener y validar apellido
  apellido = obtener_entrada_valida(
    message="Apellido:",
    validator_func=validar_nombre,
    error_message="Apellido inválido. Solo debe contener letras y tener al menos 2 caracteres."
  )
  
  # Obtener y validar email
  email = obtener_entrada_valida(
    message="Email:",
    validator_func=validar_email,
    error_message="Email inválido. Asegúrate de usar un formato correcto (ej: usuario@dominio.com)."
  ).lower() # Se convierte a minúsculas después de la validación

  # Obtener y validar contraseña
  password = obtener_entrada_valida(
    message="Contraseña:",
    validator_func=validar_password,
    error_message="La contraseña debe tener al menos 6 caracteres, una mayúscula y un número.",
    is_secret=True
  )

  # Mostrar roles posibles
  rol = inquirer.select(
    message="Selecciona el rol del usuario:",
    choices=["admin", "recepcionista", "cajero", "cliente"]
  ).execute()

  try:
    nuevo_id = Usuario.crear(nombre, apellido, email, password, rol)
    console.print(f"[green]Usuario creado exitosamente con ID: {nuevo_id}[/green]")
  except Exception as e:
    console.print(f"[red]Error al crear usuario:[/red] {e}")

def obtener_usuario_a_editar():
  """Permite seleccionar el usuario por ID o Email."""
  
  opcion = inquirer.select(
    message="Buscar usuario por:",
    choices=["ID", "Email"]
  ).execute()

  usuario_encontrado = None
  
  if opcion == "ID":
    try:
      user_id = int(inquirer.text(message="Ingresa el ID del usuario:").execute().strip())
      usuario_encontrado = Usuario.obtener_por_id(user_id)
    except ValueError:
      console.print("[red]El ID debe ser un número entero.[/red]")
      return None
          
  elif opcion == "Email":
    email = inquirer.text(message="Ingresa el Email del usuario:").execute().strip()
    usuario_encontrado = Usuario.obtener_por_email(email)
      
  if not usuario_encontrado:
    console.print("[bold red]Usuario no encontrado.[/bold red]")
  
  return usuario_encontrado

def editar_usuario():
  console.print("[bold yellow]--- Editar usuario ---[/bold yellow]")
  
  # PASO 1 y 2: Identificar y Obtener Datos
  usuario_actual = obtener_usuario_a_editar()
  if not usuario_actual:
    return

  # Muestra la información del usuario
  console.print(f"[cyan]Editando a:[/cyan] ID {usuario_actual['id']} | {usuario_actual['nombre']} {usuario_actual['apellido']}")

  # Datos que se recopilarán para la actualización
  datos_nuevos = {}
  
  # --- Solicitud y Autocompletado ---
  
  # Nombre
  nuevo_nombre = obtener_entrada_valida(
    message="Nombre:",
    validator_func=validar_nombre,
    error_message="Nombre inválido. Solo debe contener letras y tener al menos 2 caracteres.",
    default=usuario_actual['nombre']
  )
  
  if nuevo_nombre != usuario_actual['nombre']:
    datos_nuevos['nombre'] = nuevo_nombre

  # Apellido
  nuevo_apellido = obtener_entrada_valida(
    message="Apellido:",
    validator_func=validar_nombre,
    error_message="Apellido inválido. Solo debe contener letras y tener al menos 2 caracteres.",
    default=usuario_actual['apellido']
  )
  
  if nuevo_apellido != usuario_actual['apellido']:
    datos_nuevos['apellido'] = nuevo_apellido
      
  # Email
  nuevo_email = obtener_entrada_valida(
    message="Email:",
    validator_func=validar_email,
    error_message="Email inválido. Asegúrate de usar un formato correcto (ej: usuario@dominio.com).",
    default=usuario_actual['email']
  ).lower()
  
  if nuevo_email != usuario_actual['email']:
    datos_nuevos['email'] = nuevo_email

  # Rol (Usando select con el valor actual como default)
  roles = ["admin", "recepcionista", "cajero", "cliente"]
  nuevo_rol = inquirer.select(
    message=f"Rol:",
    choices=roles,
    default=usuario_actual['rol']
  ).execute()
  
  if nuevo_rol != usuario_actual['rol']:
    datos_nuevos['rol'] = nuevo_rol
      
  # --- PASO 3: Actualizar ---
  
  if not datos_nuevos:
    console.print("[bold yellow]No se detectaron cambios. No se realizó ninguna actualización.[/bold yellow]")
    return
      
  try:
    # Llamar a tu función 'actualizar' con el ID y los nuevos datos
    Usuario.actualizar(usuario_actual['id'], **datos_nuevos)
    console.print("[bold green]Datos del usuario actualizados exitosamente.[/bold green]")
      
  except Exception as e:
    console.print(f"[bold red]Error al actualizar usuario:[/bold red] {e}")

def listar_usuarios():
  console.print("[bold yellow]--- Lista de Usuarios ---[/bold yellow]")
  
  opcion = inquirer.select(
    message="Listar usuarios por:",
    choices=["Empleados", "Clientes"]
  ).execute()
  
  data = []
  titulo = ''
  
  if opcion == 'Empleados':
    data = Usuario.listar_empleados()
    titulo = "Empleados del Salón"
  elif opcion == 'Clientes':
    data = Usuario.listar_clientes()
    titulo = "Clientes Registrados"
  
  mostrar_tabla(titulo, data)

def menu_gestion_usuarios():
  while True:
    opcion = inquirer.select(
      message="Gestión de Usuarios - Selecciona una acción:",
      choices=[
        "➕ Crear nuevo usuario",
        "✏️ Editar usuario",
        "📋 Listar usuarios",
        "🚫 Desactivar usuario",
        "⬅️ Volver al menú principal"
      ]
    ).execute()

    if opcion.startswith("➕"):
      crear_usuario()
    elif opcion.startswith("✏️"):
      editar_usuario()
    elif opcion.startswith("📋"):
      listar_usuarios()
    elif opcion.startswith("🚫"):
      console.print("[red]Desactivando usuario...[/red]")
      # Aquí función desactivar_usuario()

    elif opcion.startswith("⬅️"):
      break
