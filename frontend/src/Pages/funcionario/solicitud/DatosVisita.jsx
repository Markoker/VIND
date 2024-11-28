import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export function DatosVisita() {
    const [visita, setVisita] = useState({ nombre_empresa: "", fecha: "", lugar: "", profesor_id: "" });
    const navigate = useNavigate();
    const location = useLocation();

    const handleNext = () => {
        navigate("/crear-solicitud/asistentes", { state: { ...location.state, visita } });
    };

    return (
        <div>
            <h1>Datos de la Visita</h1>
            <input
                type="text"
                placeholder="Nombre Empresa"
                value={visita.nombre_empresa}
                onChange={(e) => setVisita({ ...visita, nombre_empresa: e.target.value })}
            />
            <input
                type="date"
                placeholder="Fecha"
                value={visita.fecha}
                onChange={(e) => setVisita({ ...visita, fecha: e.target.value })}
            />
            <input
                type="text"
                placeholder="Lugar"
                value={visita.lugar}
                onChange={(e) => setVisita({ ...visita, lugar: e.target.value })}
            />
            <input
                type="text"
                placeholder="RUT Profesor"
                value={visita.profesor_id}
                onChange={(e) => setVisita({ ...visita, profesor_id: e.target.value })}
            />
            <button onClick={handleNext}>Siguiente</button>
        </div>
    );
}
