# Generated by Django 3.2.4 on 2021-06-27 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0025_alter_suscripcion_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
            ],
        ),
    ]
