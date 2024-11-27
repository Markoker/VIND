import React, { useState, useEffect } from "react";
import axios from "axios";

const Solicitudes = ({ rut, unidadAcademicaId }) => {
    const [solicitudes, setSolicitudes] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
    const fetchSolicitudes = async () => {
        try {
        const response = await axios.get(`http://localhost:8000/solicitudes/${rut}/${unidadAcademicaId}`);
        setSolicitudes(response.data);
        } catch (err) {
        setError(err.response?.data?.detail || "Error al obtener las solicitudes.");
        }
    };

    fetchSolicitudes();
    }, [rut, unidadAcademicaId]);
    
    return (
        <div>
        <h1>Solicitudes para la Unidad Académica {unidadAcademicaId}</h1>
        {error && <p style={{ color: "red" }}>{error}</p>}
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
                <td>{solicitud.fecha}</td>
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
};

export default Solicitudes;
