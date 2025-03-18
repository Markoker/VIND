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
            if (rows.length <= 0) {
                alert("Ingrese un archivo valido");
            }

            let [header, ...data] = rows;

            if (JSON.stringify(data[7]) !== JSON.stringify(["N°","ROL USM","DV","RUT","DV","Ap.Paterno","Ap.Materno","Nombres","VTR","Carrera","Correo"])) {
                alert("El archivo no tiene el formato correcto");
                return;
            }

            // Eliminar las 7 primeras filas
            data = data.slice(8);

            const asistentesProcesados = data.map((row) => ({
                rol: row[1] + "-" + row[2],
                rut: row[3] + "-" + row[4],
                nombre: row[7] + " " + row[5] + " " + row[6],
                carrera: row[9],
                correo: row[10],
                VTR: row[8],
            }));

            console.log(asistentesProcesados);

            setAsistentes(asistentesProcesados); // Guardar el listado completo
            setTotalAsistentes(asistentesProcesados.length); // Total de filas válidas
            localStorage.setItem("totalAsistentes", asistentesProcesados.length);
        });
        };
    const handleNext = () => {
        navigate("/funcionario/crear-solicitud/cotizacion", {
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
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}