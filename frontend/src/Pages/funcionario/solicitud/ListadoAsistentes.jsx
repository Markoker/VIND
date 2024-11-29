import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import readXlsxFile from "read-excel-file";
import axios from "axios";

export function ListadoAsistentes() {
    const [asistentes, setAsistentes] = useState([]); 
    const [totalAsistentes, setTotalAsistentes] = useState(0); 
    const navigate = useNavigate();
    const location = useLocation();

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;
        readXlsxFile(file).then((rows) => {
            if (rows.length > 0) {
                const [header, ...data] = rows;
                const asistentesProcesados = data.map((row) => ({
                    nombre: row[0],
                    rut: row[1],
                    email: row[2],
                }));
                setAsistentes(asistentesProcesados); // Guardar el listado completo
                setTotalAsistentes(asistentesProcesados.length); // Total de filas válidas
                localStorage.setItem("totalAsistentes", asistentesProcesados.length);
            }
        });
    };
    const handleNext = () => {
        navigate("/crear-solicitud/cotizacion", {
            state: { ...location.state, asistentes, totalAsistentes },
        });
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