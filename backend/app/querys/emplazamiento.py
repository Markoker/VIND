from querys.utils import *


def getEmplazamientos(query_type="all"):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute("SELECT id_emplazamiento, nombre, sigla FROM Emplazamiento;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Transformar los resultados en un arreglo de objetos/diccionarios
    return [{"id": row[0], "nombre": row[1], "sigla": row[2]} for row in rows]


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

def getPresupuestosEmplazamiento(id_emplazamiento, semestre, anio):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    query = '''
        SELECT ua.id_unidad_academica, ua.nombre, p.presupuesto
        FROM UnidadAcademica ua
        JOIN Presupuesto p ON ua.id_unidad_academica = p.id_unidad_academica
        WHERE ua.emplazamiento_id = %s AND p.anio = %s AND p.semestre = %s
    '''

    cur.execute(query, (id_emplazamiento, anio, semestre,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id_unidad_academica": row[0],
            "nombre": row[1],
            "presupuesto": row[2],
        }
        for row in rows
    ]

def getPresupuestoUnidadAcademica(id_unidad_academica, semestre, anio):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    query = '''
        SELECT ua.nombre, p.presupuesto
        FROM UnidadAcademica ua
        JOIN Presupuesto p ON ua.id_unidad_academica = p.id_unidad_academica
        WHERE ua.id_unidad_academica = %s AND p.anio = %s AND p.semestre = %s
    '''

    cur.execute(query, (id_unidad_academica, anio, semestre,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
            "nombre": row[0],
            "presupuesto": row[1],
        }