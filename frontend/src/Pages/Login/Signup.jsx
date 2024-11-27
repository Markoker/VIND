import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';  // Asegúrate de que esto está aquí

export function SignUp() {
  const [formData, setFormData] = useState({ // Inicializa el estado del formulario
    rut: '',
    nombre: '',
    correo: '',
    contraseña: '',
    rol: 'trabajador',
    centro_de_costos: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita que la página se recargue al enviar el formulario
    try {
      const response = await fetch('http://localhost:8000/signup', { // Envía los datos del formulario a la ruta de registro
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData), // Envía los datos del formulario como JSON
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Usuario creado:', data);
        navigate('/login'); // Redirige a la página de inicio de sesión

      } else {
      
        const errorData = await response.json();
        console.error('Error al crear el usuario:', errorData);
        alert('Error al crear la cuenta: ' + errorData.message);
      }
    } catch (error) {
      console.error('Error de red:', error);
      alert('Error de red, intenta nuevamente más tarde.');
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Registro</h1>
      <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label className="form-label">RUT:</label>
          <input
            type="text"
            name="rut"
            value={formData.rut}
            onChange={handleChange}
            required
          />
        </div>  
        <div className="form-group">
          <label className="form-label">Nombre:</label>
          <input
            type="text"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Correo:</label>
          <input
            type="email"
            name="correo"
            value={formData.correo}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Contraseña:</label>
          <input
            type="password"
            name="contraseña"
            value={formData.contraseña}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Rol:</label>
          <select
            name="rol"
            value={formData.rol}
            onChange={handleChange}
            required
          >
            <option value="trabajador">Trabajador</option>
            <option value="contador">Contador</option>
            <option value="jefe">Jefe de Área</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Centro de Costos:</label>
          <input
            type="text"
            name="centro_de_costos"
            value={formData.centro_de_costos}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submit-button">Registrarse</button>
      </form>
      <p style={{ marginTop: '20px', textAlign: 'center' }}>
        ¿Ya tienes una cuenta? <Link to="/login">Inicia sesión aquí</Link>
      </p>
    </div>
  );
}
