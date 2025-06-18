from .utils import *
#from .cotizacion import actualizar_estado_item

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
        INSERT INTO Solicitud (fecha, descripcion, usuario_rut, visita_id, cotizacion_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_solicitud;
        """,
        (
            data["fecha"],
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

def GetAllEmplazamiento(emplazamientos_id=None):
    print("Procesando GetAllIngeniero con emplazamientos_id:", emplazamientos_id)
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    query = """
            SELECT s.id_solicitud, s.fecha, s.estado, s.descripcion, ARRAY_AGG(a.sigla) AS asignatura, v.lugar, e.id_emplazamiento, e.nombre
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
            "emplazamiento_id": row[6],
            "emplazamiento": row[7]
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

def GetPorUnidad(usuario_rut=None, unidad_academica_id=None, query_from="funcionario"):
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
    elif query_from == "subdireccion":
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

def get_estado_item(item_id, tipo_item):
    """
    Obtiene el estado actual de un ítem (colación o traslado)
    
    Args:
        item_id (int): ID del ítem
        tipo_item (str): Tipo de ítem ('colacion' o 'traslado')
    
    Returns:
        dict: Información del estado actual del ítem
    """
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    
    tabla = "Colacion" if tipo_item == "colacion" else "Traslado"
    query = f"""
        SELECT estado, fecha_estado
        FROM {tabla}
        WHERE id = %s
    """
    
    cur.execute(query, (item_id,))
    row = cur.fetchone()
    
    if not row:
        cur.close()
        conn.close()
        return None
        
    estado = {
        "estado": row[0],
        "fecha": row[1]
    }
    
    cur.close()
    conn.close()
    return estado

def cambiar_estado_item(item_id, tipo_item, nuevo_estado, usuario_rut):
    """
    Cambia el estado de un ítem y registra el cambio en el historial
    
    Args:
        item_id (int): ID del ítem
        tipo_item (str): Tipo de ítem ('colacion' o 'traslado')
        nuevo_estado (int): Nuevo estado a asignar
        usuario_rut (str): RUT del usuario que realiza el cambio
    
    Returns:
        bool: True si el cambio fue exitoso, False en caso contrario
    """
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    
    try:
        # Actualizar estado en la tabla principal
        tabla = "Colacion" if tipo_item == "colacion" else "Traslado"
        query = f"""
            UPDATE {tabla}
            SET estado = %s, fecha_estado = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id
        """
        
        cur.execute(query, (nuevo_estado, item_id))
        if not cur.fetchone():
            raise Exception(f"No se encontró el ítem {item_id} de tipo {tipo_item}")
            
        # Registrar en historial
        query_historial = """
            INSERT INTO HistorialEstadoItem (item_id, tipo_item, estado_anterior, estado_nuevo, usuario_rut)
            VALUES (%s, %s, (SELECT estado FROM {tabla} WHERE id = %s), %s, %s)
        """
        
        cur.execute(query_historial, (item_id, tipo_item, item_id, nuevo_estado, usuario_rut))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error al cambiar estado: {str(e)}")
        return False
        
    finally:
        cur.close()
        conn.close()

def get_historial_item(item_id, tipo_item):
    """
    Obtiene el historial de estados de un ítem
    
    Args:
        item_id (int): ID del ítem
        tipo_item (str): Tipo de ítem ('colacion' o 'traslado')
    
    Returns:
        list: Lista de cambios de estado registrados
    """
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    
    query = """
        SELECT h.fecha_cambio, h.estado_anterior, h.estado_nuevo, 
               u.first_name, u.last_name
        FROM HistorialEstadoItem h
        INNER JOIN Usuario u ON h.usuario_rut = u.rut
        WHERE h.item_id = %s AND h.tipo_item = %s
        ORDER BY h.fecha_cambio DESC
    """
    
    cur.execute(query, (item_id, tipo_item))
    rows = cur.fetchall()
    
    historial = [
        {
            "fecha": row[0],
            "estado_anterior": row[1],
            "estado_nuevo": row[2],
            "usuario": f"{row[3]} {row[4]}"
        }
        for row in rows
    ]
    
    cur.close()
    conn.close()
    return historial

def actualizar_estado_solicitud(solicitud_id):
    """
    Actualiza el estado de la solicitud basado en los estados de colación y traslado
    
    Args:
        solicitud_id (int): ID de la solicitud
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()
    
    try:
        # Obtener estados actuales
        query = """
            SELECT c.estado as estado_colacion, t.estado as estado_traslado
            FROM Solicitud s
            LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
            LEFT JOIN Colacion col ON c.colacion_id = col.id
            LEFT JOIN Traslado t ON c.traslado_id = t.id
            WHERE s.id_solicitud = %s
        """
        
        cur.execute(query, (solicitud_id,))
        row = cur.fetchone()
        
        if not row:
            raise Exception(f"No se encontró la solicitud {solicitud_id}")
            
        estado_colacion = row[0]
        estado_traslado = row[1]
        
        # Determinar estado de la solicitud
        nuevo_estado = 0  # Por defecto rechazada
        
        if estado_colacion is not None and estado_traslado is not None:
            # Si ambos están aprobados, la solicitud está aprobada
            if estado_colacion == 1 and estado_traslado == 1:
                nuevo_estado = 6  # Aprobada
            # Si alguno está pendiente, la solicitud está en revisión
            elif estado_colacion == 0 or estado_traslado == 0:
                nuevo_estado = 3  # Revisión presupuesto
            # Si alguno está rechazado, la solicitud está rechazada
            elif estado_colacion == 2 or estado_traslado == 2:
                nuevo_estado = 0  # Rechazada
                
        # Actualizar estado de la solicitud
        query_update = """
            UPDATE Solicitud
            SET estado = %s
            WHERE id_solicitud = %s
        """
        
        cur.execute(query_update, (nuevo_estado, solicitud_id))
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Error al actualizar estado de solicitud: {str(e)}")
        return False
        
    finally:
        cur.close()
        conn.close()

