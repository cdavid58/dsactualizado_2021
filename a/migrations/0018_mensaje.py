# Generated by Django 2.2.3 on 2021-05-20 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0017_auto_20210520_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10)),
                ('asunto', models.CharField(max_length=50)),
                ('message', models.TextField()),
            ],
        ),
    ]
