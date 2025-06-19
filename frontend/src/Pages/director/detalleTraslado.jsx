import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

export function DetalleTrasladoDirector() {
    const { id } = useParams();
    const [detalle, setDetalle] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`http://localhost:8000/solicitudes/${id}`)
            .then(res => setDetalle(res.data))
            .catch(() => alert("Error al cargar detalle de traslado"));
    }, [id]);

    if (!detalle) return <p>Cargando...</p>;
    if (!detalle.cotizacion?.traslado) return <p>No hay traslado asociado.</p>;

    const traslado = detalle.cotizacion.traslado;

    return (
        <div style={{ padding: "20px" }}>
            <h1>Detalle de Traslado - Solicitud #{detalle.id}</h1>
            <p><strong>Proveedor:</strong> {traslado.nombre_proveedor}</p>
            <p><strong>RUT:</strong> {traslado.rut_proveedor}</p>
            <p><strong>Email:</strong> {traslado.correo_proveedor}</p>
            <p><strong>Monto:</strong> ${traslado.monto}</p>
            {traslado.cotizaciones && (
                <ul>
                    {traslado.cotizaciones.map((c, i) => (
                        <li key={i}>
                            <a href={`http://localhost:8000/cotizacion/traslado/${detalle.id}/cotizacion/${i + 1}`} target="_blank" rel="noreferrer">
                                Descargar Cotización {i + 1}
                            </a>
                        </li>
                    ))}
                </ul>
            )}
            <button onClick={() => navigate("/director/solicitudes")}>Volver</button>
        </div>
    );
}
