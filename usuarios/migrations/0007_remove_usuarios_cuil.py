# Generated by Django 4.2 on 2024-04-17 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_alter_usuarios_cuil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='cuil',
        ),
    ]
