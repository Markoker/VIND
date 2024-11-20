import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function SubirRendicion() {
    const navigate = useNavigate();
    const [monto, setMonto] = useState('');
    const [descripcion, setDescripcion] = useState('');
    const [actividad, setActividad] = useState('');
    const [archivos, setArchivos] = useState([]);
    
    const nombres_actividades = ['Seminario', 'Transporte', 'Almuerzo', 'Suministro'];
    const actividadIdMap = {
        "Seminario": 1,
        "Transporte": 2,
        "Almuerzo": 3,
        "Suministro": 4
    };

    useEffect(() => {
        const rutTrabajador = localStorage.getItem('userRut');
        if (!rutTrabajador) {
            alert("RUT del trabajador no encontrado. Por favor, inicie sesión de nuevo.");
            navigate("/login");
        }
    }, [navigate]);

    const handleFileChange = (e) => {
        setArchivos([...e.target.files]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const rutTrabajador = localStorage.getItem('userRut');
        console.log("RUT del trabajador:", rutTrabajador);
        if (!rutTrabajador) {
            alert("RUT del trabajador no encontrado. Por favor, inicie sesión de nuevo.");
            return;
        }
        
        const formData = new FormData();
        formData.append("t_subida", rutTrabajador);
        formData.append("estado", "Pendiente");
        formData.append("descripcion", descripcion);
        formData.append("monto", parseInt(monto, 10));
        formData.append("a_asignada", actividadIdMap[actividad]);
        formData.append("comentario", "");
        
        archivos.forEach((archivo) => {
            formData.append('archivos', archivo);
        });
    
        console.log("Datos de la rendición:", Object.fromEntries(formData.entries()));
    
        try {
            const response = await fetch('http://localhost:8000/rendiciones?rol=trabajador', {
                method: 'POST',
                body: formData
            });
    
            if (!response.ok) {
                throw new Error("Error al crear la rendición");
            }
    
            const responseData = await response.json();
            const rendicionId = responseData.message.match(/\d+/)[0];
            if (archivos.length > 0) {
                console.log("ID de rendición para subir archivos:", rendicionId);
                await handleFileUpload(rendicionId); // Función para manejar la subida de archivos
            }
            alert("Rendición creada con éxito");
        } catch (error) {
            console.error("Error:", error);
            alert("Error al crear la rendición");
        }
    };
    const handleFileUpload = async (rendicionId) => {
        const formData = new FormData();
        archivos.forEach((archivo) => formData.append("archivos", archivo));
    
        const response = await fetch(`http://localhost:8000/rendiciones/${rendicionId}/archivos`, {
            method: "POST",
            body: formData
        });
    
        if (response.ok) {
            const data = await response.json();
            console.log("Archivos subidos con éxito", data);
            // Aquí puedes almacenar los `documento_ids` si es necesario para usarlos en el futuro
        } else {
            console.error("Error al subir archivos:", await response.text());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h2 className="form-title">Crear Nueva Rendición</h2>
            <div className="form-group">
                <label className="form-label">Monto:</label>
                <input 
                    type="number" 
                    value={monto} 
                    onChange={(e) => setMonto(e.target.value)} 
                    required 
                    className="form-input" 
                />
            </div>

            <div className="form-group">
                <label className="form-label">Actividad Asignada:</label>
                <select 
                    value={actividad} 
                    onChange={(e) => setActividad(e.target.value)} 
                    required 
                    className="form-select"
                >
                    <option value="">Selecciona una actividad</option>
                    {nombres_actividades.map((nombre, index) => (
                        <option key={index} value={nombre}>{nombre}</option>
                    ))}
                </select>
            </div>

            <div className="form-group">
                <label className="form-label">Descripción:</label>
                <input 
                    type="text" 
                    value={descripcion} 
                    onChange={(e) => setDescripcion(e.target.value)} 
                    required 
                    className="form-input" 
                />
            </div>

            <div className="form-group">
                <label className="form-label">Documentos de respaldo:</label>
                <input 
                    type="file" 
                    multiple 
                    onChange={handleFileChange} 
                    required 
                    className="form-file-input" 
                />
            </div>

            <button type="submit" className="submit-button">Crear Rendición</button>
        </form>
    );
}