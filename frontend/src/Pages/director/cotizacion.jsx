import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function DetalleCotizacion() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");
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
        <div style={{padding: "10px"}}>
            <h1>Detalle Solicitud #{detalle.id}</h1>

            <div style={{display: "flex", gap: "20px"}}>
                <div>
                    <p><strong>Fecha:</strong> {new Date(detalle.fecha).toLocaleDateString()}</p>
                    <p><strong>Estado:</strong> {detalle.str_estado}</p>
                    <p><strong>Descripción:</strong> {detalle.descripcion}</p>
                </div>

                <div>
                    <h4>Usuario</h4>
                    <p><strong>RUT:</strong> {detalle.usuario.rut}</p>
                    <p><strong>Nombre:</strong> {detalle.usuario.nombre}</p>
                </div>
            </div>

            <hr/>

            <h2>Visita</h2>
            <div style={{display: "flex", gap: "20px"}}>
                <p><strong>Empresa:</strong> {detalle.visita.empresa}</p>
                <p><strong>Fecha:</strong> {new Date(detalle.visita.fecha).toLocaleDateString()}</p>
                <p><strong>Lugar:</strong> {detalle.visita.lugar}</p>
            </div>
            <h3>Asistentes</h3>
            <a href={`http://localhost:3000/visitas/${detalle.visita.id}/asistentes`} target="_blank"
               rel="noopener noreferrer">
                Ver Asistentes
            </a>

            <hr/>

            <h2>Asignaturas</h2>
            <p>{detalle.asignaturas.join(" - ")}</p>

            <hr/>

            <h2>Información de Cotización</h2>
            <p><strong>Tipo:</strong> {detalle.cotizacion.tipo}</p>
            <p><strong>Estado:</strong> {detalle.cotizacion.estado}</p>
            <p><strong>Monto total:</strong> ${detalle.cotizacion.monto}</p>

            {detalle.cotizacion.traslado && (
                <div>
                    <h2>Traslado</h2>
                    <div style={{display: "flex", gap: "30px"}}>
                        <div>
                            <p><strong>Proveedor:</strong> {detalle.cotizacion.traslado.nombre_proveedor}</p>
                            <p><strong>Correo:</strong> {detalle.cotizacion.traslado.correo_proveedor}</p>
                        </div>
                        <div>
                            <p><strong>Monto:</strong> ${detalle.cotizacion.traslado.monto}</p>

                        </div>
                    </div>
                    <p><strong>Cotizaciones:</strong></p>
                    <ul>
                        {detalle.cotizacion.traslado.cotizaciones.map((file, i) => (
                            <li key={i}>
                                <a
                                    href={`http://localhost:8000/cotizacion/traslado/${detalle.id}/cotizacion/${i + 1}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Descargar Cotización {i + 1}
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {detalle.cotizacion.colacion && (
                <div>
                    <h2>Colación</h2>
                    <div style={{display: "flex", gap: "30px"}}>
                        <div>
                            <p><strong>Subvención:</strong> {detalle.cotizacion.colacion.tipo_subvencion}</p>
                            <p><strong>Proveedor:</strong> {detalle.cotizacion.colacion.nombre_proveedor}</p>
                            <p><strong>Correo:</strong> {detalle.cotizacion.colacion.correo_proveedor}</p>
                        </div>
                        <div>
                            <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.monto}</p>
                        </div>
                    </div>
                    <p><strong>Cotizaciones:</strong></p>
                    <ul>
                        {detalle.cotizacion.colacion.cotizaciones.map((file, i) => (
                            <li key={i}>
                                <a
                                    href={`http://localhost:8000/cotizacion/colacion/${detalle.id}/cotizacion/${i + 1}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Descargar Cotización {i + 1}
                                </a>
                            </li>
                        ))}
                    </ul>

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

            <hr/>

            <br/>
            <button onClick={() => navigate("/director/solicitudes")}>Volver</button>
        </div>
    );
}
