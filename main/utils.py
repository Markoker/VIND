import pandas as pd


def cargar(archivo):
    df = pd.read_excel(archivo)

    print(df.columns)

    df = df[df['JORNADA'] == 'DIURNO']
    campus = df['CAMPUS_SEDE'].unique().tolist()
    departamento = df[['DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    semestre = df['SEMESTRE'].unique().tolist()
    asignaturas = df[['SIGLA', 'ASIGNATURA', 'DEPARTAMENTO', 'SEMESTRE', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    paralelos = df[['SIGLA', 'ASIGNATURA', 'PARALELO', 'SEMESTRE', 'DEPARTAMENTO', 'CAMPUS_SEDE']].drop_duplicates().to_dict('records')
    return campus, departamento, semestre, asignaturas, paralelos

