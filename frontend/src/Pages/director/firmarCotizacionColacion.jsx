import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function FirmarCotizacionColacionDirector() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [comentarioRechazo, setComentarioRechazo] = useState("");
    const [mostrarComentario, setMostrarComentario] = useState(false);
    const [cotizacionFirmada, setCotizacionFirmada] = useState(null);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

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

    const aprobarCotizacion = async () => {
        if (!cotizacionFirmada) {
            alert("Debe subir la cotización firmada antes de aprobar.");
            return;
        }
        try {
            const formData = new FormData();
            formData.append('archivo', cotizacionFirmada);
            formData.append('tipo_item', 'colacion');
            await axios.post(`http://localhost:8000/solicitudes/${id}/${rut}/firmar-cotizacion/colacion`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Cotización de colación aprobada exitosamente");
            navigate("/director/solicitudes");
        } catch (err) {
            alert("No se pudo aprobar la cotización.");
        }
    };

    const rechazarCotizacion = () => {
        setMostrarComentario(true);
    };

    const confirmarRechazo = async () => {
        if (comentarioRechazo.trim() === "") {
            alert("Debe ingresar un comentario para rechazar.");
            return;
        }

        try {
            await axios.post(`http://localhost:8000/solicitudes/${id}/${rut}/rechazar-cotizacion-colacion-director`, null, {
                params: {comentario: comentarioRechazo}
            });
            setMostrarComentario(false);
            setComentarioRechazo("");
            alert("Cotización de colación rechazada exitosamente");
            navigate("/director/solicitudes");
        } catch (err) {
            alert("No se pudo rechazar la cotización.");
        }
    };

    const descargarCotizacion = async (numeroCotizacion) => {
        try {
            const response = await axios.get(
                `http://localhost:8000/cotizacion/colacion/${detalle.cotizacion.colacion.id}/cotizacion/${numeroCotizacion}`,
                { responseType: 'blob' }
            );
            
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `cotizacion_${numeroCotizacion}_colacion_${detalle.cotizacion.colacion.id}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            alert("No se pudo descargar la cotización.");
        }
    };

    const handleFileChange = (e) => {
        setCotizacionFirmada(e.target.files[0]);
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

    return (
        <div style={{padding: "20px"}}>
            <h1>Firmar Cotización de Colación - Solicitud #{detalle.id}</h1>
            
            <div style={{marginBottom: "20px"}}>
                <h3>Información General</h3>
                <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                    <tbody>
                        <tr>
                            <td style={{padding: "10px", fontWeight: "bold"}}>ID Solicitud</td>
                            <td style={{padding: "10px"}}>{detalle.id}</td>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Fecha</td>
                            <td style={{padding: "10px"}}>{new Date(detalle.fecha).toLocaleDateString()}</td>
                        </tr>
                        <tr>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Estado</td>
                            <td style={{padding: "10px"}}>{estados[detalle.estado] || "Desconocido"}</td>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Descripción</td>
                            <td style={{padding: "10px"}}>{detalle.descripcion}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Usuario Solicitante</h3>
                <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                    <tbody>
                        <tr>
                            <td style={{padding: "10px", fontWeight: "bold"}}>RUT</td>
                            <td style={{padding: "10px"}}>{detalle.usuario.rut}</td>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Nombre</td>
                            <td style={{padding: "10px"}}>{detalle.usuario.nombre}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Visita</h3>
                <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                    <tbody>
                        <tr>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Empresa</td>
                            <td style={{padding: "10px"}}>{detalle.visita.empresa}</td>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Fecha</td>
                            <td style={{padding: "10px"}}>{new Date(detalle.visita.fecha).toLocaleDateString()}</td>
                        </tr>
                        <tr>
                            <td style={{padding: "10px", fontWeight: "bold"}}>Lugar</td>
                            <td style={{padding: "10px"}} colSpan="3">{detalle.visita.lugar}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Asignaturas</h3>
                <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                    <tbody>
                        <tr>
                            <td style={{padding: "10px"}}>{detalle.asignaturas.join(", ")}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {detalle.cotizacion && detalle.cotizacion.colacion && (
                <div style={{marginBottom: "20px"}}>
                    <h3>Cotización de Colación para Firmar</h3>
                    <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                        <tbody>
                            <tr>
                                <td style={{padding: "10px", fontWeight: "bold"}}>Proveedor</td>
                                <td style={{padding: "10px"}}>{detalle.cotizacion.colacion.nombre_proveedor}</td>
                                <td style={{padding: "10px", fontWeight: "bold"}}>RUT</td>
                                <td style={{padding: "10px"}}>{detalle.cotizacion.colacion.rut_proveedor}</td>
                            </tr>
                            <tr>
                                <td style={{padding: "10px", fontWeight: "bold"}}>Email</td>
                                <td style={{padding: "10px"}}>{detalle.cotizacion.colacion.correo_proveedor}</td>
                                <td style={{padding: "10px", fontWeight: "bold"}}>Monto</td>
                                <td style={{padding: "10px"}}>${detalle.cotizacion.colacion.monto}</td>
                            </tr>
                            <tr>
                                <td style={{padding: "10px", fontWeight: "bold"}}>Tipo Subvención</td>
                                <td style={{padding: "10px"}} colSpan="3">{detalle.cotizacion.colacion.tipo_subvencion}</td>
                            </tr>
                        </tbody>
                    </table>

                    {detalle.cotizacion.colacion.cotizaciones && detalle.cotizacion.colacion.cotizaciones.length > 0 && (
                        <div style={{marginTop: "20px"}}>
                            <h4>Cotizaciones Disponibles</h4>
                            <table border="1" style={{width: "100%", borderCollapse: "collapse"}}>
                                <thead>
                                    <tr>
                                        <th style={{padding: "10px"}}>Número</th>
                                        <th style={{padding: "10px"}}>Descripción</th>
                                        <th style={{padding: "10px"}}>Acción</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {detalle.cotizacion.colacion.cotizaciones.map((cot, index) => (
                                        <tr key={index}>
                                            <td style={{padding: "10px"}}>Cotización {index + 1}</td>
                                            <td style={{padding: "10px"}}>{cot}</td>
                                            <td style={{padding: "10px"}}>
                                                <button 
                                                    onClick={() => descargarCotizacion(index + 1)}
                                                    style={{backgroundColor: "blue", color: "white", padding: "5px 10px", border: "none", cursor: "pointer"}}
                                                >
                                                    Descargar
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}

                    <div style={{marginTop: "20px"}}>
                        <h4>Subir Cotización Firmada</h4>
                        <input 
                            type="file" 
                            accept=".pdf"
                            onChange={handleFileChange}
                            style={{marginBottom: "10px"}}
                        />
                        {cotizacionFirmada && (
                            <p style={{color: "green"}}>Archivo seleccionado: {cotizacionFirmada.name}</p>
                        )}
                    </div>
                </div>
            )}

            <div style={{display: "flex", gap: "10px", marginTop: "20px"}}>
                <button onClick={aprobarCotizacion} style={{backgroundColor: "green", color: "white", padding: "10px 20px"}}>
                    Firmar Cotización
                </button>
                <button onClick={rechazarCotizacion} style={{backgroundColor: "red", color: "white", padding: "10px 20px"}}>
                    Rechazar Cotización
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

            <br/>
            <button onClick={() => navigate("/director/solicitudes")}>Volver</button>
        </div>
    );
} 