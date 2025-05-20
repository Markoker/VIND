import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

export function DetalleSolicitud() {
    const { id } = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [comentarioRechazo, setComentarioRechazo] = useState("");
    const [mostrarComentario, setMostrarComentario] = useState(false);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

    const aprobarSolicitud = async () => {
        try {
            await axios.post(`http://localhost:8000/solicitudes/${id}/${rut}/aprobar`);
            setDetalle({ ...detalle, estado: 3 });
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
                params: { comentario: comentarioRechazo }
            });
            setDetalle({ ...detalle, estado: 0 });
            setMostrarComentario(false);
            setComentarioRechazo("");
        } catch (err) {
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

    if (error) return <p style={{ color: "red" }}>{error}</p>;
    if (!detalle) return <p>Cargando...</p>;

    return (
        <div style={{ padding: "10px"}}>
            <h2>Detalle Solicitud #{detalle.id}</h2>

            <div style={{ display: "flex", gap: "20px" }}>
                <div>
                    <p><strong>Fecha:</strong> {new Date(detalle.fecha).toLocaleDateString()}</p>
                    <p><strong>Estado:</strong> {detalle.estado}</p>
                    <p><strong>Descripción:</strong> {detalle.descripcion}</p>
                </div>

                <div>
                    <h4>Usuario</h4>
                    <p><strong>RUT:</strong> {detalle.usuario.rut}</p>
                    <p><strong>Nombre:</strong> {detalle.usuario.nombre}</p>
                </div>
            </div>

            <hr />

            <h4>Visita</h4>
            <div style={{ display: "flex", gap: "20px" }}>
                <p><strong>Empresa:</strong> {detalle.visita.empresa}</p>
                <p><strong>Fecha:</strong> {new Date(detalle.visita.fecha).toLocaleDateString()}</p>
                <p><strong>Lugar:</strong> {detalle.visita.lugar}</p>
            </div>

            <hr />

            <h4>Asignaturas</h4>
            <p>{detalle.asignaturas.join(" - ")}</p>

            <hr />

            <h4>Información de Cotización</h4>
            <p><strong>Tipo:</strong> {detalle.cotizacion.tipo}</p>
            <p><strong>Estado:</strong> {detalle.cotizacion.estado}</p>
            <p><strong>Monto total:</strong> ${detalle.cotizacion.monto}</p>

            {detalle.cotizacion.colacion && (
                <div>
                    <h5>Colación</h5>
                    <div style={{ display: "flex", gap: "30px" }}>
                        <div>
                            <p><strong>Subvención:</strong> {detalle.cotizacion.colacion.tipo_subvencion}</p>
                            <p><strong>Proveedor:</strong> {detalle.cotizacion.colacion.nombre_proveedor}</p>
                            <p><strong>Correo:</strong> {detalle.cotizacion.colacion.correo_proveedor}</p>
                        </div>
                        <div>
                            <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.monto}</p>
                            <p><strong>Cotizaciones:</strong></p>
                            <ul>
                                {detalle.cotizacion.colacion.cotizaciones.map((file, i) => (
                                    <li key={i}>{file}</li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {detalle.cotizacion.colacion.reembolso && (
                        <div>
                            <h6>Reembolso</h6>
                            <div style={{ display: "flex", gap: "30px" }}>
                                <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.reembolso.monto}</p>
                                <p><strong>Pago:</strong> {new Date(detalle.cotizacion.colacion.reembolso.fecha_pago).toLocaleDateString()}</p>
                                <p><strong>Estado:</strong> {detalle.cotizacion.colacion.reembolso.estado}</p>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {detalle.estado === 2 && (
                <>
                    <div style={{ display: "flex", gap: "10px" }}>
                        <button onClick={aprobarSolicitud}>Aceptar</button>
                        <button onClick={rechazarSolicitud}>Rechazar</button>
                    </div>

                    {mostrarComentario && (
                        <div style={{ marginTop: "10px" }}>
                            <label htmlFor="comentario"><strong>Motivo del rechazo:</strong></label><br />
                            <textarea
                                id="comentario"
                                rows="4"
                                cols="50"
                                value={comentarioRechazo}
                                onChange={(e) => setComentarioRechazo(e.target.value)}
                            />
                            <br />
                            <button onClick={confirmarRechazo}>Confirmar rechazo</button>
                        </div>
                    )}
                </>
            )}

            <br />
            <button onClick={() => navigate("/ingeniero/solicitudes")}>Volver</button>
        </div>
    );
}
