import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

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
      
        try {
          const response = await axios.get(`http://localhost:8000/visita/profesores`);
          const profesores = response.data;
      
          const encargadoProfesor = encargados.find(encargado =>
            profesores.some(p => p.rut.trim() === encargado.rut.trim())
          );
      
          if (!encargadoProfesor) {
            alert("Debe haber al menos un encargado registrado como profesor.");
            return;
          }
      
          const profesor = profesores.find(p => p.rut.trim() === encargadoProfesor.rut.trim());
          const visitaActualizada = { ...visita, profesor_id: profesor.id_profesor };
      
          // Guardar
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
          console.error("Error al buscar profesor:", error);
          alert("No se pudo verificar el profesor. Intenta nuevamente.");
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
