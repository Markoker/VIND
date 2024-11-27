// Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">Bienvenid@ al sistema de rendición de gastos</h1>
      <div className="home-content">
        <div className="home-section">
          <h2>Inicio de Sesión</h2>
          <Link to="/login" className="home-button">Ir a Inicio de Sesión</Link>
        </div>
        <div className="home-section">
          <h2>Registro</h2>
          <Link to="/signup" className="home-button">Registrarse</Link>
        </div>
      </div>
    </div>
  );
}
