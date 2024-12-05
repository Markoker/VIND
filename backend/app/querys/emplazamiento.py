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
