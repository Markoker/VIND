from querys.utils import get_connection


def Save(visita):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Visita (nombre_empresa, fecha, lugar, profesor_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id_visita;
        """,
        (visita["nombre_empresa"], visita["fecha"], visita["lugar"], visita["profesor_id"]),
    )
    visita_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return visita_id


def getProfesores():
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute("SELECT * FROM Profesor;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# TEMPORAL: crear un encargado 
def saveProfesor(data):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    query = "INSERT INTO Profesor (rut, nombre, email) VALUES (%s, %s, %s) RETURNING id_profesor;"
    cur.execute(query, (data["rut"], data["nombre"], data["email"]))
    id_profesor = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return id_profesor

def SaveVisitanteList(visita_id, asistentes):
    # asistentes: Lista de diccionarios con los datos de los asistentes.
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    try:
        cur = conn.cursor()
        query = """
        INSERT INTO Visitante (visita_id, nombre, rut, email)
        VALUES (%s, %s, %s, %s)
        """
        for asistente in asistentes:
            cur.execute(query, (visita_id, asistente["nombre"], asistente["rut"], asistente["email"]))

        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
