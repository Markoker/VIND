from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .utils import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.core.files import File
from random import randint
from datetime import datetime
import pandas as pd
import json
import uuid
import os


def check_user_role(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if role == 'funcionario':
                    unidad = kwargs.get('unidad', None)
                    if Funcionario.objects.filter(usuario=request.user,
                                                  unidad_academica__id_unidad_academica=unidad).exists():
                        return view_func(request, *args, **kwargs)
                elif role == 'ingeniero':
                    emplazamiento = kwargs.get('emplazamiento', None)
                    if Ingeniero.objects.filter(usuario=request.user,
                                                emplazamiento__id_emplazamiento=emplazamiento).exists():
                        return view_func(request, *args, **kwargs)
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


def logout(request):
    logout(request)
    return redirect('landing')


@login_required
def home_view(request):
    data = {}

    # Get all the UnidadAcademica objects that the user is associated with
    funcionario_en = (Funcionario.objects
                      .filter(usuario=request.user)
                      .values_list('unidad_academica', flat=True)
                      .distinct())
    ingeniero_en = (Ingeniero.objects
                    .filter(usuario=request.user)
                    .values_list('emplazamiento', flat=True)
                    .distinct())
    subdirector_en = (Subdirector.objects
                      .filter(usuario=request.user)
                      .values_list('unidad_academica', flat=True)
                      .distinct())
    director_en = (Director.objects
                   .filter(usuario=request.user)
                   .values_list('emplazamiento', flat=True)
                   .distinct())

    funcionario_en = (UnidadAcademica.objects
                      .filter(id_unidad_academica__in=funcionario_en))
    ingeniero_en = (Emplazamiento.objects
                    .filter(id_emplazamiento__in=ingeniero_en))
    subdirector_en = (UnidadAcademica.objects
                      .filter(id_unidad_academica__in=subdirector_en))
    director_en = (Emplazamiento.objects
                   .filter(id_emplazamiento__in=director_en))

    data['funcionario_en'] = funcionario_en
    data['ingeniero_en'] = ingeniero_en
    data['subdirector_en'] = subdirector_en
    data['director_en'] = director_en

    return render(request, 'home.html', data)


@check_user_role('funcionario')
def enviadas_view(request, unidad):
    data = {
        "unidad": unidad
    }

    if request.method == 'GET':
        unidades_academicas = Funcionario.objects.filter(usuario_id=request.user.rut).values_list('unidad_academica_id', flat=True)

        solicitudes = Solicitud.objects.filter(
            usuario=request.user,
            asignatura__departamento__id_unidad_academica__in=unidades_academicas
        )
        # region FILTROS
        estado = request.GET.get('estado')
        if estado:
            solicitudes = solicitudes.filter(estado=estado)
        else:
            estado = ""

        tipo = request.GET.get('tipo')
        if tipo:
            solicitudes = solicitudes.filter(cotizacion__tipo=tipo)
        else:
            tipo = ""

        rango_fecha = request.GET.get('rango_fecha')
        fecha = ""
        if rango_fecha:
            fecha = request.GET.get('fecha')

            if rango_fecha == 'antes':
                solicitudes = solicitudes.filter(fecha__lte=fecha)
            elif rango_fecha == 'despues':
                solicitudes = solicitudes.filter(fecha__gte=fecha)
        else:
            rango_fecha = ""

        monto_min = request.GET.get('monto_min')
        monto_max = request.GET.get('monto_max')
        if monto_min and monto_max:
            solicitudes = solicitudes.filter(cotizacion__monto__gte=monto_min, cotizacion__monto__lte=monto_max)
        else:
            monto_min = 0
            monto_max = 10000000

        data["filtros"] = {
            'estado': estado,
            'tipo': tipo,
            'rango_fecha': rango_fecha,
            'fecha': fecha,
            'monto_min': monto_min,
            'monto_max': monto_max
        }
        # endregion

        # region SORT_BY
        sort_by = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')
        if sort_by and sort_order:
            if sort_by == "monto":
                sort_by = "cotizacion__monto"
            if sort_order == 'asc':
                solicitudes = solicitudes.order_by(sort_by)
            elif sort_order == 'desc':
                solicitudes = solicitudes.order_by(f'-{sort_by}')
        else:
            sort_by = ""
            sort_order = ""

        data['solicitudes'] = solicitudes

    return render(request, 'funcionario.html', data)


# region FORMULARIO SOLICITUD
def asignatura_view(request):
    campus_opciones = list(Emplazamiento.objects.all().values_list('nombre', flat=True))
    unidades_opciones = list(UnidadAcademica.objects.all().values_list('id_unidad_academica', 'nombre'))
    semestre_opciones = [1,2] 
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

@login_required
def confirmacion_view(request):
    asignatura_data = request.session.get('asignatura_data')
    visita_data = request.session.get('visita_data')
    profesor_data = request.session.get('profesor_data')
    estudiantes_data = request.session.get('estudiantes_data')
    cotizacion_data = request.session.get('cotizacion_data')

    # Retrieve related instances for foreign key references
    asignatura = Asignatura.objects.get(id_asignatura=asignatura_data)
    usuario = request.user  # Usamos el usuario autenticado

    # Save Visita instance
    visita = Visita.objects.create(
        nombre_empresa=visita_data['nombre_empresa'],
        fecha=visita_data['fecha'],
        lugar=visita_data['lugar']
    )

    # Save Profesor instance
    profesor = Profesor.objects.create(
        visita=visita,
        rut=profesor_data['rut'],
        nombre=profesor_data['nombre'],
        email=profesor_data['email']
    )

    # Initialize Traslado and Colacion instances as needed
    traslado = None
    colacion = None

    # Save Traslado if type includes "traslado"
    if cotizacion_data['tipo'] in ['Solo traslado', 'Traslado y colacion']:
        traslado = Traslado.objects.create(
            nombre_proveedor=cotizacion_data['nombre_proveedor'],
            rut_proveedor=cotizacion_data['rut_proveedor'],
            correo_proveedor=cotizacion_data['correo_proveedor'],
            monto=cotizacion_data['monto']
        )

        # Attach files to traslado if paths exist
        for i in range(1, 4):
            path_key = f'cotizacion_{i}_path'
            if path_key in cotizacion_data and default_storage.exists(cotizacion_data[path_key]):
                original_file_name = cotizacion_data[path_key]
                # Usar os.path.basename() para obtener solo el nombre del archivo
                safe_file_name = os.path.basename(original_file_name)
                # Generar un nombre único si es necesario
                safe_file_name = f"{uuid.uuid4()}{os.path.splitext(safe_file_name)[1]}"
                
                with default_storage.open(original_file_name, 'rb') as f:
                    getattr(traslado, f'cotizacion_{i}').save(safe_file_name, File(f))
                default_storage.delete(original_file_name)

    # Save Colacion if type includes "colacion"
    if cotizacion_data['tipo'] in ['Solo colacion', 'Traslado y colacion']:
        if cotizacion_data['tipo_subvencion'] == 'reembolso':
            # Create Reembolso instance if needed
            reembolso = Reembolso.objects.create(
                monto=cotizacion_data['monto'],
                fecha_pago=visita_data['fecha'],
                estado="Pendiente",
                usuario=usuario
            )
            colacion = Colacion.objects.create(
                tipo_subvencion=cotizacion_data['tipo_subvencion'],
                monto=cotizacion_data['monto'],
                reembolso=reembolso
            )
        else:
            # Save colacion with file if tipo_subvencion is "presupuesto"
            colacion = Colacion.objects.create(
                tipo_subvencion=cotizacion_data['tipo_subvencion'],
                monto=cotizacion_data['monto'],
                nombre_proveedor=cotizacion_data['nombre_proveedor'],
                rut_proveedor=cotizacion_data['rut_proveedor'],
                correo_proveedor=cotizacion_data['correo_proveedor']
            )
            if 'cotizacion_1_path' in cotizacion_data and default_storage.exists(cotizacion_data['cotizacion_1_path']):
                original_file_name = cotizacion_data['cotizacion_1_path']
                safe_file_name = os.path.basename(original_file_name)
                safe_file_name = f"{uuid.uuid4()}{os.path.splitext(safe_file_name)[1]}"
                
                with default_storage.open(original_file_name, 'rb') as f:
                    colacion.cotizacion_1.save(safe_file_name, File(f))
                default_storage.delete(original_file_name)

    # Save Cotizacion instance
    cotizacion = Cotizacion.objects.create(
        tipo=cotizacion_data['tipo'],
        estado="Pendiente",
        monto=cotizacion_data['monto'],
        traslado=traslado,
        colacion=colacion
    )

    # Save Solicitud instance
    solicitud = Solicitud.objects.create(
        fecha=visita_data['fecha'],
        estado="Pendiente",
        descripcion=visita_data.get('descripcion', 'Sin descripción'),
        usuario=usuario,
        asignatura=asignatura,
        visita=visita,
        cotizacion=cotizacion
    )

    # Clear session data after saving
    request.session.pop('asignatura_data', None)
    request.session.pop('visita_data', None)
    request.session.pop('profesor_data', None)
    request.session.pop('estudiantes_data', None)
    request.session.pop('cotizacion_data', None)

    return render(request, 'cot_guardada.html')


def cotizacion_view(request):
    asignatura_data = request.session.get('asignatura_data')
    visita_data = request.session.get('visita_data')
    profesor_data = request.session.get('profesor_data')
    estudiantes_data = request.session.get('estudiantes_data')
    cantidad = estudiantes_data.get('cantidad')

    data = {}

    data['cantidad'] = cantidad

    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES, cantidad=cantidad)
        if form.is_valid():
            cotizacion_data = form.cleaned_data
            
            # Save files temporarily and store their paths in the session
            if 'cotizacion_1' in request.FILES:
                file_1 = request.FILES['cotizacion_1']
                path_1 = default_storage.save(f"temp/{file_1.name}", file_1)
                cotizacion_data['cotizacion_1_path'] = path_1

            if 'cotizacion_2' in request.FILES:
                file_2 = request.FILES['cotizacion_2']
                path_2 = default_storage.save(f"temp/{file_2.name}", file_2)
                cotizacion_data['cotizacion_2_path'] = path_2

            if 'cotizacion_3' in request.FILES:
                file_3 = request.FILES['cotizacion_3']
                path_3 = default_storage.save(f"temp/{file_3.name}", file_3)
                cotizacion_data['cotizacion_3_path'] = path_3

            non_serializable_keys = ['cotizacion_1', 'cotizacion_2', 'cotizacion_3']
            for key in non_serializable_keys:
                if key in cotizacion_data:
                    del cotizacion_data[key]

            # Debugging: Attempt to serialize cotizacion_data to check for non-serializable data
            try:
                json.dumps(cotizacion_data)  # Attempt JSON serialization
                print("cotizacion_data is JSON serializable.")
            except TypeError as e:
                print("Non-serializable data found in cotizacion_data:", e)
                raise  # Reraise the error to halt execution for debugging

            # Store the cleaned data without file objects
            request.session['cotizacion_data'] = cotizacion_data
            return redirect('confirmacion_view')
    else:
        form = CotizacionForm()

    data['form'] = form
    
    return render(request, 'cotizacion.html', data)


