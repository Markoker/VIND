const data = {
    1: {
        'Arquitectura': ['Arquitectura'], 
        'Electrónica ': ['Ingeniería Civil Electrónica', 'Ingeniería Civil Telemática'], 
        'Física ': ['Ingeniería Civil Física', 'Licenciatura en Astrofísica', 'Licenciatura en Física'], 
        'Industrias': ['Ingeniería Civil Industrial'], 'Informática': ['Ingeniería Civil en Informática'], 
        'Ingeniería Comercial': ['Ingeniería Comercial'], 
        'Ingeniería Eléctrica': ['Ingeniería Civil Eléctrica', 'Ingeniería Eléctrica'], 
        'Ingeniería Mecánica': ['Ingeniería Civil Mecánica'], 
        'Ingeniería Metalúrgica y de Materiales': ['Ingeniería Civil Metalúrgica'], 
        'Ingeniería Quimica y Ambiental': ['Ingeniería Civil Ambiental', 'Ingeniería Civil Química', 'Ingeniería Civil Química y Ingeniería Civil Ambiental'], 
        'Ingeniería en Diseño': ['Ingeniería en Diseño de Productos'], 
        'Matemática': ['Ingeniería Civil Matemática'], 
        'Obras Civiles': ['Construcción Civil', 'Ingeniería Civil'], 
        'Química': ['Licenciatura en Ciencias mención Química']}, 
    5: {
        'Construcción y Prevención de Riesgos': ['Ingeniería en Prevención de Riesgos Laborales y Ambientales (Diurno) ', 'Técnico Universitario Dibujante Proyectista', 'Técnico Universitario en Construcción'], 
        'Electricidad': ['Técnico Universitario en Automatización y Control ', 'Técnico Universitario en Electricidad '], 
        'Electrónica e Informática': ['Ingeniería en Informática (IBT)', 'Técnico Universitario Robotica y Mecatrónica', 'Técnico Universitario en Electrónica', 'Técnico Universitario en Informática', 'Técnico Universitario en Telecomunicaciones y Redes'], 
        'Ingeniería Comercial': ['Ingeniería Comercial', 'Técnico Universitario Administración de Empresas'], 
        'Mecánica': ['Ingeniería en Mantenimiento Industrial Diurno y Vespertino', 'Técnico Universitario en Mantenimiento Industrial ', 'Técnico Universitario en Mecánica Automotriz ', 'Técnico Universitario en Mecánica Industrial'], 
        'Química y Medio Ambiente ': ['Ingeniería en Biotecnología (IBT)', 'Técnico Universitario en Control del Medio Ambiente', 'Técnico Universitario en Química con Mencion en Química Analítica', 'Técnico Universitario en Química con Mencion en Química Industrial']
    }, 
    2: {
        'Arquitectura': ['Arquitectura'], 
        'Electrónica ': ['Ingeniería Civil Telemática'], 
        'Física ': ['Ingeniería Civil Física', 'Licenciatura en Astrofísica', 'Licenciatura en Física'], 
        'Informática': ['Ingeniería Civil en Informática'], 
        'Ingeniería Eléctrica': ['Ingeniería Civil Eléctrica'], 
        'Ingeniería Mecánica': ['Ingeniería Civil Mecánica'], 
        'Ingeniería Metalúrgica y de Materiales': ['Ingeniería Civil en Minas'], 
        'Ingeniería Quimica y Ambiental': ['Ingeniería Civil Química'], 
        'Ingeniería en Diseño': ['Ingeniería en Diseño de Productos'], 
        'Matemática': ['Ingeniería Civil Matemática'], 
        'Obras Civiles': ['Ingeniería Civil']
    }, 
    3: {'Aeronáutica': ['Ingeniería en Aviación Comercial'], 
        'Industrias': ['Ingeniería Civil Industrial'], 
        'Ingeniería Comercial': ['Ingeniería Comercial', 'Técnico Universitario Administración de Empresas']
    }, 
    4: {
        'Construcción y Prevención de Riesgos': ['Ingeniería en Prevención de Riesgos Laborales y Ambientales (Diurno)', 'Técnico Universitario en Construcción'], 
        'Diseño y Manufactura': ['Ingeniería en Fabricación y Diseño Industrial', 'Técnico Universitario en Proyectos de Ingenieria'], 
        'Electrotecnia e Informática': ['Ingeniería en Informática (IBT)', 'Técnico Universitario en Electricidad ', 'Técnico Universitario en Electrónica', 'Técnico Universitario en Informática', 'Técnico Universitario en Telecomunicaciones y Redes'], 
        'Ingeniería Comercial': ['Técnico Universitario Administración de Empresas'], 
        'Mecánica': ['Ingeniería en Mantenimiento Industrial c/ base Tecnológica Diurno', 'Técnico Universitario en Energías Renovables', 'Técnico Universitario en Mantenimiento Industrial', 'Técnico Universitario en Mecánica Automotriz', 'Técnico Universitario en Mecánica Industrial', 'Técnico Universitario en Minería y Metalurgia'], 
        'Química y Medio Ambiente ': ['Ingeniería en Biotecnología ', 'Técnico Universitario en Alimentos', 'Técnico Universitario en Biotecnología', 'Técnico Universitario en Control del Medio Ambiente', 'Técnico Universitario en Química con Mencion en Química Analítica']
    }
}

function crear_unidad_academica() {
    const sede = document.getElementById("emplazamiento").value;
    const unidadSelect = document.getElementById("unidad_academica");
    unidadSelect.innerHTML = '<option>Selecciona un departamento</option>';

    if (data[sede]){
        for (const unidad in data[sede]) {
            const option = document.createElement("option");
            option.text = unidad;
            option.value = unidad;
            unidadSelect.appendChild(option);
        }
    }
    crear_carreras();
}

function crear_carreras() {
    const sede = document.getElementById("emplazamiento").value;
    const unidad = document.getElementById("unidad_academica").value;
    const carreraSelect = document.getElementById("carrera");
    carreraSelect.innerHTML = '<option>Selecciona una carrera</option>';

    if(data[sede] && data[sede][unidad]){
        data[sede][unidad].forEach(carrera => {
            const option = document.createElement("option");
            option.text = carrera;
            option.value = carrera;
            carreraSelect.appendChild(option);
        });
    }
}    
const hoy = new Date().toISOString().split('T')[0];
document.getElementById('fecha').setAttribute('min', hoy);