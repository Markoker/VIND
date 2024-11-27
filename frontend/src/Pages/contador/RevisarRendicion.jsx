import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export function RevisarRendicion() {
  
  const { idRendicion } = useParams();
  const navigate = useNavigate();
  const [rendicion, setRendicion] = useState(null);
  const [comentario, setComentario] = useState('');

  useEffect(() => {
    console.log("Rendicion ID:", idRendicion);
    // Cargar los datos de la rendición con el ID
    fetch(`http://localhost:8000/rendiciones/${idRendicion}?rol=contador`)
      .then((response) => response.json())
      .then((data) => {
        setRendicion(data);
        console.log("Datos de la rendición:", data);
      });
  }, [idRendicion]);

  const handleUpdate = async (estado) => {
    if (!comentario) {
      alert('Debes dejar un comentario antes de actualizar el estado.');
      return;
    }
    
    // Extrae `userRut` del almacenamiento local
    const userRut = localStorage.getItem('userRut');
    
    try {
      const response = await fetch(`http://localhost:8000/rendiciones/${idRendicion}/estado?contador_rut=${userRut}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nuevo_estado: estado, comentario: comentario }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        alert(`No se pudo actualizar la rendición: ${errorData.detail || 'Error desconocido'}`);
        return;
      }
  
      alert('Estado actualizado correctamente');
      navigate('/dashboard-contador');
    } catch (error) {
      console.error("Error de red:", error);
      alert('Ocurrió un error al conectar con el servidor.');
    }
  };
  
  

  if (!rendicion) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="rendicion-detalles-container">
      <div className="title-container">Rendición N°{rendicion.idrendicion}</div>

      <div className="rendicion-card">
        <p><strong>Nombre trabajador:</strong> {rendicion.trabajador_nombre}</p>
        <p><strong>Actividad:</strong> {rendicion.actividad_nombre}</p>
        <p><strong>Descripción:</strong> {rendicion.descripcion}</p>
        <p><strong>Fecha de envío:</strong> {new Date(rendicion.fecha).toLocaleDateString()}</p>
        <p><strong>Monto:</strong> ${rendicion.monto.toLocaleString()}</p>
        <p><strong>Estado actual:</strong> {rendicion.estado}</p>
      </div>

      <div className="documentos-respaldo">
        <p><strong>Documento(s) de respaldo:</strong></p>
        {rendicion.documentos && rendicion.documentos.length > 0 ? (
          rendicion.documentos.map((docId) => (
            <a key={docId} href={`http://localhost:8000/documentos/${docId}`} target="_blank" download>
              <img src="/pdf.png" alt="Documento de respaldo" />
              Documento {docId}.pdf
            </a>
          ))
        ) : (
          <p>No hay documentos disponibles para esta rendición.</p>
        )}
      </div>

      <div className="acciones">
        <div className="comentario-section">
          <textarea
            placeholder="Deja un comentario"
            value={comentario}
            onChange={(e) => setComentario(e.target.value)}
            required
          ></textarea>
        </div>
        <div class="estado-section">
          <button class="volver-btn" onClick={() => navigate(-1)}>Volver</button>
          <div class="botones-estado">
          <button className="rechazar-btn" onClick={() => handleUpdate("Rechazada")}>Rechazar</button>
          <button className="validar-btn" onClick={() => handleUpdate("Por Devolver")}>Validar</button>
        </div>
    </div>
  </div>
  </div>
  )
}
