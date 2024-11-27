DROP TABLE IF EXISTS Usuario CASCADE;
DROP TABLE IF EXISTS Funcionario CASCADE;
DROP TABLE IF EXISTS Ingeniero CASCADE;
DROP TABLE IF EXISTS Director CASCADE;
DROP TABLE IF EXISTS Subdirector CASCADE;
DROP TABLE IF EXISTS Solicitud CASCADE;
DROP TABLE IF EXISTS HistorialEstadoSolicitud CASCADE;
DROP TABLE IF EXISTS Visita CASCADE;
DROP TABLE IF EXISTS Profesor CASCADE;
DROP TABLE IF EXISTS Cotizacion CASCADE;
DROP TABLE IF EXISTS Traslado CASCADE;
DROP TABLE IF EXISTS Colacion CASCADE;
DROP TABLE IF EXISTS Reembolso CASCADE;
DROP TABLE IF EXISTS Visitante CASCADE;
DROP TABLE IF EXISTS Emplazamiento CASCADE;
DROP TABLE IF EXISTS UnidadAcademica CASCADE;
DROP TABLE IF EXISTS Asignatura CASCADE;

-- 1. Usuario
CREATE TABLE Usuario (
    rut CHAR(10) PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    password VARCHAR(128) NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Emplazamiento
CREATE TABLE Emplazamiento (
    id_emplazamiento SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    sigla CHAR(8) NOT NULL
);

-- 3. UnidadAcademica
CREATE TABLE UnidadAcademica (
    id_unidad_academica SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    presupuesto INT NOT NULL,
    gasto INT NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

-- 4. Funcionario
CREATE TABLE Funcionario (
    id SERIAL PRIMARY KEY,
    usuario_rut CHAR(10) NOT NULL,
    unidad_academica_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (unidad_academica_id) REFERENCES UnidadAcademica(id_unidad_academica)
);

-- 5. Ingeniero
CREATE TABLE Ingeniero (
    id SERIAL PRIMARY KEY,
    usuario_rut CHAR(10) NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

-- 6. Director
CREATE TABLE Director (
    id SERIAL PRIMARY KEY,
    usuario_rut CHAR(10) NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

-- 7. Subdirector
CREATE TABLE Subdirector (
    id SERIAL PRIMARY KEY,
    usuario_rut CHAR(10) NOT NULL,
    unidad_academica_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (unidad_academica_id) REFERENCES UnidadAcademica(id_unidad_academica)
);

-- 8. Asignatura
CREATE TABLE Asignatura (
    id_asignatura SERIAL PRIMARY KEY,
    sigla CHAR(8) NOT NULL,
    nombre VARCHAR(128) NOT NULL,
    semestre INT NOT NULL,
    departamento_id INT NOT NULL,
    paralelo INT NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES UnidadAcademica(id_unidad_academica)
);

-- 9. Profesor
CREATE TABLE Profesor (
    id_profesor SERIAL PRIMARY KEY,
    rut CHAR(12) NOT NULL,
    nombre VARCHAR(64) NOT NULL,
    email VARCHAR(254) NOT NULL
);

-- 10. Visita
CREATE TABLE Visita (
    id_visita SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(64) DEFAULT 'NN',
    fecha DATE NOT NULL,
    lugar VARCHAR(64) NOT NULL,
    profesor_id INT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES Profesor(id_profesor)
);
-- 13. Traslado
CREATE TABLE Traslado (
    id SERIAL PRIMARY KEY,
    nombre_proveedor VARCHAR(255),
    rut_proveedor CHAR(20),
    correo_proveedor VARCHAR(254),
    monto INT NOT NULL,
    cotizacion_1 TEXT,
    cotizacion_2 TEXT,
    cotizacion_3 TEXT
);

-- 14. Reembolso
CREATE TABLE Reembolso (
    id_reembolso SERIAL PRIMARY KEY,
    monto INT NOT NULL,
    fecha_pago DATE NOT NULL,
    estado VARCHAR(16) NOT NULL,
    usuario_rut CHAR(10) NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut)
);

-- 15. Colacion
CREATE TABLE Colacion (
    id SERIAL PRIMARY KEY,
    tipo_subvencion VARCHAR(20) CHECK (tipo_subvencion IN ('reembolso', 'presupuesto')),
    nombre_proveedor VARCHAR(255),
    rut_proveedor CHAR(20),
    correo_proveedor VARCHAR(254),
    cotizacion_1 TEXT,
    cotizacion_2 TEXT,
    cotizacion_3 TEXT,
    monto INT,
    reembolso_id INT,
    FOREIGN KEY (reembolso_id) REFERENCES Reembolso(id_reembolso)
);

-- 16. Cotizacion
CREATE TABLE Cotizacion (
    id_cotizacion SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Solo traslado', 'Solo colacion', 'Traslado y colacion')),
    estado VARCHAR(16) DEFAULT 'Pendiente',
    monto INT NOT NULL,
    traslado_id INT,
    colacion_id INT,
    FOREIGN KEY (traslado_id) REFERENCES Traslado(id),
    FOREIGN KEY (colacion_id) REFERENCES Colacion(id)
);

-- 11. Solicitud
CREATE TABLE Solicitud (
    id_solicitud SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    estado INT DEFAULT 2 CHECK (estado BETWEEN 0 AND 5),
    descripcion TEXT NOT NULL,
    usuario_rut CHAR(10) NOT NULL,
    asignatura_id INT NOT NULL,
    visita_id INT NOT NULL,
    cotizacion_id INT,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (asignatura_id) REFERENCES Asignatura(id_asignatura),
    FOREIGN KEY (visita_id) REFERENCES Visita(id_visita),
    FOREIGN KEY (cotizacion_id) REFERENCES Cotizacion(id_cotizacion)
);

-- 12. HistorialEstadoSolicitud
CREATE TABLE HistorialEstadoSolicitud (
    id SERIAL PRIMARY KEY,
    usuario_decision_rut CHAR(10) NOT NULL,
    solicitud_id INT NOT NULL,
    estado_anterior INT NOT NULL CHECK (estado_anterior BETWEEN 0 AND 5),
    decision VARCHAR(10) NOT NULL CHECK (decision IN ('aprobada', 'rechazada')),
    fecha_decision DATE NOT NULL,
    FOREIGN KEY (usuario_decision_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (solicitud_id) REFERENCES Solicitud(id_solicitud)
);



-- 17. Visitante
CREATE TABLE Visitante (
    id SERIAL PRIMARY KEY,
    visita_id INT NOT NULL,
    nombre VARCHAR(64) NOT NULL,
    rut CHAR(12) NOT NULL,
    email VARCHAR(254) NOT NULL,
    FOREIGN KEY (visita_id) REFERENCES Visita(id_visita)
);
