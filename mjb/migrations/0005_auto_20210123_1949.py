# Generated by Django 3.1.5 on 2021-01-23 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mjb', '0004_theme_import_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='import_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='inventaire',
            name='import_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='matiere',
            name='import_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='photographie',
            name='import_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
