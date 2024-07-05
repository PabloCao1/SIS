from django.db.models.signals import pre_delete, pre_save, post_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
import os
from .models import Empleado, Evento


@receiver(pre_delete, sender=Empleado)
def eliminar_foto_empleado(sender, instance, **kwargs):
    # Verificar si la instancia tiene una foto asociada
    if instance.foto:
        foto_path = os.path.join(settings.MEDIA_ROOT, instance.foto.name)
        # Eliminar el archivo de la foto
        if os.path.isfile(foto_path):
            os.remove(foto_path)


@receiver(post_delete, sender=Evento)
def eliminar_flyer_evento(sender, instance, **kwargs):
    # Verifica si el evento tiene un flyer asociado
    if instance.flyer:
        # Elimina el archivo del flyer asociado
        if os.path.isfile(instance.flyer.path):
            os.remove(instance.flyer.path)


@receiver(pre_save, sender=Evento)
def eliminar_archivo_al_cambiar_flyer_evento(sender, instance, **kwargs):
    # Verifica si el evento ya existe en la base de datos
    if instance.pk:
        # Obtiene el evento existente de la base de datos
        evento_existente = Evento.objects.get(pk=instance.pk)
        # Verifica si el flyer del evento está cambiando
        if evento_existente.flyer != instance.flyer:
            # Elimina el archivo del flyer anterior si existe
            if evento_existente.flyer:
                if os.path.isfile(evento_existente.flyer.path):
                    os.remove(evento_existente.flyer.path)
