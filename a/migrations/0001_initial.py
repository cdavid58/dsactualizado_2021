# Generated by Django 2.2.3 on 2021-05-18 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cursos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='Videos')),
                ('titulo', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('duracion', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('apellido', models.CharField(max_length=20, null=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('bloqueado', models.BooleanField(default=False)),
                ('clave', models.CharField(default='1234', max_length=16)),
                ('dia', models.CharField(blank=True, default='', max_length=2, null=True)),
                ('mes', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('anio', models.CharField(blank=True, default='', max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='subCategorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('intro', models.FileField(upload_to='Intro')),
                ('precio', models.CharField(max_length=10)),
                ('duracion', models.CharField(max_length=6)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='ImagenIntro')),
                ('videoIntro', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('like', models.CharField(default=0, max_length=1000)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='likeCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Cursos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='cursos',
            name='subcategoria',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='a.subCategorias'),
        ),
        migrations.CreateModel(
            name='comentarioSubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.subCategorias')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='comentarioCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.CharField(max_length=10)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Cursos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a.Usuario')),
            ],
        ),
    ]
