import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

export function DetalleColacionDirector() {
    const { id } = useParams(); // id_solicitud
    const [detalle, setDetalle] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`http://localhost:8000/solicitudes/${id}`)
            .then(res => setDetalle(res.data))
            .catch(() => alert("Error al cargar detalle de colación"));
    }, [id]);

    if (!detalle) return <p>Cargando...</p>;
    if (!detalle.cotizacion?.colacion) return <p>No hay colación asociada.</p>;

    const colacion = detalle.cotizacion.colacion;

    return (
        <div style={{ padding: "20px" }}>
            <h1>Detalle de Colación - Solicitud #{detalle.id}</h1>
            <p><strong>Proveedor:</strong> {colacion.nombre_proveedor}</p>
            <p><strong>RUT:</strong> {colacion.rut_proveedor}</p>
            <p><strong>Email:</strong> {colacion.correo_proveedor}</p>
            <p><strong>Monto:</strong> ${colacion.monto}</p>
            <p><strong>Tipo Subvención:</strong> {colacion.tipo_subvencion}</p>
            {colacion.cotizaciones && (
                <ul>
                    {colacion.cotizaciones.map((c, i) => (
                        <li key={i}>
                            <a href={`http://localhost:8000/cotizacion/colacion/${detalle.id}/cotizacion/${i + 1}`} target="_blank" rel="noreferrer">
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
