from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# ------- EXTENSION DEL MODELO USER-----
class Usuarios(models.Model):
    """
    Extend USER model
    """

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(
    upload_to="usuarios/", null=True, blank=True)
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    darkmode = models.BooleanField(default=True, null=True, blank=True)
    intentos_contraseña_predeterminada = models.PositiveIntegerField(default=0)

    def __str__(self):
        if(self.usuario.first_name or self.usuario.last_name):
            nombre= self.usuario.first_name + ' ' + self.usuario.last_name
        else: nombre = self.usuario.username        
        return nombre
    
    def get_absolute_url(self):
        return reverse('usuarios_ver', kwargs={'pk': self.pk})