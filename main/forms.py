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


class CotizacionForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('Solo traslado', 'Solo traslado'),
                                      ('Solo colacion', 'Solo colacion'),
                                      ('Traslado y colacion', 'Traslado y colacion')],
                             label='Tipo de cotización')
    nombre_proveedor = forms.CharField(max_length=64, label='Nombre del proveedor')
    rut_proveedor = forms.CharField(max_length=12, label='RUT del proveedor')
    correo_proveedor = forms.EmailField(label='Correo del proveedor')
    monto = forms.IntegerField(min_value=0, label='Monto total')

    cotizacion_1 = forms.FileField(label='Cotización 1')
    cotizacion_2 = forms.FileField(label='Cotización 2', required=False)
    cotizacion_3 = forms.FileField(label='Cotización 3', required=False)

    correo_presupuesto = forms.EmailField(label='Correo de presupuesto', required=False)
    tipo_subvencion = forms.ChoiceField(choices=[('reembolso', 'Reembolso'), ('presupuesto', 'Previa presupuestación')],
                                        label='Tipo de subvención', required=False)
    monto_individual = forms.IntegerField(min_value=0, label='Monto individual', required=False)
    
    def __init__(self, *args, **kwargs):
        self.cantidad = kwargs.pop('cantidad', 1)  # default to 1 if not provided
        super().__init__(*args, **kwargs)


    class Meta:
        fields = ['tipo', 'nombre_proveedor', 'rut_proveedor', 'correo_proveedor',
                  'monto', 'cotizacion_1', 'cotizacion_2', 'cotizacion_3', 'correo_presupuesto',
                  'tipo_subvencion', 'monto_individual']

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        monto = cleaned_data.get('monto')
        tipo_subvencion = cleaned_data.get('tipo_subvencion')
        monto_individual = cleaned_data.get('monto_individual')
        if not cleaned_data.get('cotizacion_1'):
            self.add_error('cotizacion_1', 'Adjunta al menos una cotización.')

        if tipo in ['Solo traslado', 'Traslado y colacion'] and monto > 1000000:
            if not (cleaned_data.get('cotizacion_2') and cleaned_data.get('cotizacion_3') or cleaned_data.get('correo_presupuesto')):
                self.add_error('cotizacion_2', 'Adjunta las cotizaciones adicionales o el correo de presupuesto.')

        if tipo in ['Solo colacion', 'Traslado y colacion'] and monto_individual * self.cantidad > (3 * 29360):
            if not (cleaned_data.get('cotizacion_2') and cleaned_data.get('cotizacion_3') or cleaned_data.get('correo_presupuesto')):
                self.add_error('cotizacion_2', 'Adjunta las cotizaciones adicionales o el correo de presupuesto.')

        if monto_individual and monto and monto_individual * self.cantidad != monto:
            self.add_error('monto', 'El monto total no coincide con el monto individual multiplicado por la cantidad de estudiantes.')


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
    listado = forms.FileField(required=False)

    class Meta:
        fields = ['cantidad', 'listado']


class ProfesorForm(forms.Form):
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': 'XXXXXXXX-X'}))
    nombre = forms.CharField(max_length=64)
    email = forms.EmailField()

    class Meta:
        fields = ['rut', 'nombre', 'email']


class AsignaturaForm(forms.Form):
    class Meta:
        fields = ['campus', 'departamento', 'semestre', 'asignatura', 'paralelo']

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

        self.fields['asignatura'] = forms.ChoiceField(
            choices=[('', 'Seleccione una asignatura')] + [(a[0], a[1]) for a in asignaturas_opciones],
            label="Seleccione la asignatura"
        )

        self.fields['paralelo'] = forms.ChoiceField(
            choices=[('', 'Seleccione un paralelo')] + [(p, p) for p in paralelos_opciones],
            label="Seleccione el paralelo"
        )
