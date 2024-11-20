import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

export function RendicionesDevueltas() {
    const [data, setData] = useState([]); // Inicializa como un array vacío
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState(""); // Cambia el estado inicial a vacío
    const [searchTerm, setSearchTerm] = useState(""); 

    useEffect(() => {
        const rol = localStorage.getItem('userRole') || 'contador'; // Usa valor por defecto
        localStorage.setItem('userRole', rol); // Establece el rol en localStorage

        fetch(`http://localhost:8000/devoluciones?rol=${rol}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                console.log(data.devoluciones); // Verifica la respuesta
                setData(data.devoluciones || []); // Establece un array vacío si no hay datos
            })
            .catch((error) => {
                setError(error.toString());
            });
    }, []);

    const getEstadoClass = (estado) => {
        switch (estado) {
            case "Por Devolver":
                return "estado-por-devolver";
            case "Devuelta":
                return "estado-aprobado";
            default:
                return "";
        }
    };

    // Filtrado de datos
    const filteredData = data.filter(item => {
        const matchesFilter = filter ? item.estado === filter : true; // Filtra por estado
        const matchesSearchTerm = item.t_subida.toString().toLowerCase().includes(searchTerm.toLowerCase()); // Cambia 'T_subida' según tu estructura
        return matchesFilter && matchesSearchTerm; 
    });

    return (
        <div className="App">
            <div class="title-container">Devoluciones</div>
                <div className="search-terms">
                    {/* Menú desplegable para seleccionar el filtro */}
                    <select onChange={(e) => setFilter(e.target.value)} value={filter}>
                        <option value="">Todas</option>
                        <option value="Por Devolver">Por Devolver</option>
                        <option value="Devuelta">Devuelta</option>
                    </select>
                    {/* Se puede buscar por RUT */}
                    <input
                        type="text"
                        placeholder="Buscar por RUT"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                {data.length > 0 ? (
                    <div className="data-list">
                        <table className="rendiciones-table">
                            <thead>
                                <tr>
                                    <th>Id</th>
                                    <th>Actividad</th>
                                    <th>Trabajador</th>
                                    <th>Descripción</th>
                                    <th>Fecha envío</th>
                                    <th>Monto</th>
                                    <th>Estado</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredData.map((item, index) => (
                                    <tr key={index}>
                                        <td>{item.idRendicion}</td> {/* ID de la rendición */}
                                        <td>{item.a_asignada}</td> {/* Nombre de la actividad */}
                                        <td>{item.t_subida}</td> {/* Nombre del trabajador */}
                                        <td>{item.descripcion}</td> {/* Descripción de la rendición */}
                                        <td>{new Date(item.fecha).toLocaleDateString()}</td> {/* Fecha de la rendición */}
                                        <td>{item.monto.toLocaleString()}</td> {/* Monto de la rendición */}
                                        <td className={getEstadoClass(item.estado)}>
                                            {item.estado}
                                        </td>
                                        <td>
                                            {item.estado === "Por Devolver" ? (
                                                <Link to={`/devoluciones/${item.idRendicion}`}>
                                                    <img src="/siguiente-boton.png" alt="Revisar" />
                                                </Link>
                                            ) : (
                                                "-"
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : data.length === 0 ? (
                    <p>No hay devoluciones disponibles.</p>
                ) : error ? (
                    <p>Error: {error}</p>
                ) : (
                    <p>Loading...</p>
                )}
        </div>
    );
}