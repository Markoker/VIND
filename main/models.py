from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, rut, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        extra_fields.setdefault('rut', rut)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        logger.debug(f'Usuario creado: {user.email}')
        return user

    def create_superuser(self, email, rut, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        superuser = self.create_user(email, rut, password, **extra_fields)
        logger.debug(f'Superusuario creado: {superuser.email}')
        return superuser


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Dirección de correo', unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut']

    objects = CustomUserManager()

    rut = models.CharField(max_length=10, primary_key=True)
    telefono = models.CharField(max_length=16)

    is_funcionario = models.BooleanField(default=True)
    is_ingeniero = models.BooleanField(default=False)
    is_subdirector = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}: {self.email} - {self.telefono}"

class Funcionario(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    unidad_academica = models.ForeignKey('UnidadAcademica', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} es funcionario en {self.unidad_academica}"

class Ingeniero(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    emplezamiento = models.ForeignKey('Emplazamiento', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} es ingeniero en {self.emplezamiento}"

class Subdirector(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    unidad_academica = models.ForeignKey('UnidadAcademica', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} es subdirector en {self.unidad_academica}"

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=16, default="Pendiente")  # Rechazado, Pendiente, Revisado, Autorizado, Aprobado, Finalizado
    descripcion = models.TextField()
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)

    visita = models.ForeignKey('Visita', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.fecha} - {self.estado} - {self.descripcion} - {self.usuario}"

class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=64, default='NN')
    fecha = models.DateField()
    lugar = models.CharField(max_length=64)
    profesor_encargado = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.lugar} - {self.solicitud} - {self.profesor_encargado}"


class Cotizacion(models.Model):
    TIPO_CHOICES = [
        ('Solo traslado', 'Sólo traslado'),
        ('Solo colacion', 'Sólo colación'),
        ('Traslado y colacion', 'Traslado y colaciones'),
    ]
    SUBVENCION_CHOICES = [
        ('reembolso', 'Reembolso'),
        ('presupuesto', 'Previa presupuestación')
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    nombre_proveedor = models.CharField(max_length=255, blank=True, null=True)
    rut_proveedor = models.CharField(max_length=20, blank=True, null=True)
    correo_proveedor = models.EmailField(blank=True, null=True)

    id_cotizacion = models.AutoField(primary_key=True)
    monto = models.PositiveIntegerField()
    cotizacion_1 = models.FileField(upload_to='cotizaciones/', null=True, blank=True)
    cotizacion_2 = models.FileField(upload_to='cotizaciones/', null=True, blank=True)
    cotizacion_3 = models.FileField(upload_to='cotizaciones/', null=True, blank=True)

    tipo_subvencion = models.CharField(max_length=20, choices=SUBVENCION_CHOICES, blank=True, null=True)
    monto_individual = models.PositiveIntegerField(blank=True, null=True)
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE, null=True, blank=True)
    correo_presupuesto = models.EmailField(null=True, blank=True)
    estado = models.CharField(max_length=16, default='Pendiente')

    def __str__(self):
        return f"Cotizacion {'Primaria' if (self.es_principal) else ''} de {self.tipo} por ${self.monto} - {self.solicitud}"

class Reembolso(models.Model):
    id_reembolso = models.AutoField(primary_key=True)
    monto = models.IntegerField()
    fecha_pago = models.DateField()
    estado = models.CharField(max_length=16)
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha_visita = models.DateField()

    def __str__(self):
        return f"Reembolso de ${self.monto} - {self.estado} - {self.solicitud} - {self.usuario}"

class Estudiantes(models.Model):
    rut = models.CharField(max_length=16, primary_key=True)
    nombre = models.CharField(max_length=64)
    visita = models.ForeignKey('Visita', on_delete=models.CASCADE)

    def __str__(self):
        return f"Estudiante {self.nombre} ({self.rut}) - {self.visita}"

class Emplazamiento(models.Model):
    id_emplazamiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    sigla = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.nombre} [{self.sigla}]"

class UnidadAcademica(models.Model):
    id_unidad_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    presupuesto = models.IntegerField()
    gasto = models.IntegerField()
    emplazamiento = models.ForeignKey('Emplazamiento', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - ${self.presupuesto} - ${self.gasto} - {self.emplazamiento}"

class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True, unique=True)
    sigla = models.CharField(max_length=8)
    nombre = models.CharField(max_length=128)
    semestre = models.PositiveIntegerField()
    departamento = models.ForeignKey('UnidadAcademica', on_delete=models.CASCADE)
    paralelo = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.sigla} - {self.semestre} - {self.departamento}"

# son o 1 o 3 cotizaciones