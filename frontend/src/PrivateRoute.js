import React from 'react';
import { Navigate } from 'react-router-dom';

export function PrivateRoute({ children, allowedRoles }) {
  const userRole = localStorage.getItem('userRole');  // Recupera el rol desde localStorage
  console.log("User role:", userRole);

  // Verifica si el rol del usuario está en la lista de roles permitidos
  if (allowedRoles.includes(userRole)) {
    return children;  // Permite el acceso si el rol coincide
  }

  // Si el usuario no tiene el rol adecuado, redirige a la página de login
  return <Navigate to="/login" />;
}
