import React, { useState, useEffect } from 'react';

export function ResumenDinero() {
    const [resumen, setResumen] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://localhost:8000/rendiciones/resumen")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                setResumen(data);
            })
            .catch((error) => {
                setError(error.toString());
            });
    }, []);

    return (
        <div className="resumen-container">
            <div className="resumen-card">
                <h2>Resumen de Dinero</h2>
                {resumen ? (
                    <div className="resumen-content">
                        <p className="dinero-devuelto">
                            <strong>Dinero Devuelto:</strong> ${resumen.dinero_devuelto.toLocaleString()}
                        </p>
                        <p className="dinero-por-devolver">
                            <strong>Dinero por Devolver:</strong> ${resumen.dinero_por_devolver.toLocaleString()}
                        </p>
                    </div>
                ) : error ? (
                    <p className="error-message">Error: {error}</p>
                ) : (
                    <p className="loading-message">Cargando...</p>
                )}
            </div>
        </div>
    );
}
