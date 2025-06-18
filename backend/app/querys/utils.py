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

# Funciones para registrar y consultar historial de estado de ítems (colacion/traslado)
def registrar_historial_estado_item(solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_decision_rut, comentario=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO HistorialEstadoItem (solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_decision_rut, comentario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_decision_rut, comentario)
    )
    conn.commit()
    cur.close()
    conn.close()

def obtener_historial_item(item_tipo, item_id):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()
    cur.execute(
        """
        SELECT estado_anterior, estado_nuevo, usuario_decision_rut, comentario, fecha_decision
        FROM HistorialEstadoItem
        WHERE item_tipo = %s AND item_id = %s
        ORDER BY fecha_decision ASC
        """,
        (item_tipo, item_id)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "estado_anterior": r[0],
            "estado_nuevo": r[1],
            "usuario_decision_rut": r[2],
            "comentario": r[3],
            "fecha_decision": r[4]
        }
        for r in rows
    ]