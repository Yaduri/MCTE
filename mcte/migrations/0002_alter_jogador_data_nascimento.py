# Generated by Django 4.2.18 on 2025-01-23 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcte', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogador',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Nascimento'),
        ),
    ]
