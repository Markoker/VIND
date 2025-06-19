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
//import { ListadoAsistentes } from './Pages/funcionario/solicitud/ListadoAsistentes';
import { TipoCotizacion } from './Pages/funcionario/solicitud/TipoCotizacion';
import { Presupuestos } from './Pages/Presupuesto';
import { DetalleSolicitudI } from './Pages/administrador/detalleSolicitud';
import { RevisarSolicitud } from './Pages/administrador/revisarSolicitud';
import { DashboardDirector } from './Pages/director/dashboard-director';
import { VerSolicitudesD } from './Pages/director/verSolicitudesD';
import { DetalleSolicitudD } from './Pages/director/detalleSolicitud';
import { FirmarCotizacion } from './Pages/director/firmarCotizacion';
import { DetalleSolicitudF } from './Pages/funcionario/detalleSolicitud';
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

// Nuevas importaciones para páginas por ítem
// Administrador
import { SubirFacturaColacionAdmin } from './Pages/administrador/subirFacturaColacion';
import { SubirFacturaTrasladoAdmin } from './Pages/administrador/subirFacturaTraslado';
import { DetalleColacionAdmin } from './Pages/administrador/detalleColacion';
import { DetalleTrasladoAdmin } from './Pages/administrador/detalleTraslado';

// Director
import { FirmarCotizacionColacionDirector } from './Pages/director/firmarCotizacionColacion';
import { FirmarCotizacionTrasladoDirector } from './Pages/director/firmarCotizacionTraslado';
import { FirmarFacturaDirector } from './Pages/director/firmarFactura';
import { DetalleCotizacionDirector } from './Pages/director/detalleCotizacion';
import { DetalleColacionDirector } from './Pages/director/detalleColacion';
import { DetalleTrasladoDirector } from './Pages/director/detalleTraslado';


// Funcionario
import { SubirFacturaFuncionario } from './Pages/funcionario/subirFactura';
import { DetalleCotizacionFuncionario } from './Pages/funcionario/detalleCotizacion';

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
        path="/administrador/revisar-solicitud/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <RevisarSolicitud />
          </PrivateRoute>
        }
      />

      {/* Nuevas rutas para administrador por ítem */}
      <Route
        path="/administrador/subir-factura-colacion/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <SubirFacturaColacionAdmin />
          </PrivateRoute>
        }
      />

      <Route
        path="/administrador/subir-factura-traslado/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <SubirFacturaTrasladoAdmin />
          </PrivateRoute>
        }
      />

      <Route
        path="/administrador/detalle-colacion/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <DetalleColacionAdmin />
          </PrivateRoute>
        }
      />

      <Route
        path="/administrador/detalle-traslado/:id"
        element={
          <PrivateRoute allowedRoles={["administrador"]}>
            <DetalleTrasladoAdmin />
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
            <DetalleSolicitudD />
          </PrivateRoute>
        }
      />

    <Route
        path="/director/firmar-cotizacion/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <FirmarCotizacion />
          </PrivateRoute>
        }
      />

    {/* Nuevas rutas para director por ítem */}
    <Route
        path="/director/firmar-cotizacion-colacion/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <FirmarCotizacionColacionDirector />
          </PrivateRoute>
        }
      />

    <Route
        path="/director/firmar-cotizacion-traslado/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <FirmarCotizacionTrasladoDirector />
          </PrivateRoute>
        }
      />

    <Route
        path="/director/firmar-factura/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <FirmarFacturaDirector />
          </PrivateRoute>
        }
      />

    <Route
        path="/director/detalle-cotizacion/:id"
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <DetalleCotizacionDirector />
          </PrivateRoute>
        }
      />

    <Route
        path="/funcionario/solicitudes/:id"
        element={
          <PrivateRoute allowedRoles={["funcionario"]}>
            <DetalleSolicitudF />
          </PrivateRoute>
        }
      />

    {/* Nuevas rutas para funcionario por ítem */}
    <Route
        path="/funcionario/subir-factura/:id"
        element={
          <PrivateRoute allowedRoles={["funcionario"]}>
            <SubirFacturaFuncionario />
          </PrivateRoute>
        }
      />

    <Route
        path="/funcionario/detalle-cotizacion/:id"
        element={
          <PrivateRoute allowedRoles={["funcionario"]}>
            <DetalleCotizacionFuncionario />
          </PrivateRoute>
        }
      />

      <Route
        path='/director/detalle-colacion/:id'
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <DetalleColacionDirector />
          </PrivateRoute>
        }
      />

      <Route
        path='/director/detalle-traslado/:id'
        element={
          <PrivateRoute allowedRoles={["director"]}>
            <DetalleTrasladoDirector />
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
