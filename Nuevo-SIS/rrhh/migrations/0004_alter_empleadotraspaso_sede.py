# Generated by Django 4.2 on 2024-03-22 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sedes', '0001_initial'),
        ('rrhh', '0003_remove_empleado_img_titulo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleadotraspaso',
            name='sede',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sedes.sedes'),
        ),
    ]
