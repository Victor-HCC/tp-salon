-- -----------------------------------------------------------
-- 1. Tabla Empleado (Administradores y Empleados)
-- El campo 'rol' diferencia los permisos (administrador, peluquero, recepcionista, etc.).
-- -----------------------------------------------------------
CREATE TABLE Usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE, -- Único para login
  password_hash VARCHAR(255) NOT NULL, -- Contraseña hasheada
  rol ENUM('admin', 'peluquero', 'recepcionista', 'cliente') NOT NULL,
  activo BOOLEAN DEFAULT TRUE -- Para desactivar cuentas en lugar de eliminarlas
);

-- -----------------------------------------------------------
-- 2. Tabla Servicio
-- -----------------------------------------------------------
CREATE TABLE Servicio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  precio DECIMAL(10, 2) NOT NULL, -- Uso de DECIMAL para precisión monetaria
  duracion_estimada INT NOT NULL, -- En minutos
  activo BOOLEAN DEFAULT TRUE
);

-- -----------------------------------------------------------
-- 3. Tabla Turno 
-- -----------------------------------------------------------
CREATE TABLE Turno (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  fecha_hora DATETIME NOT NULL,
  estado ENUM('pendiente', 'confirmado', 'realizado', 'cancelado') NOT NULL DEFAULT 'pendiente',
  total DECIMAL(10, 2) DEFAULT 0.00,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id) REFERENCES Usuario(id) ON DELETE RESTRICT
);

-- -----------------------------------------------------------
-- 4. Tabla de Unión: Turno_Servicio (Muchos a Muchos)
-- Relaciona un turno con los servicios que se realizaron.
-- -----------------------------------------------------------
CREATE TABLE Turno_Servicio (
  turno_id INT NOT NULL,
  servicio_id INT NOT NULL,
  precio_cobrado DECIMAL(10, 2), -- Guardar el precio histórico por si el precio del servicio cambia
  
  PRIMARY KEY (turno_id, servicio_id),
  FOREIGN KEY (turno_id) REFERENCES Turno(id) ON DELETE CASCADE,
  FOREIGN KEY (servicio_id) REFERENCES Servicio(id) ON DELETE RESTRICT
);


