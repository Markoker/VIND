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
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('funcionario/', funcionario_view, name='funcionario'),
    path('solicitud/', solicitud, name='solicitud'),
    path('cotizacion/', cotizacion),
    path('reembolso/', Reembolso),
    path('unidad_academica/', unidad_academica_view, name='unidad_academica'),
    path('ajax/get_edificios/', get_edificios, name='get_edificios'),
    path('ajax/get_carreras/', get_carreras, name='get_carreras'),
    path('visita/', visita_view, name='visita_view'),
    path('estudiantes/', estudiantes_view, name='estudiantes_view'),
    path('profesor/', profesor_view, name='profesor_view'),
    path('load/users/', load_users, name='load_users'),
]
