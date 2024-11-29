from ..utils import *


def Save(cotizacion):
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
            INSERT INTO Traslado (nombre_proveedor, rut_proveedor, correo_proveedor, monto, cotizacion_1, cotizacion_2, cotizacion_3)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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
            ),
        )
        traslado_id = cur.fetchone()[0]

    # Crear registro en tabla Colación si corresponde
    colacion_id = None
    if "colacion" in cotizacion:
        colacion = cotizacion["colacion"]

        # Validar monto dividido por asistentes
        if colacion["monto"] / colacion["asistentes"] > 6000:
            raise ValueError("El monto por persona en colación no puede superar los 6000.")

        cur.execute(
            """
            INSERT INTO Colacion (nombre_proveedor, rut_proveedor, correo_proveedor, monto, tipo_subvencion, cotizacion_1, cotizacion_2, cotizacion_3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
            ),
        )
        colacion_id = cur.fetchone()[0]

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
