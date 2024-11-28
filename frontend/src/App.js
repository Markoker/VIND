// App.js
import React from 'react';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import { Home } from './Pages/Home';
import { SignUp } from './Pages/Login/Signup';
import { Login } from './Pages/Login/Login';
import { SelectProfile } from './Pages/selectProfile';
import { VerSolicitudes } from './Pages/funcionario/verSolicitudes'

import { Dashboard } from './Pages/Dashboard';
import { DashboardFuncionario } from './Pages/funcionario/dashboard-funcionario';
import { DatosAsignatura } from './Pages/funcionario/solicitud/DatosAsignatura';
import { DatosVisita } from './Pages/funcionario/solicitud/DatosVisita';
import { ListadoAsistentes } from './Pages/funcionario/solicitud/ListadoAsistentes';
import { TipoCotizacion } from './Pages/funcionario/solicitud/TipoCotizacion';

import { DashboardContador } from './Pages/contador/Dashboard-contador';
import { DashboardJefe } from './Pages/jefe/Dashboard-jefe';
/*
import { DashboardContador } from './Pages/contador/Dashboard-contador';
import { DashboardTrabajador } from './Pages/trabajador/Dashboard-trabajador';
import { DashboardJefe } from './Pages/jefe/Dashboard-jefe';
import { RevisarRendicion } from './Pages/contador/RevisarRendicion';
import { SubirRendicion } from './Pages/trabajador/SubirRendicion';  
import { MisRendiciones } from './Pages/trabajador/MisRendiciones';
import { RendicionJefe } from './Pages/jefe/ResumenDinero';
import { RendicionDetalles } from './Pages/jefe/RendicionDetalles';
import { RevisarDevolucion } from './Pages/contador/RevisarDevolucion';
*/
import { PrivateRoute } from './PrivateRoute';
import { Logout } from './Pages/Login/logout';

function App() {
  return (
    <Routes>
      <Route path="/" element={<SelectProfile />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />

      <Route
        path="/dashboard-funcionario"
        element={
          <PrivateRoute allowedRoles={["trabajador"]}>
            <DashboardFuncionario />
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
      <Route path="/ver-solicitudes" element={<VerSolicitudes />} />
      <Route path="/crear-solicitud/asignatura" element={<DatosAsignatura />} />
      <Route path="/crear-solicitud/visita" element={<DatosVisita />} />
      <Route path="/crear-solicitud/asistentes" element={<ListadoAsistentes />} />
      <Route path="/crear-solicitud/cotizacion" element={<TipoCotizacion />} />
      <Route path="/logout" element={<Logout />} />
    </Routes>
  );
}

export default App;
