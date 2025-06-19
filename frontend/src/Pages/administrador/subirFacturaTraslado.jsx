import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function SubirFacturaTrasladoAdmin() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [facturaTraslado, setFacturaTraslado] = useState(null);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFacturaTraslado(file);
    };

    const subirFactura = async () => {
        if (!facturaTraslado) {
            alert("Debe subir una factura.");
            return;
        }

        try {
            const formData = new FormData();
            formData.append('factura_traslado', facturaTraslado);
            formData.append('usuario_rut', rut);

            await axios.post(`http://localhost:8000/solicitudes/${id}/subir-factura-traslado-admin`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            alert("Factura de traslado subida exitosamente");
            navigate("/administrador/solicitudes");
        } catch (err) {
            alert("No se pudo subir la factura.");
        }
    };

    useEffect(() => {
        const fetchDetalle = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/solicitudes/${id}`);
                setDetalle(response.data);
            } catch (err) {
                setError("No se pudo obtener el detalle de la solicitud.");
            }
        };
        fetchDetalle();
    }, [id]);

    if (error) return <p style={{color: "red"}}>{error}</p>;
    if (!detalle) return <p>Cargando...</p>;

    return (
        <div style={{padding: "20px"}}>
            <h1>Subir Factura de Traslado - Solicitud #{detalle.id}</h1>
            
            <div style={{marginBottom: "20px"}}>
                <h3>Información General</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>Fecha:</strong> {new Date(detalle.fecha).toLocaleDateString()}</p>
                    <p><strong>Descripción:</strong> {detalle.descripcion}</p>
                </div>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Usuario Solicitante</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>RUT:</strong> {detalle.usuario.rut}</p>
                    <p><strong>Nombre:</strong> {detalle.usuario.nombre}</p>
                </div>
            </div>

            {detalle.cotizacion && detalle.cotizacion.traslado && (
                <div style={{marginBottom: "20px"}}>
                    <h3>Cotización de Traslado</h3>
                    <div style={{display: "flex", gap: "30px"}}>
                        <p><strong>Proveedor:</strong> {detalle.cotizacion.traslado.nombre_proveedor}</p>
                        <p><strong>RUT:</strong> {detalle.cotizacion.traslado.rut_proveedor}</p>
                        <p><strong>Email:</strong> {detalle.cotizacion.traslado.correo_proveedor}</p>
                        <p><strong>Monto:</strong> ${detalle.cotizacion.traslado.monto}</p>
                    </div>
                    
                    <div style={{marginTop: "10px"}}>
                        <label htmlFor="facturaTraslado"><strong>Subir Factura de Traslado:</strong></label><br/>
                        <input
                            type="file"
                            id="facturaTraslado"
                            accept=".pdf,.jpg,.jpeg,.png"
                            onChange={handleFileChange}
                            style={{marginTop: "5px"}}
                        />
                    </div>
                </div>
            )}

            <div style={{marginTop: "20px"}}>
                <button onClick={subirFactura} style={{backgroundColor: "green", color: "white", padding: "10px 20px"}}>
                    Subir Factura
                </button>
            </div>

            <br/>
            <button onClick={() => navigate("/administrador/solicitudes")}>Volver</button>
        </div>
    );
} 