import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function RevisarSolicitud() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [comentarioRechazo, setComentarioRechazo] = useState("");
    const [mostrarComentario, setMostrarComentario] = useState(false);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

    const aprobarSolicitud = async () => {
        try {
            await axios.post(`http://localhost:8000/solicitudes/${id}/${rut}/aprobar-requisitos`);
            setDetalle({...detalle, estado: 3});
            alert("Solicitud aprobada exitosamente");
        } catch (err) {
            alert("No se pudo aprobar la solicitud.");
        }
    };

    const rechazarSolicitud = () => {
        setMostrarComentario(true);
    };

    const confirmarRechazo = async () => {
        if (comentarioRechazo.trim() === "") {
            alert("Debe ingresar un comentario para rechazar.");
            return;
        }

        try {
            await axios.post(`http://localhost:8000/solicitudes/${id}/${rut}/rechazar`, null, {
                params: {comentario: comentarioRechazo}
            });
            setDetalle({...detalle, estado: 0});
            setMostrarComentario(false);
            setComentarioRechazo("");
            alert("Solicitud rechazada exitosamente");
        } catch (err) {
            console.log(err);
            alert("No se pudo rechazar la solicitud.");
        }
    };

    useEffect(() => {
        const fetchDetalle = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/solicitudes/${id}`);
                setDetalle(response.data);
            } catch (err) {
                setError("No se pudo obtener el detalle de la solicitud.");
            }
        };
        fetchDetalle();
    }, [id]);

    if (error) return <p style={{color: "red"}}>{error}</p>;
    if (!detalle) return <p>Cargando...</p>;

    const estados = {
        0: "Rechazada",
        1: "En revisión",
        2: "Revisión de requisitos",
        3: "Esperando firma de cotización",
        4: "Esperando factura",
        5: "Esperando firma de factura",
        6: "Pagada"
    };

    const estadosItem = {
        "pendiente_revision": "Pendiente de revisión",
        "pagada": "Pagada",
        "rechazado": "Rechazado",
        "en_revision": "En revisión",
        "pendiente_firma": "Pendiente de firma",
        "esperando_factura": "Esperando factura",
        "esperando_firma_factura": "Esperando firma de factura"
    };

    return (
        <div style={{padding: "20px"}}>
            <h1>Revisar Solicitud #{detalle.id}</h1>
            
            <div style={{marginBottom: "20px"}}>
                <h3>Información General</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>Fecha:</strong> {new Date(detalle.fecha).toLocaleDateString()}</p>
                    <p><strong>Estado:</strong> {estados[detalle.estado] || "Desconocido"}</p>
                    <p><strong>Descripción:</strong> {detalle.descripcion}</p>
                </div>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Usuario Solicitante</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>RUT:</strong> {detalle.usuario.rut}</p>
                    <p><strong>Nombre:</strong> {detalle.usuario.nombre}</p>
                </div>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Visita</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>Empresa:</strong> {detalle.visita.empresa}</p>
                    <p><strong>Fecha:</strong> {new Date(detalle.visita.fecha).toLocaleDateString()}</p>
                    <p><strong>Lugar:</strong> {detalle.visita.lugar}</p>
                </div>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Asignaturas</h3>
                <p>{detalle.asignaturas.join(", ")}</p>
            </div>

            {detalle.cotizacion && (
                <div style={{marginBottom: "20px"}}>
                    <h3>Cotización</h3>
                    <div style={{display: "flex", gap: "30px"}}>
                        <p><strong>Tipo:</strong> {detalle.cotizacion.tipo}</p>
                        <p><strong>Estado:</strong> {detalle.cotizacion.estado}</p>
                        <p><strong>Monto Total:</strong> ${detalle.cotizacion.monto}</p>
                    </div>

                    {detalle.cotizacion.traslado && (
                        <div style={{marginTop: "10px", padding: "10px", border: "1px solid #ccc"}}>
                            <h4>Traslado</h4>
                            <div style={{display: "flex", gap: "30px"}}>
                                <p><strong>Proveedor:</strong> {detalle.cotizacion.traslado.nombre_proveedor}</p>
                                <p><strong>RUT:</strong> {detalle.cotizacion.traslado.rut_proveedor}</p>
                                <p><strong>Email:</strong> {detalle.cotizacion.traslado.correo_proveedor}</p>
                                <p><strong>Monto:</strong> ${detalle.cotizacion.traslado.monto}</p>
                            </div>
                            {detalle.cotizacion.traslado.cotizaciones.length > 0 && (
                                <div>
                                    <p><strong>Cotizaciones:</strong></p>
                                    <ul>
                                        {detalle.cotizacion.traslado.cotizaciones.map((cot, index) => (
                                            <li key={index}>{cot}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    {detalle.cotizacion.colacion && (
                        <div style={{marginTop: "10px", padding: "10px", border: "1px solid #ccc"}}>
                            <h4>Colación</h4>
                            <div style={{display: "flex", gap: "30px"}}>
                                <p><strong>Proveedor:</strong> {detalle.cotizacion.colacion.nombre_proveedor}</p>
                                <p><strong>RUT:</strong> {detalle.cotizacion.colacion.rut_proveedor}</p>
                                <p><strong>Email:</strong> {detalle.cotizacion.colacion.correo_proveedor}</p>
                                <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.monto}</p>
                                <p><strong>Tipo Subvención:</strong> {detalle.cotizacion.colacion.tipo_subvencion}</p>
                            </div>
                            {detalle.cotizacion.colacion.cotizaciones.length > 0 && (
                                <div>
                                    <p><strong>Cotizaciones:</strong></p>
                                    <ul>
                                        {detalle.cotizacion.colacion.cotizaciones.map((cot, index) => (
                                            <li key={index}>{cot}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                            {detalle.cotizacion.colacion.reembolso && (
                                <div>
                                    <h6>Reembolso</h6>
                                    <div style={{display: "flex", gap: "30px"}}>
                                        <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.reembolso.monto}</p>
                                        <p>
                                            <strong>Pago:</strong> {new Date(detalle.cotizacion.colacion.reembolso.fecha_pago).toLocaleDateString()}
                                        </p>
                                        <p><strong>Estado:</strong> {detalle.cotizacion.colacion.reembolso.estado}</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Solo mostrar botones de acción si el estado permite al administrador actuar */}
            {(detalle.estado === 2 || detalle.estado === 1) && (
                <>
                    <div style={{display: "flex", gap: "10px", marginTop: "20px"}}>
                        <button onClick={aprobarSolicitud} style={{backgroundColor: "green", color: "white", padding: "10px 20px"}}>
                            Aprobar Solicitud
                        </button>
                        <button onClick={rechazarSolicitud} style={{backgroundColor: "red", color: "white", padding: "10px 20px"}}>
                            Rechazar Solicitud
                        </button>
                    </div>

                    {mostrarComentario && (
                        <div style={{marginTop: "10px"}}>
                            <label htmlFor="comentario"><strong>Motivo del rechazo:</strong></label><br/>
                            <textarea
                                id="comentario"
                                rows="4"
                                cols="50"
                                value={comentarioRechazo}
                                onChange={(e) => setComentarioRechazo(e.target.value)}
                                style={{marginTop: "5px", width: "100%", maxWidth: "400px"}}
                            />
                            <br/>
                            <button onClick={confirmarRechazo} style={{backgroundColor: "red", color: "white", padding: "10px 20px", marginTop: "10px"}}>
                                Confirmar rechazo
                            </button>
                        </div>
                    )}
                </>
            )}

            <br/>
            <button onClick={() => navigate("/administrador/solicitudes")}>Volver</button>
        </div>
    );
} 