import random
from datetime import datetime
from utils import get_connection
import pandas as pd

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
    cur.execute("DELETE FROM Usuario")
    cur.execute("DELETE FROM Funcionario")
    cur.execute("DELETE FROM Ingeniero")
    cur.execute("DELETE FROM Director")
    cur.execute("DELETE FROM Subdirector")
    cur.execute("DELETE FROM Solicitud")
    cur.execute("DELETE FROM HistorialEstadoSolicitud")
    cur.execute("DELETE FROM Visita")
    cur.execute("DELETE FROM Profesor")
    cur.execute("DELETE FROM Cotizacion")
    cur.execute("DELETE FROM Traslado")
    cur.execute("DELETE FROM Colacion")
    cur.execute("DELETE FROM Reembolso")
    cur.execute("DELETE FROM Visitante")
    cur.execute("DELETE FROM Emplazamiento")
    cur.execute("DELETE FROM UnidadAcademica")
    cur.execute("DELETE FROM Asignatura")
    conn.commit()

# Para reinicios de la base de datos sin necesidad de reiniciar contenedores
def reiniciar_secuencias():
    cur.execute("SELECT setval('emplazamiento_id_emplazamiento_seq', 1, false);")
    cur.execute("SELECT setval('unidadacademica_id_unidad_academica_seq', 1, false);")
    cur.execute("SELECT setval('funcionario_id_seq', 1, false);")
    cur.execute("SELECT setval('ingeniero_id_seq', 1, false);")
    cur.execute("SELECT setval('director_id_seq', 1, false);")
    cur.execute("SELECT setval('subdirector_id_seq', 1, false);")
    cur.execute("SELECT setval('asignatura_id_asignatura_seq', 1, false);")
    cur.execute("SELECT setval('profesor_id_profesor_seq', 1, false);")
    cur.execute("SELECT setval('visita_id_visita_seq', 1, false);")
    cur.execute("SELECT setval('traslado_id_seq', 1, false);")
    cur.execute("SELECT setval('reembolso_id_reembolso_seq', 1, false);")
    cur.execute("SELECT setval('colacion_id_seq', 1, false);")
    cur.execute("SELECT setval('cotizacion_id_cotizacion_seq', 1, false);")
    cur.execute("SELECT setval('solicitud_id_solicitud_seq', 1, false);")
    cur.execute("SELECT setval('historialestadosolicitud_id_seq', 1, false);")
    cur.execute("SELECT setval('visitante_id_seq', 1, false);")
    conn.commit()

def cargar_datos_universidad(archivo):
    df = pd.read_excel(archivo)

    print(df.columns)

    df = df[df['JORNADA'] == 'DIURNO']
    campus = df['CAMPUS_SEDE'].unique().tolist()
    departamento = df[['DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    semestre = df['SEMESTRE'].unique().tolist()
    asignaturas = df[['SIGLA', 'ASIGNATURA', 'DEPARTAMENTO', 'SEMESTRE', 'CAMPUS_SEDE']].drop_duplicates().to_dict(
        'records')
    paralelos = df[
        ['SIGLA', 'ASIGNATURA', 'PARALELO', 'SEMESTRE', 'DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict(
        'records')

    # Insertar datos en la tabla Emplazamiento
    for c in campus:
        cur.execute("INSERT INTO Emplazamiento (nombre, sigla) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (c, c[:8]))

    # Insertar datos en la tabla UnidadAcademica
    for d in departamento:
        cur.execute(
            "INSERT INTO UnidadAcademica (nombre, presupuesto, gasto, emplazamiento_id) VALUES (%s, %s, %s, (SELECT id_emplazamiento FROM Emplazamiento WHERE nombre = %s)) ON CONFLICT DO NOTHING;",
            (d['DEPARTAMENTO'], 0, 0, d['CAMPUS_SEDE']))

    # Insertar datos en la tabla Asignatura
    for a in asignaturas:
        cur.execute(
            "INSERT INTO Asignatura (sigla, nombre, semestre, departamento_id, paralelo) VALUES (%s, %s, %s, (SELECT id_unidad_academica FROM UnidadAcademica WHERE nombre = %s), %s) ON CONFLICT DO NOTHING;",
            (a['SIGLA'], a['ASIGNATURA'], a['SEMESTRE'], a['DEPARTAMENTO'], 0))

    # Insertar datos en la tabla Paralelo
    for p in paralelos:
        cur.execute(
            "INSERT INTO Asignatura (sigla, nombre, semestre, departamento_id, paralelo) VALUES (%s, %s, %s, (SELECT id_unidad_academica FROM UnidadAcademica WHERE nombre = %s), %s) ON CONFLICT DO NOTHING;",
            (p['SIGLA'], p['ASIGNATURA'], p['SEMESTRE'], p['DEPARTAMENTO'], p['PARALELO']))

    conn.commit()
    print("Datos cargados exitosamente.")

# Ejecutar los generadores de datos
if __name__ == "__main__":

    borrar_datos()
    reiniciar_secuencias()



    # Confirmar los cambios
    conn.commit()
    cur.close()
    conn.close()
    print("Datos generados exitosamente.")
