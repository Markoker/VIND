from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Solicitud)
admin.site.register(Usuario)
admin.site.register(Cotizacion)
admin.site.register(Reembolso)
admin.site.register(Visita)
admin.site.register(UnidadAcademica)
admin.site.register(Asignatura)
admin.site.register(Emplazamiento)
admin.site.register(Visitante)

admin.site.register(Funcionario)
admin.site.register(Ingeniero)
admin.site.register(Subdirector)
admin.site.register(Director)
