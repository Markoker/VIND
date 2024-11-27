import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../sidebar';
import { Rendicion } from './MostrarRendiciones';
import { RendicionesDevueltas } from './MostrarDevoluciones';

export function DashboardContador() {
    const [selectedOption, setSelectedOption] = useState("rendiciones");
    const navigate = useNavigate();
    const contadorOptions = [
        { key: "rendiciones", label: "Rendiciones" },
        { key: "devoluciones", label: "Devoluciones" },
        { key: "logout", label: "Logout" }
    ];

    const handleOptionSelect = (option) => {
        if (option === "logout") {
            // Redirige a la ruta de logout
            navigate("/logout");
        }else{
            setSelectedOption(option);
        }
    };

    return (
        <div className="dashboard-container">
            <Sidebar onOptionSelect={handleOptionSelect} options={contadorOptions} />
            <div className="dashboard-content">
                {selectedOption === "rendiciones" && <Rendicion />}
                {selectedOption === "devoluciones" && <RendicionesDevueltas />}
            </div>
        </div>
    );
}
