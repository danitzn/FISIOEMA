# Generated by Django 5.1.2 on 2024-12-20 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisio', '0005_alter_profesional_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='informe',
            name='servicio',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='fisio.servicio'),
            preserve_default=False,
        ),
    ]
