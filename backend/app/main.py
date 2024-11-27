from fastapi import FastAPI, HTTPException, Form, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from utils import *
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
import os

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

#El status enta en el puerto 8000
@app.get("/")
def status():
    return {"message": "Funcionando"}

# Login
@app.post("/login")
def nuevo_login(usuario: UsuarioLogin):
    rows = login(usuario.email, usuario.password)
    print(rows)
    if len(rows) == 0:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    rut = rows[0][0]   # Asumiendo que el RUT está en la primera columna de la tabla Trabajador
    first_name = rows[0][1]
    last_name = rows[0][2]

    return {
        "message": f"Bienvenido {first_name}",
        "rut": rut
    }

# SignUp
@app.post("/signup")
def signup(usuario: UsuarioCreate):
    try:
        nuevo_usuario = createUser(
            rut = usuario.rut,
            first_name = usuario.first_name,
            last_name = usuario.last_name,
            email = usuario.email,
            password = usuario.password
        )
        return {"message": f"Usuario creado con rut {nuevo_usuario}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener emplazamientos
@app.get("/emplazamiento")
async def get_emplazamientos():
    try:
        emplazamientos = getEmplazamientos()

        if emplazamientos:
            return emplazamientos

        raise HTTPException(status_code=404, detail="Emplazamientos no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener unidades académicas por emplazamiento
@app.get("/emplazamiento/{id_emplazamiento}/unidad_academica")
async def get_unidades_academicas(id_emplazamiento : int):
    try:
        unidades_academicas = getUnidadesAcademicas(query_type="by_emplazamiento", id_emplazamiento=id_emplazamiento)

        if unidades_academicas:
            return unidades_academicas

        raise HTTPException(status_code=404, detail="Unidades académicas no encontradas.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener asignaturas por unidad académica
@app.get("/emplazamiento/{id_emplazamiento}/unidad_academica/{id_unidad_academica}/asignatura")
async def get_asignatura(id_emplazamiento : int,
                         id_unidad_academica : int):
    try:
        asignaturas = getAsignaturas(id_unidad_academica=id_unidad_academica)

        if asignaturas:
            return asignaturas

        raise HTTPException(status_code=404, detail="Asignaturas no encontradas.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.get("/solicitudes/{rut}/{unidad_academica_id}")
def obtener_solicitudes_por_unidad(rut: str, unidad_academica_id: int):
    try:
        solicitudes = getSolicitudesPorUnidad(rut, unidad_academica_id)
        if solicitudes:
            return solicitudes
        raise HTTPException(status_code=404, detail="No se encontraron solicitudes para este usuario en esta unidad académica.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Obtener usuarios
@app.get("/usuario")
async def get_usuarios():
    try:
        usuarios = getUsuarios()

        if usuarios:
            return usuarios

        raise HTTPException(status_code=404, detail="Usuarios no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.get("/usuario/{rut}")
def obtener_usuario(rut: str):
    try:
        usuario = getUsuarios(query_type="by_rut", rut=rut)
        if usuario:
            return usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.get("/usuario/{rut}/rol")
def obtener_usuario(rut: str):
    try:
        roles = getRolesUsuario(rut)
        if roles:
            return roles
        raise HTTPException(status_code=404, detail=f"Roles para el usuario con rut {rut} no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@app.get("/usuario/{rut}/rol/{rol}")
def obtener_usuario(rut: str,
                    rol: str):
    try:
        isRol = getRolesUsuario(rut, query_type="by_rol", rol=rol)

        return isRol
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

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
