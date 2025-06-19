import React, { useState, useEffect } from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

export function VerSolicitudesI({ rut }) {
    const [solicitudes, setSolicitudes] = useState([]);
    const [emplazamientoId, setEmplazamientoId] = useState(null);
    const [emplazamientos, setEmplazamientos] = useState([]);
    const [error, setError] = useState("");
    // filtro por unidad academica
    const [unidadId, setUnidadId] = useState(null);
    const [unidades, setUnidades] = useState([]);
    const navigate = useNavigate();

    rut = localStorage.getItem("userRut");

    useEffect(() => {
        // Obtener unidades académicas disponibles
        const fetchEmplazamientos = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/usuario/${rut}/rol/administrador/emplazamiento`);
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
                let url = `http://localhost:8000/solicitudes/administrador/${rut}`;
                const params = new URLSearchParams();

                if (emplazamientoId) params.append("emplazamiento_id", emplazamientoId);
                if (unidadId !== null && unidadId !== "") {
                    params.append("unidad_academica_id", unidadId);
                }                

                url += `?${params.toString()}`;

                const response = await axios.get(url);
                setSolicitudes(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las solicitudes."
                );
            }
        };

        fetchSolicitudes();
    }, [rut, emplazamientoId, unidadId]);

    useEffect(() => {
        if (!emplazamientoId) {
            setUnidades([]);
            setUnidadId(null);
            return;
        }
    
        const fetchUnidades = async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/emplazamiento/${emplazamientoId}/unidad_academica`
                );
                setUnidades(response.data);
            } catch (err) {
                setError("Error al obtener las unidades académicas.");
            }
        };
    
        fetchUnidades();
    }, [emplazamientoId]);
    
    const estados = {
        0: "Rechazada",
        1: "En revisión",
        2: "Revisión de requisitos",
        3: "Autorización de presupuesto",
        4: "Firma de cotización",
        5: "Orden de compra",
        6: "Aprobada"
    };

    return (
        <div>
            <h1>Solicitudes</h1>
            {error && <p style={{color: "red"}}>{error}</p>}

            <div>
                <label htmlFor="unidadAcademica">Filtrar por Emplazamiento:</label>
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

            <div>
                <label htmlFor="unidadAcademica">Filtrar por Unidad Académica:</label>
                <select
                    id="unidadAcademica"
                    value={unidadId || ""}
                    onChange={(e) => setUnidadId(e.target.value || null)}
                >
                    <option value="">Todas</option>
                    {unidades.map((unidad) => (
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
                    <th>Descripción</th>
                    <th>Emplazamiento</th>
                    <th>Asignatura</th>
                    <th>Visita</th>
                </tr>
                </thead>
                <tbody>
                {solicitudes.map((solicitud) => (
                    <tr key={solicitud.id_solicitud}>
                        <td>{solicitud.id_solicitud}</td>
                        <td>{new Date(solicitud.fecha).toLocaleDateString()}</td>
                        <td>{estados[Number(solicitud.estado)] || "Desconocido"}</td>
                        <td>{solicitud.descripcion}</td>
                        <td>{solicitud.emplazamiento}</td>
                        <td>{solicitud.asignatura.join(" - ")}</td>
                        <td>{solicitud.visita}</td>
                        <td><a href={`/ingeniero/solicitudes/${solicitud.id_solicitud}`}>Ver</a></td>
                    </tr>
                ))}
                </tbody>
            </table>
            <button className="volver-btn" onClick={() => navigate("/ingeniero/dashboard")}>Volver</button>
        </div>
    );
}
