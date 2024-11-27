import React, { useState, useEffect } from "react";
import axios from "axios";

export function CrearSolicitud({ usuarioRut }) {
    const [campus, setCampus] = useState([]);
    const [unidadAcademica, setUnidadAcademica] = useState([]);
    const [asignaturas, setAsignaturas] = useState([]);
    const [selectedCampus, setSelectedCampus] = useState("");
    const [selectedUnidad, setSelectedUnidad] = useState("");
    const [selectedAsignatura, setSelectedAsignatura] = useState("");
    const [semestre, setSemestre] = useState("");
    const [paralelo, setParalelo] = useState("");
    const [visita, setVisita] = useState({
        nombre_empresa: "",
        fecha: "",
        lugar: "",
        profesor_id: "",
    });
    const [cotizacion, setCotizacion] = useState({
        tipo: "",
        monto: "",
        proveedor: {
            nombre: "",
            rut: "",
            email: "",
        },
        cotizaciones: [],
    });
    const [descripcion, setDescripcion] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    useEffect(() => {
        // Fetch campus data
        axios.get("http://localhost:8000/emplazamiento").then((res) => setCampus(res.data));
    }, []);

    const handleUnidadChange = (campusId) => {
        axios
            .get(`http://localhost:8000/unidades-academicas/${campusId}`)
            .then((res) => setUnidadAcademica(res.data));
    };

    const handleAsignaturasChange = (unidadId, semestre) => {
        axios
            .get(
                `http://localhost:8000/asignaturas?unidad_academica=${unidadId}&semestre=${semestre}`
            )
            .then((res) => setAsignaturas(res.data));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                descripcion,
                usuario_rut: usuarioRut,
                asignatura_id: selectedAsignatura,
                visita,
                cotizacion: cotizacion.tipo ? cotizacion : null,
            };
            const response = await axios.post(
                "http://localhost:8000/solicitudes",
                payload
            );
            setSuccess("Solicitud creada exitosamente");
        } catch (err) {
            setError(
                err.response?.data?.detail || "Error al crear la solicitud."
            );
        }
    };

    return (
        <div>
            <h1>Crear Solicitud</h1>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {success && <p style={{ color: "green" }}>{success}</p>}
            <form onSubmit={handleSubmit}>
                <h2>Datos de la Asignatura</h2>
                <select onChange={(e) => handleUnidadChange(e.target.value)}>
                    <option value="">Seleccionar Campus</option>
                    {campus.map((c) => (
                        <option key={c.id} value={c.id}>
                            {c.nombre}
                        </option>
                    ))}
                </select>
                <select
                    onChange={(e) => {
                        setSelectedUnidad(e.target.value);
                        handleAsignaturasChange(e.target.value, semestre);
                    }}
                >
                    <option value="">Seleccionar Unidad Académica</option>
                    {unidadAcademica.map((u) => (
                        <option key={u.id} value={u.id}>
                            {u.nombre}
                        </option>
                    ))}
                </select>
                <input
                    type="number"
                    placeholder="Semestre"
                    value={semestre}
                    onChange={(e) => setSemestre(e.target.value)}
                />
                <select
                    onChange={(e) => setSelectedAsignatura(e.target.value)}
                >
                    <option value="">Seleccionar Asignatura</option>
                    {asignaturas.map((a) => (
                        <option key={a.id} value={a.id}>
                            {a.nombre}
                        </option>
                    ))}
                </select>
                <input
                    type="number"
                    placeholder="Paralelo"
                    value={paralelo}
                    onChange={(e) => setParalelo(e.target.value)}
                />

                <h2>Datos de la Visita</h2>
                <input
                    type="text"
                    placeholder="Nombre Empresa"
                    value={visita.nombre_empresa}
                    onChange={(e) =>
                        setVisita({ ...visita, nombre_empresa: e.target.value })
                    }
                />
                <input
                    type="date"
                    placeholder="Fecha"
                    value={visita.fecha}
                    onChange={(e) =>
                        setVisita({ ...visita, fecha: e.target.value })
                    }
                />
                <input
                    type="text"
                    placeholder="Lugar"
                    value={visita.lugar}
                    onChange={(e) =>
                        setVisita({ ...visita, lugar: e.target.value })
                    }
                />
                <input
                    type="text"
                    placeholder="RUT Profesor"
                    value={visita.profesor_id}
                    onChange={(e) =>
                        setVisita({ ...visita, profesor_id: e.target.value })
                    }
                />

                <h2>Tipo de Cotización</h2>
                <select
                    onChange={(e) =>
                        setCotizacion({ ...cotizacion, tipo: e.target.value })
                    }
                >
                    <option value="">Seleccionar Tipo</option>
                    <option value="Solo traslado">Solo Traslado</option>
                    <option value="Solo colacion">Solo Colación</option>
                    <option value="Traslado y colacion">
                        Traslado y Colación
                    </option>
                </select>
                <input
                    type="number"
                    placeholder="Monto"
                    value={cotizacion.monto}
                    onChange={(e) =>
                        setCotizacion({ ...cotizacion, monto: e.target.value })
                    }
                />
                <button type="submit">Crear Solicitud</button>
            </form>
        </div>
    );
}
