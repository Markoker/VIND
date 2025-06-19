import random
import pandas as pd

from querys.utils import *
import querys.usuario as Usuario
import querys.emplazamiento as Emplazamiento
import querys.visita as Visita
import querys.asignatura as Asignatura
import querys.solicitud as Solicitud

# Conectar a la base de datos
conn = get_connection()
cur = conn.cursor()

# Lista de datos predeterminados
# 103 nombres
nombres = [
    'Juan', 'Maria', 'Pedro', 'Josefa', 'Carla', 'Luis', 'Ana', 'Santiago', 'Valentina', 'Diego',
    'Lucia', 'Andres', 'Camila', 'Carlos', 'Martina', 'Alejandro', 'Sofía', 'David', 'Paula', 'Javier',
    'Isabella', 'Manuel', 'Gabriela', 'Ricardo', 'Antonella', 'Miguel', 'Victoria', 'Francisco', 'Fernanda', 'Jose',
    'Daniela', 'Rafael', 'Pía', 'Elena', 'Felipe', 'Valeria', 'Alberto', 'Florencia', 'Rodrigo', 'Emilia', 'Enrique',
    'Patricia', 'Nicolas', 'Carolina', 'Eduardo', 'Samantha', 'Fernando', 'Adriana', 'Gonzalo', 'Mariana', 'Alfonso',
    'Gabriel', 'Monica', 'Roberto', 'Alejandra','Giuseppe' ,'Sebastian', 'Claudia', 'Pablo', 'Luz', 'Joaquin', 'Lorena',
    'Cristian', 'Rocio', 'Esteban', 'Bianca', 'Hugo', 'Veronica', 'Marco', 'Renata', 'Jesus', 'Julia',
    'Samuel', 'Fabiola', 'Ramon', 'Marco', 'Araceli', 'Raul', 'Belen', 'Elias', 'Victoria', 'Tomás', 'Margarita',
    'Oscar', 'Viviana', 'Dario', 'Silvia', 'Mauricio', 'Elisa', 'Bruno', 'Clara', 'Ivan', 'Cecilia',
    'Alfredo', 'Marcela', 'Jorge', 'Liliana', 'Alonso', 'Daniela', 'Ignacio', 'Susana', 'Julio', 'Pilar'
]

# 103 apellidos
apellidos = [
    'González', 'Rodríguez', 'Gómez', 'Fernández', 'López', 'Martínez', 'Pérez', 'Sánchez', 'Ramírez', 'Torres',
    'Flores', 'Rivera', 'Hernández', 'Jiménez', 'Moreno', 'Castro', 'Ortiz', 'Ramos', 'Romero', 'Cruz',
    'Vargas', 'Reyes', 'Mendoza','Correa', 'Ruiz', 'Gutiérrez', 'Castillo', 'Silva', 'Rojas', 'Guerrero', 'Núñez',
    'Contreras', 'Fuentes', 'Álvarez', 'Espinoza', 'Salazar', 'Chávez', 'Ríos', 'Vega', 'Cortés', 'Delgado',
    'Acosta', 'Campos', 'Paredes', 'Peña', 'Navarro', 'Soto', 'Valenzuela', 'Mejía', 'Molina', 'Figueroa',
    'Aguilar', 'Ortiz', 'Ponce', 'Medina', 'Morales', 'Salinas', 'Lara', 'Mora', 'Muñoz', 'Ibarra',
    'Zamora','Repetto', 'Villanueva', 'Paz', 'Cárdenas', 'Escobar', 'León', 'Cabrera', 'Barrios', 'Lozano', 'Serrano',
    'Vásquez', 'Quintero', 'Orozco', 'Montoya', 'Carrillo', 'Guevara', 'Pineda', 'Juárez', 'Hurtado', 'Padilla',
    'Valle', 'Sosa', 'Suárez', 'Roldán', 'Maldonado', 'Bravo', 'Queirolo', 'Miranda', 'Esteban', 'Coronado', 'Santana',
    'Solís', 'Bustamante', 'Córdoba', 'Benítez', 'Castañeda', 'Beltrán', 'Ferrer', 'Arroyo', 'Velasco', 'Villarreal'
]
nombres_centros = ['Centro de Costos A', 'Centro de Costos B', 'Centro de Costos C','Centro de Costos D', 'Centros de Costos E']
nombres_actividades = ['Seminario', 'Transporte', 'Almuerzo', 'Suministro']
roles = ['jefe', 'trabajador', 'contador']


