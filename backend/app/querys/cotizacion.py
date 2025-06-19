from .utils import get_connection, registrar_historial_estado_item
from .solicitud import actualizar_estado_solicitud


def Save(cotizacion, solicitud_id=None, usuario_rut=None):
    if not cotizacion:
        return None

    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    # Crear registro en tabla Traslado si corresponde
    traslado_id = None
    if "traslado" in cotizacion:
        traslado = cotizacion["traslado"]
        cur.execute(
            """
            INSERT INTO Traslado (nombre_proveedor, rut_proveedor, correo_proveedor, monto, cotizacion_1, cotizacion_2, cotizacion_3, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                traslado["nombre_proveedor"],
                traslado["rut_proveedor"],
                traslado["correo_proveedor"],
                traslado["monto"],
                traslado.get("cotizacion_1"),
                traslado.get("cotizacion_2"),
                traslado.get("cotizacion_3"),
                "pendiente_revision"
            ),
        )
        traslado_id = cur.fetchone()[0]
        # Registrar historial si corresponde
        if solicitud_id and usuario_rut:
            registrar_historial_estado_item(solicitud_id, "traslado", traslado_id, None, "pendiente_revision", usuario_rut, "Creación de traslado")

    # Crear registro en tabla Colación si corresponde
    colacion_id = None
    if "colacion" in cotizacion:
        colacion = cotizacion["colacion"]

        # Validar monto dividido por asistentes
        if colacion["monto"] / colacion["asistentes"] > 6000:
            raise ValueError("El monto por persona en colación no puede superar los 6000.")

        cur.execute(
            """
            INSERT INTO Colacion (nombre_proveedor, rut_proveedor, correo_proveedor, monto, tipo_subvencion, cotizacion_1, cotizacion_2, cotizacion_3, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                colacion.get("nombre_proveedor"),
                colacion.get("rut_proveedor"),
                colacion.get("correo_proveedor"),
                colacion["monto"],
                colacion["tipo_subvencion"],
                colacion.get("cotizacion_1"),
                colacion.get("cotizacion_2"),
                colacion.get("cotizacion_3"),
                "pendiente_revision"
            ),
        )
        colacion_id = cur.fetchone()[0]
        # Registrar historial si corresponde
        if solicitud_id and usuario_rut:
            registrar_historial_estado_item(solicitud_id, "colacion", colacion_id, None, "pendiente_revision", usuario_rut, "Creación de colación")

    # Crear la cotización general
    cur.execute(
        """
        INSERT INTO Cotizacion (tipo, estado, monto, traslado_id, colacion_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_cotizacion;
        """,
        (
            cotizacion["tipo"],
            "Pendiente",
            cotizacion["monto"],
            traslado_id,
            colacion_id,
        ),
    )
    cotizacion_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return cotizacion_id

# Función para actualizar el estado de un ítem y registrar historial
def actualizar_estado_item(item_tipo, item_id, solicitud_id, estado_nuevo, usuario_rut, comentario=None, conn=None, cur=None):
    if conn is None or cur is None:
        raise ValueError("Se requiere una conexión y cursor externos para actualizar_estado_item.")
    try:
        # Obtener estado anterior
        cur.execute(f"SELECT estado FROM {item_tipo.capitalize()} WHERE id = %s", (item_id,))
        result = cur.fetchone()
        if result is None:
            raise Exception(f"No se encontró el ítem {item_id} de tipo {item_tipo}")
        estado_anterior = result[0]
        print(f"Actualizando estado de {item_tipo} {item_id} de {estado_anterior} a {estado_nuevo}")
        print(f"Solicitud ID: {solicitud_id}")
        print(f"Usuario RUT: {usuario_rut}")
        print(f"Comentario: {comentario}")
        # Actualizar estado
        cur.execute(f"UPDATE {item_tipo.capitalize()} SET estado = %s WHERE id = %s", (estado_nuevo, item_id))
        print(f"Estado actualizado a {estado_nuevo}")
        # Registrar historial
        registrar_historial_estado_item(solicitud_id, item_tipo, item_id, estado_anterior, estado_nuevo, usuario_rut, comentario, conn=conn, cur=cur)
        print("Estado actualizado")
        # Actualizar estado de la solicitud según los ítems
        actualizar_estado_solicitud(solicitud_id, usuario_rut, conn=conn, cur=cur)
        print("Estado de la solicitud actualizado")
    except Exception as e:
        print(f"Error al actualizar el estado de {item_tipo} {item_id}: {e}")
        raise e
