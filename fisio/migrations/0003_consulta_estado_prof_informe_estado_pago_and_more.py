# Generated by Django 5.1.3 on 2024-12-19 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisio', '0002_profesional_registro_profesional'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='estado_prof',
            field=models.CharField(choices=[('C', 'Cancelado'), ('P', 'Pendiente'), ('PP', 'Pago Parcial')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='informe',
            name='estado_pago',
            field=models.CharField(choices=[('C', 'Cancelado'), ('P', 'Pendiente'), ('PP', 'Pago Parcial')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='informe',
            name='estado_prof',
            field=models.CharField(choices=[('C', 'Cancelado'), ('P', 'Pendiente'), ('PP', 'Pago Parcial')], default='P', max_length=2),
        ),
        migrations.AddField(
            model_name='sesiondetalle',
            name='estado_prof',
            field=models.CharField(choices=[('C', 'Cancelado'), ('P', 'Pendiente'), ('PP', 'Pago Parcial')], default='P', max_length=2),
        ),
        migrations.AlterField(
            model_name='sesiondetalle',
            name='estado_pago',
            field=models.CharField(choices=[('C', 'Cancelado'), ('P', 'Pendiente'), ('PP', 'Pago Parcial')], default='P', max_length=2),
        ),
    ]
