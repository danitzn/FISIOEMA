# Generated by Django 4.0.1 on 2024-11-09 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fisio', '0006_alter_flujodinero_monto'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FlujoDinero',
            new_name='FlujoCaja',
        ),
    ]
