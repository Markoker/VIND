import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

export function Presupuestos() {
  const [presupuestos, setPresupuestos] = useState([]);
  const userRut = localStorage.getItem('userRut');
  const perfilActivo = localStorage.getItem("perfilActivo");
  const navigate = useNavigate();

  useEffect(() => {
    if (userRut && perfilActivo) {
      console.log(`http://localhost:8000/presupuestos/${userRut}?perfil=${perfilActivo}`);
      axios.get(`http://localhost:8000/presupuestos/${userRut}?perfil=${perfilActivo}`)
        .then(res => setPresupuestos(res.data))
        .catch(err => {
          console.error(err);
          alert("No se pudieron cargar los presupuestos");
        });
    }
  }, [userRut, perfilActivo]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Presupuesto por Unidad Académica</h2>
      <table className="w-full border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Unidad Académica</th>
            <th className="p-2 border">Emplazamiento</th> 
            <th className="p-2 border">Presupuesto Total</th>
            <th className="p-2 border">Gasto Actual</th>
            <th className="p-2 border">Disponible</th>
          </tr>
        </thead>
        <tbody>
          {presupuestos.map((unidad, idx) => (
            <tr key={idx}>
              <td className="p-2 border">{unidad.nombre}</td>
              <td className="p-2 border">{unidad.emplazamiento}</td>
              <td className="p-2 border">${unidad.presupuesto.toLocaleString()}</td>
              <td className="p-2 border">${unidad.gasto.toLocaleString()}</td>
              <td className="p-2 border">${(unidad.presupuesto - unidad.gasto).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="volver-btn" onClick={() => navigate(-1)}>Volver</button>
    </div>
  );
};

