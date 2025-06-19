import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function SubirFacturaColacionAdmin() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [facturaColacion, setFacturaColacion] = useState(null);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setFacturaColacion(file);
    };

    const subirFactura = async () => {
        if (!facturaColacion) {
            alert("Debe subir una factura.");
            return;
        }

        try {
            const formData = new FormData();
            formData.append('factura_colacion', facturaColacion);
            formData.append('usuario_rut', rut);

            await axios.post(`http://localhost:8000/solicitudes/${id}/subir-factura-colacion-admin`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            alert("Factura de colación subida exitosamente");
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
            <h1>Subir Factura de Colación - Solicitud #{detalle.id}</h1>
            
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

            {detalle.cotizacion && detalle.cotizacion.colacion && (
                <div style={{marginBottom: "20px"}}>
                    <h3>Cotización de Colación</h3>
                    <div style={{display: "flex", gap: "30px"}}>
                        <p><strong>Proveedor:</strong> {detalle.cotizacion.colacion.nombre_proveedor}</p>
                        <p><strong>RUT:</strong> {detalle.cotizacion.colacion.rut_proveedor}</p>
                        <p><strong>Email:</strong> {detalle.cotizacion.colacion.correo_proveedor}</p>
                        <p><strong>Monto:</strong> ${detalle.cotizacion.colacion.monto}</p>
                        <p><strong>Tipo Subvención:</strong> {detalle.cotizacion.colacion.tipo_subvencion}</p>
                    </div>
                    
                    <div style={{marginTop: "10px"}}>
                        <label htmlFor="facturaColacion"><strong>Subir Factura de Colación:</strong></label><br/>
                        <input
                            type="file"
                            id="facturaColacion"
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