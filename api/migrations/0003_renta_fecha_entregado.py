# Generated by Django 4.2.6 on 2023-10-22 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_renta_entregado_alter_renta_fecha_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='renta',
            name='fecha_entregado',
            field=models.DateTimeField(null=True),
        ),
    ]