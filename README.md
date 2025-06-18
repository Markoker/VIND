# VIND: Sistema de Gestión de Solicitudes y Rendiciones

VIND es una plataforma web para la gestión de solicitudes, cotizaciones y rendiciones de gastos en el contexto universitario, permitiendo la interacción de distintos perfiles de usuario (funcionario, administrador y dirección) y la administración de presupuestos, visitas y documentos asociados.

---

## Tecnologías Utilizadas

* **Backend:** Python 3.12, FastAPI, Uvicorn, PostgreSQL, Pandas, Openpyxl
* **Frontend:** React, Material UI, React Router, Axios
* **Base de datos:** PostgreSQL
* **Contenedores:** Docker

---

## Estructura del Proyecto

```
VIND/
  backend/         # API REST y lógica de negocio (FastAPI)
    app/
      main.py      # Punto de entrada del backend
      poblar_bd.py # Script para poblar la base de datos
      querys/      # Módulos de consulta y lógica de negocio
      uploads/     # Archivos subidos (PDFs de cotizaciones, facturas, etc.)
    Dockerfile     # Imagen Docker del backend
  db/
    init.sql       # Script de inicialización de la base de datos PostgreSQL
  frontend/        # Aplicación web (React)
    src/           # Código fuente del frontend
      Pages/       # Páginas por perfil de usuario
    Dockerfile     # Imagen Docker del frontend
```

---

## Instalación y Ejecución

### Requisitos previos

* Docker y Docker Compose
* (Opcional) Python 3.12 y Node.js si se desea correr sin Docker

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd VIND
```

### 2. Configuración de la base de datos

* El archivo `db/init.sql` contiene la estructura de tablas y relaciones necesarias.

### 3. Backend (API)

#### Con Docker

```bash
cd backend
docker build -t vind-backend .
docker run -p 8000:8000 vind-backend
```

#### Manualmente

```bash
cd backend/app
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend (React)

#### Con Docker

```bash
cd frontend
docker build -t vind-frontend .
docker run -p 3000:3000 vind-frontend
```

#### Manualmente

```bash
cd frontend
npm install
npm start
```

### 5. Acceso

* Frontend: [http://localhost:3000](http://localhost:3000)
* Backend (API): [http://localhost:8000](http://localhost:8000)

---

## Nuevo Flujo de Solicitudes (Actualizado)

### Roles:

* **FUNC**: Funcionario que ingresa la solicitud
* **ADM**: Administrador que revisa datos y carga factura
* **DIR**: Dirección que firma cotización y factura

### Etapas del Proceso:

1. **FUNC** ingresa solicitud: rellena formulario con información general, adjunta cotización de colación y/o traslado (ambos opcionales, pero al menos uno debe existir). La solicitud se guarda con estado `pendiente_revision`.
2. **ADM** revisa la solicitud: valida presupuesto, documentos y datos. Si hay errores, puede devolverla al funcionario con observaciones. Si todo está correcto, cambia el estado a `pendiente_firma`.
3. **DIR** firma la cotización: si se aprueba, el estado cambia a `esperando_factura`. Si se rechaza, vuelve a `pendiente_revision`.
4. **FUNC/ADM** carga la(s) factura(s): cada ítem (colación/traslado) puede tener factura distinta. El estado del ítem cambia a `factura_ingresada`.
5. **DIR** firma la(s) factura(s): sube el PDF firmado, estado pasa a `pendiente_pago`.
6. **ADM** envía a pago: estado final `pagado`.

Cada ítem de la solicitud (colación/traslado) mantiene su estado de forma independiente.

### Reglas y Estructura de Datos:

* Una `solicitud` puede tener 1 o 2 ítems: `colación` y/o `traslado`.
* Cada `item` tiene su propio flujo y estado.
* Toda acción de cambio de estado queda registrada en una tabla `HistorialEstadoItem`.
* Los usuarios `FUNC` pueden estar asociados a una o más `UnidadesAcademicas`.
* Cada `UnidadAcademica` pertenece a un solo `Emplazamiento`.
* Los usuarios `ADM` y `DIR` tienen acceso completo.

---

## Descripción de Componentes

### Backend

* **main.py**: API REST principal
* **querys/**: consultas SQL y lógica de negocio por entidad
* **uploads/**: carpeta de PDFs subidos
* **poblar\_bd.py**: script para poblar la BD con datos iniciales

### Frontend

* **Pages/**: páginas por perfil

  * FUNC: formulario solicitud, seguimiento
  * ADM: revisión de solicitudes, carga factura, envío a pago
  * DIR: firma cotización y factura

---

## Ejemplo de Uso Básico

1. FUNC inicia sesión y crea una solicitud.
2. ADM revisa la solicitud y la aprueba.
3. DIR firma la cotización.
4. ADM o FUNC carga factura(s).
5. DIR firma la factura.
6. ADM marca como pagada.

---

## To Do

* [ ] Refactorizar modelo de datos según nuevo flujo
* [ ] Implementar tabla `HistorialEstadoItem`
* [ ] Separar estados por ítem (colación y traslado)
* [ ] Página de seguimiento de estado por solicitud
* [ ] Validación por rol en frontend
* [ ] Subida de facturas firmadas por parte de Dirección
* [ ] Registro de comentarios y timestamps en todos los cambios de estado

---

## Licencia

MIT License
