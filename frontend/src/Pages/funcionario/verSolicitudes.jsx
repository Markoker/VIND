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
                console.log(response.data);
            } catch (err) {
                setError(
                    err.response?.data?.detail || "Error al obtener las solicitudes."
                );
            }
        };

        fetchSolicitudes();
    }, [rut, unidadAcademicaId]);

    const estados = {
        0: "Rechazada",
        1: "En revisión",
        2: "Revisión de requisitos",
        3: "Esperando firma de cotización",
        4: "Esperando factura",
        5: "Esperando firma de factura",
        6: "Pagada"
    };

    const estadosItem = {
        "pendiente_revision": "Pendiente de revisión",
        "pagada": "Pagada",
        "rechazado": "Rechazado",
        "en_revision": "En revisión",
        "pendiente_firma": "Pendiente de firma",
        "esperando_factura": "Esperando factura",
        "esperando_firma_factura": "Esperando firma de factura"
    };

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
                    <th>Estado Colación</th>
                    <th>Colación</th>
                    <th>Estado Traslado</th>
                    <th>Traslado</th>
                    <th>Descripción</th>
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
                        <td>{estados[Number(solicitud.estado)] || "Desconocido"}</td>
                        <td>{solicitud.estado_colacion ? estadosItem[solicitud.estado_colacion] || solicitud.estado_colacion : "No aplica"}</td>
                        <td>
                            {solicitud.estado_colacion && solicitud.estado_colacion !== "No aplica" && (
                                <button 
                                    onClick={() => {
                                        // Estado pendiente_firma: funcionario puede subir factura
                                        if (solicitud.estado_colacion === "esperando_factura") {
                                            navigate(`/funcionario/subir-factura-colacion/${solicitud.id_solicitud}`);
                                        }
                                        // Otros estados: solo visualización
                                        else {
                                            navigate(`/funcionario/detalle-colacion/${solicitud.id_solicitud}`);
                                        }
                                    }}
                                    style={{backgroundColor: "green", color: "white", padding: "5px 10px", border: "none", cursor: "pointer"}}
                                >
                                    {solicitud.estado_colacion === "esperando_factura" ? "Subir Factura" : "Ver Colación"}
                                </button>
                            )}
                        </td>
                        
                        <td>{solicitud.estado_traslado ? estadosItem[solicitud.estado_traslado] || solicitud.estado_traslado : "No aplica"}</td>
                        
                        <td>
                            {solicitud.estado_traslado && solicitud.estado_traslado !== "No aplica" && (
                                <button 
                                    onClick={() => {
                                        // Estado pendiente_firma: funcionario puede subir factura
                                        if (solicitud.estado_traslado === "esperando_factura") {
                                            navigate(`/funcionario/subir-factura-traslado/${solicitud.id_solicitud}`);
                                        }
                                        // Otros estados: solo visualización
                                        else {
                                            navigate(`/funcionario/detalle-traslado/${solicitud.id_solicitud}`);
                                        }
                                    }}
                                    style={{backgroundColor: "green", color: "white", padding: "5px 10px", border: "none", cursor: "pointer"}}
                                >
                                    {solicitud.estado_traslado === "esperando_factura" ? "Subir Factura" : "Ver Traslado"}
                                </button>
                            )}
                        </td>
                        <td>{solicitud.descripcion}</td>
                        <td>{solicitud.asignatura.join(" - ")}</td>
                        <td>{solicitud.visita}</td>
                        <td>
                            <button 
                                onClick={() => {
                                    navigate(`/funcionario/solicitudes/${solicitud.id_solicitud}`);
                                }}
                                style={{backgroundColor: "blue", color: "white", padding: "5px 10px", border: "none", cursor: "pointer"}}
                            >
                                Ver
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <button className="volver-btn" onClick={() => navigate("/funcionario/dashboard")}>Volver</button>
        </div>
    );
}
