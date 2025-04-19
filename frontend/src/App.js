// App.js
import React from 'react';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import { Home } from './Pages/Home';
import { SignUp } from './Pages/Login/Signup';
import { Login } from './Pages/Login/Login';
import { SelectProfile } from './Pages/selectProfile';
import { VerSolicitudesF } from './Pages/funcionario/verSolicitudes'
import { VerSolicitudesI } from './Pages/ingeniero/verSolicitudes'

import { Dashboard } from './Pages/Dashboard';
import { DashboardFuncionario } from './Pages/funcionario/dashboard-funcionario';
import { DatosAsignatura } from './Pages/funcionario/solicitud/DatosAsignatura';
import { DatosVisita } from './Pages/funcionario/solicitud/DatosVisita';
import { ListadoAsistentes } from './Pages/funcionario/solicitud/ListadoAsistentes';
import { TipoCotizacion } from './Pages/funcionario/solicitud/TipoCotizacion';

// import { DashboardContador } from './Pages/contador/Dashboard-contador';
// import { DashboardJefe } from './Pages/jefe/Dashboard-jefe';
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
import {Encargados} from "./Pages/funcionario/solicitud/encargados";
import {DashboardIngeniero} from "./Pages/ingeniero/dashboard-ingeniero";
import {SolicitudI} from "./Pages/ingeniero/solicitud/solicitudI";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home/>} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/home" element={<SelectProfile />} />

      <Route
        path="/funcionario/dashboard"
        element={
          <PrivateRoute allowedRoles={["funcionario"]}>
            <DashboardFuncionario />
          </PrivateRoute>
        }
      />

      <Route
          path="/funcionario/solicitudes"
          element={
              <PrivateRoute allowedRoles={["funcionario"]}>
                <VerSolicitudesF />
              </PrivateRoute>
            }
      />
      <Route
          path="/funcionario/crear-solicitud/asignatura"
          element={
              <PrivateRoute allowedRoles={["funcionario"]}>
                  <DatosAsignatura />
              </PrivateRoute>
          }
      />
      <Route
          path="/funcionario/crear-solicitud/visita"
          element={
              <PrivateRoute allowedRoles={["funcionario"]}>
                  <DatosVisita />
              </PrivateRoute>
          }
      />
      <Route
          path="/funcionario/crear-solicitud/encargados"
          element={
              <PrivateRoute allowedRoles={["funcionario"]}>
                  <Encargados />
              </PrivateRoute>
          }
      />
      <Route
          path="/funcionario/crear-solicitud/cotizacion"
          element={
              <PrivateRoute allowedRoles={["funcionario"]}>
                  <TipoCotizacion />
              </PrivateRoute>
          }
      />

      <Route
        path="/ingeniero/dashboard"
        element={
          <PrivateRoute allowedRoles={["ingeniero"]}>
            <DashboardIngeniero />
          </PrivateRoute>
        }
      />

      <Route
        path="/ingeniero/solicitudes"
        element={
          <PrivateRoute allowedRoles={["ingeniero"]}>
            <VerSolicitudesI />
          </PrivateRoute>
        }
      />

      <Route
          path="/logout"
          element={<Logout />}
      />
    </Routes>
  );
}

export default App;
