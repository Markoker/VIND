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


def GetPorUnidad(usuario_rut, unidad_academica_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if unidad_academica_id:
        query = """
            SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, a.nombre AS asignatura, v.nombre_empresa AS visita
            FROM Solicitud s
            INNER JOIN Asignatura a ON s.asignatura_id = a.id_asignatura
            INNER JOIN Visita v ON s.visita_id = v.id_visita
            INNER JOIN Funcionario f ON s.usuario_rut = f.usuario_rut
            WHERE f.usuario_rut = %s AND f.unidad_academica_id = %s
            ORDER BY s.fecha DESC;
        """
        cur.execute(query, (usuario_rut, unidad_academica_id))
    else:
        query = """
            SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, a.nombre AS asignatura, v.nombre_empresa AS visita
            FROM Solicitud s
            INNER JOIN Asignatura a ON s.asignatura_id = a.id_asignatura
            INNER JOIN Visita v ON s.visita_id = v.id_visita
            INNER JOIN Funcionario f ON s.usuario_rut = f.usuario_rut
            WHERE f.usuario_rut = %s
            ORDER BY s.fecha DESC;
        """
        cur.execute(query, (usuario_rut,))

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