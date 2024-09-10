from django.db import models


# Create your models here.
class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=16)  # Rechazado, Pendiente, Revisado, Autorizado, Aprobado, Finalizado
    descripcion = models.TextField()
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    sigla_asignatura = models.CharField(max_length=8)
    paralelo = models.IntegerField()


    def __str__(self):
        return f"{self.fecha} - {self.estado} - {self.descripcion} - {self.usuario}"


class Usuario(models.Model):
    rut = models.CharField(max_length=16, primary_key=True)
    nombre = models.CharField(max_length=64)
    correo = models.EmailField()
    telefono = models.CharField(max_length=16)
    rol = models.CharField(max_length=16)  # Profesor, secretaria, ingeniero, director

    def __str__(self):
        return f"{self.nombre}[{self.rol}]: {self.correo} - {self.telefono}"


# Cotizacion necesita guardar archivos PDF
class Cotizacion(models.Model):
    id_cotizacion = models.AutoField(primary_key=True)
    es_principal = models.BooleanField()
    monto = models.IntegerField()
    tipo = models.CharField(max_length=16)  # Traslado, colacion
    archivo = models.FileField(upload_to='cotizaciones/')
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
    estado = models.CharField(max_length=16)  # Rechazado, Pendiente, Pagado


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
    fecha = models.DateField()
    semestre = models.CharField(max_length=5)
    lugar = models.CharField(max_length=64)
    solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
    profesor_encargado = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.hora} - {self.lugar} - {self.descripcion} - {self.solicitud} - {self.usuario}"

class Estudiantes(models.Model):
    rut = models.CharField(max_length=16, primary_key=True)
    nombre = models.CharField(max_length=64)
    visita = models.ForeignKey('Visita', on_delete=models.CASCADE)

    def __str__(self):
        return f"Estudiante {self.nombre} ({self.rut}) - {self.visita}"