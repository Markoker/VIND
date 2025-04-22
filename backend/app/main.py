from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
import os

from querys.utils import *
import querys.cotizacion as Cotizacion
import querys.emplazamiento as Emplazamiento
import querys.solicitud as Solicitud
import querys.visita as Visita
import querys.usuario as Usuario
import querys.asignatura as Asignatura

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
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/visitantes")
async def guardar_visitantes_endpoint(visita_id: int, asistentes: list):
    try:
        Visita.SaveVisitanteList(visita_id, asistentes)
        return {"message": "Visitantes almacenados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al guardar asistentes: {str(e)}")



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

@solicitud_router.get("/ingeniero/{rut}")
def obtener_solicitudes_ingeniero(rut: str, emplazamiento_id: Optional[int] = None, unidad_academica_id: Optional[int] = None):
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
            solicitudes = Solicitud.GetAllIngeniero([emplazamiento_id])
        else:
            emplazamientos = Usuario.getRolEmplacements(rut, "ingeniero")
            emplazamiento_ids = [e["id"] for e in emplazamientos]
            solicitudes = Solicitud.GetAllIngeniero(emplazamiento_ids)
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@solicitud_router.get("/{id_solicitud}")
def get_solicitud_detalle(id_solicitud: int):
    try:
        return Solicitud.GetDetalle(id_solicitud)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/aprobar")
def aprobar_solicitud(id_solicitud: int, RUT: str):
    try:
        Solicitud.CambiarEstado(id_solicitud, 1)
        return {"message": "Solicitud aprobada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/aprobar")
