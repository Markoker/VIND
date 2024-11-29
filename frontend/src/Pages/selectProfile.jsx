// selectProfile.jsx
import React from 'react';
import { Link } from 'react-router-dom';

export function SelectProfile(){
    // Esta página debería mostrar un mensaje de bienvenida y un botón para ir a cada perfil correspondiente
    // al usuario que inició sesión (extraidos desde localhost:8000/usuario/{rut}/rol)

    // Obtenemos el rut del usuario desde localStorage
    const rut = localStorage.getItem("userRut");

    // Obtenemos el rol del usuario desde la API
    const [isFuncionario, setIsFuncionario] = React.useState(false);
    const [isIngeniero, setIsIngeniero] = React.useState(false);
    const [isDirector, setIsDirector] = React.useState(false);
    const [isSubdirector, setIsSubdirector] = React.useState(false);

    React.useEffect(() => {
        fetch(`http://localhost:8000/usuario/${rut}/rol`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setIsFuncionario(data.funcionario);
            setIsIngeniero(data.ingeniero);
            setIsDirector(data.director);
            setIsSubdirector(data.subdirector);

            // Guardar un array con los roles del usuario en localStorage
            const roles = [];
            if (data.funcionario) roles.push("funcionario");
            if (data.ingeniero) roles.push("ingeniero");
            if (data.director) roles.push("director");
            if (data.subdirector) roles.push("subdirector");
            localStorage.setItem("userRoles", JSON.stringify(roles));
        })
        .catch(error => console.error(error));
    }, [rut]);

    return (
        <div className="home-container">
            <h1 className="home-title">Bienvenid@ al sistema de rendición de gastos</h1>
            <div className="home-content">
                {isFuncionario && <div className="home-section">
                    <h2>Funcionario</h2>
                    <Link to="/dashboard-funcionario" className="home-button">Ir a Funcionario</Link>
                </div>}
                {isIngeniero && <div className="home-section">
                    <h2>Ingeniero</h2>
                    <Link to="/dashboard-ingeniero" className="home-button">Ir a Ingeniero</Link>
                </div>}
                {isDirector && <div className="home-section">
                    <h2>Director</h2>
                    <Link to="/dashboard-director" className="home-button">Ir a Director</Link>
                </div>}
                {isSubdirector && <div className="home-section">
                    <h2>Subdirector</h2>
                    <Link to="/dashboard-subdirector" className="home-button">Ir a Subdirector</Link>
                </div>}
            </div>
        </div>
    );
}