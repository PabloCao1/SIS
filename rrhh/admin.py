# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import TipoEvento, Evento, Tarea, Empleado, EmpleadoLicencia, EmpleadoTraspaso, EmpleadoEvento


@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'fk_tipo',
        'nombre',
        'modalidad',
        'fecha',
        'horario',
        'duracion',
        'lugar',
        'flyer',
        'descripcion',
        'link',
    )
    list_filter = ('created', 'modified', 'fk_tipo', 'fecha')


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'SECACGC',
        'GO_equipo',
        'area',
        'delegacion',
        'unidad_organizativa',
        'apellidos',
        'nombres',
        'DNI',
        'estado_civil',
        'CUIT',
        'telefono',
        'mail_particular',
        'mail_oficial',
        'sexo',
        'fecha_nacimiento',
        'anio_ingreso',
        'calle',
        'altura',
        'piso',
        'departamento',
        'ciudad',
        'provincia',
        'CP',
        'comuna',
        'tipo_contratacion',
        'activo',
        'en_comision',
        'remoto',
        'id_puesto',
        'gremio',
        'discapacidad',
        'capacitacion_polivalente',
        'val_nomina_2021',
        'ult_eval_desemp',
        'hijos',
        'hijos_escolar',
        'hijos_discapacidad',
        'foto',
        'organismo',
        'sede',
        'fecha_baja',
        'funcion',
        'anio_egreso',
        'niv_educativo',
        'profesion_oficio',
        'anio_graduacion',
        'establecimiento',
        'titulo',
        'nro_expediente',
        'vacaciones_anuales',
        'observaciones',
    )
    list_filter = (
        'created',
        'modified',
        'fecha_nacimiento',
        'activo',
        'en_comision',
        'remoto',
        'gremio',
        'discapacidad',
        'capacitacion_polivalente',
        'sede',
        'fecha_baja',
    )
    raw_id_fields = ('m2m_tareas', 'm2m_eventos')


@admin.register(EmpleadoLicencia)
class EmpleadoLicenciaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'fk_empleado',
        'tipo',
        'motivo',
        'fecha_desde',
        'fecha_hasta',
    )
    list_filter = (
        'created',
        'modified',
        'fk_empleado',
        'fecha_desde',
        'fecha_hasta',
    )


@admin.register(EmpleadoTraspaso)
class EmpleadoTraspasoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'fk_empleado',
        'tipo',
        'sede',
        'motivo',
        'fecha_desde',
        'fecha_hasta',
    )
    list_filter = (
        'created',
        'modified',
        'fk_empleado',
        'sede',
        'fecha_desde',
        'fecha_hasta',
    )


@admin.register(EmpleadoEvento)
class EmpleadoEventoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'empleado',
        'evento',
        'asistio',
        'inscripto',
    )
    list_filter = (
        'created',
        'modified',
        'empleado',
        'evento',
        'asistio',
        'inscripto',
    )