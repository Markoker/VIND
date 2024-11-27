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
def getUsuarios(query_type="all", rut=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if query_type == "all":
        cur.execute("SELECT * FROM Usuario;")
        rows = cur.fetchall()
    elif query_type == "by_rut":
        cur.execute("SELECT * FROM Usuario WHERE rut = %s;", (rut,))
        rows = cur.fetchone()
    else:
        raise ValueError("Tipo de consulta no válido")

    cur.close()
    conn.close()
    return rows

# Retorna los roles de un usuario
def getRolesUsuario(rut, query_type="all", rol=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    '''
    Retorna un diccionario con los roles y un booleano que indica si el usuario tiene ese rol
    '''

    es_funcionario = False
    es_ingeniero = False
    es_director = False
    es_subdirector = False

    if query_type == "all":
        cur = conn.cursor()
        cur.execute("SELECT * FROM Funcionario WHERE usuario_rut = %s;", (rut,))
        print(cur.fetchone())
        es_funcionario = cur.fetchone() is not None

        cur.execute("SELECT * FROM Ingeniero WHERE usuario_rut = %s;", (rut,))
        es_ingeniero = cur.fetchone() is not None

        cur.execute("SELECT * FROM Director WHERE usuario_rut = %s;", (rut,))
        es_director = cur.fetchone() is not None

        cur.execute("SELECT * FROM Subdirector WHERE usuario_rut = %s;", (rut,))
        es_subdirector = cur.fetchone() is not None
        cur.close()

    elif query_type == "by_rol":
        if rol == "funcionario":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Funcionario WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        elif rol == "ingeniero":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Ingeniero WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        elif rol == "director":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Director WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        elif rol == "subdirector":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Subdirector WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        else:
            raise ValueError("Rol no válido")

        cur.close()
        conn.close()

        return flag


    conn.close()

    return {
        "funcionario": es_funcionario,
        "ingeniero": es_ingeniero,
        "director": es_director,
        "subdirector": es_subdirector
    }

def getSolicitudesPorUnidad(usuario_rut, unidad_academica_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute("""
        SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, a.nombre AS asignatura, v.nombre_empresa AS visita
        FROM Solicitud s
        INNER JOIN Asignatura a ON s.asignatura_id = a.id_asignatura
        INNER JOIN Visita v ON s.visita_id = v.id_visita
        INNER JOIN Funcionario f ON s.usuario_rut = f.usuario_rut
        WHERE f.usuario_rut = %s AND f.unidad_academica_id = %s
        ORDER BY s.fecha DESC;
    """, (usuario_rut, unidad_academica_id))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id_solicitud": row[0],
            "fecha": row[1],
            "estado": row[2],
            "descripcion": row[3],
            "asignatura": row[4],
            "visita": row[5]
        }
        for row in rows
    ]


'''
def getRendicionesParaTrabajador(trabajador_rut):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    
    cur = conn.cursor()
    cur.execute("""
        SELECT r.idRendicion, r.fecha, r.t_subida, r.monto, r.estado, 
               a.nombre AS actividad_nombre, r.descripcion, r.comentario
        FROM Rendicion r
        JOIN Actividad a ON r.a_asignada = a.idActividad
        WHERE r.t_subida = %s;
    """, (trabajador_rut,))
    
    rendiciones = cur.fetchall()
    cur.close()
    conn.close()
    return rendiciones




# Crear una nueva rendición
def createRendicion(fecha, t_subida, monto, estado, a_asignada, descripción):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Rendicion (fecha, t_subida, monto, estado, a_asignada, descripcion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING idRendicion;",
        (fecha, t_subida, monto, estado, a_asignada, descripción)
    )
    conn.commit()
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return new_id


def saveDocument(nombre, ruta, rendicion_id):
# Retorna los usuarios
def getUsuarios(query_type="all"):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Docs (nombre, archivo, rendicion) VALUES (%s, %s, %s) RETURNING idDocs;",
            (nombre, ruta, rendicion_id)
        )
        doc_id = cur.fetchone()[0]
        conn.commit()
        print(f"Documento guardado en la base de datos con ID: {doc_id}, asociado a rendicion_id: {rendicion_id}")
        return doc_id
    except Exception as e:
        conn.rollback()
        print(f"Error al guardar el documento: {e}")
        return None
    finally:
        cur.close()
        conn.close()


# Actualizar una rendición existente
def updateRendicion(idRendicion, fecha, T_asignado, monto, estado, A_asignada, Descripción):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute(
        "UPDATE Rendicion SET fecha = %s, T_asignado = %s, monto = %s, estado = %s, A_asignada = %s, Descripción = %s WHERE id = %s;",
        (fecha, T_asignado, monto, estado, A_asignada, Descripción, idRendicion)
    )
    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return updated_rows

# Eliminar una rendición
def deleteRendicion(idRendicion):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute("DELETE FROM Rendicion WHERE id = %s;", (idRendicion,))
    deleted_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return deleted_rows

# Devoluciones
def getDevoluciones():
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    
    cur = conn.cursor()
    cur.execute("""
        SELECT r.idRendicion, r.fecha, r.t_subida, r.monto, r.estado, a.nombre AS actividad_nombre, t.nombre AS trabajador_nombre, r.descripcion, t.rut
        FROM Rendicion r
        JOIN Actividad a ON r.a_asignada = a.idActividad
        JOIN Trabajador t ON r.t_subida = t.rut
        WHERE r.estado IN ('Por Devolver', 'Devuelta');
    """)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def updateRendicionEstado(idRendicion, nuevo_estado, comentario, contador_rut):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    if nuevo_estado == "Devuelta":
        # Actualiza el contador devolutivo al cambiar el estado a "Devuelta"
        cur.execute(
            "UPDATE Rendicion SET estado = %s, contador_devolutivo = %s WHERE idRendicion = %s;",
            (nuevo_estado, contador_rut, idRendicion)
        )
    else:
        # Actualiza el contador resolutivo para otros cambios de estado
        cur.execute(
            "UPDATE Rendicion SET estado = %s, comentario = %s, contador_resolutivo = %s WHERE idRendicion = %s;",
            (nuevo_estado, comentario, contador_rut, idRendicion)
        )

    updated_rows = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    return updated_rows



def direccionDocumento(documento_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    
    cur = conn.cursor()
    cur.execute("SELECT archivo FROM Docs WHERE idDocs = %s;", (documento_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return None
    
    return result[0]
'''