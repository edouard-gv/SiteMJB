# Generated by Django 3.1.5 on 2023-10-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mjb', '0019_auto_20231029_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographie',
            name='import_auto',
            field=models.BooleanField(default=False),
        ),
    ]