def get_unidades(request):
    campus = request.GET.get('campus')

    unidades = list(
        UnidadAcademica.objects.filter(emplazamiento__nombre=campus).values_list('id_unidad_academica', 'nombre'))
    print(unidades)

    return JsonResponse({'unidades_academicas': unidades})


def get_asignaturas(request):
    unidad = request.GET.get('unidad')
    semestre = request.GET.get('semestre')
    #asignaturas = Asignatura.objects.filter(departamento__id=unidad, semestre=semestre).values_list('id_asignatura', 'nombre')

    asignaturas = Asignatura.objects.filter(departamento_id=unidad, semestre=semestre).values_list('id_asignatura',
                                                                                                   'nombre', 'sigla').order_by('sigla').distinct('sigla')

    asignaturas = list(asignaturas)
    for i in range(len(asignaturas)):
        print(asignaturas[i])
    return JsonResponse({'asignaturas': asignaturas})


def get_paralelos(request):
    asignatura = request.GET.get('asignatura')

    a = Asignatura.objects.get(id_asignatura=asignatura)

    paralelos = Asignatura.objects.filter(sigla=a.sigla, departamento_id=a.departamento.id_unidad_academica,
                                          semestre=a.semestre).values_list('paralelo', flat=True)
    paralelos = list(paralelos)

    # Retornamos los paralelos en formato JSON
    return JsonResponse({'paralelos': paralelos})


