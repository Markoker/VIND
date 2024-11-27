// App.js
import React from 'react';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import { Home } from './Pages/Home';
import { SignUp } from './Pages/Login/Signup';
import { Login } from './Pages/Login/Login';
import { selectProfile } from './Pages/selectProfile';
import { Solicitudes } from './Pages/funcionario/verSolicitudes'
/*
import { Dashboard } from './Pages/Dashboard';
import { DashboardContador } from './Pages/contador/Dashboard-contador';
import { DashboardTrabajador } from './Pages/trabajador/Dashboard-trabajador';
import { DashboardJefe } from './Pages/jefe/Dashboard-jefe';
import { PrivateRoute } from './PrivateRoute';
import { RevisarRendicion } from './Pages/contador/RevisarRendicion';
import { SubirRendicion } from './Pages/trabajador/SubirRendicion';  
import { MisRendiciones } from './Pages/trabajador/MisRendiciones';
import { RendicionJefe } from './Pages/jefe/ResumenDinero';
import { RendicionDetalles } from './Pages/jefe/RendicionDetalles';
import { RevisarDevolucion } from './Pages/contador/RevisarDevolucion';
import { Logout } from './Pages/Login/logout';
*/

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />

      <Route
        path="/dashboard-funcionario"
        element={
          <PrivateRoute allowedRoles={["trabajador"]}>
            <DashboardTrabajador />
          </PrivateRoute>
        }
      />

      <Route
        path="/dashboard-contador"
        element={
          <PrivateRoute allowedRoles={["contador"]}>
            <DashboardContador />
          </PrivateRoute>
        }
      />

      <Route
          path="/dashboard-jefe"
          element={
              <PrivateRoute allowedRoles={["jefe"]}>
                  <DashboardJefe />
              </PrivateRoute>
          }
      />
      <Route path="/devoluciones/:idDevolucion" element={<RevisarDevolucion />} />
      <Route path="/rendiciones/detalles/:rendicion_id" element={<PrivateRoute allowedRoles={['jefe']}><RendicionDetalles /></PrivateRoute>} />
      <Route path="/subir-rendicion" element={<SubirRendicion />} />
      <Route path="/mis-rendiciones" element={<MisRendiciones />} />
      <Route path="/rendiciones/:idRendicion" element={<RevisarRendicion />} />
      <Route path="/logout" element={<Logout />} />
    </Routes>
  );
}

export default App;
