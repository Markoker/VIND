// selectProfile.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export function selectProfile(){
    return (
        <div>
            <div>
                <h1>Seleccionar Perfil</h1>
                <Link to="/dashboard-funcionario">Trabajador</Link>
            </div>
            <div>
                <h1>Seleccionar Perfil</h1>
                <Link to="/dashboard-contador">Contador</Link>
            </div>
            <div>
                <h1>Seleccionar Perfil</h1>
                <Link to="/dashboard-jefe">Jefe</Link>
            </div>
        </div
    );
}