# Generated by Django 4.2 on 2024-03-22 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0002_alter_empleado_sede'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='img_titulo',
        ),
        migrations.AlterField(
            model_name='empleado',
            name='capacitacion_polivalente',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='discapacidad',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='en_comision',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='gremio',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='remoto',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='tipo_contratacion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]