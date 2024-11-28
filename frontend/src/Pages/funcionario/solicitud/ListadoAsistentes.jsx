import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import readXlsxFile from "read-excel-file";
import axios from "axios";

export function ListadoAsistentes() {
    const [asistentes, setAsistentes] = useState([]); // Guarda el listado completo
    const [totalAsistentes, setTotalAsistentes] = useState(0); // Total de asistentes
    const navigate = useNavigate();
    const location = useLocation();

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        readXlsxFile(file).then((rows) => {
            if (rows.length > 0) {
                const [header, ...data] = rows; // Separar cabecera y filas
                const asistentesProcesados = data.map((row) => ({
                    nombre: row[0], // Suponiendo que la primera columna es el nombre
                    rut: row[1],    // Suponiendo que la segunda columna es el RUT
                    email: row[2],  // Suponiendo que la tercera columna es el email
                }));
                setAsistentes(asistentesProcesados); // Guardar el listado completo
                setTotalAsistentes(asistentesProcesados.length); // Total de filas válidas
            }
        });
    };

    const handleNext = async () => {
        const visitaId = location.state.visita_id; // Obtener el ID de la visita desde el estado

        try {
            // Enviar los asistentes al backend
            await axios.post("http://localhost:8000/visitantes", {
                visita_id: visitaId,
                asistentes,
            });

            // Navegar al siguiente paso
            navigate("/crear-solicitud/cotizacion", {
                state: { ...location.state, totalAsistentes },
            });
        } catch (error) {
            console.error("Error al guardar asistentes:", error);
            alert("Hubo un error al guardar los asistentes. Por favor, intente de nuevo.");
        }
    };

    return (
        <div>
            <h1>Listado de Asistentes</h1>
            <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} />
            <p>Total asistentes: {totalAsistentes}</p>
            <button onClick={handleNext} disabled={totalAsistentes === 0}>
                Siguiente
            </button>
        </div>
    );
}
