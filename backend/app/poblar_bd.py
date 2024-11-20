import random
from datetime import datetime
from utils import get_connection

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
    cur.execute("DELETE FROM Docs")
    cur.execute("DELETE FROM Rendicion")
    cur.execute("DELETE FROM Trabajador_Actividad")
    cur.execute("DELETE FROM Trabajador")
    cur.execute("DELETE FROM Actividad")
    cur.execute("DELETE FROM Centro_de_Costo")
    conn.commit()
    
# Para reinicios de la base de datos sin necesidad de reiniciar contenedores
def reiniciar_secuencias():
    cur.execute("SELECT setval('centro_de_costo_idCentro_de_Costo_seq', 1, false);")
    cur.execute("SELECT setval('actividad_idActividad_seq', 1, false);")
    cur.execute("SELECT setval('rendicion_idRendicion_seq', 1, false);")
    cur.execute("SELECT setval('docs_idDocs_seq', 1, false);")

# Generador de nombres:
def generar_nombres_trabajadores(num):
    # Retorna una lista de los nombres de los trabajadores
    nombres_trabajadores = []
    for _ in range(num): 
        nombre = random.choice(nombres)    
        apellido = random.choice(apellidos)
        nombre_trabajador = f"{nombre} {apellido}"  
        nombres_trabajadores.append(nombre_trabajador)
    return nombres_trabajadores

# Generador de correos
def generador_correos(nombres_a_usar):
    # Retorna una lista de los correos de los trabajadores
    correos_trabajadores = []
    for i in nombres_a_usar:
        nombre = i.replace(" ", "").lower()
        correo = f"{nombre}@docker.com"
        correos_trabajadores.append(correo)
    return correos_trabajadores


# Generador de datos para Centro_de_Costo
def generar_centros_de_costos():
    # Ejecuta los comandos SQL para insertar los centros de costos
    cur.execute("ALTER SEQUENCE centro_de_costo_idCentro_de_Costo_seq RESTART WITH 1;")
    for nombre in nombres_centros:
        presupuesto = random.randint(100000, 10000000)
        cur.execute("INSERT INTO Centro_de_Costo (nombre, presupuesto) VALUES (%s, %s)", (nombre, presupuesto))
        cur.execute("SELECT * FROM Centro_de_Costo")
        centros_de_costos = cur.fetchall()
        print("Centros de Costo (ID, Nombre, Presupuesto):")
        for centro in centros_de_costos:
            print(f"ID: {centro[0]}, Nombre: {centro[1]}, Presupuesto: {centro[2]}")

# Generador de datos para Actividad
def generar_actividades():
    # Ejecuta los comandos SQL para insertar las actividades
    for nombre in nombres_actividades:
        lim_gasto = random.randint(50000, 300000)
        cur.execute("INSERT INTO Actividad (nombre, lim_gasto) VALUES (%s, %s)", (nombre, lim_gasto))

# Función para calcular el dígito verificador del RUT
def calcular_digito_verificador(rut_base):
    suma = 0
    multiplicador = 2
    for digito in reversed(str(rut_base)):
        suma += int(digito) * multiplicador
        multiplicador = 9 if multiplicador == 2 else multiplicador - 1
    resultado = 11 - (suma % 11)
    if resultado == 11:
        return "0"
    elif resultado == 10:
        return "K"
    else:
        return str(resultado)

# Generador de RUTs
def generar_rut():
    rut_base = random.randint(10000000, 99999999)  # Número base entre 8 y 9 dígitos
    digito_verificador = calcular_digito_verificador(rut_base)
    return f"{rut_base}-{digito_verificador}"


# Generador de datos para Trabajador
def generar_trabajadores(nombres_trabajadores, correos_trabajadores):
    n_trabajadores = len(nombres_trabajadores)
    n_correos_trabajadores= len(correos_trabajadores)
    for i in range(min(n_trabajadores, n_correos_trabajadores)):
        rut = generar_rut() # Generar un RUT ficticio secuencial
        nombre = nombres_trabajadores[i]
        correo = correos_trabajadores[i]
        contraseña = "1234"  # Contraseña genérica
        rol = random.choice(roles)
        centro_de_costos = random.randint(1, 5)  # Centros de costo con IDs 1, 2 o 3
        cur.execute("INSERT INTO Trabajador (rut, nombre, correo, contraseña, rol, centro_de_costos) VALUES (%s, %s, %s, %s, %s, %s)",
                    (rut, nombre, correo, contraseña, rol, centro_de_costos))

# Generador de datos para Trabajador_Actividad (relación muchos a muchos)
def generar_trabajador_actividad():
    cur.execute("SELECT rut FROM Trabajador")
    trabajadores = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT idActividad FROM Actividad")
    actividades = [row[0] for row in cur.fetchall()]
    
    for _ in range(10):  # Crear 10 relaciones
        id_trabajador = random.choice(trabajadores)
        id_actividad = random.choice(actividades)
        cur.execute("INSERT INTO Trabajador_Actividad (idTrabajador, idActividad) VALUES (%s, %s)", (id_trabajador, id_actividad))

# Generador de datos para Rendicion
def generar_rendiciones():
    cur.execute("SELECT rut FROM Trabajador")
    trabajadores = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT idActividad FROM Actividad")
    actividades = [row[0] for row in cur.fetchall()]
    
    estados = ['Pendiente', 'Por Devolver', 'Devuelta', 'Rechazada']
    
    for _ in range(random.randint(1, 100)):    # Acá se cambia la cantidad de rendiciones ya hechas
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        T_subida = random.choice(trabajadores)
        monto = random.randint(50000, 300000)
        estado = random.choice(estados)
        A_asignada = random.choice(actividades)
        descripcion = f"Descripción {random.randint(1, 100)}"
        comentario = f"Comentario {random.randint(1, 100)}"
        cur.execute("INSERT INTO Rendicion (fecha, T_subida, monto, Estado, A_asignada, Descripción, Comentario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (fecha, T_subida, monto, estado, A_asignada, descripcion, comentario))

# Generador de datos para Docs
def generar_docs():
    cur.execute("SELECT idRendicion FROM Rendicion")
    rendiciones = [row[0] for row in cur.fetchall()]
    for _ in range(10):
        nombre = f"Doc {random.randint(1, 100)}"
        archivo = f"archivo{random.randint(1, 100)}.pdf"
        rendicion = random.choice(rendiciones)
        cur.execute("INSERT INTO Docs (nombre, archivo, rendicion) VALUES (%s, %s, %s)", (nombre, archivo, rendicion))

# Ejecutar los generadores de datos
if __name__ == "__main__":
    
    borrar_datos()
    reiniciar_secuencias()
    
    nombres_trabajadores_of = generar_nombres_trabajadores(100) 
    # Acá se cambia la cantidad de trabajadores
    # Los ruts están escritos como: 12345678-{i}
    generar_rut()
    correos = generador_correos(nombres_trabajadores_of)
    generar_centros_de_costos()
    generar_actividades()
    generar_trabajadores(nombres_trabajadores_of, correos)
    generar_trabajador_actividad()
    generar_rendiciones()
    generar_docs()
 
    # Confirmar los cambios
    conn.commit()
    cur.close()
    conn.close()
    print("Datos generados exitosamente.")
