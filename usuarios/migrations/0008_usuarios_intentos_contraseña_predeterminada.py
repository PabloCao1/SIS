# Generated by Django 4.2 on 2024-04-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_remove_usuarios_cuil'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='intentos_contraseña_predeterminada',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
