# Generated by Django 4.2 on 2024-03-20 17:33

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
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
                ('flyer', models.ImageField(blank=True, null=True, upload_to='cursos_flyers')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, max_length=250, null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('SECACGC', models.CharField(blank=True, max_length=50, null=True)),
                ('GO_equipo', models.CharField(blank=True, max_length=250, null=True)),
                ('area', models.CharField(blank=True, max_length=250, null=True)),
                ('delegacion', models.CharField(blank=True, max_length=250, null=True)),
                ('unidad_organizativa', models.IntegerField(blank=True, null=True)),
                ('apellidos', models.CharField(max_length=250)),
                ('nombres', models.CharField(max_length=250)),
                ('CUIT', models.BigIntegerField()),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('mail_particular', models.EmailField(blank=True, max_length=254, null=True)),
                ('mail_oficial', models.EmailField(blank=True, max_length=254, null=True)),
                ('sexo', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('anio_ingreso', models.IntegerField(blank=True, null=True)),
                ('calle', models.CharField(blank=True, max_length=250, null=True)),
                ('altura', models.IntegerField(blank=True, null=True)),
                ('piso', models.CharField(blank=True, max_length=100, null=True)),
                ('departamento', models.CharField(blank=True, max_length=15, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('provincia', models.CharField(blank=True, max_length=250, null=True)),
                ('CP', models.CharField(blank=True, max_length=10, null=True)),
                ('comuna', models.IntegerField(blank=True, null=True)),
                ('tipo_contratacion', models.CharField(blank=True, max_length=250, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('en_comision', models.CharField(blank=True, max_length=250, null=True)),
                ('remoto', models.CharField(blank=True, max_length=250, null=True)),
                ('id_puesto', models.CharField(blank=True, max_length=250, null=True)),
                ('gremio', models.CharField(blank=True, max_length=250, null=True)),
                ('discapacidad', models.CharField(blank=True, max_length=250, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('capacitacion_polivalente', models.CharField(blank=True, max_length=250, null=True)),
                ('val_nomina_2021', models.CharField(blank=True, max_length=250, null=True)),
                ('ult_eval_desemp', models.CharField(blank=True, max_length=100, null=True)),
                ('DNI', models.IntegerField(blank=True, null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=250, null=True)),
                ('hijos', models.IntegerField(blank=True, null=True)),
                ('hijos_escolar', models.IntegerField(blank=True, null=True)),
                ('hijos_discapacidad', models.IntegerField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='empleados_foto')),
                ('organismo', models.CharField(blank=True, max_length=100, null=True)),
                ('sede', models.CharField(max_length=30)),
                ('fecha_baja', models.DateTimeField(blank=True, null=True)),
                ('funcion', models.CharField(blank=True, max_length=250, null=True)),
                ('anio_egreso', models.IntegerField(blank=True, null=True)),
                ('niv_educativo', models.CharField(blank=True, max_length=100, null=True)),
                ('profesion_oficio', models.CharField(blank=True, max_length=250, null=True)),
                ('anio_graduacion', models.IntegerField(blank=True, null=True)),
                ('establecimiento', models.CharField(blank=True, max_length=250, null=True)),
                ('titulo', models.CharField(blank=True, max_length=250, null=True)),
                ('img_titulo', models.ImageField(blank=True, null=True, upload_to='empleados_titulo')),
                ('nro_expediente', models.CharField(blank=True, max_length=50, null=True)),
                ('vacaciones_anuales', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmpleadoTraspaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tipo', models.CharField(choices=[('', ''), ('PERMANENTE', 'PERMANENTE'), ('TEMPORARIO', 'TEMPORARIO')], max_length=100)),
                ('sede', models.CharField(max_length=100)),
                ('motivo', models.CharField(max_length=100)),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField(blank=True, null=True)),
                ('fk_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.empleado')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadoLicencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tipo', models.CharField(choices=[('', ''), ('ORDINARIA', 'ORDINARIA'), ('ESPECIAL', 'ESPECIAL')], max_length=50)),
                ('motivo', models.CharField(blank=True, choices=[('', ''), ('SALUD', 'SALUD'), ('SALUD FAMILIAR', 'SALUD FAMILIAR'), ('MATERNIDAD/PATERNIDAD', 'MATERNIDAD/PATERNIDAD'), ('MOTIVOS PERSONALES', 'MOTIVOS PERSONALES'), ('DIAS DE ESTUDIO', 'DIAS DE ESTUDIO'), ('OTROS', 'OTROS')], max_length=100, null=True)),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('fk_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.empleado')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadoCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('cursado', models.BooleanField(default=False)),
                ('inscripto', models.DateField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.curso')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rrhh.empleado')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='empleado',
            name='m2m_cursos',
            field=models.ManyToManyField(blank=True, related_name='empleados', through='rrhh.EmpleadoCurso', to='rrhh.curso'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='m2m_tareas',
            field=models.ManyToManyField(blank=True, to='rrhh.tarea'),
        ),
    ]