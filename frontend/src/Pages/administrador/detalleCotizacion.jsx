import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function DetalleCotizacionAdmin() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const navigate = useNavigate();

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

    return (
        <div style={{padding: "20px"}}>
            <h1>Detalle de Cotización - Solicitud #{detalle.id}</h1>
            
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

            <br/>
            <button onClick={() => navigate("/administrador/solicitudes")}>Volver</button>
        </div>
    );
} 