# Generated by Django 4.2 on 2024-06-24 15:06

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tkt_GOPA', '0011_remove_ticketgopa_banda_horaria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TurnosHorarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('hora', models.TextField(blank=True, null=True, verbose_name='Hora turno')),
                ('cantidad', models.TextField(blank=True, null=True, verbose_name='Cantidad turnos')),
                ('fk_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tkt_GOPA.ticketgopa')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]