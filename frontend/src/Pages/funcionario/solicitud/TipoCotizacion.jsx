import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export function TipoCotizacion() {
    const [cotizacion, setCotizacion] = useState({
        tipo: "",
        montoTraslado: "",
        montoColacion: "",
        proveedorTraslado: { nombre: "", rut: "", email: "" },
        proveedorColacion: { nombre: "", rut: "", email: "" },
        tipoPresupuestacion: "",
        cotizacionesTraslado: [],
        cotizacionesColacion: [],
    });
    const [error, setError] = useState("");
    const location = useLocation();
    const { totalAsistentes } = location.state || { totalAsistentes: 0 };
    const navigate = useNavigate();

    const handleFileUpload = (e, tipo, index) => {
        const file = e.target.files[0];
        if (tipo === "traslado") {
        const updated = [...cotizacion.cotizacionesTraslado];
        updated[index] = file;
        setCotizacion({ ...cotizacion, cotizacionesTraslado: updated });
        } else if (tipo === "colacion") {
        const updated = [...cotizacion.cotizacionesColacion];
        updated[index] = file;
        setCotizacion({ ...cotizacion, cotizacionesColacion: updated });
        }
    };

    const handleNext = () => {
        navigate("/crear-solicitud/resumen", { state: { ...location.state, cotizacion } });
    };

    const handleMontoColacionChange = (e) => {
        const montoColacion = e.target.value;
        setError(""); // Clear previous error
        setCotizacion({ ...cotizacion, montoColacion });

        // Validate if the amount per attendee exceeds 6000
        const montoPorPersona = montoColacion / totalAsistentes;
        if (montoPorPersona > 6000) {
        setError("El monto por persona no puede superar los 6000.");
        }
    };

    return (
        <div>
        <h1>Tipo de Cotización</h1>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <select
            value={cotizacion.tipo}
            onChange={(e) => setCotizacion({ ...cotizacion, tipo: e.target.value })}
        >
            <option value="">Seleccionar Tipo</option>
            <option value="Solo traslado">Solo Traslado</option>
            <option value="Solo colacion">Solo Colación</option>
            <option value="Traslado y colacion">Traslado y Colación</option>
        </select>

        {cotizacion.tipo && (
            <div>
            {/* Sección de Traslado */}
            {(cotizacion.tipo.includes("traslado") || cotizacion.tipo === "Traslado y colacion") && (
                <div>
                <h3>Proveedor de Traslado</h3>
                <input
                    type="text"
                    placeholder="Nombre"
                    value={cotizacion.proveedorTraslado.nombre}
                    onChange={(e) =>
                    setCotizacion({
                        ...cotizacion,
                        proveedorTraslado: { ...cotizacion.proveedorTraslado, nombre: e.target.value },
                    })
                    }
                />
                <input
                    type="text"
                    placeholder="RUT"
                    value={cotizacion.proveedorTraslado.rut}
                    onChange={(e) =>
                    setCotizacion({
                        ...cotizacion,
                        proveedorTraslado: { ...cotizacion.proveedorTraslado, rut: e.target.value },
                    })
                    }
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={cotizacion.proveedorTraslado.email}
                    onChange={(e) =>
                    setCotizacion({
                        ...cotizacion,
                        proveedorTraslado: { ...cotizacion.proveedorTraslado, email: e.target.value },
                    })
                    }
                />
                <input
                    type="number"
                    placeholder="Monto Traslado"
                    value={cotizacion.montoTraslado}
                    onChange={(e) =>
                    setCotizacion({ ...cotizacion, montoTraslado: e.target.value })
                    }
                />
                <h4>Subir Cotizaciones de Traslado</h4>
                {cotizacion.montoTraslado > 1000000
                    ? [0, 1, 2].map((index) => (
                        <input
                        key={index}
                        type="file"
                        onChange={(e) => handleFileUpload(e, "traslado", index)}
                        />
                    ))
                    : [0].map((index) => (
                        <input
                        key={index}
                        type="file"
                        onChange={(e) => handleFileUpload(e, "traslado", index)}
                        />
                    ))}
                </div>
            )}

            {/* Sección de Colación */}
            {(cotizacion.tipo.includes("colacion") || cotizacion.tipo === "Traslado y colacion") && (
                <div>
                <h3>Monto de Colación</h3>
                <input
                    type="number"
                    placeholder="Monto Colación"
                    value={cotizacion.montoColacion}
                    onChange={handleMontoColacionChange}
                />
                {error === "" && (
                    <>
                    <h4>Tipo de Presupuestación</h4>
                    <select
                        value={cotizacion.tipoPresupuestacion}
                        onChange={(e) =>
                        setCotizacion({ ...cotizacion, tipoPresupuestacion: e.target.value })
                        }
                    >
                        <option value="">Seleccionar Tipo</option>
                        <option value="reembolso">Reembolso</option>
                        <option value="presupuesto">Previa Presupuestación</option>
                    </select>
                    {cotizacion.tipoPresupuestacion === "reembolso" && (
                        <>
                        <p>
                            Debe completar un archivo y enviarlo al correo oficial. Tenga un buen día.
                        </p>
                        </>
                    )}
                    {cotizacion.tipoPresupuestacion === "presupuesto" && (
                        <>
                        <h4>Datos del Proveedor de Colación</h4>
                        <input
                            type="text"
                            placeholder="Nombre"
                            value={cotizacion.proveedorColacion.nombre}
                            onChange={(e) =>
                            setCotizacion({
                                ...cotizacion,
                                proveedorColacion: {
                                ...cotizacion.proveedorColacion,
                                nombre: e.target.value,
                                },
                            })
                            }
                        />
                        <input
                            type="text"
                            placeholder="RUT"
                            value={cotizacion.proveedorColacion.rut}
                            onChange={(e) =>
                            setCotizacion({
                                ...cotizacion,
                                proveedorColacion: {
                                ...cotizacion.proveedorColacion,
                                rut: e.target.value,
                                },
                            })
                            }
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={cotizacion.proveedorColacion.email}
                            onChange={(e) =>
                            setCotizacion({
                                ...cotizacion,
                                proveedorColacion: {
                                ...cotizacion.proveedorColacion,
                                email: e.target.value,
                                },
                            })
                            }
                        />
                        <h4>Subir Cotizaciones de Colación</h4>
                        {cotizacion.montoColacion <= 3 * 30000
                            ? [0].map((index) => (
                                <input
                                key={index}
                                type="file"
                                onChange={(e) => handleFileUpload(e, "colacion", index)}
                                />
                            ))
                            : [0, 1, 2].map((index) => (
                                <input
                                key={index}
                                type="file"
                                onChange={(e) => handleFileUpload(e, "colacion", index)}
                                />
                            ))}
                        </>
                    )}
                    </>
                )}
                </div>
            )}
            </div>
        )}
        <button onClick={handleNext} disabled={error !== ""}>
            Siguiente
        </button>
        </div>
    );
    }
