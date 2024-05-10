from django.db import models
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import *
from .choices import *


class Barrios(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"


class Servicios(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def get_absolute_url(self):
        return reverse("ver_servicios", kwargs={"pk": self.pk})


class Tramites(models.Model):
    fk_servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250, null=False, blank=False)
    turnos = models.BooleanField(default=False)
    espontaneos = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=300, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Tramite"
        verbose_name_plural = "Tramites"

    def get_absolute_url(self):
        return reverse("ver_tramites", kwargs={"pk": self.pk})


class Sedes(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    calle = models.CharField(max_length=250, null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    piso = models.CharField(max_length=100, null=True, blank=True)
    barrios = models.ManyToManyField(Barrios, blank=True)
    tramites = models.ManyToManyField(Tramites, blank=True)
    presidente = models.CharField(max_length=250, null=True, blank=True)
    telefono = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    mapa = models.CharField(max_length=350, null=True, blank=True)
    portada = models.ImageField(upload_to="sedes", blank=True, null=True)
    observaciones = models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.capitalize()

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def get_absolute_url(self):
        return reverse("ver_sede", kwargs={"pk": self.pk})


class SedesArchivos(models.Model):

    fk_sedes = models.ForeignKey(Sedes, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="sedes/archivos/")
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=12)

    def __str__(self):
        return f"Archivo {self.id} de la sede {self.fk_sedes}"


class SedesPlanos(models.Model):

    fk_sedes = models.ForeignKey(Sedes, on_delete=models.CASCADE)
    planos = models.FileField(upload_to="sedes/planos/")
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=12)

    def __str__(self):
        return f"Plano {self.id} de la sede {self.fk_sedes}"
