import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export function Encargados() {
    const [numEncargados, setNumEncargados] = useState(1);
    const [maxEncargados, setMaxEncargados] = useState(10);
    const [encargadosSeleccionados, setEncargadosSeleccionados] = useState([]);
    const navigate = useNavigate();

    // Maneja el cambio en cada campo de un encargado
    const handleEncargadoChange = (index, field, value) => {
        const nuevos = [...encargadosSeleccionados];
        nuevos[index] = { ...nuevos[index], [field]: value };
        setEncargadosSeleccionados(nuevos);
    };

    // Renderiza campos según cantidad
    const renderEncargados = () => {
        return Array.from({ length: numEncargados }, (_, index) => {
            const encargado = encargadosSeleccionados[index] || {};
            return (
                <div key={index}>
                    <h3>Encargado {index + 1}</h3>
                    <label>
                        Nombre:
                        <input
                            type="text"
                            value={encargado.nombre || ""}
                            onChange={(e) => handleEncargadoChange(index, "nombre", e.target.value)}
                        />
                    </label>
                    <label>
                        Apellido:
                        <input
                            type="text"
                            value={encargado.apellido || ""}
                            onChange={(e) => handleEncargadoChange(index, "apellido", e.target.value)}
                        />
                    </label>
                    <label>
                        Correo:
                        <input
                            type="email"
                            value={encargado.correo || ""}
                            onChange={(e) => handleEncargadoChange(index, "correo", e.target.value)}
                        />
                    </label>
                    <label>
                        Rut:
                        <input
                            type="text"
                            value={encargado.rut || ""}
                            onChange={(e) => handleEncargadoChange(index, "rut", e.target.value)}
                        />
                    </label>
                </div>
            );
        });
    };

    const handleEnviarDatos = async () => {
        const encargados = encargadosSeleccionados;
        const visita = JSON.parse(localStorage.getItem("datosVisita"));
        const asignaturas = JSON.parse(localStorage.getItem("asignaturasSeleccionadas"));
        const asistentes = JSON.parse(localStorage.getItem("listadoAsistentes")) || [];

        // Validación básica
        if (encargados.length === 0 || encargados.some(e => !e.rut || !e.nombre || !e.correo)) {
            alert("Todos los encargados deben tener nombre, correo y RUT.");
            return;
        }

        try {
            const response = await axios.get("http://localhost:8000/visita/profesores");
            let profesores = response.data;

            let primerProfesor = null;

            for (const encargado of encargados) {
                const rutEncargado = encargado.rut?.trim();
                const nombreEncargado = `${encargado.nombre?.trim() || ""} ${encargado.apellido?.trim() || ""}`;
                const correoEncargado = encargado.correo?.trim();

                if (!rutEncargado || !nombreEncargado || !correoEncargado) {
                    continue;
                }

                let encontrado = profesores.find(
                    p => p?.rut && p.rut.trim() === rutEncargado
                );

                if (!encontrado) {
                    const nuevo = await axios.post("http://localhost:8000/visita/profesores", {
                        rut: rutEncargado,
                        nombre: nombreEncargado,
                        email: correoEncargado
                    });

                    encontrado = {
                        id_profesor: nuevo.data.id_profesor,
                        rut: rutEncargado,
                        nombre: nombreEncargado,
                        email: correoEncargado
                    };
                    profesores.push(encontrado);
                }

                if (!primerProfesor) {
                    primerProfesor = encontrado;
                }
            }

            if (!primerProfesor) {
                alert("Debe haber al menos un encargado válido.");
                return;
            }

            const visitaActualizada = { ...visita, profesor_id: primerProfesor.id_profesor };
            localStorage.setItem("datosVisita", JSON.stringify(visitaActualizada));
            localStorage.setItem("encargados", JSON.stringify(encargados));

            navigate("/funcionario/crear-solicitud/cotizacion", {
                state: {
                    asistentes,
                    encargados,
                    asignaturas,
                    visita: visitaActualizada,
                    totalAsistentes: asistentes.length
                }
            });

        } catch (error) {
            console.error("Error al procesar encargados:", error);
            alert("Hubo un error al verificar o crear profesores.");
        }
    };

    return (
        <div>
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

            {renderEncargados()}
            <button onClick={handleEnviarDatos}>Siguiente</button>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
