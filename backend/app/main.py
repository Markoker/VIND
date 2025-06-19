from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Query, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from querys.utils import *
from querys.utils import get_connection
import querys.cotizacion as Cotizacion
import querys.emplazamiento as Emplazamiento
import querys.solicitud as Solicitud
import querys.visita as Visita
import querys.usuario as Usuario
import querys.asignatura as Asignatura
import querys.presupuesto as Presupuesto
from querys.cotizacion import actualizar_estado_item
from querys.utils import obtener_historial_item
from querys.utils import registrar_historial_estado_item
from querys.solicitud import actualizar_estado_solicitud

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Clase para el signup
class UsuarioCreate(BaseModel):
    rut: str
    first_name: str
    last_name: str
    email: str
    password: str
    

# Clase para el login
class UsuarioLogin(BaseModel):
    email: str
    password: str

class CrearSolicitudRequest(BaseModel):
    descripcion: str
    usuario_rut: str
    asignatura_id: int
    visita: dict
    cotizacion: Optional[dict] = None

user_router = APIRouter(prefix="/usuario", tags=["usuario"])
solicitud_router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])
emplazamiento_router = APIRouter(prefix="/emplazamiento", tags=["emplazamiento"])
asignatura_router = APIRouter(prefix="/asignatura", tags=["asignatura"])
visita_router = APIRouter(prefix="/visita", tags=["visita"])
presupuesto_router = APIRouter(prefix="/presupuestos", tags=["presupuestos"])

