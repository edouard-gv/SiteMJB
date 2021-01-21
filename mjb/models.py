from enum import Enum

from django.db import models

class Photographie(models.Model):

    class Orientation(models.TextChoices):
        PORTRAIT = 'Portrait'
        PAYSAGE = 'Paysage'

    class Qualite(models.TextChoices):
        BASSE_DEFINITION = 'Basse Définition (BD)', 'Basse Définition (BD)'
        HAUTE_DEFINITION = 'Haute Dédinition (HD)', 'Haute Définition (HD)'

    numero = models.CharField(max_length=1000, unique=True, verbose_name='numéro_photo')
    qualite = models.CharField(max_length=1000, blank=True, choices=Qualite.choices, verbose_name='QualitéPhoto')
    orientation = models.CharField(max_length=1000, blank=True, choices=Orientation.choices, verbose_name='OrientationPhoto')
    nom_fichier = models.CharField(max_length=1000, verbose_name='Nom_Fichier_Photo')

    def __str__(self):
        return self.numero


class Theme(models.Model):
    mot_cle = models.CharField(max_length=1000, unique=True, verbose_name='Mot Clé')

    def __str__(self):
        return self.mot_cle


class Matiere(models.Model):
    matiere = models.CharField(max_length=1000, unique=True, verbose_name='Matière')

    def __str__(self):
        return self.matiere


class Contact(models.Model):
    institution = models.CharField(max_length=1000, blank=True, verbose_name='Institution')
    nom = models.CharField(max_length=1000, blank=True, verbose_name='Nom')
    prenom = models.CharField(max_length=1000, blank=True, verbose_name='Prénom')

    def __str__(self):
        return self.institution + ' - ' + self.nom + ' - ' + self.prenom


class CommentairePhoto(models.Model):
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    photographie = models.ForeignKey(Photographie, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=5000, blank=True)

class RelationContact(models.Model):
    class EtatContact(models.TextChoices):
        ARTISTE = 'Artiste'
        PROPRIETAIRE = 'Propriétaire'
        MARCHAND = 'Marchand'
        COMMANDITAIRE = 'Commanditaire'
        CIREUR = 'Cireur'
        MOULEUR = 'Mouleur'
        MARBRIER = 'Marbrier'
        FONDEUR = 'Fondeur'

    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    etat = models.CharField(max_length=1000, choices=EtatContact.choices, verbose_name='EtatContact')
    debut = models.CharField(max_length=1000, blank=True, verbose_name='ContactDateDebut')
    fin = models.CharField(max_length=1000, blank=True, verbose_name='ContactDateFin')
    prix_cession = models.CharField(max_length=1000, blank=True, verbose_name='PrixCession')



class Inventaire(models.Model):

    class ValeursVolume(models.TextChoices):
        RONDE_BOSSE = 'Ronde-bosse'
        BAS_RELIEF = 'Bas-relief'

    nom = models.CharField(max_length=1000, verbose_name='Nom')
    num_mgg = models.CharField(max_length=1000, unique=True, verbose_name='NUM_MGG')
    num_mjb1 = models.CharField(max_length=1000, verbose_name='NUM_MJB1')
    num_mjb2 = models.CharField(max_length=1000, blank=True, verbose_name='NUM_MJB2')
    commande = models.BooleanField(null=True, verbose_name='Commande')
    volume = models.CharField(max_length=1000, blank=True, choices=ValeursVolume.choices, verbose_name='Volume')
    notes_mjb = models.CharField(max_length=5000, blank=True, verbose_name='NotesMJB')
    description = models.CharField(max_length=5000, blank=True, verbose_name='Description')
    dim_hauteur = models.CharField(max_length=1000, blank=True, verbose_name='Dim_Hauteur')
    dim_base = models.CharField(max_length=1000, blank=True, verbose_name='Dim_Base')
    type_original_moulage = models.CharField(max_length=1000, blank=True, verbose_name='TypeOriginalMoulage')
    inventaire_parent = models.ForeignKey('self', null=True, blank=True, verbose_name='lienIDInventaireOriginal', on_delete=models.RESTRICT, related_name='declinaisons')
    date_creation = models.DateTimeField(verbose_name='DateCreation')
    date_modification = models.DateTimeField(verbose_name='DateModification')

    themes = models.ManyToManyField(Theme, blank=True)
    photographies = models.ManyToManyField(Photographie, through=CommentairePhoto)
    matieres = models.ManyToManyField(Matiere, blank=True, verbose_name='matière')
    contacts = models.ManyToManyField(Contact, through=RelationContact)

    def __str__(self):
        return self.num_mgg