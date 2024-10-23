from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .utils import cargar
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from random import randint
import pandas as pd


def check_user_role(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if role == 'funcionario' and request.user.is_funcionario:
                    return view_func(request, *args, **kwargs)
                elif role == 'ingeniero' and request.user.is_ingeniero:
                    return view_func(request, *args, **kwargs)
                elif role == 'subdirector' and request.user.is_subdirector:
                    return view_func(request, *args, **kwargs)
                elif role == 'director' and request.user.is_director:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse("No tienes permisos para acceder a esta vista")
            else:
                return redirect('login')

        return wrapper

    return decorator


def landing_view(request):
    unidades_opciones = list(UnidadAcademica.objects.all().values_list('nombre', 'emplazamiento__nombre'))

    print(unidades_opciones)
    return render(request, 'landing.html')


def login_view(request):
    if request.method == 'POST':
        login_form = EmailAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        login_form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': login_form})


@login_required
def home_view(request):
    print(request.user.is_funcionario)
    print(request.user.is_ingeniero)
    print(request.user.is_subdirector)
    print(request.user.is_director)

    roles = {
        'is_funcionario': request.user.is_funcionario,
        'is_ingeniero': request.user.is_ingeniero,
        'is_subdirector': request.user.is_subdirector,
        'is_director': request.user.is_director,
    }

    return render(request, 'home.html', {'roles': roles})


def funcionario_view(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user)

    data = {
        'solicitudes': solicitudes
    }

    return render(request, 'funcionario.html', data)


# region FORMULARIO SOLICITUD

def asignatura_view(request):
    campus_opciones = list(Emplazamiento.objects.all().values_list('nombre', flat=True))
    unidades_opciones = list(UnidadAcademica.objects.all().values_list('id_unidad_academica', 'nombre'))
    semestre_opciones = list(range(1, 3))
    asignaturas_opciones = list(Asignatura.objects.all().values_list('id_asignatura', 'nombre'))
    paralelos_opciones = list(Asignatura.objects.all().distinct('paralelo').values_list('paralelo', flat=True))

    if request.method == 'POST':
        form = AsignaturaForm(request.POST,
                              campus_opciones=campus_opciones,
                              unidades_opciones=unidades_opciones,
                              semestre_opciones=semestre_opciones,
                              asignaturas_opciones=asignaturas_opciones,
                              paralelos_opciones=paralelos_opciones)
        if form.is_valid():
            data = form.cleaned_data

            request.session['asignatura_data'] = data['asignatura']

            return redirect('visita_view')
    else:
        form = AsignaturaForm(campus_opciones=campus_opciones,
                              unidades_opciones=unidades_opciones,
                              semestre_opciones=semestre_opciones,
                              asignaturas_opciones=asignaturas_opciones,
                              paralelos_opciones=paralelos_opciones)
    return render(request, 'asignatura.html', {'form': form})


def visita_view(request):
    print(request.session['asignatura_data'])
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita_data = form.cleaned_data
            visita_data['fecha'] = visita_data['fecha'].strftime('%Y-%m-%d')
            request.session['visita_data'] = visita_data
            return redirect('profesor_view')
    else:
        form = VisitaForm()
    return render(request, 'visita.html', {'form': form})


def profesor_view(request):
    print(request.session['asignatura_data'])
    print(request.session['visita_data'])
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            request.session['profesor_data'] = form.cleaned_data

            return redirect('estudiantes_view')
    else:
        form = ProfesorForm()
    return render(request, 'profesor.html', {'form': form})


# endregion

def estudiantes_view(request):
    print(request.session['asignatura_data'])
    print(request.session['visita_data'])
    print(request.session['profesor_data'])

    if request.method == 'POST':
        form = EstudiantesForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            archivo = data['listado']
            extension = archivo.name.split('.')[-1]

            if extension == 'csv':
                df = pd.read_csv(archivo)
            elif extension == 'xlsx':
                df = pd.read_excel(archivo)
            else:
                return HttpResponse("Archivo no soportado")

            datos = df.to_dict('records')

            estudiantes_data = {
                'datos': datos,
                'cantidad': df.shape[0]
            }

            request.session['estudiantes_data'] = estudiantes_data

            return redirect('cotizacion_view')
    else:
        form = EstudiantesForm()
    return render(request, 'estudiantes.html', {'form': form})


def cotizacion_view(request):
    print(request.session['asignatura_data'])
    print(request.session['visita_data'])
    print(request.session['profesor_data'])
    print(request.session['estudiantes_data'])
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse("Cotización guardada")
    else:
        form = CotizacionForm()

    return render(request, 'cotizacion.html', {'form': form})


def get_unidades(request):
    campus = request.GET.get('campus')

    unidades = list(
        UnidadAcademica.objects.filter(emplazamiento__nombre=campus).values_list('id_unidad_academica', 'nombre'))
    print(unidades)

    return JsonResponse({'unidades_academicas': unidades})


def get_asignaturas(request):
    unidad = request.GET.get('unidad')
    semestre = request.GET.get('semestre')

    asignaturas = Asignatura.objects.filter(departamento_id=unidad, semestre=semestre).values_list('id_asignatura',
                                                                                                   'nombre').distinct(
        'nombre')

    asignaturas = list(asignaturas)

    return JsonResponse({'asignaturas': asignaturas})


def get_paralelos(request):
    asignatura = request.GET.get('asignatura')

    a = Asignatura.objects.get(id_asignatura=asignatura)

    paralelos = Asignatura.objects.filter(sigla=a.sigla, departamento_id=a.departamento.id_unidad_academica,
                                          semestre=a.semestre).values_list('paralelo', flat=True)
    paralelos = list(paralelos)

    # Retornamos los paralelos en formato JSON
    return JsonResponse({'paralelos': paralelos})


def visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Visita guardada")
    form = VisitaForm()
    return render(request, 'visita.html', {'form': form})


# region UTILIDADES
def load_users(request):
    # Remove all users
    Usuario.objects.all().delete()

    Usuario.objects.create_user(email="juan.tapia@usm.cl", password="9876ABCD", rut="12345678-9")
    Usuario.objects.create_user(email="pedro.urdemales@usm.cl", password="1234ABCD", rut="87654321-0")
    # Usuario.objects.create_superuser(email="marco.repetto@usm.cl", password="1234", rut="21489358-4")

    return redirect('login')


def poblar_bbdd(request):
    campus, departamento, semestre, asignaturas, paralelos = cargar('main/data/REPORTE ASIGNATURAS 2024.xlsx')

    for emplazamiento in campus:
        emplazamiento = emplazamiento.strip()

        sigla = ''.join([word[0] for word in emplazamiento.split()]).upper()

        e = Emplazamiento(sigla=sigla, nombre=emplazamiento)

        if Emplazamiento.objects.filter(sigla=sigla).exists():
            print(f"Emplazamiento {sigla} ya existe")
            continue

        e.save()
        print(f"Emplazamiento {sigla} creado")

    print()
    # Clear the UnidadAcademica table
    UnidadAcademica.objects.all().delete()

    for unidad in departamento:
        depto = unidad['DEPARTAMENTO'].strip()
        emplazamiento = unidad['CAMPUS_SEDE'].strip()

        print(f"Depto: {depto}, Emplazamiento: {emplazamiento}")

        # Get the id of the emplazamiento
        emplazamiento = Emplazamiento.objects.get(nombre=emplazamiento)

        presupuesto = randint(100000, 10000000)
        gasto = randint(0, presupuesto)

        u = UnidadAcademica(nombre=depto,
                            emplazamiento=emplazamiento,
                            presupuesto=presupuesto,
                            gasto=gasto)

        if UnidadAcademica.objects.filter(nombre=depto, emplazamiento=emplazamiento.id_emplazamiento).exists():
            print(f"Unidad {depto} ({emplazamiento}) ya existe")
            continue

        u.save()
        print(f"Unidad {depto} ({emplazamiento}) creada")

    print()
    Asignatura.objects.all().delete()
    for asignatura in paralelos:
        sigla = str(asignatura['SIGLA']).strip()
        nombre = asignatura['ASIGNATURA'].strip()
        semestre = asignatura['SEMESTRE']
        paralelo = asignatura['PARALELO']
        depto = asignatura['DEPARTAMENTO'].strip()
        emplazamiento = asignatura['CAMPUS_SEDE'].strip()

        print(
            f"Asignatura: {nombre}, Sigla: {sigla}, Semestre: {semestre}, Paralelo: {paralelo}, Depto: {depto}, Emplazamiento: {emplazamiento}")

        unidad_academica = UnidadAcademica.objects.get(nombre=depto,
                                                       emplazamiento=Emplazamiento.objects.get(nombre=emplazamiento))

        a = Asignatura(sigla=sigla,
                       nombre=nombre,
                       semestre=semestre,
                       departamento=unidad_academica,
                       paralelo=paralelo)

        if Asignatura.objects.filter(sigla=sigla,
                                     paralelo=paralelo,
                                     semestre=semestre).exists():
            print(f"Asignatura {nombre} ya existe")
            continue

        a.save()
        print(f"Asignatura {nombre} creada")

    return redirect('landing')


def poblar_bbdd_u(request):
    nombres = ['Juan', 'Pedro', 'Diego', 'Marco', 'Javier', 'Felipe', 'Cristian', 'Rodrigo', 'Andres', 'Carlos']
    apellidos = ['Perez', 'Gonzalez', 'Diaz', 'Gomez', 'Torres', 'Vargas', 'Silva', 'Molina', 'Soto', 'Lopez']

    for i in range(30):
        nombre = nombres[randint(0, len(nombres) - 1)]
        apellido = apellidos[randint(0, len(apellidos) - 1)]
        rut = str(randint(10000000, 25000000)) + '-' + str(randint(0, 9))
        email = f"{nombre}.{apellido}@usm.cl"
        telefono = str(randint(10000000, 99999999))

        c = 1
        while Usuario.objects.filter(email=email).exists():
            email = f"{nombre}.{apellido}{c}@usm.cl"
            c += 1

        u = Usuario(email=email, rut=rut, telefono=telefono, first_name=nombre, last_name=apellido)
        u.set_password('1234')
        u.save()
    return redirect('landing')


def poblar_bbdd_s(request):
    # Random date between today and 2025
    from datetime import date, timedelta
    from random import randrange

    for i in range(300):
        # Solicitud
        # Random date between today and 2025
        start_date = date.today()
        end_date = date(2025, 1, 1)
        delta = end_date - start_date
        random_days = randrange(delta.days)
        fecha = start_date + timedelta(days=random_days)

        estado = 'Pendiente'

        # Random asignatura
        asignatura = Asignatura.objects.all().order_by('?').first()
        usuario = Usuario.objects.all().order_by('?').first()

        s = Solicitud(fecha=fecha, estado=estado, asignatura=asignatura, usuario=usuario)
        s.save()

    return redirect('landing')
# endregion
