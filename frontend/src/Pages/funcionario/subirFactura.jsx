import {useParams, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";

export function SubirFacturaFuncionario() {
    const {id} = useParams();
    const [detalle, setDetalle] = useState(null);
    const [error, setError] = useState("");
    const [facturaTraslado, setFacturaTraslado] = useState(null);
    const [facturaColacion, setFacturaColacion] = useState(null);
    const navigate = useNavigate();
    const rut = localStorage.getItem("userRut");

    const handleFileChange = (e, tipo) => {
        const file = e.target.files[0];
        if (tipo === 'traslado') {
            setFacturaTraslado(file);
        } else if (tipo === 'colacion') {
            setFacturaColacion(file);
        }
    };

    const subirFacturas = async () => {
        if (!facturaTraslado && !facturaColacion) {
            alert("Debe subir al menos una factura.");
            return;
        }

        try {
            const formData = new FormData();
            if (facturaTraslado) {
                formData.append('factura_traslado', facturaTraslado);
            }
            if (facturaColacion) {
                formData.append('factura_colacion', facturaColacion);
            }
            formData.append('usuario_rut', rut);

            await axios.post(`http://localhost:8000/solicitudes/${id}/subir-factura-funcionario`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setDetalle({...detalle, estado: 5});
            alert("Facturas subidas exitosamente");
        } catch (err) {
            alert("No se pudieron subir las facturas.");
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

    const estados = {
        0: "Rechazada",
        1: "En revisión",
        2: "Revisión de requisitos",
        3: "Esperando firma de cotización",
        4: "Esperando factura",
        5: "Esperando firma de factura",
        6: "Pagada"
    };

    return (
        <div style={{padding: "20px"}}>
            <h1>Subir Facturas - Solicitud #{detalle.id}</h1>
            
            <div style={{marginBottom: "20px"}}>
                <h3>Información General</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>Fecha:</strong> {new Date(detalle.fecha).toLocaleDateString()}</p>
                    <p><strong>Estado:</strong> {estados[detalle.estado] || "Desconocido"}</p>
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

            <div style={{marginBottom: "20px"}}>
                <h3>Visita</h3>
                <div style={{display: "flex", gap: "30px"}}>
                    <p><strong>Empresa:</strong> {detalle.visita.empresa}</p>
                    <p><strong>Fecha:</strong> {new Date(detalle.visita.fecha).toLocaleDateString()}</p>
                    <p><strong>Lugar:</strong> {detalle.visita.lugar}</p>
                </div>
            </div>

            <div style={{marginBottom: "20px"}}>
                <h3>Asignaturas</h3>
                <p>{detalle.asignaturas.join(", ")}</p>
            </div>

            {detalle.cotizacion && (
                <div style={{marginBottom: "20px"}}>
                    <h3>Cotización</h3>
                    <div style={{display: "flex", gap: "30px"}}>
                        <p><strong>Tipo:</strong> {detalle.cotizacion.tipo}</p>
                        <p><strong>Estado:</strong> {detalle.cotizacion.estado}</p>
                        <p><strong>Monto Total:</strong> ${detalle.cotizacion.monto}</p>
                    </div>

                    {detalle.cotizacion.traslado && (
                        <div style={{marginTop: "10px", padding: "10px", border: "1px solid #ccc"}}>
                            <h4>Traslado</h4>
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
                                    onChange={(e) => handleFileChange(e, 'traslado')}
                                    style={{marginTop: "5px"}}
                                />
                            </div>
                        </div>
                    )}

                    {detalle.cotizacion.colacion && (
                        <div style={{marginTop: "10px", padding: "10px", border: "1px solid #ccc"}}>
                            <h4>Colación</h4>
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
                                    onChange={(e) => handleFileChange(e, 'colacion')}
                                    style={{marginTop: "5px"}}
                                />
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Solo mostrar botones de acción si el estado permite al funcionario actuar */}
            {detalle.estado === 4 && (
                <div style={{marginTop: "20px"}}>
                    <button onClick={subirFacturas} style={{backgroundColor: "green", color: "white", padding: "10px 20px"}}>
                        Subir Facturas
                    </button>
                </div>
            )}

            <br/>
            <button onClick={() => navigate("/funcionario/dashboard")}>Volver</button>
        </div>
    );
} 