# endregion

# region INGENIER
@check_user_role('ingeniero')
def recibidas_view(request, emplazamiento):
    data = {
        "emplazamiento": emplazamiento
    }

    if request.method == 'GET':
        solicitudes = Solicitud.objects.filter(asignatura__departamento__emplazamiento__id_emplazamiento=emplazamiento,
                                               estado=2)

        tipo = request.GET.get('tipo')
        if tipo:
            solicitudes = solicitudes.filter(cotizacion__tipo=tipo)
        else:
            tipo = ""

        rango_fecha = request.GET.get('rango_fecha')
        fecha = ""
        if rango_fecha:
            fecha = request.GET.get('fecha')

            if rango_fecha == 'antes':
                solicitudes = solicitudes.filter(fecha__lte=fecha)
            elif rango_fecha == 'despues':
                solicitudes = solicitudes.filter(fecha__gte=fecha)
        else:
            rango_fecha = ""

        monto_min = request.GET.get('monto_min')
        monto_max = request.GET.get('monto_max')
        if monto_min and monto_max:
            solicitudes = solicitudes.filter(cotizacion__monto__gte=monto_min, cotizacion__monto__lte=monto_max)
        else:
            monto_min = 0
            monto_max = 10000000

        data["filtros"] = {
            'tipo': tipo,
            'rango_fecha': rango_fecha,
            'fecha': fecha,
            'monto_min': monto_min,
            'monto_max': monto_max
        }
        # endregion

        # region SORT_BY
        sort_by = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')
        if sort_by and sort_order:
            if sort_by == "monto":
                sort_by = "cotizacion__monto"
            if sort_order == 'asc':
                solicitudes = solicitudes.order_by(sort_by)
            elif sort_order == 'desc':
                solicitudes = solicitudes.order_by(f'-{sort_by}')
        else:
            sort_by = ""
            sort_order = ""

        data['solicitudes'] = solicitudes

    return render(request, 'ingeniero/ingeniero.html', data)

