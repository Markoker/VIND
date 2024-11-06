from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
path('', landing_view, name='landing'),
path('login/', login_view, name='login'),
path('logout/', logout, name='logout'),
path('home/', home_view, name='home'),

# FUNCIONARIO
path('funcionario/unidad_<str:unidad>/solicitudes', enviadas_view, name='funcionario'),

# ENVIAR SOLICITUD (URLS EN ORDEN)
path('funcionario/crear_solicitud/', asignatura_view, name='crear_solicitud'),
path('funcionario/crear_solicitud/visita/', visita_view, name='visita_view'),
path('funcionario/crear_solicitud/profesor/', profesor_view, name='profesor_view'),
path('funcionario/crear_solicitud/estudiantes/', estudiantes_view, name='estudiantes_view'),
path('funcionario/crear_solicitud/cotizacion/', cotizacion_view, name='cotizacion_view'),
path('funcionario/crear_solicitud/confirmacion/', confirmacion_view, name='confirmacion_view'),

path('funcionario/crear_solicitud/get_unidades', get_unidades, name='get_unidades'),
path('funcionario/crear_solicitud/get_asignaturas', get_asignaturas, name='get_asignaturas'),
path('funcionario/crear_solicitud/get_paralelos', get_paralelos, name='get_paralelos'),




# INGENIERO
path('ingeniero/<str:emplazamiento>/recibidas', recibidas_view, name='ingeniero'),
# path('ingeniero/emplazamiento_<str:emplazamiento>/historial', historial_view, name='ingeniero_historial'),
path('ingeniero/<str:emplazamiento>/recibidas/<str:solicitud>', validar_ingeniero, name='validar_ingeniero'),

# DIRECTOR

# SUBDIRECTOR

# UTILIDADES
path('admin/load_users/', load_users, name='load_users'),
path('admin/poblar/', poblar_bbdd, name='poblar_bbdd'),
path('admin/poblar/usuarios', poblar_bbdd_u, name='poblar_bbdd_u'),
path('admin/poblar/solicitudes', poblar_bbdd_s, name='poblar_bbdd_s'),
path('test/correo_rechazo', correo_rechazo, name='correo_rechazo'),


# ADMIN
path('admin/', admin.site.urls, name='admin'),

]
