"""
URL configuration for VIND project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
path('', landing_view, name='landing'),
path('login/', login_view, name='login'),
path('home/', home_view, name='home'),
path('load_users/', load_users, name='load_users'),
path('funcionario/', funcionario_view, name='funcionario'),
path('funcionario/crear_solicitud/', asignatura_view, name='crear_solicitud'),
path('funcionario/crear_solicitud/get_unidades', get_unidades, name='get_unidades'),
path('funcionario/crear_solicitud/get_paralelos', get_paralelos, name='get_paralelos'),
path('funcionario/crear_solicitud/get_asignaturas', get_asignaturas, name='get_asignaturas'),
path('funcionario/crear_solicitud/visita/', visita_view, name='visita_view'),
path('funcionario/crear_solicitud/estudiantes/', estudiantes_view, name='estudiantes_view'),
path('funcionario/crear_solicitud/profesor/', profesor_view, name='profesor_view'),
path('funcionario/crear_solicitud/cotizacion/', cotizacion_view, name='cotizacion_view'),
path('funcionario/crear_solicitud/', asignatura_view, name='crear_solicitud'),
path('admin/', admin.site.urls),
]
