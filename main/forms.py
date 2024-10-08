from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    rut = forms.CharField(required=True, label="RUT")

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'rut')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rut = self.cleaned_data['rut']
        user.set_password(self.cleaned_data["password1"])  # Establece la contraseña
        if commit:
            user.save()
        return user


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
        fields = ['rut', 'first_name', 'email', 'telefono']


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
        fields = ['rut', 'first_name', 'email']
