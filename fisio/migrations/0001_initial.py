# Generated by Django 4.0.1 on 2024-10-19 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente de Confirmación'), ('confirmado', 'Confirmado'), ('reprogramado', 'Reprogramado'), ('cancelado_paciente', 'Cancelado por el Paciente'), ('cancelado_profesional', 'Cancelado por el Profesional'), ('no_asistido', 'No Asistido'), ('en_curso', 'En Curso'), ('finalizado', 'Finalizado')], default='pendiente', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_banco', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DatosFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=100)),
                ('fecha_emision', models.DateField()),
                ('detalle', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domicilio', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_gasto', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_trabajo', models.CharField(max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_informe', models.DateField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('honorario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateField()),
                ('metodo_pago', models.CharField(max_length=50)),
                ('agendamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.agendamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrodocumento', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.CharField(max_length=20)),
                ('correo', models.EmailField(max_length=254)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10)),
                ('activo', models.BooleanField(default=True)),
                ('responsable_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profesionales', to='fisio.area')),
            ],
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrodocumento', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('celular', models.CharField(max_length=20)),
                ('mail', models.EmailField(max_length=254)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeguroMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDescuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_transaccion', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(max_length=50)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.banco')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProfesionalArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('profesionales', models.ManyToManyField(related_name='tipos_profesional', to='fisio.Profesional')),
            ],
        ),
        migrations.CreateModel(
            name='TipoInformeArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('informe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_informe', to='fisio.informe')),
            ],
        ),
        migrations.CreateModel(
            name='TipoGasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('gastos', models.ManyToManyField(related_name='tipos_gasto', to='fisio.Gasto')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('evolucion', models.CharField(max_length=200)),
                ('agendamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='fisio.agendamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ADMINISTRADOR', 'Administrador'), ('PROFESIONAL', 'Profesional'), ('PACIENTE', 'Paciente'), ('ADMINISTRATIVO', 'Administrativo')], max_length=20)),
                ('nro_documento', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PagoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.pago')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nrodocumento', models.CharField(max_length=20, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
                ('celular', models.CharField(max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10)),
                ('diagnostico_medico', models.CharField(max_length=200)),
                ('medico_tratante', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('mail', models.EmailField(max_length=254, unique=True)),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='fisio.responsable')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioAtencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('idturno', models.CharField(blank=True, choices=[('M', 'Mañana (07:00 - 10:00)'), ('S', 'Siesta (10:00 - 13:00)'), ('T', 'Tarde (14:00 - 18:00)')], max_length=1)),
                ('profesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_atencion', to='fisio.profesional')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_atencion', to='fisio.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriaMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('informe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.informe')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historias_medicas', to='fisio.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado_clinico', models.TextField()),
                ('agendamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='fisio.agendamiento')),
            ],
        ),
        migrations.CreateModel(
            name='DiasTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=10)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.horario')),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('codigo_descuento', models.CharField(max_length=50)),
                ('tipo_descuento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.tipodescuento')),
            ],
        ),
        migrations.CreateModel(
            name='DatosCheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacion', models.CharField(max_length=100)),
                ('fecha_emision', models.DateField()),
                ('descripcion', models.TextField()),
                ('cheque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.transaccion')),
            ],
        ),
        migrations.CreateModel(
            name='CobroSeguroMedico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cobro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.cobro')),
                ('seguro_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.seguromedico')),
            ],
        ),
        migrations.AddField(
            model_name='cobro',
            name='tarifa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fisio.tarifa'),
        ),
        migrations.AddField(
            model_name='agendamiento',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamientos', to='fisio.paciente'),
        ),
        migrations.AddField(
            model_name='agendamiento',
            name='profesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamientos', to='fisio.profesional'),
        ),
        migrations.AddField(
            model_name='agendamiento',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamientos', to='fisio.servicio'),
        ),
    ]
