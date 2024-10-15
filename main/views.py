from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import *
from .models import *
from .utils import cargar
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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


def load_users(request):
    # Remove all users
    Usuario.objects.all().delete()

    Usuario.objects.create_user(email="juan.tapia@usm.cl", password="9876ABCD", rut="12345678-9")
    Usuario.objects.create_user(email="pedro.urdemales@usm.cl", password="1234ABCD", rut="87654321-0")
    # Usuario.objects.create_superuser(email="marco.repetto@usm.cl", password="1234", rut="21489358-4")

    return redirect('login')


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


@check_user_role('funcionario')
def funcionario_view(request):
    return HttpResponse("Funcionario")


def form(request):
    return render(request, 'test_form.html')

def visita_view(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita_data = form.cleaned_data
            visita_data['fecha'] = visita_data['fecha'].strftime('%Y-%m-%d')
            request.session['visita_data'] = visita_data
            return redirect('estudiantes_view')
    else:
        form = VisitaForm()
    return render(request, 'visita.html', {'form': form})

def estudiantes_view(request):
    if request.method == 'POST':
        form = EstudiantesForm(request.POST)
        if form.is_valid():
            request.session['estudiantes_data'] = form.cleaned_data
            return redirect('profesor_view')
    else:
        form = EstudiantesForm()
    return render(request, 'estudiantes.html', {'form': form})

def profesor_view(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            '''
            visita_data = request.session.get('visita_data')
            # Parse the date string back to a date object
            visita_data['fecha'] = parse_date(visita_data['fecha'])
            profesor = form.save()
            messages.success(request, 'Los datos han sido enviados correctamente.')
            visita = Visita(
                nombre_empresa=visita_data.get('nombre_empresa'),
                fecha=visita_data.get('fecha'),
                lugar=visita_data.get('lugar'),
                profesor_encargado=profesor
            )
            visita.save()
            request.session.flush()
            '''
            form.save()
            return redirect('cotizacion_view')
    else:
        form = ProfesorForm()
    return render(request, 'profesor.html', {'form': form})

def asignatura_view(request):
    archivo = 'main/data/REPORTE ASIGNATURAS 2024.xlsx'
    campus_opciones, unidades_opciones, semestre_opciones, asignaturas_opciones, paralelos_opciones = cargar(archivo)
    if request.method == 'POST':
        form = AsignaturaForm(request.POST,
                                campus_opciones=campus_opciones,
                                unidades_opciones=unidades_opciones,
                                semestre_opciones=semestre_opciones,
                                asignaturas_opciones=asignaturas_opciones,
                                paralelos_opciones=paralelos_opciones)
        if form.is_valid():
            form.save()
            return redirect('visita_view')
    else:
        form = AsignaturaForm(campus_opciones=campus_opciones,
                                unidades_opciones=unidades_opciones,
                                semestre_opciones=semestre_opciones,
                                asignaturas_opciones=asignaturas_opciones,
                                paralelos_opciones=paralelos_opciones)
    return render(request, 'asignatura.html', {'form': form})

def get_unidades(request):
    campus = request.GET.get('campus')
    _, unidades, _, _, _ = cargar('main/data/REPORTE ASIGNATURAS 2024.xlsx')
    unidades = [unidad['DEPARTAMENTO'] for unidad in unidades if unidad['CAMPUS_SEDE'] == campus]
    return JsonResponse({'unidades_academicas': unidades})

def get_asignaturas(request):
    unidad = request.GET.get('unidad')
    semestre = request.GET.get('semestre')
    campus = request.GET.get('campus')
    print(f"Unidad: {unidad}, Semestre: {semestre}")
    _, _, _, asignaturas, _ = cargar('main/data/REPORTE ASIGNATURAS 2024.xlsx')
    asignaturas_f = [
        {'sigla': asignatura['SIGLA'], 'nombre': asignatura['SIGLA']}  # Devuelve la sigla como valor
        for asignatura in asignaturas
        if asignatura['DEPARTAMENTO'] == unidad and asignatura['SEMESTRE'] == int(semestre) and asignatura['CAMPUS_SEDE'] == campus
    ]
    if not asignaturas_f:
        print(f"No se encontraron asignaturas para Unidad: {unidad} y Semestre: {semestre}")

    return JsonResponse({'asignaturas': asignaturas_f})

def get_paralelos(request):
    asignatura = request.GET.get('asignatura')
    unidad_academica = request.GET.get('unidad')
    semestre = request.GET.get('semestre')
    campus = request.GET.get('campus')
    print(f"Asignatura: {asignatura}, Unidad: {unidad_academica}, Semestre: {semestre}")
    _, _, _, _, paralelos = cargar('main/data/REPORTE ASIGNATURAS 2024.xlsx')
    paralelos_f = [
        paralelo['PARALELO']
        for paralelo in paralelos
        if paralelo['SIGLA'] == asignatura and paralelo['SEMESTRE'] == int(semestre) and paralelo['DEPARTAMENTO'] == unidad_academica and paralelo['CAMPUS_SEDE'] == campus
    ]

    # Si no hay paralelos, lo notificamos
    if not paralelos_f:
        print(f"No se encontraron paralelos para Asignatura: {asignatura}, Unidad: {unidad_academica}, Semestre: {semestre}")

    # Retornamos los paralelos en formato JSON
    return JsonResponse({'paralelos': paralelos_f})



def solicitud(request):
    submission = False
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/solicitud/?submit=True')
    else:
        form = SolicitudForm()
        if 'submit' in request.GET:
            submission = True
    form = SolicitudForm()
    return render(request, 'solicitud.html', {'form': form, 'submission': submission})

def cotizacion_view(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Cotización guardada")
    else:
        form = CotizacionForm()

    return render(request, 'cotizacion.html', {'form': form})


def visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Visita guardada")
    form = VisitaForm()
    return render(request, 'visita.html', {'form': form})