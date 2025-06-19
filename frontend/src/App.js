// App.js
import React from 'react';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import { Home } from './Pages/Home';
import { SignUp } from './Pages/Login/Signup';
import { Login } from './Pages/Login/Login';
import { SelectProfile } from './Pages/selectProfile';
import { VerSolicitudesF } from './Pages/funcionario/verSolicitudes'
import { VerSolicitudesI } from './Pages/administrador/verSolicitudes'

import { Dashboard } from './Pages/Dashboard';
import { DashboardFuncionario } from './Pages/funcionario/dashboard-funcionario';
import { DatosAsignatura } from './Pages/funcionario/solicitud/DatosAsignatura';
import { DatosVisita } from './Pages/funcionario/solicitud/DatosVisita';
import { VerSolicitudesS } from './Pages/subdirector/verSolicitudes';
import { DashboardSubdirector } from './Pages/subdirector/dashboard-subdirector';
//import { ListadoAsistentes } from './Pages/funcionario/solicitud/ListadoAsistentes';
import { TipoCotizacion } from './Pages/funcionario/solicitud/TipoCotizacion';
import { Presupuestos } from './Pages/Presupuesto';
import { DetalleSolicitudI } from './Pages/administrador/detalleSolicitud';
import { DetalleSolicitudS } from './Pages/subdirector/detalleSolicitud';
import { DashboardDirector } from './Pages/director/dashboard-director';
import { VerSolicitudesD } from './Pages/director/verSolicitudesD';
import { DetalleCotizacion } from './Pages/director/cotizacion';
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
import {DashboardAdministrador} from "./Pages/administrador/dashboard-administrador";
import {SolicitudI} from "./Pages/administrador/solicitud/solicitudI";

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
          path="/funcionario/solicitud/:id"
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
        path="/administrador/dashboard"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <DashboardAdministrador />
          </PrivateRoute>
        }
      />

      <Route
        path="/administrador/solicitudes"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <VerSolicitudesI />
          </PrivateRoute>
        }
      />

      <Route
        path="/administrador/solicitudes/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <DetalleSolicitudI />
          </PrivateRoute>
        }
      />

      <Route
        path="/presupuestos"
        element={
          <PrivateRoute allowedRoles={["funcionario", "administrador"]}>
            <Presupuestos />
          </PrivateRoute>
        }
      />
        <Route
        path="/subdireccion/dashboard"
        element={
          <PrivateRoute allowedRoles={["subdirector"]}>
            <DashboardSubdirector />
          </PrivateRoute>
        }
      />
        <Route
        path="/subdireccion/solicitudes"
        element={
          <PrivateRoute allowedRoles={["subdirector"]}>
            <VerSolicitudesS />
          </PrivateRoute>
        }
      />
        <Route
        path="/subdireccion/solicitudes/:id"
        element={
          <PrivateRoute allowedRoles={["subdirector"]}>
            <DetalleSolicitudS />
          </PrivateRoute>
        }
      />
        <Route
        path="/subdireccion/presupuestos"
        element={
          <PrivateRoute allowedRoles={["subdirector"]}>
            <Presupuestos />
          </PrivateRoute>
        }
      />

      <Route
        path="/director/dashboard"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <DashboardDirector />
          </PrivateRoute>
        }
      /> 

    <Route
        path="/director/solicitudes"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <VerSolicitudesD />
          </PrivateRoute>
        }
      /> 
    <Route
        path="/director/solicitudes/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <DetalleCotizacion />
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
