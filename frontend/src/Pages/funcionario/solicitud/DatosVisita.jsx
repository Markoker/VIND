import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

export function DatosVisita() {
    const [visita, setVisita] = useState({
        nombre_empresa: "",
        fecha: "",
        lugar: "",
        descripcion: "",
    });
    const navigate = useNavigate();
    const location = useLocation();
    const handleNext = () => {
        localStorage.setItem("datosVisita", JSON.stringify(visita));
        navigate("/funcionario/crear-solicitud/encargados", { state: { ...location.state, visita } });
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
                placeholder="Descripcion"
                value={visita.descripcion}
                onChange={(e) => setVisita({ ...visita, descripcion: e.target.value })}
                rows="4"
                cols="50"
            />
            <button onClick={handleNext}>Siguiente</button>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
