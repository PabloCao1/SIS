from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import date
from django.urls import reverse
from .choices import *
from sedes.models import Sedes


# -----------TABLAS AUXILIARES-----------------------
class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return str(self.nombre)


class Evento(TimeStampedModel):
    fk_tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=250)
    modalidad = models.CharField(max_length=20)
    fecha = models.DateField()
    horario = models.TimeField(null=True, blank=True)
    duracion = models.CharField(max_length=250, null=True, blank=True)
    lugar = models.CharField(max_length=250, null=True, blank=True)
    flyer = models.ImageField(
        upload_to="eventos_flyers",
        null=True,
        blank=True,
    )
    descripcion = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("evento_detail", kwargs={"pk": self.pk})


class Tarea(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)


# ---------TABLA PRINCIPAL EMPLEADOS ------------
class Empleado(TimeStampedModel):
    SECACGC = models.CharField(max_length=50, null=True, blank=True)
    GO_equipo = models.CharField(max_length=250, null=True, blank=True)
    area = models.CharField(max_length=250, null=True, blank=True)
    delegacion = models.CharField(max_length=250, null=True, blank=True)
    unidad_organizativa = models.IntegerField(null=True, blank=True)
    apellidos = models.CharField(max_length=250, null=False, blank=False)
    nombres = models.CharField(max_length=250, null=False, blank=False)
    DNI = models.IntegerField(null=True, blank=True)
    estado_civil = models.CharField(max_length=250, null=True, blank=True)
    CUIT = models.BigIntegerField(null=False, blank=False)
    telefono = models.IntegerField(null=True, blank=True)
    mail_particular = models.EmailField(null=True, blank=True)
    mail_oficial = models.EmailField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    anio_ingreso = models.IntegerField(null=True, blank=True)
    calle = models.CharField(max_length=250, null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    piso = models.CharField(max_length=100, null=True, blank=True)
    departamento = models.CharField(max_length=15, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    provincia = models.CharField(max_length=250, null=True, blank=True)
    CP = models.CharField(max_length=10, null=True, blank=True)
    comuna = models.IntegerField(null=True, blank=True)
    tipo_contratacion = models.CharField(max_length=100, null=True, blank=True)
    activo = models.BooleanField(default=True)
    en_comision = models.BooleanField(default=False,null=True, blank=True)
    remoto = models.BooleanField(default=False,null=True, blank=True)
    id_puesto = models.CharField(max_length=250, null=True, blank=True)
    gremio = models.BooleanField(default=False,null=True, blank=True)
    discapacidad = models.BooleanField(default=False,null=True, blank=True)
    capacitacion_polivalente = models.BooleanField(default=False,null=True, blank=True)
    val_nomina_2021 = models.CharField(max_length=250, null=True, blank=True)
    ult_eval_desemp = models.CharField(max_length=100, null=True, blank=True)
    hijos = models.IntegerField(null=True, blank=True)
    hijos_escolar = models.IntegerField(null=True, blank=True)
    hijos_discapacidad = models.IntegerField(null=True, blank=True)
    foto = models.ImageField(
        upload_to="empleados_foto",
        null=True,
        blank=True,
    )
    organismo = models.CharField(max_length=100, null=True, blank=True)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE , null=False, blank=False)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    funcion = models.CharField(max_length=250, null=True, blank=True)
    anio_egreso = models.IntegerField(null=True, blank=True)
    niv_educativo = models.CharField(max_length=100, null=True, blank=True)
    profesion_oficio = models.CharField(max_length=250, null=True, blank=True)
    anio_graduacion = models.IntegerField(null=True, blank=True)
    establecimiento = models.CharField(max_length=250, null=True, blank=True)
    titulo = models.CharField(max_length=250, null=True, blank=True)
    nro_expediente = models.CharField(max_length=50, null=True, blank=True)
    vacaciones_anuales = models.PositiveIntegerField(null=True, blank=True)
    m2m_tareas = models.ManyToManyField(Tarea, blank=True)
    m2m_eventos = models.ManyToManyField(
        Evento, through="EmpleadoEvento", related_name="empleados", blank=True
    )
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'
    
    def edad(self):
        today = date.today()

        if self.fecha_nacimiento:
            age = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month or (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
                age -= 1

            if age == 0:
                # Calcular la cantidad de meses entre las fechas
                months = (today.year - self.fecha_nacimiento.year) * 12 + today.month - self.fecha_nacimiento.month
                if months == 0:
                    # Calcular la cantidad de días entre las fechas
                    days = (today - self.fecha_nacimiento).days
                    return f"{days} días"
                return f"{months} meses"
            return f"{age}"

        return '-'

    def direccion_completa(self):
        direccion = ""
        if self.calle:
            direccion += f"{self.calle} "
        if self.altura:
            direccion += f"{self.altura} "
        if self.piso:
            direccion += f"| Piso {self.piso} "
        if self.departamento:
            direccion += f"| Dpto {self.departamento} "
        if self.ciudad:
            direccion += f"| {self.ciudad} "
        if self.CP:
            direccion += f" ({self.CP}) "
        if self.comuna:
            direccion += f"| Comuna {self.comuna} "
        if self.provincia:
            direccion += f"| {self.provincia} "
        return direccion

    def get_absolute_url(self):
        return reverse("empleado_detail", kwargs={"pk": self.pk})


# ---------TABLA LICENCIAS DE EMPLEADOS ------------
class EmpleadoLicencia(TimeStampedModel):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=CHOICE_TIPO_LICENCIA)
    motivo = models.CharField(
        max_length=100, choices=CHOICE_MOTIVO_LICENCIA, null=True, blank=True
    )
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    def dias_tomados(self):
        return int(int((self.fecha_hasta - self.fecha_desde).days) + 1)


# ---------TABLA HISTORIAL EMPLEADOS ------------
class EmpleadoTraspaso(TimeStampedModel):
    fk_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=CHOICE_TRASPASOS)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=100)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField(null=True, blank=True)


# ---------TABLA EVENTOS DEL EMPLEADO ------------
class EmpleadoEvento(TimeStampedModel):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)
    inscripto = models.DateField()
