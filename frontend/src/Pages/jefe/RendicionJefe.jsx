import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

export function RendicionJefe() {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState(""); // Estado para el filtro
    const [searchTerm, setSearchTerm] = useState(""); 

    useEffect(() => {
        let rol = localStorage.getItem('userRole');
        if (rol === null) {
            rol = 'jefe';
            localStorage.setItem('userRole', 'jefe');
        }

        fetch("http://localhost:8000/rendiciones?rol=" + rol)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                setData(data.rendiciones); 
            })
            .catch((error) => {
                setError(error.toString());
            });
        localStorage.setItem('userRole', 'jefe');
    }, []);

    const getEstadoClass = (estado) => {
        switch (estado) {
            case "Pendiente":
                return "estado-pendiente";
            case "Rechazada":
                return "estado-rechazado";
            case "Por Devolver":
                return "estado-por-devolver";
            case "Devuelta":
                return "estado-aprobado";
            default:
                return "";
        }
    };

    const filteredData = data ? 
    (filter ? data.filter(item => item[3] === filter) : data)
    .filter(item => item[8].toString().includes(searchTerm)) : [];

    return (
        <div className="App">
            <div className="title-container">Rendiciones</div>
            <div className="search-terms">
                <select onChange={(e) => setFilter(e.target.value)} value={filter}>
                    <option value="">Todos</option>
                    <option value="Pendiente">Pendiente</option>
                    <option value="Rechazada">Rechazada</option>
                    <option value="Por Devolver">Por Devolver</option>
                </select>

                <input
                    type="text"
                    placeholder="Buscar por RUT"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>
            {data && data.length > 0 ? (
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
                                <th>Detalles</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredData.map((item, index) => (
                                <tr key={index}>
                                    <td>{item[0]}</td> {/* ID de la rendición */}
                                    <td>{item[6]}</td> {/* Nombre de la actividad */}
                                    <td>{item[7]}</td> {/* Nombre del trabajador */}
                                    <td>{item[4]}</td> {/* Descripción de la rendición */}
                                    <td>{new Date(item[1]).toLocaleDateString()}</td> {/* Fecha de la rendición */}
                                    <td>{item[2].toLocaleString()}</td> {/* Monto de la rendición */}
                                    <td className={getEstadoClass(item[3])}>
                                        {item[3]}
                                    </td>
                                    <td>
                                        <Link to={`/rendiciones/detalles/${item[0]}`}>
                                            <button className="button">
                                                Ver Detalles
                                            </button>
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : data && data.length === 0 ? (
                <p>No hay rendiciones disponibles.</p>
            ) : error ? (
                <p>Error: {error}</p>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}
