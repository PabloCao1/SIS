# Generated by Django 4.2 on 2024-04-30 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tkt_GOPA', '0004_alter_ticketgopa_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiasSemana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='ticketgopa',
            name='dias_atencion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tkt_GOPA.diassemana', verbose_name='Dias de atención.'),
        ),
    ]
