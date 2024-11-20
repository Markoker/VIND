import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    // Lógica de logout
    localStorage.removeItem('userRole'); // Borra el rol del usuario
    localStorage.removeItem('userRut'); // Borra el id del usuario

    // Redirigir al usuario a la página de login
    navigate('/login');
  }, [navigate]);

  return null; // Este componente no renderiza nada
}
