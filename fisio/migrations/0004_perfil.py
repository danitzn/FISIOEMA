# Generated by Django 5.1 on 2024-09-04 02:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisio', '0003_alter_profesional_responsable_area'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ADMINISTRADOR', 'Administrador'), ('PROFESIONAL', 'Profesional'), ('PACIENTE', 'Paciente'), ('ADMINISTRATIVO', 'Administrativo')], max_length=20)),
                ('nro_documento', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]