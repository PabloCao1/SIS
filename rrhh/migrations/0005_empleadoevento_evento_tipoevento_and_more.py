# Generated by Django 4.2 on 2024-03-27 11:25

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0004_alter_empleadotraspaso_sede'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpleadoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('asistio', models.BooleanField(default=False)),
                ('inscripto', models.DateField()),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(max_length=250)),
                ('modalidad', models.CharField(max_length=20)),
                ('fecha', models.DateField()),
                ('horario', models.TimeField(blank=True, null=True)),
                ('duracion', models.CharField(blank=True, max_length=250, null=True)),
                ('lugar', models.CharField(blank=True, max_length=250, null=True)),
                ('flyer', models.ImageField(blank=True, null=True, upload_to='eventos_flyers')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, max_length=250, null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='empleadocurso',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='empleadocurso',
            name='empleado',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='m2m_cursos',
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
        migrations.DeleteModel(
            name='EmpleadoCurso',
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.tipoevento'),
        ),
        migrations.AddField(
            model_name='empleadoevento',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.empleado'),
        ),
        migrations.AddField(
            model_name='empleadoevento',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.evento'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='m2m_eventos',
            field=models.ManyToManyField(blank=True, related_name='empleados', through='rrhh.EmpleadoEvento', to='rrhh.evento'),
        ),
    ]
