import React, { useState, useEffect } from "react";
import { useNavigate} from "react-router-dom";
import axios from "axios";

export function DatosAsignatura() {
    const [campus, setCampus] = useState([]);
    const [unidadAcademica, setUnidadAcademica] = useState([]);
    const [asignaturas, setAsignaturas] = useState([]);
    const [selectedCampus, setSelectedCampus] = useState("");
    const [selectedUnidad, setSelectedUnidad] = useState("");
    const [semestre, setSemestre] = useState("");
    const [minAsignaturas, setMinAsignaturas] = useState(0);
    const [maxAsignaturas, setMaxAsignaturas] = useState(0);
    const [numAsignaturas, setNumAsignaturas] = useState(0);
    const [asignaturasSeleccionadas, setAsignaturasSeleccionadas] = useState([]);
    const navigate = useNavigate();

    const rut = localStorage.getItem("userRut");

    useEffect(() => {
        // Cargar los campus al inicio
        axios
            .get(`http://localhost:8000/usuario/${rut}/rol/funcionario/emplazamiento`)
            .then((res) => setCampus(res.data))
            .catch((err) => console.error("Error al obtener los campus:", err));
    }, []);

    const handleUnidadChange = (campusId) => {
        setSelectedCampus(campusId);
        axios
            .get(`http://localhost:8000/usuario/${rut}/rol/funcionario/emplazamiento/${campusId}/unidad-academica`)
            .then((res) => setUnidadAcademica(res.data))
            .catch((err) => console.error("Error al obtener unidades académicas:", err));
    };

    useEffect(() => {
        if (selectedUnidad && semestre) {
            axios
                .get(`http://localhost:8000/asignatura/paralelo?unidad_academica=${selectedUnidad}&semestre=${semestre}`)
                .then((res) => {
                    console.log("Asignaturas obtenidas:", res.data);
                    setAsignaturas(res.data);
                    setMaxAsignaturas(res.data.length);

                    if (res.data.length < 1) {
                        setMinAsignaturas(0);
                    } else {
                        setMinAsignaturas(1);
                        setNumAsignaturas(1)
                    }
                })
                .catch((err) => {
                    console.error("Error al obtener asignaturas:", err.response?.data || err.message);
                });
        }
    }, [selectedUnidad, semestre]);

    const handleAsignaturaChange = (index, nombreAsignatura) => {
        const nuevasAsignaturas = [...asignaturasSeleccionadas];
        const asignatura = asignaturas.find((a) => a.nombre === nombreAsignatura);

        if (asignatura) {
            nuevasAsignaturas[index] = {
                nombre: nombreAsignatura,
                paralelos: asignatura.paralelos,
                maxParalelos: asignatura.paralelos.length,
                numParalelos: 0,
                paralelosSeleccionados: [],
            };
        } else {
            nuevasAsignaturas[index] = null; // En caso de seleccionar vacío
        }

        setAsignaturasSeleccionadas(nuevasAsignaturas);
        localStorage.setItem("asignaturasSeleccionadas", JSON.stringify(nuevasAsignaturas));
    };
    const handleNumParalelosChange = (index, numParalelos) => {
        const nuevasAsignaturas = [...asignaturasSeleccionadas];
        nuevasAsignaturas[index] = {
            ...nuevasAsignaturas[index],
            numParalelos: Math.min(numParalelos, nuevasAsignaturas[index].paralelos.length), // Respetar el máximo
            paralelosSeleccionados: new Array(numParalelos).fill(""),
        };
        setAsignaturasSeleccionadas(nuevasAsignaturas);
        localStorage.setItem("asignaturasSeleccionadas", JSON.stringify(nuevasAsignaturas));
    };
    
    const handleParaleloSeleccionadoChange = (asignaturaIndex, paraleloIndex, paraleloValue) => {
        const nuevasAsignaturas = [...asignaturasSeleccionadas];
        nuevasAsignaturas[asignaturaIndex].paralelosSeleccionados[paraleloIndex] = paraleloValue;
        setAsignaturasSeleccionadas(nuevasAsignaturas);
        localStorage.setItem("asignaturasSeleccionadas", JSON.stringify(nuevasAsignaturas));
    };
    
    const getParalelosDisponibles = (asignaturaIndex, paraleloIndex) => {
        const seleccionados = asignaturasSeleccionadas[asignaturaIndex]?.paralelosSeleccionados || [];
        return asignaturasSeleccionadas[asignaturaIndex]?.paralelos.filter(
            (p) => !seleccionados.includes(p) || seleccionados[paraleloIndex] === p // Permitir el actual
        ) || [];
    };

    const handleEnviarDatos = () => {
        const datosAsignaturas = JSON.parse(localStorage.getItem("asignaturasSeleccionadas"));
        if(!datosAsignaturas || datosAsignaturas.length === 0){
            alert("No hay datos de asignaturas seleccionados para enviar.");
            return;
        }
        navigate("/crear-solicitud/visita", { state: { asignaturas: datosAsignaturas } });
    }
    
    const renderAsignaturas = () => {
        return Array.from({ length: numAsignaturas }, (_, index) => (
            <div key={index}>
                <h3>Asignatura {index + 1}</h3>
                <select
                    onChange={(e) => handleAsignaturaChange(index, e.target.value)}
                    value={asignaturasSeleccionadas[index]?.nombre || ""}
                >
                    <option value="">Seleccionar Asignatura</option>
                    {asignaturas.map((a) => (
                        <option key={a.nombre} value={a.nombre}>
                            {a.nombre}
                        </option>
                    ))}
                </select>
                {asignaturasSeleccionadas[index]?.paralelos && (
                    <div>
                        <label>
                            Número de paralelos (máx: {asignaturasSeleccionadas[index].paralelos.length}):
                            <input
                                type="number"
                                min="1"
                                max={asignaturasSeleccionadas[index].paralelos.length}
                                value={asignaturasSeleccionadas[index]?.numParalelos || 1}
                                onChange={(e) => handleNumParalelosChange(index, Number(e.target.value))}
                            />
                        </label>
                        <div>
                            {Array.from({ length: asignaturasSeleccionadas[index]?.numParalelos || 1 }).map(
                                (_, paraleloIndex) => (
                                    <div key={paraleloIndex}>
                                        <label>Paralelo {paraleloIndex + 1}:</label>
                                        <select
                                            value={
                                                asignaturasSeleccionadas[index]?.paralelosSeleccionados[paraleloIndex] || ""
                                            }
                                            onChange={(e) =>
                                                handleParaleloSeleccionadoChange(index, paraleloIndex, e.target.value)
                                            }
                                        >
                                            <option value="">Seleccionar Paralelo</option>
                                            {getParalelosDisponibles(index, paraleloIndex).map((p) => (
                                                <option key={p} value={p}>
                                                    {p}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                )
                            )}
                        </div>
                    </div>
                )}
            </div>
        ));
    };
    return (
        <div>
            <h1>Datos de la Asignatura</h1>

            {/* Selector de Campus */}
            <select onChange={(e) => handleUnidadChange(e.target.value)}>
                <option value="">Seleccionar Campus</option>
                {campus.map((c) => (
                    <option key={c.id} value={c.id}>
                        {c.nombre}
                    </option>
                ))}
            </select>

            {/* Selector de Unidad Académica */}
            <select
                onChange={(e) => {
                    setSelectedUnidad(e.target.value);
                }}
            >
                <option value="">Seleccionar Unidad Académica</option>
                {unidadAcademica.map((u) => (
                    <option key={u.id} value={u.id}>
                        {u.nombre}
                    </option>
                ))}
            </select>

            {/* Selector de Semestre */}
            <select
                value={semestre}
                onChange={(e) => setSemestre(e.target.value)}
            >
                <option value="">Seleccionar Semestre</option>
                <option value="1">1</option>
                <option value="2">2</option>
            </select>

            {/* Número de asignaturas */}
            <label>
                Número de asignaturas:
                <input
                    type="number"
                    min={minAsignaturas}
                    max={maxAsignaturas}
                    value={numAsignaturas}
                    onChange={(e) => {
                        const value = Math.min(Number(e.target.value), maxAsignaturas);
                        setNumAsignaturas(value);
                        setAsignaturasSeleccionadas(asignaturasSeleccionadas.slice(0, value));
                    }}
                />
            </label>

            {/* Renderizado dinámico de asignaturas */}
            {renderAsignaturas()}
            <button onClick={handleEnviarDatos}>Siguiente</button>
            <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
        </div>
    );
}
