# Generated by Django 2.2.3 on 2021-05-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0012_suscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategorias',
            name='home',
            field=models.BooleanField(default=False),
        ),
    ]
