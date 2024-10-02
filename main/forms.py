from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['fecha', 'estado', 'descripcion', 'usuario', 'sigla_asignatura', 'paralelo']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'correo', 'telefono', 'rol']

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['es_principal', 'monto', 'archivo', 'solicitud', 'estado']
        widgets = {
            'tipo': forms.Select(choices=Cotizacion.TIPO_CHOICES),
        }
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        if tipo == "Solo Traslado":
            if not cleaned_data.get("archivo"):
                self.add_error('archivo', "Este campo es requerido")
        elif tipo == "Solo Colacion":
            if not cleaned_data.get("archivo"):
                self.add_error('archivo', "Este campo es requerido")
        elif tipo == "Traslado y Colacion":
            if not cleaned_data.get("archivo"):
                self.add_error('archivo', "Este campo es requerido")
        return cleaned_data
        


class ReembolsoForm(forms.ModelForm):
    class Meta:
        model = Reembolso
        fields = ['monto', 'fecha_pago', 'estado', 'solicitud', 'usuario', 'fecha_visita']

class UnidadAcademicaForm(forms.ModelForm):
    emplazamiento = forms.ModelChoiceField(queryset=Campus.objects.all(), label='Emplazamiento')
    unidad_academica = forms.ModelChoiceField(queryset=Edificio.objects.none(), label='Unidad Academica')
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.none(), label='Carrera')
    '''
    class Meta:
        model = UnidadAcademica
        fields = ['nombre', 'presupuesto', 'gasto', 'emplazamiento']
    '''

class VisitaForm(forms.ModelForm):
    fecha = forms.DateField(
        input_formats=['%d-%m-%Y'],  
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy'})
    )
     
    class Meta:
        model = Visita
        fields = ['nombre_empresa', 'fecha', 'lugar']
    
    def clean_fecha(self):
        data = self.cleaned_data['fecha']
        if data < timezone.now().date():
            raise ValidationError('La fecha no puede ser anterior al día actual.')
        return data

class EstudiantesForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1)
    # make optional file field
    listado = forms.FileField(required=False)
    
class ProfesorForm(forms.ModelForm):
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'XXXXXXXX-X'}))

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'correo']

