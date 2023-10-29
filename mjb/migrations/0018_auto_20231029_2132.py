# Generated by Django 3.1.5 on 2023-10-29 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mjb', '0017_import_photo_meta_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventaire',
            name='volume',
            field=models.CharField(blank=True, choices=[('Ronde-bosse', 'Ronde Bosse'), ('Bas-relief', 'Bas Relief'), ('Haut-relief', 'Haut Relief')], max_length=1000, verbose_name='Volume'),
        ),
        migrations.AlterField(
            model_name='relationcontact',
            name='debut',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Date Début'),
        ),
        migrations.AlterField(
            model_name='relationcontact',
            name='etat',
            field=models.CharField(choices=[('Artiste', 'Artiste'), ('Propriétaire', 'Proprietaire'), ('Commanditaire', 'Commanditaire'), ('Marchand', 'Marchand'), ('Mouleur', 'Mouleur'), ('Cireur', 'Cireur'), ('Fondeur', 'Fondeur'), ('Ciseleur', 'Ciseleur'), ('Marbrier', 'Marbrier'), ('Autre', 'Autre')], max_length=1000, verbose_name='Qualité'),
        ),
        migrations.AlterField(
            model_name='relationcontact',
            name='fin',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Date Fin'),
        ),
        migrations.AlterField(
            model_name='relationcontact',
            name='prix_cession',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Prix Cession/Autre qualité'),
        ),
    ]