@solicitud_router.post("/")
async def crear_solicitud_endpoint(data: CrearSolicitudRequest):
    try:
        # Crear visita
        visita_id = Visita.Save(data.visita)

        # Validar y crear cotización
        cotizacion_id = None
        if data.cotizacion:
            if data.cotizacion["tipo"] == "Solo colacion" and data.cotizacion["monto"] / data.cotizacion["asistentes"] > 6000:
                raise HTTPException(status_code=400, detail="El monto por persona en colación no puede superar los 6000.")
            cotizacion_id = Cotizacion.Save(data.cotizacion)

        # Crear solicitud
        solicitud_data = {
            "fecha": date.today(),
            "estado": 2,  # Estado inicial
            "descripcion": data.descripcion,
            "usuario_rut": data.usuario_rut,
            "asignatura_id": data.asignatura_id,
            "visita_id": visita_id,
            "cotizacion_id": cotizacion_id,
        }
        solicitud_id = Solicitud.Save(solicitud_data)

        return {"id_solicitud": solicitud_id, "message": "Solicitud creada exitosamente"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/visitantes")
async def guardar_visitantes_endpoint(visita_id: int, asistentes: list):
    try:
        Visita.SaveVisitanteList(visita_id, asistentes)
        return {"message": "Visitantes almacenados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al guardar asistentes: {str(e)}")

# TEMPORAL: crear un encargado de visita
@visita_router.post("/profesores")
async def create_profesor(data: dict):
    try:
        profesor_id = Visita.saveProfesor(data)
        return {"id_profesor": profesor_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presupuesto_router.get("/{rut}")
async def get_presupuestos_usuario(rut: str, perfil: str = Query(...)):
    try:
        resultados = Presupuesto.getPresupuestosPorPerfil(rut, perfil)
        if resultados:
            return resultados
        raise HTTPException(status_code=404, detail="No se encontraron presupuestos.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#El status enta en el puerto 8000
@app.get("/")
def status():
    return {"message": "Funcionando"}

# Login
@user_router.post("/login")
def nuevo_login(usuario: UsuarioLogin):
    rows = Usuario.login(usuario.email, usuario.password)
    print(rows)
    if len(rows) == 0:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    rut = rows[0][0]   # Asumiendo que el RUT está en la primera columna de la tabla Trabajador
    first_name = rows[0][2]
    last_name = rows[0][3]

    return {
        "message": f"{first_name.title()}.",
        "rut": rut
    }

# SignUp
@user_router.post("/signup")
def signup(usuario: UsuarioCreate):
    try:
        nuevo_usuario = usuario.createUser(
            rut = usuario.rut,
            first_name = usuario.first_name,
            last_name = usuario.last_name,
            email = usuario.email,
            password = usuario.password
        )
        print(nuevo_usuario)
        return {"message": f"Usuario creado con rut {nuevo_usuario}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener emplazamientos
@emplazamiento_router.get("/")
async def get_emplazamientos():
    try:
        emplazamientos = Emplazamiento.getEmplazamientos()
        if emplazamientos:
            return emplazamientos

        raise HTTPException(status_code=404, detail="Emplazamientos no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener unidades académicas por emplazamiento
@emplazamiento_router.get("/{id_emplazamiento}/unidad_academica")
async def get_unidades_academicas(id_emplazamiento: int):
    try:
        print(f"Recibiendo unidades académicas para emplazamiento: {id_emplazamiento}")
        unidades_academicas = Emplazamiento.getUnidadesAcademicas(query_type="by_emplazamiento", id_emplazamiento=id_emplazamiento)
        print("Unidades académicas encontradas:", unidades_academicas)
        if unidades_academicas:
            return [{"id": ua[0], "nombre": ua[1]} for ua in unidades_academicas]
        raise HTTPException(status_code=404, detail="Unidades académicas no encontradas.")
    except Exception as e:
        print("Error al obtener unidades académicas:", e)
        raise HTTPException(status_code=400, detail=str(e))

    
@solicitud_router.get("/")
def obtener_solicitudes():
    try:
        solicitudes = Solicitud.Get()
        if solicitudes:
            return solicitudes
        raise HTTPException(status_code=404, detail="No se encontraron solicitudes.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/funcionario/{rut}")
def obtener_solicitudes_funcionario(rut: str, unidad_academica_id: Optional[int] = None):
    try:
        solicitudes = Solicitud.GetPorUnidad(rut, unidad_academica_id, query_from="funcionario")
        if solicitudes:
            return solicitudes
        raise HTTPException(status_code=404, detail="No se encontraron solicitudes para este usuario.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/administrador/{rut}")
def obtener_solicitudes_administrador(rut: str, emplazamiento_id: Optional[int] = None, unidad_academica_id: Optional[int] = None):
    print("→ FILTROS RECIBIDOS")
    print("RUT:", rut)
    print("emplazamiento_id:", emplazamiento_id)
    print("unidad_academica_id:", unidad_academica_id)
    try:
        if unidad_academica_id:
            solicitudes = Solicitud.GetPorUnidadYEmplazamiento(
                rut,
                unidad_academica_id=unidad_academica_id,
                emplazamiento_id=emplazamiento_id
            )
        elif emplazamiento_id:
            solicitudes = Solicitud.GetAllEmplazamiento([emplazamiento_id])
        else:
            emplazamientos = Usuario.getRolEmplacements(rut, "administrador")
            emplazamiento_ids = [e["id"] for e in emplazamientos]
            solicitudes = Solicitud.GetAllEmplazamiento(emplazamiento_ids)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/subdirector/{rut}")
def obtener_solicitudes_subdirector(rut: str, emplazamiento_id: Optional[int] = None, unidad_academica_id: Optional[int] = None):
    print("→ FILTROS RECIBIDOS")
    print("RUT:", rut)
    print("emplazamiento_id:", emplazamiento_id)
    print("unidad_academica_id:", unidad_academica_id)
    try:
        if unidad_academica_id:
            solicitudes = Solicitud.GetPorUnidadYEmplazamiento(
                rut,
                unidad_academica_id=unidad_academica_id,
                emplazamiento_id=emplazamiento_id
            )
        elif emplazamiento_id:
            solicitudes = Solicitud.GetAllEmplazamiento([emplazamiento_id])
        else:
            emplazamientos = Usuario.getRolEmplacements(rut, "subdirector")
            emplazamiento_ids = [e["id"] for e in emplazamientos]
            solicitudes = Solicitud.GetAllEmplazamiento(emplazamiento_ids)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/director/{rut}")
def obtener_solicitudes_direccion(rut: str, emplazamiento_id: Optional[int] = None,
                                  unidad_academica_id: Optional[int] = None):
    print("→ FILTROS RECIBIDOS")
    print("RUT:", rut)
    print("emplazamiento_id:", emplazamiento_id)
    print("unidad_academica_id:", unidad_academica_id)
    try:
        if unidad_academica_id:
            solicitudes = Solicitud.GetPorUnidadYEmplazamiento(
                rut,
                unidad_academica_id=unidad_academica_id,
                emplazamiento_id=emplazamiento_id
            )
        elif emplazamiento_id:
            solicitudes = Solicitud.GetAllEmplazamiento([emplazamiento_id])
        else:
            emplazamientos = Usuario.getRolEmplacements(rut, "director")
            emplazamiento_ids = [e["id"] for e in emplazamientos]
            solicitudes = Solicitud.GetAllEmplazamiento(emplazamiento_ids)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/{id_solicitud}")
def get_solicitud_detalle(id_solicitud: int):
    try:
        return Solicitud.GetDetalle(id_solicitud)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/")
def aprobar_solicitud(id_solicitud: int, RUT: str):
    try:
        Solicitud.CambiarEstado(RUT, id_solicitud, 1)
        return {"message": "Solicitud aprobada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/rechazar")
def rechazar_solicitud(id_solicitud: int, RUT: str, comentario: str):
    try:
        Solicitud.CambiarEstado(RUT, id_solicitud, 0, comentario)
        return {"message": "Solicitud rechazada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/aprobar-requisitos")
def aprobar_requisitos_solicitud(id_solicitud: int, RUT: str):
    try:
        Solicitud.CambiarEstado(RUT, id_solicitud, 3)
        return {"message": "Requisitos aprobados, solicitud en espera de firma de cotización"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/firmar-cotizacion/{tipo_item}")
async def firmar_cotizacion(id_solicitud: int, RUT: str, tipo_item: str, archivo: UploadFile = File(...)):
    import os
    from querys.utils import registrar_historial_estado_item
    from querys.solicitud import actualizar_estado_solicitud
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    cur = conn.cursor()
    try:
        # 1. Obtener el ID del ítem
        if tipo_item not in ["colacion", "traslado"]:
            raise HTTPException(status_code=400, detail="tipo_item debe ser 'colacion' o 'traslado'")
        if tipo_item == "colacion":
            cur.execute("""
                SELECT c.colacion_id
                FROM Solicitud s
                LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
                WHERE s.id_solicitud = %s
            """, (id_solicitud,))
        else:
            cur.execute("""
                SELECT c.traslado_id
                FROM Solicitud s
                LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
                WHERE s.id_solicitud = %s
            """, (id_solicitud,))
            
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail=f"No se encontró {tipo_item} para esta solicitud")
        item_id = result[0]

        # 2. Guardar el archivo PDF
        ruta_archivo = f"uploads/{tipo_item}/cotizacion_firmada_{item_id}.pdf"
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        with open(ruta_archivo, "wb") as f:
            contenido = await archivo.read()
            f.write(contenido)
        # 3. Actualizar el estado del ítem
        cur.execute(f"UPDATE {tipo_item.capitalize()} SET estado = %s WHERE id = %s", ("esperando_factura", item_id))
        # 4. Commit y verificación
        conn.commit()
        cur.execute(f"SELECT estado FROM {tipo_item.capitalize()} WHERE id = %s", (item_id,))
        estado = cur.fetchone()
        if not estado or estado[0] != "esperando_factura":
            return {"error": "Fallo en update directo", "estado": estado}

        # 5. Agregar historial
        registrar_historial_estado_item(id_solicitud, tipo_item, item_id, "pendiente_firma", "esperando_factura", RUT, "Cotización firmada por director", conn=conn, cur=cur)
        conn.commit()

        # 6. Actualizar estado de la solicitud
        actualizar_estado_solicitud(id_solicitud, RUT, conn=conn, cur=cur)
        conn.commit()
        
        return {"message": f"Cotización de {tipo_item} firmada exitosamente", "estado": estado}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@solicitud_router.post("/{id_solicitud}/{RUT}/rechazar-cotizacion-colacion-director")
def rechazar_cotizacion_colacion_director(id_solicitud: int, RUT: str, comentario: str):
    try:
        # Obtener el ID de colación de la solicitud
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cur = conn.cursor()
        cur.execute("""
            SELECT c.colacion_id
            FROM Solicitud s
            LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
            WHERE s.id_solicitud = %s
        """, (id_solicitud,))
        
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No se encontró colación para esta solicitud")
        
        colacion_id = result[0]
        cur.close()
        conn.close()
        
        from querys.cotizacion import actualizar_estado_item
        actualizar_estado_item("colacion", colacion_id, id_solicitud, "en_revision", RUT, comentario)
        return {"message": "Cotización de colación rechazada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/aprobar-cotizacion-traslado-director")
async def aprobar_cotizacion_traslado_director(id_solicitud: int, RUT: str, archivo: UploadFile = File(...)):
    try:
        # Obtener el ID de traslado de la solicitud
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cur = conn.cursor()
        cur.execute("""
            SELECT c.traslado_id
            FROM Solicitud s
            LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
            WHERE s.id_solicitud = %s
        """, (id_solicitud,))
        
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No se encontró traslado para esta solicitud")
        
        traslado_id = result[0]
        cur.close()
        conn.close()
        
        # Primero guardar la cotización firmada
        await guardar_cotizacion_firmada("traslado", traslado_id, archivo)
        
        # Luego cambiar el estado del ítem
        from querys.cotizacion import actualizar_estado_item
        actualizar_estado_item("traslado", traslado_id, id_solicitud, "esperando_factura", RUT, "Cotización firmada por director")
        
        return {"message": "Cotización de traslado aprobada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/rechazar-cotizacion-traslado-director")
def rechazar_cotizacion_traslado_director(id_solicitud: int, RUT: str, comentario: str):
    try:
        # Obtener el ID de traslado de la solicitud
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
        
        cur = conn.cursor()
        cur.execute("""
            SELECT c.traslado_id
            FROM Solicitud s
            LEFT JOIN Cotizacion c ON s.cotizacion_id = c.id_cotizacion
            WHERE s.id_solicitud = %s
        """, (id_solicitud,))
        
        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="No se encontró traslado para esta solicitud")
        
        traslado_id = result[0]
        cur.close()
        conn.close()
        
        from querys.cotizacion import actualizar_estado_item
        actualizar_estado_item("traslado", traslado_id, id_solicitud, "en_revision", RUT, comentario)
        return {"message": "Cotización de traslado rechazada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/unidades-academicas")
def obtener_unidades_academicas():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")

    cur = conn.cursor()
    try:
        cur.execute("SELECT id_unidad_academica, nombre FROM UnidadAcademica ORDER BY nombre;")
        rows = cur.fetchall()
        return [{"id": row[0], "nombre": row[1]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()




# Obtener usuarios
@user_router.get("/")
async def get_usuarios():
    try:
        usuarios = Usuario.getUsuarios()

        if usuarios:
            return usuarios

        raise HTTPException(status_code=404, detail="Usuarios no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.get("/{rut}")
def obtener_usuario(rut: str):
    try:
        usuario = Usuario.getUsuarios(query_type="by_rut", rut=rut)
        if usuario:
            return usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@user_router.get("/{rut}/rol")
def obtener_roles_usuario(rut: str):
    try:
        roles = Usuario.getRolesUsuario(rut)
        if roles:
            return roles
        raise HTTPException(status_code=404, detail=f"Roles para el usuario con rut {rut} no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@user_router.get("/{rut}/rol/{rol}")
def obtener_rol_usuario(rut: str,
                    rol: str):
    try:
        isRol = Usuario.getRolesUsuario(rut, query_type="by_rol", rol=rol)

        return isRol
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@user_router.get("/{rut}/rol/{rol}/emplazamiento")
def obtener_emplazamientos_por_rol(rut: str, rol: str):
    try:
        rows = Usuario.getRolEmplacements(rut, rol)

        if not rows:
            raise HTTPException(status_code=404,
                                detail=f"No se encontraron emplazamientos para el usuario {rut} con rol {rol}")

        return rows
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@user_router.get("/{rut}/rol/{rol}/unidad-academica")
def obtener_unidades_por_rol(rut: str, rol: str):
    try:
        rows = Usuario.getRolDeptos(rut, rol)

        if not rows:
            raise HTTPException(status_code=404,
                                detail=f"No se encontraron emplazamientos para el usuario {rut} con rol {rol}")

        return rows
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@user_router.get("/{rut}/rol/{rol}/emplazamiento/{emplazamiento_id}/unidad-academica")
def obtener_unidades_por_rol_y_emplazamiento(rut: str, rol: str, emplazamiento_id: int):
    try:
        rows = Usuario.getRolDeptos(rut, rol, emplazamiento_id)

        if not rows:
            raise HTTPException(status_code=404,
                                detail=f"No se encontraron emplazamientos para el usuario {rut} con rol {rol}")

        return rows
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@asignatura_router.get("/")
def obtener_asignaturas(unidad_academica: int, semestre: int):
    try:
        print(f"Unidad Académica: {unidad_academica}, Semestre: {semestre}")
        rows = Asignatura.Get(query_type="by_unidad", id_unidad_academica=unidad_academica, semestre=semestre)
        print("Resultados obtenidos:", rows)

        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron asignaturas.")

        return [{"id": row[0], "nombre": row[2]} for row in rows]
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@asignatura_router.get("/paralelo")
def obtener_asignaturas_paralelos(unidad_academica: int, semestre: int):
    try:
        print(f"Recibiendo unidad_academica={unidad_academica}, semestre={semestre}")
        if semestre not in [1, 2]:
            raise HTTPException(status_code=400, detail="Semestre no válido.")

        asignaturas = Asignatura.GetConParalelos(
            query_type="by_unidad",
            id_unidad_academica=unidad_academica,
            semestre=semestre,
        )

        if not asignaturas:
            raise HTTPException(status_code=404, detail="No se encontraron asignaturas.")

        print(f"Asignaturas encontradas para unidad_academica={unidad_academica}, semestre={semestre}: {asignaturas}")
        return asignaturas
    except Exception as e:
        print(f"Error en obtener_asignaturas_paralelos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@asignatura_router.get("/max")
def obtener_max_asignaturas(unidad_academica: int, semestre: int):
    try:
        max_asignaturas = Asignatura.Count(id_unidad_academica=unidad_academica, semestre=semestre)
        return {"total_asignaturas": max_asignaturas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener asignaturas por unidad académica
@emplazamiento_router.get("/{id_emplazamiento}/unidad_academica/{id_unidad_academica}/asignatura")
async def get_asignatura(id_emplazamiento: int,
                         id_unidad_academica: int):
    try:
        asignaturas = Asignatura.Get(id_unidad_academica=id_unidad_academica)

        if asignaturas:
            return asignaturas

        raise HTTPException(status_code=404, detail="Asignaturas no encontradas.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# Obtener los profesores
@visita_router.get("/profesores")
async def get_profesores():
    try:
        profesores = Visita.getProfesores()

        if profesores:
            return profesores

        raise HTTPException(status_code=404, detail="Profesores no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.post("/cotizacion/{tipo}/{id}/archivo/{cotizacion_n}")
async def guardar_archivo_cotizacion(
    tipo: str,
    id: int,
    cotizacion_n: int,
    archivo: UploadFile = File(...)
):
    """
    Guarda un archivo PDF de cotización en la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    :param archivo: Archivo PDF a guardar.
    :param cotizacion_n: Especifica a cual de las tres cotizaciones corresponde.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    # Verificar que el archivo sea un PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    if cotizacion_n > 3 or cotizacion_n < 1:
        raise HTTPException(status_code=400, detail="El número de cotización debe estar entre 1 y 3.")

    # Guardar el archivo en el sistema de archivos
    str_cotizacion_n = f"cotizacion_{cotizacion_n}"

    ruta_archivo = f"uploads/{tipo}/{str_cotizacion_n}_{id}.pdf"
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "wb") as f:
        f.write(archivo.file.read())

    # Actualizar la base de datos
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("UPDATE Traslado SET %s = %s WHERE id = %s;", (str_cotizacion_n, ruta_archivo, id))
        elif tipo == "colacion":
            cur.execute("UPDATE Colacion SET %s = %s WHERE id = %s;", (str_cotizacion_n, ruta_archivo, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"message": "Archivo guardado exitosamente.", "ruta_archivo": ruta_archivo}

@app.post("/cotizacion/{tipo}/{id}/cotizacion-firmada")
async def guardar_cotizacion_firmada(
    tipo: str,
    id: int,
    archivo: UploadFile = File(...)
):
    """
    Guarda un archivo PDF de cotización firmada en la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    :param archivo: Archivo PDF firmado a guardar.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    # Verificar que el archivo sea un PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    # Guardar el archivo en el sistema de archivos
    ruta_archivo = f"uploads/{tipo}/cotizacion_firmada_{id}.pdf"
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "wb") as f:
        f.write(archivo.file.read())

    print(f"Archivo guardado en {ruta_archivo}")

    # Actualizar la base de datos
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("UPDATE Traslado SET cotizacion_firmada = %s WHERE id = %s;", (ruta_archivo, id))
        elif tipo == "colacion":
            cur.execute("UPDATE Colacion SET cotizacion_firmada = %s WHERE id = %s;", (ruta_archivo, id))
        conn.commit()
        print(f"Cotización firmada guardada en {ruta_archivo}")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"message": "Cotización firmada guardada exitosamente.", "ruta_archivo": ruta_archivo}

@app.post("/cotizacion/{tipo}/{id}/factura")
async def guardar_factura(
    tipo: str,
    id: int,
    archivo: UploadFile = File(...)
):
    """
    Guarda un archivo PDF de factura en la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    :param archivo: Archivo PDF de factura a guardar.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    # Verificar que el archivo sea un PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    # Guardar el archivo en el sistema de archivos
    ruta_archivo = f"uploads/{tipo}/factura_{id}.pdf"
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "wb") as f:
        f.write(archivo.file.read())

    # Actualizar la base de datos
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("UPDATE Traslado SET factura = %s WHERE id = %s;", (ruta_archivo, id))
        elif tipo == "colacion":
            cur.execute("UPDATE Colacion SET factura = %s WHERE id = %s;", (ruta_archivo, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"message": "Factura guardada exitosamente.", "ruta_archivo": ruta_archivo}

@app.post("/cotizacion/{tipo}/{id}/factura-firmada")
async def guardar_factura_firmada(
    tipo: str,
    id: int,
    archivo: UploadFile = File(...)
):
    """
    Guarda un archivo PDF de factura firmada en la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    :param archivo: Archivo PDF de factura firmada a guardar.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    # Verificar que el archivo sea un PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    # Guardar el archivo en el sistema de archivos
    ruta_archivo = f"uploads/{tipo}/factura_firmada_{id}.pdf"
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "wb") as f:
        f.write(archivo.file.read())

    # Actualizar la base de datos
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("UPDATE Traslado SET factura_firmada = %s WHERE id = %s;", (ruta_archivo, id))
        elif tipo == "colacion":
            cur.execute("UPDATE Colacion SET factura_firmada = %s WHERE id = %s;", (ruta_archivo, id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"message": "Factura firmada guardada exitosamente.", "ruta_archivo": ruta_archivo}

@solicitud_router.put("/{id_solicitud}/{item_tipo}/{item_id}/estado")
def cambiar_estado_item(id_solicitud: int, item_tipo: str, item_id: int, estado_nuevo: str = Body(...), usuario_rut: str = Body(...), comentario: str = Body(None)):
    """
    Cambia el estado de un ítem (colacion o traslado) y registra el historial.
    """
    if item_tipo not in ["colacion", "traslado"]:
        raise HTTPException(status_code=400, detail="Tipo de ítem no válido.")
    try:
        actualizar_estado_item(item_tipo, item_id, id_solicitud, estado_nuevo, usuario_rut, comentario)
        return {"message": f"Estado de {item_tipo} actualizado a {estado_nuevo}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.get("/{id_solicitud}/{item_tipo}/{item_id}/historial")
def historial_estado_item(id_solicitud: int, item_tipo: str, item_id: int):
    """
    Devuelve el historial de cambios de estado de un ítem (colacion o traslado).
    """
    if item_tipo not in ["colacion", "traslado"]:
        raise HTTPException(status_code=400, detail="Tipo de ítem no válido.")
    try:
        historial = obtener_historial_item(item_tipo, item_id)
        return {"historial": historial}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cotizacion/{tipo}/{id}/cotizacion/{cotizacion_n}", response_class=FileResponse)
async def descargar_archivo_cotizacion(tipo: str, id: int, cotizacion_n: int):
    """
    Descarga un archivo PDF de cotización desde la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    :param cotizacion_n: Especifica cuál de las tres cotizaciones descargar.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    if cotizacion_n > 3 or cotizacion_n < 1:
        raise HTTPException(status_code=400, detail="El número de cotización debe estar entre 1 y 3.")

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    str_cotizacion_n = f"cotizacion_{cotizacion_n}"

    try:
        if tipo == "traslado":
            cur.execute(f"SELECT {str_cotizacion_n} FROM Traslado WHERE id = %s;", (id,))
        elif tipo == "colacion":
            cur.execute(f"SELECT {str_cotizacion_n} FROM Colacion WHERE id = %s;", (id,))

        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Archivo no encontrado.")

        ruta_archivo = result[0]
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="El archivo no existe en el servidor.")

        return FileResponse(
            path=ruta_archivo,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={os.path.basename(ruta_archivo)}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

@app.get("/cotizacion/{tipo}/{id}/cotizacion-firmada", response_class=FileResponse)
async def descargar_cotizacion_firmada(tipo: str, id: int):
    """
    Descarga un archivo PDF de cotización firmada desde la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("SELECT cotizacion_firmada FROM Traslado WHERE id = %s;", (id,))
        elif tipo == "colacion":
            cur.execute("SELECT cotizacion_firmada FROM Colacion WHERE id = %s;", (id,))

        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Archivo no encontrado.")

        ruta_archivo = result[0]
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="El archivo no existe en el servidor.")

        return FileResponse(
            path=ruta_archivo,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={os.path.basename(ruta_archivo)}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

@app.get("/cotizacion/{tipo}/{id}/factura", response_class=FileResponse)
async def descargar_factura(tipo: str, id: int):
    """
    Descarga un archivo PDF de factura desde la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("SELECT factura FROM Traslado WHERE id = %s;", (id,))
        elif tipo == "colacion":
            cur.execute("SELECT factura FROM Colacion WHERE id = %s;", (id,))

        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Archivo no encontrado.")

        ruta_archivo = result[0]
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="El archivo no existe en el servidor.")

        return FileResponse(
            path=ruta_archivo,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={os.path.basename(ruta_archivo)}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

@app.get("/cotizacion/{tipo}/{id}/factura-firmada", response_class=FileResponse)
async def descargar_factura_firmada(tipo: str, id: int):
    """
    Descarga un archivo PDF de factura firmada desde la tabla Traslado o Colacion.
    :param tipo: 'traslado' o 'colacion'.
    :param id: ID del registro en la tabla correspondiente.
    """
    if tipo not in ["traslado", "colacion"]:
        raise HTTPException(status_code=400, detail="Tipo no válido. Debe ser 'traslado' o 'colacion'.")

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
    cur = conn.cursor()

    try:
        if tipo == "traslado":
            cur.execute("SELECT factura_firmada FROM Traslado WHERE id = %s;", (id,))
        elif tipo == "colacion":
            cur.execute("SELECT factura_firmada FROM Colacion WHERE id = %s;", (id,))

        result = cur.fetchone()
        if not result or not result[0]:
            raise HTTPException(status_code=404, detail="Archivo no encontrado.")

        ruta_archivo = result[0]
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="El archivo no existe en el servidor.")

        return FileResponse(
            path=ruta_archivo,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={os.path.basename(ruta_archivo)}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el archivo: {str(e)}")
    finally:
        cur.close()
        conn.close()

app.include_router(user_router)
app.include_router(solicitud_router)
app.include_router(emplazamiento_router)
app.include_router(asignatura_router)
app.include_router(visita_router)
app.include_router(presupuesto_router)
