# Generated by Django 5.1.3 on 2024-12-18 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesional',
            name='registro_profesional',
            field=models.CharField(default='SR', max_length=40),
            preserve_default=False,
        ),
    ]