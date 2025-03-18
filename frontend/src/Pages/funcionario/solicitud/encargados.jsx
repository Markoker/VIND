import React, { useState, useEffect } from "react";
import { useNavigate} from "react-router-dom";
import axios from "axios";

export function Encargados() {
    const [numEncargados, setNumEncargados] = useState(1);
    const [maxEncargados, setMaxEncargados] = useState(10);
    const [encargados, setEncargados] = useState([]);
    const navigate = useNavigate();

    const handleEnviarDatos = () => {
        // Guardar datos de los encargados en el local storage

    }

    const renderEncargados = () => {
        return Array.from({ length: numEncargados }, (_, index) => (
            <div key={index}>
                <h3>Encargado {index + 1}</h3>
                <label>
                    Nombre:
                    <input type="text" />
                </label>
                <label>
                    Apellido:
                    <input type="text" />
                </label>
                <label>
                    Correo:
                    <input type="email" />
                </label>
                <label>
                    Rut:
                    <input type="text" />
                </label>
            </div>
        ));
    };

    return (
        <div>
            {/* Número de asignaturas */}
            <label>
                Número de encargados:
                <input
                    type="number"
                    min="1"
                    max={maxEncargados}
                    value={numEncargados}
                    onChange={(e) => {
                        const value = Math.min(Number(e.target.value), maxEncargados);
                        setNumEncargados(value);
                    }}
                />
            </label>

            {/* Renderizado dinámico de asignaturas */}
            {renderEncargados()}
            <button onClick={handleEnviarDatos}>Siguiente</button>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
