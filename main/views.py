from django.shortcuts import render, redirect
from .forms import *
from .models import *
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
            return HttpResponse("Visita guardada")
    else:
        form = ProfesorForm()
    return render(request, 'profesor.html', {'form': form})


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

def cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Cotizacion guardada")
    form = CotizacionForm()
    return render(request, 'cotizacion.html', {'form': form})

def unidad_academica_view(request):
    if request.method == 'POST':
        form = UnidadAcademicaForm(request.POST)
        if form.is_valid():
            emplazamiento = form.cleaned_data.get('emplazamiento')
            unidad_academica = form.cleaned_data.get('unidad_academica')
            carrera = form.cleaned_data.get('carrera')

            registro = UnidadAcademica(emplazamiento=emplazamiento)
            registro.save()
            return HttpResponse("Unidad Academica guardada")
    else:
        form = UnidadAcademicaForm()
    return render(request, 'unidad_academica.html', {'form': form})


def get_edificios(request):
    campus_id = request.GET.get('campus_id')
    edificios = Edificio.objects.filter(campus_id=campus_id).order_by('nombre')
    return render(request, 'hr/dropdown_list_options.html', {'items': edificios})


def get_carreras(request):
    edificio_id = request.GET.get('edificio_id')
    carreras = Carrera.objects.filter(edificio_id=edificio_id).order_by('nombre')
    return render(request, 'hr/dropdown_list_options.html', {'items': carreras})

def visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Visita guardada")
    form = VisitaForm()
    return render(request, 'visita.html', {'form': form})
'''
def ua(request):
    submission = False
    if request.method == 'POST':
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ua/?submit=True')
    else:
        form = CarreraForm()
        if 'submit' in request.GET:
            submission = True
    return render(request, 'ua.html', {'form': form, 'submission': submission})
'''