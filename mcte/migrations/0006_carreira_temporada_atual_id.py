# Generated by Django 4.2.18 on 2025-02-01 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcte', '0005_carreiratimejogador_titular'),
    ]

    operations = [
        migrations.AddField(
            model_name='carreira',
            name='temporada_atual_id',
            field=models.IntegerField(default=0),
        ),
    ]
