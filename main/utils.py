import pandas as pd

def cargar(archivo):
    df = pd.read_excel(archivo)
    df = df[df['JORNADA'] == 'DIURNO']
    campus = df['CAMPUS_SEDE'].unique().tolist()
    departamento = df[['DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    semestre = df['SEMESTRE'].unique().tolist()
    asignaturas = df[['SIGLA', 'DEPARTAMENTO', 'SEMESTRE', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    paralelos = df[['SIGLA', 'PARALELO', 'SEMESTRE', 'DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    return campus, departamento, semestre, asignaturas, paralelos