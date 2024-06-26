# Generated by Django 4.2 on 2024-04-30 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tkt_GOPA', '0008_documentos_remove_ticketgopa_documentos_requeridos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketgopa',
            name='banda_horaria',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Banda horaria de atención'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='cant_turnos_simultaneo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de turnos en simultaneo'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='cupos_citas_diarios',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de cupos de citas diarios'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='dias_atencion',
            field=models.ManyToManyField(blank=True, null=True, to='tkt_GOPA.diassemana', verbose_name='Días de atención'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='documentos_permitidos',
            field=models.ManyToManyField(blank=True, null=True, to='tkt_GOPA.documentos', verbose_name='Documentos permitidos'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='duracion_tramite',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Duracion del tramite'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='estado',
            field=models.CharField(default='Pendiente', max_length=250),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='login_BA',
            field=models.BooleanField(blank=True, null=True, verbose_name='Requiere Login con MiBA?'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='max_turnos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Maxima cantidad de turnos por ciudadano'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='tiempo_precancelacion',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tiempo de precancelación. (En minutos)'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='url_tramite',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='vecino_reagendar_cita',
            field=models.BooleanField(blank=True, null=True, verbose_name='El vecino puede reagendar cita?'),
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='visibilidad_agenda',
            field=models.IntegerField(blank=True, null=True, verbose_name='Visibilidad de agenda. (En dias hábiles)'),
        ),
    ]
