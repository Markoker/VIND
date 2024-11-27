import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export function RendicionDetalles() {
    const { rendicion_id } = useParams();
    const [rendicion, setRendicion] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`http://localhost:8000/rendiciones/${rendicion_id}?rol=jefe`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                console.log("Datos recibidos:", data);
                setRendicion(data);
            })
            .catch((error) => {
                console.error("Error al cargar la rendición:", error);
            });
    }, [rendicion_id]);
    

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!rendicion) {
        return <div>Loading...</div>;
    }

    return (
        <div className="rendicion-detalles-container">
            <div className="title-container">Detalles de la Rendición</div>
            <div className="rendicion-card">
                <p><strong>ID:</strong> {rendicion.idrendicion}</p>
                <p><strong>Fecha:</strong> {new Date(rendicion.fecha).toLocaleString()}</p>
                <p><strong>Monto:</strong> ${rendicion.monto.toLocaleString()}</p>
                <p className={`estado-${rendicion.estado.toLowerCase().replace(" ", "-")}`}>
                    <strong>Estado:</strong> {rendicion.estado}
                </p>
                <p><strong>Descripción:</strong> {rendicion.descripcion}</p>
                <p><strong>Comentario:</strong> {rendicion.comentario}</p>
                <p><strong>Actividad:</strong> {rendicion.actividad_nombre}</p>
                <p><strong>Trabajador:</strong> {rendicion.trabajador_nombre}</p>
                <p><strong>Contador Resolutivo:</strong> {rendicion.contador_resolutivo || "No asignado"}</p>
                <p><strong>Contador Devolutivo:</strong> {rendicion.contador_devolutivo || "No asignado"}</p>
                <div className="documentos-respaldo">
                <p><strong>Documento(s) de respaldo:</strong></p>
                {rendicion.documentos && rendicion.documentos.length > 0 ? (
                    rendicion.documentos.map((docId) => (
                        <a
                            key={docId}
                            href={`http://localhost:8000/documentos/${docId}`}
                            target="_blank"
                            download
                        >
                            <img src="/pdf.png" alt="Documento de respaldo" className="doc-icon" />
                            Documento {docId}.pdf
                        </a>
                    ))
                ) : (
                    <p>No hay documentos disponibles para esta rendición.</p>
                )}
            </div>
            </div>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}

