# Generated by Django 5.2.1 on 2025-05-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0002_alter_pokemons_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemons',
            name='altura',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pokemons',
            name='peso',
            field=models.IntegerField(null=True),
        ),
    ]
