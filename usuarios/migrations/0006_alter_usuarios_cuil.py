# Generated by Django 4.2 on 2024-04-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_remove_usuarios_dni_usuarios_cuil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='cuil',
            field=models.BigIntegerField(unique=True),
        ),
    ]