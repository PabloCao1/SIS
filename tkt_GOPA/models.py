from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import date
from django.urls import reverse
from .choices import *
from sedes.models import Sedes
from django.core.validators import RegexValidator
from django.utils import timezone

############################ Modelos adicionales #########################

class DiasSemana(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
class Documentos(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

############################# Modelo principal ############################
class TicketGOPA(TimeStampedModel):
    cuit_validator = RegexValidator(regex=r'^[0-9]{11}$', message='El CUIT debe contener exactamente 11 dígitos numéricos.')

    ticket = models.CharField(max_length=100, verbose_name="Ticket", null=True, blank=True)
    fk_sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, verbose_name="Sede")
    otra_sede = models.CharField(max_length=250, verbose_name="Otra sede", null=True, blank=True)
    subsede = models.CharField(max_length=250, verbose_name="Subsede", null=True, blank=True)
    nombre = models.CharField(max_length=250, null=False, blank=False, verbose_name="Nombre")
    apellido = models.CharField(max_length=250, null=False, blank=False, verbose_name="Apellido")
    CUIT = models.CharField(max_length=11, null=False, blank=False, verbose_name="CUIT", validators=[cuit_validator])
    mail = models.CharField(max_length=250, null=False, blank=False, verbose_name="Email")
    area = models.CharField(max_length=250, null=False, blank=False, verbose_name="Area")
    organismo = models.CharField(max_length=250, null=False, blank=False, verbose_name="Organismo")


    nombre_agenda = models.CharField(max_length=250, null=False, blank=False, verbose_name="Nombre de la agenda")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicacion", null=False, blank=False)
    fecha_primer_turno = models.DateField(verbose_name="Fecha del primer turno", null=False, blank=False)
    max_turnos = models.IntegerField(verbose_name="Maxima cantidad de turnos por ciudadano", null=True, blank=True)
    #dias_atencion = models.ManyToManyField(DiasSemana, verbose_name="Días de atención", null=True, blank=True)
    #banda_horaria = models.CharField(max_length=250, verbose_name="Banda horaria de atención", null=True, blank=True)
    #duracion_tramite = models.CharField(max_length=250, verbose_name="Duracion del tramite", null=True, blank=True)
    #cant_turnos_simultaneo = models.IntegerField(verbose_name="Cantidad de turnos en simultaneo", null=True, blank=True)
    #tiempo_precancelacion = models.IntegerField(verbose_name="Tiempo de precancelación. (En minutos)", null=True, blank=True)
    visibilidad_agenda = models.IntegerField(verbose_name="Visibilidad de agenda. (En dias hábiles)", null=True, blank=True)
    #cupos_citas_diarios = models.IntegerField(verbose_name="Cantidad de cupos de citas diarios", null=True, blank=True)
    popup = models.TextField(null=True, blank=True, verbose_name="Leyenda que figura antes de confirmar el turno")
    txt_mail_confirmacion = models.TextField(null=True, blank=True, verbose_name="Texto en el mail de confirmación.")
    login_BA = models.BooleanField(verbose_name="Requiere Login con MiBA?", null=True, blank=True)
    documentos_permitidos = models.ManyToManyField(Documentos, verbose_name="Documentos permitidos", null=True, blank=True)
    vecino_reagendar_cita = models.BooleanField(verbose_name="El vecino puede reagendar cita?", null=True, blank=True)
    url_tramite = models.URLField(null=True, blank=True)
    estado = models.CharField(max_length=250, default="Pendiente", null=True, blank=True)

class TurnosHorarios(TimeStampedModel):
    fk_ticket = models.ForeignKey(TicketGOPA, on_delete=models.CASCADE)
    hora = models.TextField(null=True, blank=True, verbose_name="Hora turno")
    cantidad = models.TextField(null=True, blank=True, verbose_name="Cantidad turnos")