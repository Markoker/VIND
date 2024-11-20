// Dashboard.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export function Dashboard(){
    return (
        <div>
            <div>
                <h1>Dashboard</h1>
                <Link to="/Rendiciones">Rendiciones</Link>
            </div>
            <div>
                <h1>Devoluciones</h1>
                <Link to="/Devoluciones">Devoluciones</Link>
            </div>
        </div>
    );
}