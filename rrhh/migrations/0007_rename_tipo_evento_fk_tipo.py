# Generated by Django 4.2 on 2024-03-27 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0006_rename_tipo_tipoevento_nombre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evento',
            old_name='tipo',
            new_name='fk_tipo',
        ),
    ]
