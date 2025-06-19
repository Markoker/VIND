DROP TABLE IF EXISTS HistorialEstadoItem CASCADE;
DROP TABLE IF EXISTS Solicitud CASCADE;
DROP TABLE IF EXISTS Cotizacion CASCADE;
DROP TABLE IF EXISTS Colacion CASCADE;
DROP TABLE IF EXISTS Traslado CASCADE;
DROP TABLE IF EXISTS Reembolso CASCADE;
DROP TABLE IF EXISTS AsignaturaSolicitud CASCADE;
DROP TABLE IF EXISTS Asignatura CASCADE;
DROP TABLE IF EXISTS UnidadAcademica CASCADE;
DROP TABLE IF EXISTS Emplazamiento CASCADE;
DROP TABLE IF EXISTS Usuario CASCADE;
DROP TABLE IF EXISTS Visitante CASCADE;
DROP TABLE IF EXISTS Visita CASCADE;
DROP TABLE IF EXISTS Profesor CASCADE;
DROP TABLE IF EXISTS Presupuesto CASCADE;
DROP TABLE IF EXISTS HistorialPresupuesto CASCADE;

-- Usuarios (sin campo perfil)
CREATE TABLE Usuario (
    rut VARCHAR(10) PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emplazamientos y Unidades Académicas
CREATE TABLE Emplazamiento (
    id_emplazamiento SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    sigla CHAR(8) NOT NULL
);

CREATE TABLE UnidadAcademica (
    id_unidad_academica SERIAL PRIMARY KEY,
    nombre VARCHAR(64) NOT NULL,
    presupuesto INT NOT NULL,
    gasto INT NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

-- Tablas de roles (un usuario puede tener más de un rol)
CREATE TABLE Funcionario (
    id SERIAL PRIMARY KEY,
    usuario_rut VARCHAR(10) NOT NULL,
    unidad_academica_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (unidad_academica_id) REFERENCES UnidadAcademica(id_unidad_academica)
);

CREATE TABLE Administrador (
    id SERIAL PRIMARY KEY,
    usuario_rut VARCHAR(10) NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

CREATE TABLE Director (
    id SERIAL PRIMARY KEY,
    usuario_rut VARCHAR(10) NOT NULL,
    emplazamiento_id INT NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (emplazamiento_id) REFERENCES Emplazamiento(id_emplazamiento)
);

-- Presupuesto y su historial
CREATE TABLE Presupuesto (
    id_unidad_academica INT NOT NULL,
    anio INT NOT NULL,
    semestre INT NOT NULL CHECK (semestre IN (1,2)),
    cantidad INT NOT NULL,
    FOREIGN KEY (id_unidad_academica) REFERENCES UnidadAcademica(id_unidad_academica),
    CONSTRAINT presupuesto_unico UNIQUE (id_unidad_academica, anio, semestre)
);

CREATE TABLE HistorialPresupuesto (
    id_usuario VARCHAR(10) NOT NULL,
    id_unidad_academica INT NOT NULL,
    anio INT NOT NULL,
    semestre INT NOT NULL CHECK (semestre IN (1,2)),
    nueva_cantidad INT NOT NULL,
    fecha_cambio TIMESTAMP NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(rut)
);

-- Asignaturas y relación con solicitudes
CREATE TABLE Asignatura (
    id_asignatura SERIAL PRIMARY KEY,
    sigla CHAR(8) NOT NULL,
    nombre VARCHAR(128) NOT NULL,
    semestre INT NOT NULL,
    departamento_id INT NOT NULL,
    paralelo INT NOT NULL,
    anio INT NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES UnidadAcademica(id_unidad_academica)
);

-- Visitas y visitantes
CREATE TABLE Visita (
    id_visita SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(64) DEFAULT 'NN',
    fecha DATE NOT NULL,
    lugar VARCHAR(64) NOT NULL
);

CREATE TABLE Visitante (
    id SERIAL PRIMARY KEY,
    visita_id INT NOT NULL,
    nombre VARCHAR(96) NOT NULL,
    rut CHAR(12) NOT NULL,
    rol VARCHAR(12) NOT NULL,
    email VARCHAR(254) NOT NULL,
    vtr VARCHAR(12) NOT NULL,
    carrera VARCHAR(64) NOT NULL,
    FOREIGN KEY (visita_id) REFERENCES Visita(id_visita)
);

CREATE TABLE Profesor (
    id_profesor SERIAL PRIMARY KEY,
    rut CHAR(12) NOT NULL,
    nombre VARCHAR(64) NOT NULL,
    email VARCHAR(254) NOT NULL,
    visita_id INT NOT NULL,
    FOREIGN KEY (visita_id) REFERENCES Visita(id_visita)
);

-- Ítems: Colación y Traslado (cada uno con su propio estado)
CREATE TABLE Traslado (
    id SERIAL PRIMARY KEY,
    nombre_proveedor VARCHAR(255),
    rut_proveedor CHAR(20),
    correo_proveedor VARCHAR(254),
    monto INT NOT NULL,
    cotizacion_1 TEXT,
    cotizacion_2 TEXT,
    cotizacion_3 TEXT,
    estado VARCHAR(32) DEFAULT 'pendiente_revision'
);

CREATE TABLE Reembolso (
    id_reembolso SERIAL PRIMARY KEY,
    monto INT NOT NULL,
    fecha_pago DATE NOT NULL,
    estado VARCHAR(16) NOT NULL,
    usuario_rut VARCHAR(10) NOT NULL,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut)
);

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
    estado VARCHAR(32) DEFAULT 'pendiente_revision',
    FOREIGN KEY (reembolso_id) REFERENCES Reembolso(id_reembolso)
);

-- Cotización general (puede tener solo traslado, solo colación, o ambos)
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

-- Solicitud (referencia a cotización, usuario, visita)
CREATE TABLE Solicitud (
    id_solicitud SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    anio INT NOT NULL,
    semestre INT NOT NULL CHECK (semestre IN (1,2)),
    estado INT DEFAULT 2 CHECK (estado BETWEEN 0 AND 6),
    descripcion TEXT NOT NULL,
    usuario_rut VARCHAR(10) NOT NULL,
    visita_id INT NOT NULL,
    cotizacion_id INT,
    FOREIGN KEY (usuario_rut) REFERENCES Usuario(rut),
    FOREIGN KEY (visita_id) REFERENCES Visita(id_visita),
    FOREIGN KEY (cotizacion_id) REFERENCES Cotizacion(id_cotizacion)
);

-- Historial de estados por ítem (colación o traslado)
CREATE TABLE HistorialEstadoItem (
    id SERIAL PRIMARY KEY,
    solicitud_id INT NOT NULL,
    item_tipo VARCHAR(16) NOT NULL CHECK (item_tipo IN ('colacion', 'traslado')),
    item_id INT NOT NULL,
    estado_anterior VARCHAR(32) NOT NULL,
    estado_nuevo VARCHAR(32) NOT NULL,
    usuario_decision_rut VARCHAR(10) NOT NULL,
    comentario TEXT,
    fecha_decision TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (solicitud_id) REFERENCES Solicitud(id_solicitud),
    FOREIGN KEY (usuario_decision_rut) REFERENCES Usuario(rut)
);


CREATE TABLE AsignaturaSolicitud (
    id SERIAL PRIMARY KEY,
    solicitud_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    FOREIGN KEY (solicitud_id) REFERENCES Solicitud(id_solicitud),
    FOREIGN KEY (asignatura_id) REFERENCES Asignatura(id_asignatura)
);

