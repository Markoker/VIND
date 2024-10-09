from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import *
from .models import *
from .utils import cargar
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.dateparse import parse_date
from django.contrib import messages


# Create your views here.
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