from .utils import *


# Inicio de Sesión
def login(correo, contrasena):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()

    contrasena = sha256(contrasena.encode()).hexdigest()
    cur.execute("SELECT * FROM Usuario WHERE email = %s AND password = %s;", (correo, contrasena))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# Creación de Usuario
def createUser(rut, first_name, last_name, email, password):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")
    cur = conn.cursor()

    password = sha256(password.encode()).hexdigest()
    cur.execute(
        "INSERT INTO Usuario (rut, email, first_name, last_name, password) VALUES (%s, %s, %s, %s, %s) RETURNING rut;",
        (rut, email, first_name, last_name, password)
    )

    conn.commit()
    new_rut = cur.fetchone()[0]  # Recupera el RUT del trabajador insertado
    cur.close()
    conn.close()

    return new_rut


# Retorna los usuarios
def getUsuarios(query_type="all", rut=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if query_type == "all":
        cur.execute("SELECT * FROM Usuario;")
        rows = cur.fetchall()
    elif query_type == "by_rut":
        cur.execute("SELECT * FROM Usuario WHERE rut = %s;", (rut,))
        rows = cur.fetchone()
    else:
        raise ValueError("Tipo de consulta no válido")

    cur.close()
    conn.close()
    return rows


# Retorna los roles de un usuario
def getRolesUsuario(rut, query_type="all", rol=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    '''
    Retorna un diccionario con los roles y un booleano que indica si el usuario tiene ese rol
    '''

    es_funcionario = False
    es_administrador = False
    es_director = False

    if query_type == "all":
        cur = conn.cursor()
        cur.execute("SELECT * FROM Funcionario WHERE usuario_rut = %s;", (rut,))
        print(cur.fetchone())
        es_funcionario = cur.fetchone() is not None

        cur.execute("SELECT * FROM Administrador WHERE usuario_rut = %s;", (rut,))
        es_administrador = cur.fetchone() is not None

        cur.execute("SELECT * FROM Director WHERE usuario_rut = %s;", (rut,))
        es_director = cur.fetchone() is not None

    elif query_type == "by_rol":
        if rol == "funcionario":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Funcionario WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        elif rol == "administrador":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Administrador WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        elif rol == "director":
            cur = conn.cursor()
            cur.execute("SELECT * FROM Director WHERE usuario_rut = %s;", (rut,))
            flag = cur.fetchone() is not None
        else:
            raise ValueError("Rol no válido")

        cur.close()
        conn.close()

        return flag

    conn.close()

    return {
        "funcionario": es_funcionario,
        "director": es_director,
        "administrador": es_administrador
    }


def getRolEmplacements(rut,
                       rol):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if rol == "funcionario":
        cur.execute("""
            SELECT DISTINCT e.id_emplazamiento, e.nombre, e.sigla
            FROM Funcionario f
            JOIN UnidadAcademica u ON f.unidad_academica_id = u.id_unidad_academica
            JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
            WHERE f.usuario_rut = %s;
        """, (rut,))
    elif rol == "administrador":
        cur.execute("""
            SELECT DISTINCT e.id_emplazamiento, e.nombre, e.sigla
            FROM Administrador i
            JOIN Emplazamiento e ON i.emplazamiento_id = e.id_emplazamiento
            WHERE i.usuario_rut = %s;
        """, (rut,))
    elif rol == "director":
        cur.execute("""
            SELECT DISTINCT e.id_emplazamiento, e.nombre, e.sigla
            FROM Director d
            JOIN Emplazamiento e ON d.emplazamiento_id = e.id_emplazamiento
            WHERE d.usuario_rut = %s;
        """, (rut,))
    elif rol == "subdirector":
        cur.execute("""
            SELECT DISTINCT e.id_emplazamiento, e.nombre, e.sigla
            FROM Subdirector s
            JOIN UnidadAcademica u ON s.unidad_academica_id = u.id_unidad_academica
            JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
            WHERE s.usuario_rut = %s;
        """, (rut,))
    else:
        raise ValueError("Rol no válido")

    rows = cur.fetchall()
    cur.close()

    return [{"id": row[0], "nombre": row[1], "sigla": row[2]} for row in rows]


# Retorna los departamentos donde el usuario tiene acceso como el rol especificado
def getRolDeptos(rut, rol, id_emplazamiento=None):
    conn = get_connection()
    if conn is None:
        raise ConnectionError("No se pudo conectar a la base de datos")

    cur = conn.cursor()

    if rol == "funcionario":
        if id_emplazamiento is None:
            cur.execute("""
                            SELECT DISTINCT u.id_unidad_academica, u.nombre
                            FROM Funcionario f
                            JOIN UnidadAcademica u ON f.unidad_academica_id = u.id_unidad_academica
                            WHERE f.usuario_rut = %s;
                        """, (rut,))
        else:
            cur.execute("""
                    SELECT DISTINCT u.id_unidad_academica, u.nombre
                    FROM Funcionario f
                    JOIN UnidadAcademica u ON f.unidad_academica_id = u.id_unidad_academica
                    JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
                    WHERE f.usuario_rut = %s AND e.id_emplazamiento = %s;
                """, (rut, id_emplazamiento))
    elif rol == "subdirector":
        if id_emplazamiento is None:
            cur.execute("""
                            SELECT DISTINCT u.id_unidad_academica, u.nombre
                            FROM Subdirector f
                            JOIN UnidadAcademica u ON f.unidad_academica_id = u.id_unidad_academica
                            WHERE f.usuario_rut = %s;
                        """, (rut,))
        else:
            cur.execute("""
                    SELECT DISTINCT u.id_unidad_academica, u.nombre
                    FROM Subdirector f
                    JOIN UnidadAcademica u ON f.unidad_academica_id = u.id_unidad_academica
                    JOIN Emplazamiento e ON u.emplazamiento_id = e.id_emplazamiento
                    WHERE f.usuario_rut = %s AND e.id_emplazamiento = %s;
                """, (rut, id_emplazamiento))
    else:
        raise ValueError("Rol no válido, endpoint válido solo para funcionarios y subdirección")

    rows = cur.fetchall()
    cur.close()

    return [{"id": row[0], "nombre": row[1]} for row in rows]