'''
@check_user_role('ingeniero')
def historial_view(request, emplazamiento):
    return render(request, "vista.html")
'''


@check_user_role('ingeniero')
def validar_ingeniero(request, emplazamiento, solicitud):
    data = {'emplazamiento': emplazamiento, 'solicitud': solicitud}

    if request.method == 'GET':
        solicitud = Solicitud.objects.filter(id_solicitud=solicitud).first()

        data['solicitud'] = solicitud

        visita = solicitud.visita

        visitantes = Visitante.objects.filter(visita=visita)
        data['visitantes'] = visitantes
    elif request.method == 'POST':
        decision = request.POST.get('decision')
        print(decision)

        if decision == "0":
            print("Rechazada")
            soli = Solicitud.objects.get(id_solicitud=solicitud)
            hist = HistorialEstadoSolicitud(usuario_decision=request.user,
                                            solicitud=soli,
                                            estado_anterior=soli.estado,
                                            decision='rechazada',
                                            fecha_decision=datetime.now())

            soli.estado = 0
            soli.save()
        else:
            print("Aprobada")
            soli = Solicitud.objects.get(id_solicitud=solicitud)
            hist = HistorialEstadoSolicitud(usuario_decision= request.user,
                                            solicitud=soli,
                                            estado_anterior=soli.estado,
                                            decision='aprobada',
                                            fecha_decision=datetime.now())

            soli.estado = 3
            soli.save()

        hist.save()

        return redirect('requerimientosTabular', emplazamiento=emplazamiento)

    return render(request, 'ingeniero/validar_ingeniero.html', data)

# endregion

