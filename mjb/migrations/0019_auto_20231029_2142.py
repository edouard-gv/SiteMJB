# Generated by Django 3.1.5 on 2023-10-29 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mjb', '0018_auto_20231029_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventaire',
            name='description_modele',
            field=models.TextField(blank=True, verbose_name='Description modèle'),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description sculpture'),
        ),
    ]