def aprobar_solicitud(id_solicitud: int, RUT: str):
    try:
        Solicitud.CambiarEstado(RUT, id_solicitud, 1)
        return {"message": "Solicitud aprobada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@solicitud_router.post("/{id_solicitud}/{RUT}/rechazar")
def aprobar_solicitud(id_solicitud: int, RUT: str, comentario: str):
    try:
        Solicitud.CambiarEstado(RUT, id_solicitud, 0, comentario)
        return {"message": "Solicitud rechazada"}
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

app.include_router(user_router)
app.include_router(solicitud_router)
app.include_router(emplazamiento_router)
app.include_router(asignatura_router)

'''
@app.get("/rendiciones/resumen", response_model=DineroResumen)
def calcular_dinero_resumen():
    print("Endpoint /rendiciones/resumen fue llamado")
    devoluciones = getDevoluciones()
    dinero_devuelto = sum([dev[3] for dev in devoluciones if dev[4] == "Devuelta"])
    dinero_por_devolver = sum([dev[3] for dev in devoluciones if dev[4] == "Por Devolver"])

    # Crear una instancia de DineroResumen
    return DineroResumen(
        dinero_devuelto=dinero_devuelto,
        dinero_por_devolver=dinero_por_devolver
    )

# Crear rendición
@app.post("/rendiciones")
async def create_rendicion(
    t_subida: str = Form(...),
    monto: int = Form(...),
    estado: str = Form(...),
    descripcion: str = Form(...),
    a_asignada: int = Form(...),  # Asegúrate de que sea int en el frontend
    comentario: Optional[str] = Form(None)
):
    fecha = datetime.now()  # Fecha actual en el backend
    print(f"T_subida recibido: {t_subida}")  # Agregar este log
    try:
        # Crear la rendición
        new_id = createRendicion(fecha, t_subida, monto, estado, a_asignada, descripcion)
        return {"message": f"Rendición creada con ID {new_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para subir archivos
@app.post("/rendiciones/{rendicion_id}/archivos")
async def upload_files(rendicion_id: int, archivos: List[UploadFile] = File(...)):
    documento_ids = []  # Lista para almacenar los IDs de documentos
    try:
        for archivo in archivos:
            file_location = os.path.join(os.path.dirname(__file__), "uploads", archivo.filename)
            with open(file_location, "wb") as file_object:
                file_object.write(archivo.file.read())
            
            # Guardar el documento en la base de datos y obtener el ID
            doc_id = saveDocument(nombre=archivo.filename, ruta=file_location, rendicion_id=rendicion_id)
            if doc_id:
                documento_ids.append(doc_id)  # Agregar el ID a la lista
            else:
                print("Error al guardar el documento en la base de datos")
        
        return {"message": "Archivos subidos con éxito", "documento_ids": documento_ids}
    except Exception as e:
        print(f"Error al subir archivo: {e}")
        raise HTTPException(status_code=500, detail="Error al subir archivos")



# Actualizar rendición
@app.put("/rendiciones/{rendicion_id}")
def update_rendicion(rendicion_id: int, rendicion: RendicionUpdate):
    updated_rows = updateRendicion(rendicion.idRendicion, rendicion.fecha, rendicion.T_subida, rendicion.monto, rendicion.Estado, rendicion.A_asignada, rendicion.Descripción)
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail=f"Rendicion con ID {rendicion_id} no encontrada")
    return {"message": f"Rendicion con ID {rendicion_id} actualizada"}

# Borrar rendición
@app.delete("/rendiciones/{rendicion_id}")
def delete_rendicion(rendicion_id: int):
    deleted_rows = deleteRendicion(rendicion_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail=f"Rendicion con ID {rendicion_id} no encontrada")
    return {"message": f"Rendicion con ID {rendicion_id} eliminada"}

@app.get("/devoluciones/{devolucion_id}")
def get_devolucion(devolucion_id: int, rol: str = Query(...)):
    print(f"Solicitud recibida para devolución ID: {devolucion_id}, rol: {rol}")
    if rol not in ["contador", "jefe"]:
        raise HTTPException(status_code=401, detail="No tienes permisos para ver devoluciones")

    devolucion = getRendiciones(query_type="by_id", rendicion_id=devolucion_id, rol=rol)
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")

    return {
        "idRendicion": devolucion[0][0],
        "fecha": devolucion[0][1],
        "monto": devolucion[0][2],
        "estado": devolucion[0][3],
        "descripcion": devolucion[0][4],
        "trabajador_nombre": devolucion[0][7],
        "a_asignada": devolucion[0][6],
        "contador_resolutivo": devolucion[0][9] if rol == "jefe" else None
    }



@app.get("/devoluciones")
def read_devoluciones(rol: str):
    if rol != "contador":
        raise HTTPException(status_code=401, detail="No tienes permisos para ver devoluciones")
    
    devoluciones = getDevoluciones()
    
    return {"devoluciones": [
        {
            "idRendicion": devolucion[0],   # ID de la rendición
            "fecha": devolucion[1],         # Fecha de la rendición
            "t_subida": devolucion[6],      # Nombre del trabajador
            "monto": devolucion[3],         # Monto de la rendición
            "estado": devolucion[4],        # Estado de la rendición
            "a_asignada": devolucion[5],    # Nombre de la actividad
            "descripcion": devolucion[7],    # Descripción de la rendición
            "rut": devolucion[8]             # RUT del trabajador, no se muestra en la tabla
        }
        for devolucion in devoluciones
    ]}

@app.put("/rendiciones/{rendicion_id}/estado")
def update_rendicion_estado(
    rendicion_id: int,
    request: RendicionEstadoUpdate,
    contador_rut: str = Query(...)
):
    print(f"PUT Request for rendicion_id: {rendicion_id}")
    print(f"Data received: {request.dict()}")
    print(f"contador_rut: {contador_rut}")
    if request.nuevo_estado not in ["Pendiente", "Por Devolver", "Devuelta", "Rechazada"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    updated_rows = updateRendicionEstado(rendicion_id, request.nuevo_estado, request.comentario, contador_rut)

    if updated_rows == 0:
        raise HTTPException(status_code=404, detail=f"Rendicion con ID {rendicion_id} no encontrada")
    return {"message": f"Rendicion con ID {rendicion_id} actualizada a estado {request.nuevo_estado}"}

# Ver una rendicion
@app.get("/rendiciones")
def read_rendiciones(rol: str = Query(...), trabajador_rut: str = None):
    if rol == "trabajador":
        if trabajador_rut is None:
            raise HTTPException(status_code=400, detail="Falta el RUT del trabajador")
        # Obtener rendiciones solo para este trabajador
        rendiciones = getRendicionesParaTrabajador(trabajador_rut)
    elif rol in ["contador", "jefe"]:
        # Obtener todas las rendiciones o según el estado
        rendiciones = getRendiciones()
    else:
        raise HTTPException(status_code=401, detail="No tienes permisos para ver rendiciones")

    return {"rendiciones": rendiciones}

@app.get("/rendiciones/resumen", response_model=DineroResumen)
def calcular_dinero_resumen():
    print("Endpoint /rendiciones/resumen fue llamado")
    devoluciones = getDevoluciones()
    dinero_devuelto = sum([dev[3] for dev in devoluciones if dev[4] == "Devuelta"])
    dinero_por_devolver = sum([dev[3] for dev in devoluciones if dev[4] == "Por Devolver"])

    # Crear una instancia de DineroResumen
    return DineroResumen(
        dinero_devuelto=dinero_devuelto,
        dinero_por_devolver=dinero_por_devolver
    )

@app.get("/rendiciones/{rendicion_id}")
def get_rendicion(rendicion_id: int, rol: str = None):
    try:
        if rol not in ["contador", "jefe"]:
            raise HTTPException(status_code=401, detail="No tienes permisos para ver rendiciones")

        rows = getRendiciones(query_type="by_id", rendicion_id=rendicion_id, rol=rol)
        if len(rows) == 0:
            raise HTTPException(status_code=404, detail=f"Rendicion con ID {rendicion_id} no encontrada")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT idDocs FROM Docs WHERE rendicion = %s;", (rendicion_id,))
        documentos = [doc[0] for doc in cur.fetchall()]
        cur.close()
        conn.close()

        response = {
            "idrendicion": rows[0][0],
            "fecha": rows[0][1],
            "monto": rows[0][2],
            "estado": rows[0][3],
            "descripcion": rows[0][4],
            "comentario": rows[0][5],
            "actividad_nombre": rows[0][6],
            "trabajador_nombre": rows[0][7],
            "trabajador_rut": rows[0][8],
            "contador_resolutivo": rows[0][9],
            "contador_devolutivo": rows[0][10],
            "documentos": documentos  # Incluye los documentos en la respuesta
        }

        print("Respuesta para /rendiciones/{rendicion_id}:", response)
        return response
    except Exception as e:
        print("Error en get_rendicion:", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")





@app.get("/documentos/{documento_id}", response_class=FileResponse)
def descargar_documento(documento_id: int):
    # Llama a la función en utils.py para obtener la ruta del archivo
    file_path = direccionDocumento(documento_id)
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Documento no encontrado en la base de datos")
    
    # Verifica que el archivo existe en el sistema de archivos
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="El archivo no existe en el servidor")

    # Devuelve el archivo como respuesta
    return FileResponse(path=file_path, media_type='application/pdf', filename=os.path.basename(file_path))
'''
