# Generated by Django 4.2.6 on 2023-10-22 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='renta',
            name='entregado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='renta',
            name='fecha_entrega',
            field=models.DateTimeField(),
        ),
    ]
