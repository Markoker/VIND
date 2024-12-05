from querys.utils import *


# Retorna las asignaturas
def Get(query_type="by_unidad",
        id_unidad_academica=None,
        semestre=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if id_unidad_academica:
        if semestre:
            cur.execute("""
                SELECT * FROM Asignatura WHERE departamento_id = %s AND semestre = %s ORDER BY sigla;
            """, (id_unidad_academica, semestre,))
        else:
            cur.execute("""
                SELECT * FROM Asignatura WHERE departamento_id = %s ORDER BY sigla;
            """, (id_unidad_academica,))
    else:
        pass

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def GetConParalelos(query_type="by_unidad",
                    id_unidad_academica=None,
                    semestre=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if query_type == "by_unidad":
        if id_unidad_academica and semestre:
            cur.execute("""
                SELECT nombre, ARRAY_AGG(paralelo) AS paralelos
                FROM Asignatura
                WHERE departamento_id = %s AND semestre = %s
                GROUP BY nombre;
            """, (id_unidad_academica, semestre,))
        else:
            raise ValueError("Faltan parámetros: id_unidad_academica y semestre son obligatorios.")
    else:
        raise ValueError("Tipo de consulta no válido.")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Devuelve las asignaturas con sus paralelos
    return [{"nombre": row[0], "paralelos": row[1]} for row in rows]


def Count(id_unidad_academica=None, semestre=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if id_unidad_academica and semestre:
        cur.execute("""
            SELECT COUNT(DISTINCT nombre) 
            FROM Asignatura 
            WHERE departamento_id = %s AND semestre = %s;
        """, (id_unidad_academica, semestre,))
    else:
        raise ValueError("Faltan parámetros: id_unidad_academica y semestre son obligatorios.")

    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    return count

def Save(nombre, sigla, semestre, anio, departamento_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Asignatura (nombre, sigla, semestre, anio, departamento_id) VALUES (%s, %s, %s, %s, %s) RETURNING id_asignatura;",
        (nombre, sigla, semestre, anio, departamento_id)
    )
    conn.commit()
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return new_id
