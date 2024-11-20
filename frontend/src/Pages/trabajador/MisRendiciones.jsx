import React, { useState, useEffect } from "react";

export function MisRendiciones() {
    const [rendiciones, setRendiciones] = useState([]);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState("");
    const [estadoFilter, setEstadoFilter] = useState("");

    
    useEffect(() => {
        const fetchRendiciones = async () => {
            try {
                const rol = "trabajador";
                const trabajadorRut = localStorage.getItem("userRut");
                
                if (!trabajadorRut) {
                    throw new Error("RUT del trabajador no encontrado. Por favor, inicie sesión de nuevo.");
                }
                
                const response = await fetch(`http://localhost:8000/rendiciones?rol=${rol}&trabajador_rut=${trabajadorRut}`);
                
                if (!response.ok) {
                    throw new Error("Error al obtener las rendiciones");
                }
                
                const data = await response.json();
                console.log(data.rendiciones);
                setRendiciones(data.rendiciones);
            } catch (error) {
                setError(error.message);
            }
        };

        fetchRendiciones();
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

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

    const rendicionesfiltradas = rendiciones.filter(item => 
        (filter === "" || item[5] === filter) && 
        (estadoFilter === "" || item[4] === estadoFilter)
    );

    return (
        <div className="App">
            <div class="title-container">Mis Rendiciones</div>
            <div className="search-terms">
                <p>Filtrar por Actividad</p>
                <select onChange={(e) => setFilter(e.target.value)} value={filter}>
                    <option value="">Todas</option>
                    <option value="Almuerzo">Almuerzo</option>
                    <option value="Transporte">Transporte</option>
                    <option value="Seminario">Seminario</option>
                    <option value="Suministro">Suministro</option>
                </select>
                <p>Filtrar por Estado</p>
                <select onChange={(e) => setEstadoFilter(e.target.value)} value={estadoFilter}>
                    <option value="">Todos</option>
                    <option value="Pendiente">Pendiente</option>
                    <option value="Rechazada">Rechazada</option>
                    <option value="Por Devolver">Por Devolver</option>
                    <option value="Devuelta">Devuelta</option>
                </select>
            </div>    
            {rendiciones.length > 0 ? (
                <table className="rendiciones-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Fecha</th>
                            <th>Monto</th>
                            <th>Estado</th>
                            <th>Descripción</th>
                            <th>Actividad</th>
                            <th>Comentario</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rendicionesfiltradas.map((rendicion) => (
                            <tr key={rendicion[0]}>
                                <td>{rendicion[0]}</td>
                                <td>{new Date(rendicion[1]).toLocaleDateString()}</td>
                                <td>{rendicion[3].toLocaleString()}</td>
                                <td className={getEstadoClass(rendicion[4])}>
                                    {rendicion[4]}
                                </td>
                                <td>{rendicion[6]}</td>
                                <td>{rendicion[5]}</td> {/* Nombre de la actividad */}
                                <td>{rendicion[7]}</td> {/* Comentario */}
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No tienes rendiciones registradas.</p>
            )}
        </div>
    );
}
