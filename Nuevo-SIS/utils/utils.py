from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

def recortar_imagen(imagen):
    ''' Permite recortar las imagenes para dejarlas cuadradas, 
    tomando el minimo valor de h o w que tenga la misma.
    '''
    if imagen:
        # Abrir la imagen usando PIL
        imagen_pil = Image.open(imagen)
        
        # Recortar la imagen
        tamaño_minimo = min(imagen_pil.width, imagen_pil.height)
        area = (0, 0, tamaño_minimo, tamaño_minimo)
        imagen_recortada = imagen_pil.crop(area)
        
        # Guardar la imagen recortada en un objeto BytesIO
        buffer = BytesIO()
        imagen_recortada.save(buffer, format='PNG')
        
        # Crear un objeto ContentFile con el contenido de la imagen recortada
        content_file = ContentFile(buffer.getvalue(), name=imagen.name)
        
        return content_file
    return None