# region SUBDIRECTOR
def presupuestoTabular_view(request, unidad):
    data = {
        "unidad": UnidadAcademica.objects.get(id_unidad_academica=unidad)
    }

    if request.method == 'GET':
        solicitudes = Solicitud.objects.filter(asignatura__departamento__id_unidad_academica=unidad, estado=3)

        tipo = request.GET.get('tipo')
        if tipo:
            solicitudes = solicitudes.filter(cotizacion__tipo=tipo)
        else:
            tipo = ""

        rango_fecha = request.GET.get('rango_fecha')
        fecha = ""
        if rango_fecha:
            fecha = request.GET.get('fecha')

            if rango_fecha == 'antes':
                solicitudes = solicitudes.filter(fecha__lte=fecha)
            elif rango_fecha == 'despues':
                solicitudes = solicitudes.filter(fecha__gte=fecha)
        else:
            rango_fecha = ""

        monto_min = request.GET.get('monto_min')
        monto_max = request.GET.get('monto_max')
        if monto_min and monto_max:
            solicitudes = solicitudes.filter(cotizacion__monto__gte=monto_min, cotizacion__monto__lte=monto_max)
        else:
            monto_min = 0
            monto_max = 10000000

        data["filtros"] = {
            'tipo': tipo,
            'rango_fecha': rango_fecha,
            'fecha': fecha,
            'monto_min': monto_min,
            'monto_max': monto_max
        }
        # endregion

        # region SORT_BY
        sort_by = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')
        if sort_by and sort_order:
            if sort_by == "monto":
                sort_by = "cotizacion__monto"
            if sort_order == 'asc':
                solicitudes = solicitudes.order_by(sort_by)
            elif sort_order == 'desc':
                solicitudes = solicitudes.order_by(f'-{sort_by}')
        else:
            sort_by = ""
            sort_order = ""

        data['solicitudes'] = solicitudes

    return render(request, 'subdirector/presupuestoTabular.html', data)
# endregion

# region UTILIDADES
def load_users(request):
    # Remove all users
    Usuario.objects.all().delete()

    Usuario.objects.create_user(email="juan.tapia@usm.cl", password="9876ABCD", rut="12345678-9")
    Usuario.objects.create_user(email="pedro.urdemales@usm.cl", password="1234ABCD", rut="87654321-0")
    # Usuario.objects.create_superuser(email="marco.repetto@usm.cl", password="1234", rut="21489358-4")

    return redirect('login')


def correo_rechazo(request):
    subject = 'Su solicitud para la visita bla bla ha sido rechazada'

    message = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec purus nec nunc'
               'consequat fermentum. Nullam nec purus nec nunc consequat fermentum. Nullam nec purus nec nunc consequat fermentum.'
               'Nullam nec purus nec nunc consequat fermentum. Nullam nec purus nec nunc consequat fermentum.')

    from_email = 'correo_emisor@usm.cl'  # Puedes usar cualquier dirección aquí
    recipient_list = ['correo_receptor@usm.cl']  # Lista de destinatarios

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Correo enviado")


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


nombres = ['Juan', 'Pedro', 'Diego', 'Marco', 'Javier', 'Felipe', 'Cristian', 'Rodrigo', 'Andres', 'Carlos']
apellidos = ['Perez', 'Gonzalez', 'Diaz', 'Gomez', 'Torres', 'Vargas', 'Silva', 'Molina', 'Soto', 'Lopez']


