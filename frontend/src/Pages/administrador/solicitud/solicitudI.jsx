import React, { useState, useEffect } from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

export function SolicitudI({ rut }) {
    const [solicitudes, setSolicitudes] = useState([]);
    const [emplazamientoId, setEmplazamientoId] = useState(null);
    const [emplazamientos, setEmplazamientos] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    rut = localStorage.getItem("userRut");

    useEffect(() => {
        // Obtener unidades académicas disponibles
        const fetchEmplazamientos = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/usuario/${rut}/rol/ingeniero/emplazamiento`);
                setEmplazamientos(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener los emplazamientos."
                );
            }
        };

        fetchEmplazamientos();
    }, []);

    rut = localStorage.getItem("userRut");

    useEffect(() => {
        const fetchSolicitudes = async () => {
            try {

                const url = emplazamientoId
                    ? `http://localhost:8000/solicitudes/${rut}?unidad_academica_id=${emplazamientoId}`
                    : `http://localhost:8000/solicitudes/ingeniero/${rut}`;
                const response = await axios.get(url);
                setSolicitudes(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las solicitudes."
                );
            }
        };

        fetchSolicitudes();
    }, [rut, emplazamientoId]);
    

    const estados = {
        "0": "Rechazada",
        "1": "En revisión",
        "2": "Revisión de requisitos",
        "3": "Autorización de presupuesto",
        "4": "Firma de cotización",
        "5": "Orden de compra",
        "6": "Aprobada"
    };

    const estadosItem = {
        "pendiente_revision": "Pendiente de revisión",
        "aprobado": "Aprobado",
        "rechazado": "Rechazado",
        "en_revision": "En revisión",
        "pendiente_firma": "Pendiente de firma",
        "orden_compra": "Orden de compra enviada"
    };

    return (
        <div>
            <h1>Solicitudes</h1>
            {error && <p style={{color: "red"}}>{error}</p>}

            <div>
                <label htmlFor="unidadAcademica">Filtrar por Unidad Académica:</label>
                <select
                    id="unidadAcademica"
                    value={emplazamientoId || ""}
                    onChange={(e) => setEmplazamientoId(e.target.value || null)}
                >
                    <option value="">Todas</option>
                    {emplazamientos.map((unidad) => (
                        <option key={unidad.id} value={unidad.id}>
                            {unidad.nombre}
                        </option>
                    ))}
                </select>
            </div>

            <table border="1">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Fecha</th>
                    <th>Estado</th>
                    <th>Estado Colación</th>
                    <th>Estado Traslado</th>
                    <th>Descripción</th>
                    <th>Emplazamiento</th>
                    <th>Asignatura</th>
                    <th>Visita</th>
                    <th>Acciones</th>
                </tr>
                </thead>
                <tbody>
                {solicitudes.map((solicitud) => (
                    <tr key={solicitud.id_solicitud}>
                        <td>{solicitud.id_solicitud}</td>
                        <td>{new Date(solicitud.fecha).toLocaleDateString()}</td>
                        <td>{estados[String(solicitud.estado)] || "Desconocido"}</td>
                        <td>{solicitud.estado_colacion ? estadosItem[solicitud.estado_colacion] || solicitud.estado_colacion : "No aplica"}</td>
                        <td>{solicitud.estado_traslado ? estadosItem[solicitud.estado_traslado] || solicitud.estado_traslado : "No aplica"}</td>
                        <td>{solicitud.descripcion}</td>
                        <td>{solicitud.emplazamiento}</td>
                        <td>{solicitud.asignatura.join(" - ")}</td>
                        <td>{solicitud.visita}</td>
                        <td><a href={`/solicitudes/${solicitud.id_solicitud}`}>Ver</a></td>
                    </tr>
                ))}
                </tbody>
            </table>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
