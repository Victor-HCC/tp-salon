-- ******************************************************
-- INSERCIÓN DE DATOS DE EJEMPLO
-- ******************************************************

-- -----------------------------------------------------------
-- 1. Usuarios de Administración y Empleados (ROL = 'admin', 'recepcionista', 'cajero', 'peluquero')
-- La contraseña de ejemplo es '1234' (se almacena el hash)
-- -----------------------------------------------------------

-- Recepcionista (ID: 2)
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Laura', 'Recepcionista', 'laura@salon.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'recepcionista');

-- Cajero (ID: 3)
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Andres', 'Cajero', 'andres@salon.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'cajero');

-- Peluqueros
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Sofia', 'Perez', 'sofia@salon.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'peluquero'); -- ID: 4
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Matias', 'Gomez', 'matias@salon.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'peluquero'); -- ID: 5
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Camila', 'Diaz', 'camila@salon.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'peluquero'); -- ID: 6

-- Clientes
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Elena', 'Cliente', 'elena@cliente.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'cliente'); -- ID: 7
INSERT INTO Usuario (nombre, apellido, email, password_hash, rol) VALUES 
('Juan', 'Cliente', 'juan@cliente.com', '$2b$12$bym078Of1msOYnm0jaD9hORISitVrSekpzRW.kTta2imkN21Ee48C', 'cliente'); -- ID: 8

-- -----------------------------------------------------------
-- 2. Servicios Ofrecidos
-- -----------------------------------------------------------

INSERT INTO Servicio (nombre, descripcion, precio, duracion_estimada) VALUES
('Corte de Pelo Caballero', 'Corte clásico con lavado.', 8000.00, 30, 1),
('Corte de Pelo Dama', 'Corte, secado y peinado.', 12000.00, 45, 1),
('Coloración Raíz', 'Aplicación de tintura solo en la raíz.', 25000.00, 60, 1),
('Manicura Básica', 'Limado, esmaltado y cutículas.', 5000.00, 30, 1),
('Pedicura Spa', 'Limpieza profunda, exfoliación y esmaltado.', 9500.00, 60, 1),
('Tratamiento Capilar', 'Mascarilla de hidratación intensiva.', 15000.00, 45, 1);

-- -----------------------------------------------------------
-- 3. Inserción de un Turno de Ejemplo 
-- Cliente (ID: 7) con Peluquero (ID: 4) para un Corte Caballero.
-- -----------------------------------------------------------

-- Insertar el Turno (primero el registro principal)
INSERT INTO Turno (cliente_id, fecha_hora, estado, total) VALUES
(7, '2025-11-01 10:00:00', 'confirmado', 800.00); -- Asumimos que el corte cuesta 800.00

-- Insertar el Servicio asociado al Turno (asumiendo que Corte Caballero tiene ID: 1)
-- NOTA: Debes verificar los IDs de los servicios insertados en tu BD.
INSERT INTO Turno_Servicio (turno_id, servicio_id, precio_cobrado) VALUES
(LAST_INSERT_ID(), 1, 800.00); 

COMMIT;