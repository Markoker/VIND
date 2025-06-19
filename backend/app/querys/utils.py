import os
import psycopg2
from hashlib import sha256

# Función para obtener la conexión a la base de datos
def get_connection():
    # Establece la conexión a la base de datos y retorna el objeto de conexión
    try:
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME', 'vind'),
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