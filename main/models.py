from django.db import models


# Create your models here.
class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=16)  # Rechazado, Pendiente, Revisado, Autorizado, Aprobado, Finalizado
    descripcion = models.TextField() 
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    sigla_asignatura = models.CharField(max_length=8)
    paralelo = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.fecha} - {self.estado} - {self.descripcion} - {self.usuario}"


class Usuario(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=64)
    correo = models.EmailField()
    telefono = models.CharField(max_length=16)
    rol = models.CharField(max_length=16)  # Profesor, secretaria, ingeniero, director

    def __str__(self):
        return f"{self.nombre}[{self.rol}]: {self.correo} - {self.telefono}"


# Cotizacion necesita guardar archivos PDF
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
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
    correo_presupuesto = models.EmailField(null=True, blank=True)
    estado = models.CharField(max_length=16, default='Pendiente') 


    def __str__(self):
        return f"Cotizacion {'Primaria' if (self.es_principal) else ''} de {self.tipo} por ${self.monto} - {self.solicitud}"

class Reembolso(models.Model):
    id_reembolso = models.AutoField(primary_key=True)
    monto = models.IntegerField()
    fecha_pago = models.DateField()
    estado = models.CharField(max_length=16)  # Rechazado, Espera, Pagado, En revisión, Pendiente
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha_visita = models.DateField()

    def __str__(self):
        return f"Reembolso de ${self.monto} - {self.fecha} - {self.estado} - {self.solicitud} - {self.usuario}"

class UnidadAcademica(models.Model):
    id_unidad_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    presupuesto = models.IntegerField()
    gasto = models.IntegerField()
    emplazamiento = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nombre} - ${self.presupuesto} - ${self.gasto} - {self.emplazamiento}"

class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=64, default='NN')
    fecha = models.DateField()
    semestre = models.CharField(max_length=5)
    lugar = models.CharField(max_length=64)
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE, null=True)
    profesor_encargado = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.hora} - {self.lugar} - {self.descripcion} - {self.solicitud} - {self.usuario}"

class Estudiantes(models.Model):
    rut = models.CharField(max_length=16, primary_key=True)
    nombre = models.CharField(max_length=64)
    visita = models.ForeignKey('Visita', on_delete=models.CASCADE)

    def __str__(self):
        return f"Estudiante {self.nombre} ({self.rut}) - {self.visita}"
    
class Asignatura(models.Model):
    sigla = models.CharField(max_length=8, primary_key=True)
    semestre = models.PositiveIntegerField()
    departamento = models.CharField(max_length=64)
    campus = models.CharField(max_length=64)
    paralelo = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.sigla} - {self.nombre} - {self.semestre} - {self.departamento} - {self.campus}"

# son o 1 o 3 cotizaciones