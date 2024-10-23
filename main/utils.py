import pandas as pd
import random

adjetivos = ["Global", "Innovative", "Dynamic", "Smart", "Bright", "Creative", "Eco", "Digital", "Tech", "Next",
             "Advanced"]
sustantivos = ["Solutions", "Systems", "Enterprises", "Ventures", "Industries", "Labs", "Partners", "Corporation",
               "Group", "Technologies"]


# Función para generar nombres ficticios de empresas
def generar_empresa():
    adj = random.choice(adjetivos)
    sust = random.choice(sustantivos)
    nombre = f"{adj} {sust}"
    rut = f"{random.randint(10000000, 99999999)}-{random.randint(0, 9)}"
    correo = f"{adj.lower()}.{sust.lower()}@{random.choice(['gmail.com', 'hotmail.com', 'yahoo.com'])}"
    return {
        'nombre': nombre,
        'rut': rut,
        'correo': correo
    }


def generar_lugar():
    ciudades = ["Santiago", "Valparaíso", "Concepción", "Temuco", "Antofagasta", "Arica", "Iquique", "Punta Arenas",
                "Rancagua", "Curicó", "Los Ángeles", "Osorno", "Puerto Montt", "Calama", "Copiapó", "La Serena",
                "Coquimbo", "Chillán", "Quillota", "San Antonio", "San Felipe", "Talca", "Linares", "Vallenar",
                "Angol", "Villarrica", "Pucón", "Valdivia", "Castro", "Ancud", "Puerto Natales", "Coyhaique",
                "Puerto Aysén", "Punta Arenas", "Porvenir", "Cabo de Hornos", "Viña del Mar", "Quilpué", "Villa Alemana",
                "Limache", "La Calera", "Los Andes", "San Felipe", "Rancagua", "Machalí", "Graneros", "San Fernando"]
    return f"Calle {random.randint(1, 1000)}, {random.choice(ciudades)}"

def cargar(archivo):
    df = pd.read_excel(archivo)

    print(df.columns)

    df = df[df['JORNADA'] == 'DIURNO']
    campus = df['CAMPUS_SEDE'].unique().tolist()
    departamento = df[['DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    semestre = df['SEMESTRE'].unique().tolist()
    asignaturas = df[['SIGLA', 'ASIGNATURA', 'DEPARTAMENTO', 'SEMESTRE', 'CAMPUS_SEDE']].drop_duplicates().to_dict(
        'records')
    paralelos = df[
        ['SIGLA', 'ASIGNATURA', 'PARALELO', 'SEMESTRE', 'DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict(
        'records')
    return campus, departamento, semestre, asignaturas, paralelos
