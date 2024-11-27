import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export function DashboardFuncionario() {
    const navigate = useNavigate();
    const handleLogout = () => {
        // Aquí puedes manejar el proceso de logout, como limpiar el estado global o cookies
        console.log("Logout exitoso");
        navigate("/login"); // Redirige al usuario a la página de login
    };

    return (
        <div style={{ padding: "20px" }}>
            <h1>Dashboard del Funcionario</h1>
            <div style={{ marginBottom: "20px" }}>
                <button onClick={handleLogout}>Logout</button>
            </div>
            <div>
                <Link to="/ver-solicitudes">Ver Solicitudes</Link>
            </div>
            <div>
                <Link to="/crear-solicitud">Crear Solicitud</Link>
            </div>
        </div>
    );
}