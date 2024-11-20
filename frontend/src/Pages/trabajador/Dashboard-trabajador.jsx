import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../sidebar';
import { SubirRendicion } from './SubirRendicion';
import { MisRendiciones } from './MisRendiciones';

export function DashboardTrabajador() {
    const [selectedOption, setSelectedOption] = useState("crearRendicion");
    const navigate = useNavigate();
    const trabajadorOptions = [
        { key: "crearRendicion", label: "Crear Rendición" },
        { key: "verMisRendiciones", label: "Ver Mis Rendiciones" },
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
            <Sidebar onOptionSelect={handleOptionSelect} options={trabajadorOptions} />
            <div className="dashboard-content">
                {selectedOption === "crearRendicion" && <SubirRendicion />}
                {selectedOption === "verMisRendiciones" && <MisRendiciones />}
            </div>
        </div>
    );
}
