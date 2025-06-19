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
    const [isAdministrador, setIsAdministrador] = React.useState(false);
    const [isDirector, setIsDirector] = React.useState(false);

    React.useEffect(() => {
        fetch(`http://localhost:8000/usuario/${rut}/rol`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setIsFuncionario(data.funcionario);
            setIsAdministrador(data.administrador);
            setIsDirector(data.director);

            // Guardar un array con los roles del usuario en localStorage
            const roles = [];
            if (data.funcionario) roles.push("funcionario");
            if (data.administrador) roles.push("administrador");
            if (data.director) roles.push("director");
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
                    <Link to="/funcionario/dashboard" className="home-button" onClick={() => localStorage.setItem("perfilActivo", "funcionario")}>Ir a Funcionario</Link>
                </div>}
                {isAdministrador && <div className="home-section">
                    <h2>Administrador</h2>
                    <Link to="/administrador/dashboard" className="home-button" onClick={() => localStorage.setItem("perfilActivo", "administrador")}>Ir a Administrador</Link>
                </div>}
                {isDirector && <div className="home-section">
                    <h2>Director</h2>
                    <Link to="/director/dashboard" className="home-button" onClick={() => localStorage.setItem("perfilActivo", "director")}>Ir a Director</Link>
                </div>}
            </div>
        </div>
    );
}