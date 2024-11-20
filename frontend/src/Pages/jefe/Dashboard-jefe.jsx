import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from '../sidebar';
import { ResumenDinero } from './ResumenDinero';
import { RendicionJefe } from './RendicionJefe';

export function DashboardJefe() {
    const [selectedOption, setSelectedOption] = useState("resumen");
    const navigate = useNavigate();
    const jefeOptions = [
        { key: "resumen", label: "Resumen de Dinero" },
        { key: "rendiciones", label: "Rendiciones" },
        { key: "logout", label: "Logout" }
    ];

    const handleOptionSelect = (option) => {
        if (option === "logout") {
            navigate("/logout");
        } else {
            setSelectedOption(option);
        }
    };

    return (
        <div className="dashboard-container">
            <Sidebar onOptionSelect={handleOptionSelect} options={jefeOptions} />
            <div className="dashboard-content">
                {selectedOption === "resumen" && <ResumenDinero />}
                {selectedOption === "rendiciones" && <RendicionJefe />}
            </div>
        </div>
    );
}
