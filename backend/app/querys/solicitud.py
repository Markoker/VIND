from querys.utils import *

estados_dict_str = {
    0: "Rechazada",
    1: "En revision requisitos",
    2: "Pendiente requisitos",
    3: "Revisión presupuesto",
    4: "Pendiente firma",
    5: "Orden de compra enviada",
    6: "Aprobada",
}

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
            "estado": row[4],
            "str_estado": estados_dict_str[row[4]],
            "descripcion": row[5],
            "asignatura": row[6],
            "visita": row[7]
        }
        for row in rows
    ]

def GetAllIngeniero(emplazamientos_id=None):
    print("Procesando GetAllIngeniero con emplazamientos_id:", emplazamientos_id)
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    query = """
            SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar, e.id_emplazamiento
            FROM Solicitud s
            INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
            INNER JOIN Asignatura a ON a.id_asignatura = sa.asignatura_id
            INNER JOIN Visita v ON s.visita_id = v.id_visita
            INNER JOIN UnidadAcademica u ON a.departamento_id = u.id_unidad_academica
            INNER JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
            WHERE e.id_emplazamiento = ANY(%s)
            GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar, e.id_emplazamiento
            ORDER BY s.fecha DESC;
        """
    cur.execute(query, (emplazamientos_id,))

    rows = cur.fetchall()
    for r in rows:
        print(r)
        print()

    cur.close()
    conn.close()

    return [
        {
            "id_solicitud": row[0],
            "fecha": row[1],
            "str_estado": estados_dict_str[row[2]],
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
    cur.execute(query, (emplazamiento_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id_solicitud": row[0],
            "fecha": row[1],
            "str_estado": estados_dict_str[row[2]],
            "estado": row[2],
            "descripcion": row[3],
            "asignatura": row[4],
            "visita": row[5],
            "emplazamiento": row[6]
        }
        for row in rows
    ]

def GetPorUnidad(usuario_rut, unidad_academica_id=None, query_from="funcionario"):
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
            "str_estado": estados_dict_str[row[2]],
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

def GetPorUnidadYEmplazamiento(usuario_rut, unidad_academica_id, emplazamiento_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    query = """
        SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion,
               ARRAY_AGG(DISTINCT a.sigla) AS asignatura,
               v.lugar,
               e.nombre
        FROM Solicitud s
        INNER JOIN AsignaturaSolicitud sa ON s.id_solicitud = sa.solicitud_id
        INNER JOIN Asignatura a ON sa.asignatura_id = a.id_asignatura
        INNER JOIN UnidadAcademica u ON a.departamento_id = u.id_unidad_academica
        INNER JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
        INNER JOIN Visita v ON s.visita_id = v.id_visita
        WHERE s.usuario_rut = %s
          AND u.id_unidad_academica = %s
          AND e.id_emplazamiento = %s
        GROUP BY s.id_solicitud, s.fecha, s.estado, s.descripcion, v.lugar, e.nombre
        ORDER BY s.fecha DESC
    """

    cur.execute(query, (usuario_rut, unidad_academica_id, emplazamiento_id))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id_solicitud": row[0],
            "fecha": row[1],
            "str_estado": estados_dict_str[row[2]],
            "estado": row[2],
            "descripcion": row[3],
            "asignatura": row[4],
            "visita": row[5],
            "emplazamiento": row[6]
        }
        for row in rows
    ]

def GetDetalle(id_solicitud):
    conn = get_connection()
    cur = conn.cursor()

    # Primero obtenemos los datos base
    query = """
        SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion,
               u.rut, u.first_name, u.last_name,
               v.nombre_empresa, v.fecha, v.lugar,
               ARRAY_AGG(DISTINCT a.sigla) AS asignaturas,
               c.tipo, c.estado, c.monto, c.traslado_id, c.colacion_id, v.id_visita
        FROM Solicitud s
        INNER JOIN Usuario u ON s.usuario_rut = u.rut
        INNER JOIN Visita v ON s.visita_id = v.id_visita
        INNER JOIN AsignaturaSolicitud sa ON sa.solicitud_id = s.id_solicitud
        INNER JOIN Asignatura a ON sa.asignatura_id = a.id_asignatura
        LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
        WHERE s.id_solicitud = %s
        GROUP BY s.id_solicitud, u.rut, u.first_name, u.last_name,
                 v.id_visita, v.nombre_empresa, v.fecha, v.lugar,
                 c.tipo, c.estado, c.monto, c.traslado_id, c.colacion_id
    """
    cur.execute(query, (id_solicitud,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    detalle = {
        "id": row[0],
        "fecha": row[1],
        "str_estado": estados_dict_str[row[2]],
        "estado": row[2],
        "descripcion": row[3],
        "usuario": {
            "rut": row[4],
            "nombre": f"{row[5]} {row[6]}"
        },
        "visita": {
            "id": row[16],
            "empresa": row[7],
            "fecha": row[8],
            "lugar": row[9]
        },
        "asignaturas": row[10],
        "cotizacion": {
            "tipo": row[11],
            "estado": row[12],
            "monto": row[13],
            "traslado": None,
            "colacion": None
        }
    }

    # Si hay traslado asociado
    traslado_id = row[14]
    if traslado_id:
        cur.execute("""
            SELECT nombre_proveedor, rut_proveedor, correo_proveedor,
                   monto, cotizacion_1, cotizacion_2, cotizacion_3
            FROM Traslado WHERE id = %s
        """, (traslado_id,))
        t = cur.fetchone()

        list_cotizaciones = [t[i] for i in range(4, 7) if t[i] is not None]

        if t:
            detalle["cotizacion"]["traslado"] = {
                "nombre_proveedor": t[0],
                "rut_proveedor": t[1],
                "correo_proveedor": t[2],
                "monto": t[3],
                "cotizaciones": list_cotizaciones
            }

    # Si hay colación asociada
    colacion_id = row[15]
    if colacion_id:
        cur.execute("""
            SELECT tipo_subvencion, nombre_proveedor, rut_proveedor, correo_proveedor,
                   monto, cotizacion_1, cotizacion_2, cotizacion_3, reembolso_id
            FROM Colacion WHERE id = %s
        """, (colacion_id,))
        c = cur.fetchone()
        if c:
            list_cotizaciones = [c[i] for i in range(5, 8) if c[i] is not None]

            colacion_info = {
                "tipo_subvencion": c[0],
                "nombre_proveedor": c[1],
                "rut_proveedor": c[2],
                "correo_proveedor": c[3],
                "monto": c[4],
                "cotizaciones": list_cotizaciones
            }

            # Si es reembolso, obtener los datos del reembolso
            if c[8]:
                cur.execute("""
                    SELECT monto, fecha_pago, estado FROM Reembolso WHERE id_reembolso = %s
                """, (c[8],))
                r = cur.fetchone()
                if r:
                    colacion_info["reembolso"] = {
                        "monto": r[0],
                        "fecha_pago": r[1],
                        "estado": r[2]
                    }

            detalle["cotizacion"]["colacion"] = colacion_info

    cur.close()
    conn.close()
    return detalle

def CambiarEstado(RUT, id_solicitud, decision, comentario=""):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    estados = [
        {
            0:0,
            1:0,
            2:0,
            3:0,
            4:1,
            5:5,
            6:6,
        },
        {
            0:0,
            1:3,
            2:3,
            3:4,
            4:5,
            5:6,
            6:6
        }
    ]

    query = """
        SELECT estado FROM Solicitud WHERE id_solicitud = %s;
    """
    cur.execute(query, (id_solicitud,))
    estado_actual = cur.fetchone()[0]

    query = """
        UPDATE Solicitud
        SET estado = %s
        WHERE id_solicitud = %s;
    """

    cur.execute(query, (estados[decision][estado_actual], id_solicitud))

    query = """
        INSERT INTO HistorialEstadoSolicitud (solicitud_id, fecha_decision, estado_anterior, usuario_decision_rut, comentario, decision)
        VALUES (%s, NOW(), %s, %s, %s, %s);
    """

    cur.execute(query, (id_solicitud, estados[decision][estado_actual], RUT, comentario, decision))

    conn.commit()

    cur.close()
    conn.close()

def GetHistorial(id_solicitud):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    query = '''
    SELECT h.estado_anterior, h.decision, h.comentario, h.fecha_decision, h.usuario_decision_rut, u.first_name, u.last_name
    FROM HistorialEstadoSolicitud AS h
    JOIN Usuario AS u ON h.usuario_decision_rut = u.rut
    WHERE h.solicitud_id = %s
    ORDER BY h.fecha_decision ASC;
    '''

    cur.execute(query, (id_solicitud,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "estado": r[0],
            "estado_str": estados_dict_str[r[0]],
            "decision": r[1],
            "decision_str": "Aprobada" if r[1] else "Rechazada",
            "comentario": r[2],
            "fecha_decision": r[3],
            "rut_decididor": r[4],
            "nombre_decididor": f"{r[5]} {r[6]}"
        }
        for r in rows
    ]
