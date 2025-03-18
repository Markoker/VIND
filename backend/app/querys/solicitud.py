from querys.utils import *


def Save(data):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Solicitud (fecha, estado, descripcion, usuario_rut, visita_id, cotizacion_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_solicitud;
        """,
        (
            data["fecha"],
            data["estado"],
            data["descripcion"],
            data["usuario_rut"],
            data["visita_id"],
            data["cotizacion_id"],
        ),
    )
    solicitud_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return solicitud_id

def Get():
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    query = """
        SELECT * FROM Solicitud;
        """
    cur.execute(query)

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

def GetAllIngeniero(emplazamientos_id=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    # Emplazamientos_id es una lista de ids, obten todas las solicitudes que tengan al menos una asignatura en alguno de los emplazamientos
    query = """
        SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar, e.nombre
        FROM Solicitud s
        INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
        INNER JOIN Asignatura a ON a.id_asignatura = sa.asignatura_id
        INNER JOIN Visita v ON s.visita_id = v.id_visita
        INNER JOIN UnidadAcademica u ON a.departamento_id = u.id_unidad_academica
        INNER JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
        WHERE a.departamento_id = ANY(SELECT departamento_id FROM UnidadAcademica WHERE id_emplazamiento = ANY(%s))
        GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar, e.nombre
        ORDER BY s.fecha DESC;
    """
    cur.execute(query, (emplazamientos_id,))

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
            "visita": row[5],
            "emplazamiento": row[6]
        }
        for row in rows
    ]

def getPorEmplazamiento(emplazamiento_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    # Emplazamientos_id es una lista de ids, obten todas las solicitudes que tengan al menos una asignatura en alguno de los emplazamientos
    query = """
            SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar, e.nombre
            FROM Solicitud s
            INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
            INNER JOIN Asignatura a ON a.id_asignatura = sa.asignatura_id
            INNER JOIN Visita v ON s.visita_id = v.id_visita
            INNER JOIN UnidadAcademica u ON a.departamento_id = u.id_unidad_academica
            INNER JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
            WHERE a.departamento_id = ANY(SELECT departamento_id FROM Emplazamiento WHERE id_emplazamiento = ANY(%s))
            GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar, e.nombre
            ORDER BY s.fecha DESC;
        """
    cur.execute(query, (emplazamientos_id,))

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
            "visita": row[5],
            "emplazamiento": row[6]
        }
        for row in rows
    ]

def GetPorUnidad(usuario_rut, unidad_academica_id=None, departamento_id=None, query_from="funcionario"):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if query_from == "funcionario":
        if not unidad_academica_id:
            query = """
                SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar
                FROM Solicitud s
                INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
                INNER JOIN Asignatura a ON sa.asignatura_id = a.id_asignatura
                INNER JOIN Visita v ON s.visita_id = v.id_visita
                WHERE s.usuario_rut = %s
                GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar
                ORDER BY s.fecha DESC;
            """
            cur.execute(query, (usuario_rut,))
        else:
            query = """
                        SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar
                        FROM Solicitud s
                        INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
                        INNER JOIN Asignatura a ON sa.asignatura_id = a.id_asignatura
                        INNER JOIN Visita v ON s.visita_id = v.id_visita
                        WHERE s.usuario_rut = %s AND s.id_solicitud IN (
                            SELECT s.id_solicitud
                            FROM Solicitud s
                            INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
                            INNER JOIN Asignatura a ON sa.asignatura_id = a.id_asignatura
                            WHERE a.departamento_id = %s
                        )
                        GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar
                        ORDER BY s.fecha DESC;
                    """
            cur.execute(query, (usuario_rut, unidad_academica_id))

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

def SaveAsignatura(id_solicitud, id_asignatura):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO SolicitudAsignatura (solicitud_id, asignatura_id) VALUES (%s, %s);
        """, (id_solicitud, id_asignatura)
    )

    conn.commit()
    cur.close()
