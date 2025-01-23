# Generated by Django 4.2.18 on 2025-01-23 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campeonato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carreira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Temporada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(default='24/25', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Treinador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Jogador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('carreira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.carreira')),
            ],
        ),
        migrations.CreateModel(
            name='Estatistica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jogos', models.IntegerField(verbose_name='Quantidade de Jogos')),
                ('gol', models.IntegerField(verbose_name='Quantidade de Gols')),
                ('assistencia', models.IntegerField(verbose_name='Quantidade de Assistencias')),
                ('campeonato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.campeonato')),
                ('carreira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.carreira')),
                ('jogador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.jogador')),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.temporada')),
            ],
        ),
        migrations.AddField(
            model_name='carreira',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.time'),
        ),
        migrations.AddField(
            model_name='carreira',
            name='treinador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcte.treinador'),
        ),
        migrations.AddField(
            model_name='carreira',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
