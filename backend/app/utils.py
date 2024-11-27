import os
import psycopg2
from hashlib import sha256

# Función para obtener la conexión a la base de datos
def get_connection():
    # Establece la conexión a la base de datos y retorna el objeto de conexión
    try:
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME', 'proyecto_db'),
            user=os.getenv('DB_USER', 'ayds123'),
            password=os.getenv('DB_PASS', 'ayds123'),
            host=os.getenv('DB_HOST', 'db'),               # Asegúrate de que la contraseña sea la misma que en docker-compose.yml        
            port=os.getenv('DB_PORT', '5432')              # Este "db" debe coincidir con el nombre del servicio en docker-compose.yml
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None

# Inicio de Sesión
def login(correo, contraseña):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()

    contraseña = sha256(contraseña.encode()).hexdigest()
    cur.execute("SELECT * FROM Usuario WHERE email = %s AND password = %s;", (correo, contraseña))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Creación de Usuario
def createUser(rut, first_name, last_name, email, password):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos") 
    cur = conn.cursor()

    password = sha256(password.encode()).hexdigest()
    cur.execute(
        "INSERT INTO Usuario (rut, email, first_name, last_name, password) VALUES (%s, %s, %s, %s, %s) RETURNING rut;",
        (rut,email, first_name, last_name, password)
    )

    conn.commit()
    new_rut = cur.fetchone()[0]  # Recupera el RUT del trabajador insertado
    cur.close()
    conn.close()

    return new_rut

# Retorna los emplazamientos
def getEmplazamientos(query_type="all"):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute("SELECT * FROM Emplazamiento;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Retorna las unidades académicas
def getUnidadesAcademicas(query_type="all",
                          id_emplazamiento=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if query_type == "all":
        cur.execute("SELECT * FROM UnidadAcademica;")
    elif query_type == "by_emplazamiento":
        cur.execute("""
            SELECT * FROM UnidadAcademica WHERE emplazamiento_id = %s;
        """, (id_emplazamiento,))
    else:
        # Raise an error
        raise ValueError("Tipo de consulta no válido")

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# Retorna las asignaturas
def getAsignaturas(query_type="by_unidad",
                   id_unidad_academica=None,
                   semestre=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if id_unidad_academica:
        if semestre:
            cur.execute("""
                SELECT * FROM Asignatura WHERE departamento_id = %s AND semestre = %s;
            """, (id_unidad_academica, semestre,))
        else:
            cur.execute("""
                SELECT * FROM Asignatura WHERE departamento_id = %s;
            """, (id_unidad_academica,))
    else:
        pass

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Retorna los usuarios
def getUsuarios(query_type="all"):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute("SELECT * FROM Usuario;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows