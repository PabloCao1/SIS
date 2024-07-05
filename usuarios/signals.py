# signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Usuarios
import os



@receiver(post_delete, sender=User)
def delete_user_preferences(sender, instance, **kwargs):
    try:
        instance.usuarios.delete()
    except Usuarios.DoesNotExist:
        pass

# borrado físico de las imagenes al borrar el usuario
def _delete_file(path):
    """Deletes file from filesystem."""
    if os.path.isfile(path):
        os.remove(path)



@receiver(post_delete, sender=Usuarios)
def delete_file(sender, instance, *args, **kwargs):
    """Deletes image files on `post_delete`"""
    if instance.imagen:
        _delete_file(instance.imagen.path)