# Borrar datos de todas las tablas respetando el orden de dependencias
# Para reinicios de la base de datos
def borrar_datos():
    cur.execute("DELETE FROM HistorialEstadoItem")
    cur.execute("DELETE FROM AsignaturaSolicitud")
    cur.execute("DELETE FROM Funcionario")
    cur.execute("DELETE FROM Administrador")
    cur.execute("DELETE FROM Director")
    cur.execute("DELETE FROM Solicitud")
    cur.execute("DELETE FROM Profesor")
    cur.execute("DELETE FROM Visita")
    cur.execute("DELETE FROM Cotizacion")
    cur.execute("DELETE FROM Traslado")
    cur.execute("DELETE FROM Colacion")
    cur.execute("DELETE FROM Reembolso")
    cur.execute("DELETE FROM Visitante")
    cur.execute("DELETE FROM Asignatura")
    cur.execute("DELETE FROM UnidadAcademica")
    cur.execute("DELETE FROM Emplazamiento")
    cur.execute("DELETE FROM Usuario")
    conn.commit()

# Para reinicios de la base de datos sin necesidad de reiniciar contenedores
def reiniciar_secuencias():
    cur.execute("SELECT setval('emplazamiento_id_emplazamiento_seq', 1, false);")
    cur.execute("SELECT setval('unidadacademica_id_unidad_academica_seq', 1, false);")
    cur.execute("SELECT setval('funcionario_id_seq', 1, false);")
    cur.execute("SELECT setval('administrador_id_seq', 1, false);")
    cur.execute("SELECT setval('director_id_seq', 1, false);")
    cur.execute("SELECT setval('asignatura_id_asignatura_seq', 1, false);")
    cur.execute("SELECT setval('profesor_id_profesor_seq', 1, false);")
    cur.execute("SELECT setval('visita_id_visita_seq', 1, false);")
    cur.execute("SELECT setval('traslado_id_seq', 1, false);")
    cur.execute("SELECT setval('reembolso_id_reembolso_seq', 1, false);")
    cur.execute("SELECT setval('colacion_id_seq', 1, false);")
    cur.execute("SELECT setval('cotizacion_id_cotizacion_seq', 1, false);")
    cur.execute("SELECT setval('solicitud_id_solicitud_seq', 1, false);")
    cur.execute("SELECT setval('historialestadoitem_id_seq', 1, false);")
    cur.execute("SELECT setval('visitante_id_seq', 1, false);")
    conn.commit()

