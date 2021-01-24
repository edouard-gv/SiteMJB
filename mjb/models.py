from enum import Enum

from django.db import models

class Photographie(models.Model):
    #Pour importCSV column1=import_id,column2=numero,column3=qualite,column4=orientation,column6=nom_fichier

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
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.numero+" - "+self.nom_fichier


class Theme(models.Model):
    mot_cle = models.CharField(max_length=1000, unique=True, verbose_name='Mot Clé')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.mot_cle


class Inventaire_Theme(models.Model):
    #Pour importcsv: column2=inventaire(Inventaire|import_id),column3=theme(Theme|import_id)
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)


class Matiere(models.Model):
    #Pour importcsv: column1=import_id,column2=matiere
    matiere = models.CharField(max_length=1000, unique=True, verbose_name='Matière')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.matiere


class Inventaire_Matiere(models.Model):
    #Pour importcsv: column2=inventaire(Inventaire|import_id),column3=matiere(Matiere|import_id)
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class Contact(models.Model):
    #Pour importcsv: column1=import_id,column3=institution,column4=nom,column5=prenom
    institution = models.CharField(max_length=1000, blank=True, verbose_name='Institution')
    nom = models.CharField(max_length=1000, blank=True, verbose_name='Nom')
    prenom = models.CharField(max_length=1000, blank=True, verbose_name='Prénom')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.institution + ' - ' + self.nom + ' - ' + self.prenom


class CommentairePhoto(models.Model):
    #Pour importcsv: column2=inventaire(Inventaire|import_id),column3=photographie(Photographie|import_id),column7=commentaire
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    photographie = models.ForeignKey(Photographie, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=5000, blank=True)

class RelationContact(models.Model):
    #Pour importcsv: column2=inventaire(Inventaire|import_id),column3=contact(Contact|import_id),column7=etat,column8=debut,column9=fin,column10=prix_cession

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
    ##Pour importCSV column1=import_id,column2=nom,column3=num_mgg,column4=num_mjb1,column5=num_mjb2,column6=commande,column7=volume,column8=notes_mjb,column9=description,column10=dim_hauteur,column11=dim_base,column13=type_original_moulage,column14=inventaire_parent(Inventaire|import_id),column15=date_creation,column16=date_modification

    class ValeursVolume(models.TextChoices):
        RONDE_BOSSE = 'Ronde-bosse'
        BAS_RELIEF = 'Bas-relief'

    nom = models.CharField(max_length=1000, verbose_name='Nom')
    num_mgg = models.CharField(max_length=1000, unique=True, verbose_name='NUM_MGG')
    num_mjb1 = models.CharField(max_length=1000, verbose_name='NUM_MJB1')
    num_mjb2 = models.CharField(max_length=1000, blank=True, verbose_name='NUM_MJB2')
    commande = models.BooleanField(null=True, verbose_name='Commande')
    volume = models.CharField(max_length=1000, blank=True, choices=ValeursVolume.choices, verbose_name='Volume')
    notes_mjb = models.TextField(blank=True, verbose_name='NotesMJB')
    description = models.TextField(blank=True, verbose_name='Description')
    dim_hauteur = models.CharField(max_length=1000, blank=True, verbose_name='Dim_Hauteur')
    dim_base = models.CharField(max_length=1000, blank=True, verbose_name='Dim_Base')
    type_original_moulage = models.CharField(max_length=1000, blank=True, verbose_name='TypeOriginalMoulage')
    inventaire_parent = models.ForeignKey('self', null=True, blank=True, verbose_name='lienIDInventaireOriginal', on_delete=models.RESTRICT, related_name='declinaisons')
    date_creation = models.DateTimeField(verbose_name='DateCreation', auto_now_add=True)
    date_modification = models.DateTimeField(verbose_name='DateModification', auto_now=True)
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    themes = models.ManyToManyField(Theme, blank=True, through=Inventaire_Theme)
    photographies = models.ManyToManyField(Photographie, through=CommentairePhoto)
    matieres = models.ManyToManyField(Matiere, blank=True, verbose_name='matière', through=Inventaire_Matiere)
    contacts = models.ManyToManyField(Contact, through=RelationContact)

    def __str__(self):
        return self.num_mgg