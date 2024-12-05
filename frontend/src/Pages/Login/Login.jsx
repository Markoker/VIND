import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export function Login() {
  const [correo, setCorreo] = useState('');
  const [contraseña, setContraseña] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault(); // Evita que se recargue la página

    try {
      const response = await fetch('http://localhost:8000/usuario/login', {  // Envía los datos del formulario a la ruta de inicio de sesión
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "email": correo,
          "password": contraseña
        }),
      });

      if (!response.ok) {
        throw new Error('Credenciales incorrectas'); // Lanza un error si la respuesta no es ok
      }

      const data = await response.json();
      const rut = data.rut; // Obtiene el RUT del usuario de la respuesta
      console.log("Respuesta del servidor:", data);
      if (rut) {
        // Guarda el RUT en localStorage si está disponible
        localStorage.setItem("userRut", rut);
        alert(`Bienvenido, ${data.message}`);
      } else {
          throw new Error("RUT no encontrado en la respuesta del servidor.");
      } // Muestra un mensaje de alerta
      navigate('/home'); // Redirige al usuario a la página de selección de perfil
    } catch (err) {
      setError(err.message); // Captura cualquier error y establece el estado de error
    }
  };


  return (
    <div className="form-container">
      <h1 className="form-title">Iniciar Sesión</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Muestra el error si existe */}
      <form onSubmit={handleSubmit}>
      <div className="form-group">
          <label htmlFor="correo" className="form-label">Correo:</label>
          <input
            type="email"
            id="correo"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="contraseña" className="form-label">Contraseña:</label>
          <input
            type="password"
            id="contraseña"
            value={contraseña}
            onChange={(e) => setContraseña(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="submit-button">Iniciar Sesión</button>
      </form>
      <p style={{ marginTop: '20px', textAlign: 'center' }}>
        ¿No tienes una cuenta? <Link to="/signup">Regístrate aquí</Link>
      </p>
    </div>
  );
}
