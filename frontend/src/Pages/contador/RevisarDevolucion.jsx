import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export function RevisarDevolucion() {
    const { idDevolucion } = useParams();
    const navigate = useNavigate();
    const [devolucion, setDevolucion] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/devoluciones/${idDevolucion}?rol=contador`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
            })
            .then((data) => {
            console.log("Datos de la devolución:", data);
            setDevolucion(data);
            })
            .catch((error) => {
            console.error("Error al cargar la devolución:", error);
            });
        }, [idDevolucion]);

        const handlePagar = async () => {
            const userRut = localStorage.getItem('userRut'); // RUT del contador
            try {
                const response = await fetch(
                    `http://localhost:8000/rendiciones/${idDevolucion}/estado?contador_rut=${userRut}`,
                    {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nuevo_estado: 'Devuelta', comentario: '' }), // Agrega un comentario vacío si no es requerido
                    }
                );
        
                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || 'Error desconocido'}`);
                    return;
                }
        
                alert('Estado actualizado a "Devuelta"');
                navigate('/dashboard-contador'); // Vuelve a la lista de devoluciones
            } catch (error) {
                console.error("Error de red:", error);
                alert('Ocurrió un error al conectar con el servidor.');
            }
        };
        

    if (!devolucion) {
        return <div>Cargando...</div>;
    }

    return (
        <div className="rendicion-detalles-container">
        <div className="title-container">Devolución N°{devolucion.idRendicion}</div>
        <div className="rendicion-card">
            <p><strong>Nombre trabajador:</strong> {devolucion.trabajador_nombre}</p>
            <p><strong>Actividad:</strong> {devolucion.a_asignada}</p>
            <p><strong>Monto:</strong> ${devolucion?.monto ? devolucion.monto.toLocaleString() : "Cargando..."}</p>

            <p><strong>Estado actual:</strong> {devolucion.estado}</p>
        </div>
        <div class="estado-section">
            
        <button className="volver-btn" onClick={() => navigate('/dashboard-contador')}>Volver</button>
        <div className="botones-estado">
            <button className="validar-btn" onClick={handlePagar}>Pagar</button>
        </div>
        </div> 
        </div>
    );
    }
