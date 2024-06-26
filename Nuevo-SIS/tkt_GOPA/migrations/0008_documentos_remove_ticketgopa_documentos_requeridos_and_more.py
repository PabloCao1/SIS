# Generated by Django 4.2 on 2024-04-30 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tkt_GOPA', '0007_remove_ticketgopa_dias_atencion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='ticketgopa',
            name='documentos_requeridos',
        ),
        migrations.AddField(
            model_name='ticketgopa',
            name='documentos_permitidos',
            field=models.ManyToManyField(to='tkt_GOPA.documentos', verbose_name='Documentos permitidos.'),
        ),
    ]
