# Generated by Django 3.1.5 on 2021-01-24 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mjb', '0009_auto_20210123_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='notes_mjb',
            field=models.TextField(blank=True, verbose_name='NotesMJB'),
        ),
    ]
