import React, { useState, useEffect } from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

export function VerSolicitudesF({ rut }) {
    const [solicitudes, setSolicitudes] = useState([]);
    const [unidadAcademicaId, setUnidadAcademicaId] = useState(null);
    const [unidades, setUnidades] = useState([]);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    rut = localStorage.getItem("userRut");

    useEffect(() => {
        // Obtener unidades académicas disponibles
        const fetchUnidades = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/usuario/${rut}/rol/funcionario/unidad-academica`);
                setUnidades(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las unidades académicas."
                );
            }
        };

        fetchUnidades();
    }, []);

    rut = localStorage.getItem("userRut");

    useEffect(() => {
        const fetchSolicitudes = async () => {
            try {

                const url = unidadAcademicaId
                    ? `http://localhost:8000/solicitudes/funcionario/${rut}?unidad_academica_id=${unidadAcademicaId}`
                    : `http://localhost:8000/solicitudes/funcionario/${rut}`;
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
            {error && <p style={{color: "red"}}>{error}</p>}

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
                        <td>{solicitud.asignatura.join(" - ")}</td>
                        <td>{solicitud.visita}</td>
                        <td><a href={`/funcionario/solicitudes/${solicitud.id_solicitud}`}>Ver</a></td>
                    </tr>
                ))}
                </tbody>
            </table>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
