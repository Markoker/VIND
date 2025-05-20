from querys.utils import *

def getPresupuestosPorPerfil(rut, perfil):
    print(f"RUT recibido: {rut}, perfil recibido: {perfil}")
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    
    cur = conn.cursor()

    if perfil == "funcionario":
        cur.execute("""
            SELECT ua.nombre, ua.presupuesto, ua.gasto, e.nombre
            FROM Funcionario f
            JOIN UnidadAcademica ua ON ua.id_unidad_academica = f.unidad_academica_id
            JOIN Emplazamiento e ON ua.emplazamiento_id = e.id_emplazamiento
            WHERE f.usuario_rut = %s
        """, (rut,))
    elif perfil in ["ingeniero", "director"]:
        cur.execute("""
            SELECT DISTINCT ua.nombre, ua.presupuesto, ua.gasto, e.nombre
            FROM UnidadAcademica ua
            JOIN Emplazamiento e ON ua.emplazamiento_id = e.id_emplazamiento
            WHERE e.id_emplazamiento IN (
                SELECT emplazamiento_id FROM Ingeniero WHERE usuario_rut = %s
                UNION
                SELECT emplazamiento_id FROM Director WHERE usuario_rut = %s
            )
        """, (rut, rut))
    elif perfil == "subdirector":
        cur.execute("""
            SELECT ua.nombre, ua.presupuesto, ua.gasto, e.nombre
            FROM Subdirector s
            JOIN UnidadAcademica ua ON ua.id_unidad_academica = s.unidad_academica_id
            JOIN Emplazamiento e ON ua.emplazamiento_id = e.id_emplazamiento
            WHERE s.usuario_rut = %s
        """, (rut,))
    else:
        cur.close()
        conn.close()
        raise ValueError("Perfil no reconocido")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "nombre": row[0],
            "presupuesto": row[1],
            "gasto": row[2],
            "emplazamiento": row[3]
        }
        for row in rows
    ]