def poblar_bbdd_u(request):
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

    # Delete all data
    Visita.objects.all().delete()
    Solicitud.objects.all().delete()
    Profesor.objects.all().delete()
    Visitante.objects.all().delete()
    Cotizacion.objects.all().delete()
    Traslado.objects.all().delete()
    Colacion.objects.all().delete()

    for i in range(302):
        # Profesor
        nombre = nombres[randint(0, len(nombres) - 1)]
        apellido = apellidos[randint(0, len(apellidos) - 1)]
        rut = str(randint(10000000, 25000000)) + '-' + str(randint(0, 9))
        email = f"{nombre}.{apellido}@usm.cl"

        p = Profesor(rut=rut, nombre=f"{nombre} {apellido}", email=email)
        p.save()

        # Visita
        nombre_empresa = generar_empresa()['nombre']
        fecha_visita = date.today() + timedelta(days=randrange(120))
        lugar = generar_lugar()

        v = Visita(nombre_empresa=nombre_empresa, fecha=fecha_visita, lugar=lugar, profesor=p)
        v.save()

        # Visitantes
        cantidad = randint(15, 60)
        for j in range(cantidad):
            nombre = nombres[randint(0, len(nombres) - 1)]
            apellido = apellidos[randint(0, len(apellidos) - 1)]
            rut = str(randint(10000000, 25000000)) + '-' + str(randint(0, 9))
            email = f"{nombre}.{apellido}@usm.cl"

            visitante = Visitante(rut=rut, nombre=f"{nombre} {apellido}", email=email, visita=v)
            visitante.save()

        # Cotización
        TIPO_CHOICES = [
            ('Solo traslado', 'Sólo traslado'),
            ('Solo colacion', 'Sólo colación'),
            ('Traslado y colacion', 'Traslado y colaciones'),
        ]

        tipo = random.choice(TIPO_CHOICES)[0]
        estado = 'Pendiente'

        empresa_traslado = generar_empresa()
        monto_traslado = 0

        t = None
        c = None

        if tipo == 'Solo traslado' or tipo == 'Traslado y colacion':
            monto_traslado = randint(10000, 10000000)

            t = Traslado(nombre_proveedor=empresa_traslado['nombre'],
                         rut_proveedor=empresa_traslado['rut'],
                         correo_proveedor=empresa_traslado['correo'],
                         monto=monto_traslado)

            if monto_traslado > 1000000:
                with open('/home/sofia/vind3/VIND/main/data/test.pdf', 'rb') as f:
                    t.cotizacion_1.save('test.pdf', f)
                    t.cotizacion_2.save('test.pdf', f)
                    t.cotizacion_3.save('test.pdf', f)
            else:
                with open('/home/sofia/vind3/VIND/main/data/test.pdf', 'rb') as f:
                    t.cotizacion_1.save('test.pdf', f)

            t.save()

        monto_colacion = 0
        if tipo == 'Solo colacion' or tipo == 'Traslado y colacion':
            SUBVENCION_CHOICES = [
                ('reembolso', 'Reembolso'),
                ('presupuesto', 'Previa presupuestación')
            ]

            tipo_subvencion = random.choice(SUBVENCION_CHOICES)[0]

            monto_colacion = randint(20000, 500000)

            if tipo_subvencion == 'reembolso':
                r = Reembolso(monto=monto_colacion,
                              fecha_pago=fecha_visita + timedelta(days=randrange(30)),
                              estado="Pendiente",
                              # Random user
                              usuario=Usuario.objects.all().order_by('?').first())
                r.save()

                c = Colacion(tipo_subvencion=tipo_subvencion,
                             monto=monto_colacion,
                             reembolso=r)
                c.save()
            else:
                empresa_colacion = generar_empresa()
                c = Colacion(tipo_subvencion=tipo_subvencion,
                             monto=monto_colacion,
                             nombre_proveedor=empresa_colacion['nombre'],
                             rut_proveedor=empresa_colacion['rut'],
                             correo_proveedor=empresa_colacion['correo'])

                with open('/home/sofia/vind3/VIND/main/data/test.pdf', 'rb') as f:
                    c.cotizacion_1.save('test.pdf', f)

                c.save()

        cotizacion = Cotizacion(tipo=tipo, estado=estado, traslado=t, colacion=c, monto=monto_traslado + monto_colacion)
        cotizacion.save()

        # Solicitud
        # Random date between today and 2025
        start_date = date.today()
        end_date = date(2025, 1, 1)
        delta = end_date - start_date
        random_days = randrange(delta.days)
        fecha = start_date + timedelta(days=random_days)

        estado = randint(0, 3)

        # Random asignatura
        asignatura = Asignatura.objects.all().order_by('?').first()
        usuario = Usuario.objects.filter(email="marco.repetto@usm.cl").first()

        s = Solicitud(fecha=fecha,
                      estado=estado,
                      asignatura=asignatura,
                      usuario=usuario,
                      visita=v,
                      cotizacion=cotizacion)
        s.save()

    return redirect('landing')
# endregion
