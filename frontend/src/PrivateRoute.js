import React from 'react';
import { Navigate } from 'react-router-dom';

export function PrivateRoute({ children, allowedRoles }) {
  const userRole = localStorage.getItem('userRoles');  // Recupera el rol desde localStorage
  console.log("User role:", userRole);

  for (let i = 0; i < allowedRoles.length; i++) {
    if (userRole.includes(allowedRoles[i])) {
      return children;  // Si el usuario tiene el rol adecuado, muestra el contenido
    }
  }

  // Si el usuario no tiene el rol adecuado, redirige a la página de login
  return <Navigate to="/login" />;
}
