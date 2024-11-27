import React, { useState, useEffect } from "react";
import axios from "axios";

export function VerSolicitudes({ rut }) {
    const [solicitudes, setSolicitudes] = useState([]);
    const [unidadAcademicaId, setUnidadAcademicaId] = useState(null);
    const [unidades, setUnidades] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        // Obtener unidades académicas disponibles
        const fetchUnidades = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/unidades-academicas`);
                setUnidades(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las unidades académicas."
                );
            }
        };

        fetchUnidades();
    }, []);

    useEffect(() => {
        const fetchSolicitudes = async () => {
            try {
                const url = unidadAcademicaId
                    ? `http://localhost:8000/solicitudes/${rut}?unidad_academica_id=${unidadAcademicaId}`
                    : `http://localhost:8000/solicitudes/${rut}`;
                const response = await axios.get(url);
                setSolicitudes(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las solicitudes."
                );
            }
        };

        fetchSolicitudes();
    }, [rut, unidadAcademicaId]);

    return (
        <div>
            <h1>Solicitudes</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}

            <div>
                <label htmlFor="unidadAcademica">Filtrar por Unidad Académica:</label>
                <select
                    id="unidadAcademica"
                    value={unidadAcademicaId || ""}
                    onChange={(e) => setUnidadAcademicaId(e.target.value || null)}
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
                        <th>Asignatura</th>
                        <th>Visita</th>
                    </tr>
                </thead>
                <tbody>
                    {solicitudes.map((solicitud) => (
                        <tr key={solicitud.id_solicitud}>
                            <td>{solicitud.id_solicitud}</td>
                            <td>{new Date(solicitud.fecha).toLocaleDateString()}</td>
                            <td>{solicitud.estado}</td>
                            <td>{solicitud.descripcion}</td>
                            <td>{solicitud.asignatura}</td>
                            <td>{solicitud.visita}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