def cargar_datos_universidad(archivo):
    df = pd.read_excel(archivo)

    print(df.columns)

    df = df[df['JORNADA'] == 'DIURNO']

    df['SIGLA'] = df['SIGLA'].str.strip()

    campus = df['CAMPUS_SEDE'].unique().tolist()
    departamento = df[['DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    semestre = df['SEMESTRE'].unique().tolist()
    asignaturas = df[['SIGLA', 'ASIGNATURA', 'DEPARTAMENTO', 'SEMESTRE', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    paralelos = df[['SIGLA', 'ASIGNATURA', 'PARALELO', 'SEMESTRE', 'DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')

    # Insertar datos en la tabla Emplazamiento
    for c in campus:
        cur.execute("INSERT INTO Emplazamiento (nombre, sigla) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (c, c[:8]))

    # Insertar datos en la tabla UnidadAcademica
    for d in departamento:
        presupuesto = random.randint(1_000_000, 10_000_000)
        gasto = random.randint(1, int(presupuesto * 0.8))

        cur.execute(
            "INSERT INTO UnidadAcademica (nombre, presupuesto, gasto, emplazamiento_id) VALUES (%s, %s, %s, (SELECT id_emplazamiento FROM Emplazamiento WHERE nombre = %s)) ON CONFLICT DO NOTHING;",
            (d['DEPARTAMENTO'], presupuesto, gasto, d['CAMPUS_SEDE']))

    # Insertar datos en la tabla Asignatura
    for p in paralelos:
        cur.execute(
            "INSERT INTO Asignatura (sigla, nombre, semestre, departamento_id, paralelo, anio) VALUES (%s, %s, %s, (SELECT id_unidad_academica FROM UnidadAcademica WHERE nombre = %s AND emplazamiento_id = (SELECT id_emplazamiento FROM Emplazamiento WHERE nombre = %s)), %s, 2024) ON CONFLICT DO NOTHING;",
            (p['SIGLA'], p['ASIGNATURA'], p['SEMESTRE'], p['DEPARTAMENTO'], p['CAMPUS_SEDE'], p['PARALELO']))

    conn.commit()
    print("Datos cargados exitosamente.")

def generar_usuarios():
    Usuario.createUser(rut="99999999-9", email="test@test.cl", first_name="nombre", last_name="apellido", password="1234")
    # Generar usuarios
    for i in range(100):
        rut = str(random.randint(10000000, 25000000)) + "-" + str(random.randint(0, 9))
        nombre = (random.choice(nombres).lower()
                  .replace("á", "a")
                  .replace("é", "e")
                  .replace("í", "i")
                  .replace("ó", "o")
                  .replace("ú", "u")
                  .replace("ñ", "n"))
        apellido = (random.choice(apellidos).lower()
                  .replace("á", "a")
                  .replace("é", "e")
                  .replace("í", "i")
                  .replace("ó", "o")
                  .replace("ú", "u")
                  .replace("ñ", "n"))

        email = f"{nombre}.{apellido}@usm.cl".lower()

        # Check if email already exists
        cur.execute("SELECT * FROM Usuario WHERE email = %s;", (email,))
        while cur.fetchone() is not None:
            email = f"{nombre}.{apellido}{random.randint(1, 100)}@usm.cl".lower()
            cur.execute("SELECT * FROM Usuario WHERE email = %s;", (email,))

        Usuario.createUser(rut=rut, email=email, first_name=nombre, last_name=apellido, password="1234")

    print("Usuarios generados exitosamente.")

def generar_roles():
    usuarios = Usuario.getUsuarios()
    unidades = Emplazamiento.getUnidadesAcademicas()
    emplazamientos = Emplazamiento.getEmplazamientos()

    for usuario in usuarios:
        isFuncionario = random.randint(0, 1)
        isAdministrador = random.randint(0, 1)
        isDirector = random.randint(0, 1)

        if isFuncionario:
            cantidad = random.randint(1, 5)
            for i in range(cantidad):
                unidad = random.choice(unidades)
                cur.execute("INSERT INTO Funcionario (usuario_rut, unidad_academica_id) VALUES (%s, %s);", (usuario[0], unidad[0]))

        if isAdministrador:
            cantidad = random.randint(1, 5)
            for i in range(cantidad):
                emplazamiento = random.choice(emplazamientos)
                cur.execute("INSERT INTO Administrador (usuario_rut, emplazamiento_id) VALUES (%s, %s);", (usuario[0], emplazamiento['id']))

        if isDirector:
            cantidad = random.randint(1, 5)
            for i in range(cantidad):
                emplazamiento = random.choice(emplazamientos)
                cur.execute("INSERT INTO Director (usuario_rut, emplazamiento_id) VALUES (%s, %s);", (usuario[0], emplazamiento['id']))

    usuario_rut = "99999999-9"
    unidad = random.sample(unidades, k=7)
    emplazamiento = random.sample(emplazamientos, k=2)

    for i in range(7):
        cur.execute("INSERT INTO Funcionario (usuario_rut, unidad_academica_id) VALUES (%s, %s);",
                    (usuario_rut, unidad[i][0]))

    for i in range(2):
        cur.execute("INSERT INTO Administrador (usuario_rut, emplazamiento_id) VALUES (%s, %s);",
                    (usuario_rut, emplazamiento[i]['id']))

    for i in range(2):
        cur.execute("INSERT INTO Director (usuario_rut, emplazamiento_id) VALUES (%s, %s);",
                    (usuario_rut, emplazamiento[i]['id']))

    conn.commit()
    print("Roles generados exitosamente.")

def generar_profesores(n, visita_id):
    # Generate professors
    for i in range(n):  # Adjust the number of professors as needed
        rut = str(random.randint(10000000, 25000000)) + "-" + str(random.randint(0, 9))
        nombre = (random.choice(nombres).lower()
                  .replace("á", "a")
                  .replace("é", "e")
                  .replace("í", "i")
                  .replace("ó", "o")
                  .replace("ú", "u")
                  .replace("ñ", "n"))
        apellido = (random.choice(apellidos).lower()
                  .replace("á", "a")
                  .replace("é", "e")
                  .replace("í", "i")
                  .replace("ó", "o")
                  .replace("ú", "u")
                  .replace("ñ", "n"))

        email = f"{nombre}.{apellido}@usm.cl".lower()

        cur.execute(
            "INSERT INTO Profesor (rut, nombre, email, visita_id) VALUES (%s, %s, %s, %s);",
            (rut, f"{nombre} {apellido}", email, visita_id)
        )

    conn.commit()
    print("Profesores generados exitosamente.")

def generar_solicitud(rut_usuario=None, estado=2):
    # Seleccionar un usuario aleatorio
    if rut_usuario is not None:
        usuario = Usuario.getUsuarios(query_type="by_rut", rut=rut_usuario)
    else:
        usuario = random.choice(Usuario.getUsuarios())

    # Crear una visita
    nombre_empresa = random.choice(['Empresa A', 'Empresa B', 'Empresa C'])
    fecha_visita = f"{random.randint(2024, 2025)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    lugar_visita = f"Lugar {random.randint(1, 100)}"
    
    cur.execute(
        "INSERT INTO Visita (nombre_empresa, fecha, lugar) VALUES (%s, %s, %s) RETURNING id_visita;",
        (nombre_empresa, fecha_visita, lugar_visita)
    )
    visita_id = cur.fetchone()[0]

    generar_profesores(random.randint(1, 2), visita_id)

    # Crear una cotización
    tipo_cotizacion = random.choice(['Solo traslado', 'Solo colacion', 'Traslado y colacion'])

    id_traslado = None
    id_colacion = None

    if tipo_cotizacion == 'Solo traslado' or tipo_cotizacion == 'Traslado y colacion':
        # Crear un traslado
        nombre_proveedor = f'Proveedor {random.randint(1, 100)}'
        rut_proveedor = f"{random.randint(10000000, 25000000)}-{random.randint(0, 9)}"
        correo_proveedor = 'aaa@proveedor.com'
        monto_traslado = random.randint(1000, 10000)

        cotizacion = "uploads/colacion/test.pdf"
        n_cotizaciones = random.randint(1, 3)
        cotizaciones = [cotizacion if c < n_cotizaciones else None for c in range(3)]

        cur.execute(
            '''INSERT INTO Traslado 
               (nombre_proveedor, rut_proveedor, correo_proveedor, monto,
               cotizacion_1, cotizacion_2, cotizacion_3, estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
               RETURNING id;
            ''',
            (nombre_proveedor, rut_proveedor, correo_proveedor, monto_traslado,
            cotizaciones[0], cotizaciones[1], cotizaciones[2], 'pendiente_revision')
        )
        id_traslado = cur.fetchone()[0]

    if tipo_cotizacion == 'Solo colacion' or tipo_cotizacion == 'Traslado y colacion':
        # Crear una colacion
        nombre_proveedor = 'Proveedor Y'
        tipo_sub = 'presupuesto'
        rut_proveedor = '12345678-9'
        correo_proveedor = 'aaa@proveedor.com'
        monto_colacion = random.randint(1000, 10000)

        cotizacion = "uploads/colacion/test.pdf"
        n_cotizaciones = random.randint(1, 3)
        cotizaciones = [cotizacion if c < n_cotizaciones else None for c in range(3)]

        cur.execute(
            '''INSERT INTO Colacion 
               (nombre_proveedor, tipo_subvencion, rut_proveedor, 
                correo_proveedor, monto, cotizacion_1, cotizacion_2, cotizacion_3, estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
               RETURNING id;
            ''',
            (nombre_proveedor, tipo_sub, rut_proveedor, correo_proveedor, monto_colacion,
             cotizaciones[0], cotizaciones[1], cotizaciones[2], 'pendiente_revision')
        )

        id_colacion = cur.fetchone()[0]

    monto_cotizacion = random.randint(1000, 10000)

    cur.execute(
        "INSERT INTO Cotizacion (tipo, monto, traslado_id, colacion_id) VALUES (%s, %s, %s, %s) RETURNING id_cotizacion;",
        (tipo_cotizacion, monto_cotizacion, id_traslado, id_colacion)
    )

    cotizacion_id = cur.fetchone()[0]

    # Insertar la solicitud en la base de datos
    descripcion_solicitud = 'Descripción de la solicitud'
    cur.execute(
        "INSERT INTO Solicitud (fecha, anio, semestre, estado, descripcion, usuario_rut, visita_id, cotizacion_id) VALUES (CURRENT_DATE, 2025, 1, %s, %s, %s, %s, %s) RETURNING id_solicitud;",
        (estado, descripcion_solicitud, usuario[0], visita_id, cotizacion_id)
    )

    solicitud_id = cur.fetchone()[0]

    # Registrar historial de estados para los ítems
    if id_traslado:
        cur.execute(
            '''INSERT INTO HistorialEstadoItem 
               (solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_decision_rut) 
               VALUES (%s, %s, %s, %s, %s, %s);''',
            (solicitud_id, 'traslado', id_traslado, 'inicial', 'pendiente_revision', usuario[0])
        )

    if id_colacion:
        cur.execute(
            '''INSERT INTO HistorialEstadoItem 
               (solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_decision_rut) 
               VALUES (%s, %s, %s, %s, %s, %s);''',
            (solicitud_id, 'colacion', id_colacion, 'inicial', 'pendiente_revision', usuario[0])
        )

    conn.commit()

    # Crear registros correspondientes en la tabla AsignaturaSolicitud en base a las unidades academicas del usuario
    unidades_academicas = Usuario.getRolDeptos(usuario[0], "funcionario")
    cant_asignaturas = random.randint(1, 3)

    for i in range(cant_asignaturas):
        asignatura = random.choice(Asignatura.Get(query_type="by_unidad", id_unidad_academica=random.choice(unidades_academicas)['id'], semestre=2))
        cur.execute(
            "INSERT INTO AsignaturaSolicitud (asignatura_id, solicitud_id) VALUES (%s, %s);",
            (asignatura[0], solicitud_id)
        )

    conn.commit()
    print("Solicitud generada exitosamente.")

# Ejecutar los generadores de datos
if __name__ == "__main__":
    borrar_datos()
    reiniciar_secuencias()

    cargar_datos_universidad('DATA.xlsx')
    generar_usuarios()
    generar_roles()

    usuario_rut = "12345678-9"

    Usuario.createUser(rut=usuario_rut, email="test@usm.cl", first_name="Juan", last_name="Tapia", password="1234")

    unidades = Emplazamiento.getUnidadesAcademicas()
    emplazamientos = Emplazamiento.getEmplazamientos()

    # Asignar roles al usuario de prueba
    for i in range(7):
        cur.execute("INSERT INTO Funcionario (usuario_rut, unidad_academica_id) VALUES (%s, %s);",
                    (usuario_rut, unidades[i][0]))

    for i in range(2):
        cur.execute("INSERT INTO Administrador (usuario_rut, emplazamiento_id) VALUES (%s, %s);",
                    (usuario_rut, emplazamientos[i]['id']))

    for i in range(2):
        cur.execute("INSERT INTO Director (usuario_rut, emplazamiento_id) VALUES (%s, %s);",
                    (usuario_rut, emplazamientos[i]['id']))

    conn.commit()

    # Generar solicitudes de prueba
    for _ in range(20):
        generar_solicitud("99999999-9", estado=2)

    # Confirmar los cambios
    conn.commit()
    cur.close()
    conn.close()
    print("Datos generados exitosamente.")
