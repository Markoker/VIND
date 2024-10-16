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

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['tipo', 'nombre_proveedor', 'rut_proveedor', 'correo_proveedor',
                   'monto', 'cotizacion_1', 'cotizacion_2', 'cotizacion_3', 'correo_presupuesto',
                   'tipo_subvencion', 'monto_individual']
    def __init__(self, *args, **kwargs):
        super(CotizacionForm, self).__init__(*args, **kwargs)
        self.fields['nombre_proveedor'].required = False
        self.fields['rut_proveedor'].required = False
        self.fields['correo_proveedor'].required = False
        self.fields['monto'].required = False
        self.fields['cotizacion_1'].required = False
        self.fields['cotizacion_2'].required = False
        self.fields['cotizacion_3'].required = False
        self.fields['correo_presupuesto'].required = False
        self.fields['tipo_subvencion'].required = False
        self.fields['monto_individual'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')
        tipo_subvencion = cleaned_data.get('tipo_subvencion')
        monto_individual= cleaned_data.get('monto_individual')
        if not cleaned_data.get('cotizacion_1'):
            self.add_error('cotizacion_1', 'Adjunta al menos una cotización.')
        if tipo == 'Solo traslado' or tipo == 'Traslado y colacion':
            if monto and monto > 1000000:
                if not(cleaned_data.get('cotizacion_1') and cleaned_data.get('cotizacion_2') and cleaned_data.get('cotizacion_3')):
                    if not(cleaned_data.get('correo_presupuesto')):
                        self.add_error('Debe adjuntar las cotizaciones o el correo de presupuesto.')
        if tipo == 'Solo colacion' or tipo == 'Traslado y colacion':
            total = monto_individual * 2 if monto_individual else 0 #temporal
            if total > 3 * 29360:
                if not(cleaned_data.get('cotizacion_1') and cleaned_data.get('cotizacion_2') and cleaned_data.get('cotizacion_3')):
                    if not(cleaned_data.get('correo_presupuesto')):
                        self.add_error('Debe adjuntar las cotizaciones o el correo de presupuesto.')



class VisitaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.now().date().strftime('%Y-%m-%d'),  # Establece la fecha mínima como la actual
                'placeholder': 'dd-mm-yyyy'
            }
        ),
        input_formats=['%Y-%m-%d'],
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

class AsignaturaForm(forms.Form):
    class Meta:
        fields = ['campus', 'departamento', 'semestre', 'sigla', 'paralelo']
    def __init__(self, *args, **kwargs):
        campus_opciones = kwargs.pop('campus_opciones', [])
        unidades_opciones = kwargs.pop('unidades_opciones', [])
        semestre_opciones = kwargs.pop('semestre_opciones', [])
        asignaturas_opciones = kwargs.pop('asignaturas_opciones', [])
        paralelos_opciones = kwargs.pop('paralelos_opciones', [])

        super().__init__(*args, **kwargs)
        self.fields['campus'] = forms.ChoiceField(
            choices=[('', 'Seleccione un campus')] + [(c, c) for c in campus_opciones],
            label="Seleccione un campus"
        )

        self.fields['departamento'] = forms.ChoiceField(
            choices=[('', 'Seleccione una unidad académica')] + [(u[0], u[1]) for u in unidades_opciones],
            label="Seleccione la unidad académica"
        )

        self.fields['semestre'] = forms.ChoiceField(
            choices=[(s, s) for s in semestre_opciones],
            label="Seleccione el semestre"
        )

        self.fields['sigla'] = forms.ChoiceField(
            choices=[('', 'Seleccione una asignatura')] + [(a[0], a[1]) for a in asignaturas_opciones],
            label="Seleccione la asignatura"
        )

        self.fields['paralelo'] = forms.ChoiceField(
            choices=[('', 'Seleccione un paralelo')] + [(p, p) for p in paralelos_opciones],
            label="Seleccione el paralelo"
        )