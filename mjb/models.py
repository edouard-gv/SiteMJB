from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from SiteMJB import settings


class Photographie(models.Model):
    # Pour importCSV column1=import_id,column2=numero,column3=qualite,column4=orientation,column6=nom_fichier

    class Orientation(models.TextChoices):
        PORTRAIT = 'Portrait'
        PAYSAGE = 'Paysage'

    class Qualite(models.TextChoices):
        BASSE_DEFINITION = 'Basse Définition (BD)', 'Basse Définition (BD)'
        HAUTE_DEFINITION = 'Haute Dédinition (HD)', 'Haute Définition (HD)'

    numero = models.CharField(max_length=1000, blank=True, verbose_name='numéro_photo')
    qualite = models.CharField(max_length=1000, blank=True, choices=Qualite.choices, verbose_name='QualitéPhoto')
    orientation = models.CharField(max_length=1000, blank=True, choices=Orientation.choices, verbose_name='OrientationPhoto')
    nom_fichier = models.CharField(max_length=1000, verbose_name='Nom_Fichier_Photo')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)
    image_ok = models.BooleanField(null=True)
    vignette_ok = models.BooleanField(null=True)
    import_auto = models.BooleanField(null=False, default=False)

    def lien(self):
        return settings.RACINE_IMAGES + self.nom_fichier

    def lien_vignette(self):
        lien_splite = self.lien().split('/')
        chemin = "/".join(lien_splite[:-1]) + "/"
        fichier = lien_splite[-1]
        return chemin + self.fichier_vignette(fichier)

    @staticmethod
    def fichier_vignette(fichier):
        suffixe_vignette = "-150x150"

        fichier_splite = fichier.split('.')
        if len(fichier_splite) > 1:
            nom_vignette = ".".join(fichier_splite[:-1]) + suffixe_vignette + "." + fichier_splite[-1]
        else:
            nom_vignette = fichier + suffixe_vignette
        return nom_vignette

    def __vignette(self, taille):
        if self.vignette_ok:
            return mark_safe('<img height="%i" width="%i" src="%s">' % (taille, taille, self.lien_vignette(),))
        return mark_safe('<img height="%i" src="%s">' % (taille, self.lien(),))

    def vignette50(self):
        return self.__vignette(50)

    def image(self):
        return mark_safe('<img src="%s">' % (self.lien(),))

    def __str__(self):
        return (self.numero + " - " if self.numero else "") + self.nom_fichier


class Theme(models.Model):
    mot_cle = models.CharField(max_length=1000, unique=True, verbose_name='Mot Clé')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.mot_cle


class Inventaire_Theme(models.Model):
    # Pour importcsv: column2=inventaire(Inventaire|import_id),column3=theme(Theme|import_id)
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.theme) + "/" + str(self.inventaire)


class Matiere(models.Model):
    # Pour importcsv: column1=import_id,column2=matiere
    matiere = models.CharField(max_length=1000, unique=True, verbose_name='Matière')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.matiere


class Inventaire_Matiere(models.Model):
    # Pour importcsv: column2=inventaire(Inventaire|import_id),column3=matiere(Matiere|import_id)
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.matiere) + "/" + str(self.inventaire)


class Contact(models.Model):
    # Pour importcsv: column1=import_id,column3=institution,column4=nom,column5=prenom
    institution = models.CharField(max_length=1000, blank=True, verbose_name='Institution')
    nom = models.CharField(max_length=1000, blank=True, verbose_name='Nom')
    prenom = models.CharField(max_length=1000, blank=True, verbose_name='Prénom')
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        list = []
        for data in [self.institution, self.nom, self.prenom]:
            if data is not None and len(data) > 1:
                list.append(data)
        return " - ".join(list)


class CommentairePhoto(models.Model):
    # Pour importcsv: column2=inventaire(Inventaire|import_id),column3=photographie(Photographie|import_id),column7=commentaire
    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    photographie = models.ForeignKey(Photographie, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=5000, blank=True)

    def vignette(self):
        return self.photographie.vignette50()

    def lien(self):
        return self.inventaire.lien()

    def __str__(self):
        return str(self.photographie) + "/" + str(self.inventaire)


class RelationContact(models.Model):
    # Pour importcsv: column2=inventaire(Inventaire|import_id),column3=contact(Contact|import_id),column7=etat,column8=debut,column9=fin,column10=prix_cession

    class EtatContact(models.TextChoices):
        ARTISTE = 'Artiste'
        PROPRIETAIRE = 'Propriétaire'
        COMMANDITAIRE = 'Commanditaire'
        MARCHAND = 'Marchand'
        MOULEUR = 'Mouleur'
        CIREUR = 'Cireur'
        FONDEUR = 'Fondeur'
        CISELEUR = 'Ciseleur'
        MARBRIER = 'Marbrier'
        AUTRE = 'Autre'

    inventaire = models.ForeignKey('Inventaire', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    etat = models.CharField(max_length=1000, choices=EtatContact.choices, verbose_name='Qualité')
    debut = models.CharField(max_length=1000, blank=True, verbose_name='Date Début')
    fin = models.CharField(max_length=1000, blank=True, verbose_name='Date Fin')
    prix_cession = models.CharField(max_length=1000, blank=True, verbose_name='Prix Cession/Autre qualité')

    def __str__(self):
        return str(self.contact) + "/" + str(self.inventaire)


class Inventaire(models.Model):
    ##Pour importCSV column1=import_id,column2=nom,column3=num_mgg,column4=num_mjb1,column5=num_mjb2,column6=commande,column7=volume,column8=notes_mjb,column9=description,column10=dim_hauteur,column11=dim_base,column13=type_original_moulage,column14=inventaire_parent(Inventaire|import_id),column15=date_creation,column16=date_modification

    class ValeursVolume(models.TextChoices):
        RONDE_BOSSE = 'Ronde-bosse'
        BAS_RELIEF = 'Bas-relief'
        HAUT_RELIEF = 'Haut-relief'

    nom = models.CharField(max_length=1000, verbose_name='Nom')
    num_mgg = models.CharField(max_length=1000, unique=True, verbose_name='N° d\'inventaire')
    num_mjb1 = models.CharField(max_length=1000, blank=True, verbose_name='N° Marie-Jo')
    num_mjb2 = models.CharField(max_length=1000, blank=True, verbose_name='Complément')
    commande = models.BooleanField(null=True, verbose_name='Commande')
    volume = models.CharField(max_length=1000, blank=True, choices=ValeursVolume.choices, verbose_name='Volume')
    notes_mjb = models.TextField(blank=True, verbose_name='Notes Marie-Jo')
    description = models.TextField(blank=True, verbose_name='Description sculpture')
    description_modele = models.TextField(blank=True, verbose_name='Description modèle')
    dim_hauteur = models.CharField(max_length=1000, blank=True, verbose_name='Hauteur (cm)')
    dim_base = models.CharField(max_length=1000, blank=True, verbose_name='Base (cm)')
    type_original_moulage = models.CharField(max_length=1000, blank=True, verbose_name='Connu/Inconnu/De suite')
    inventaire_parent = models.ForeignKey('self', null=True, blank=True, verbose_name='Original', on_delete=models.RESTRICT, related_name='declinaisons')
    date_creation = models.DateTimeField(verbose_name='Date création fiche', auto_now_add=True)
    date_modification = models.DateTimeField(verbose_name='Date modification fiche', auto_now=True)
    import_id = models.BigIntegerField(blank=True, unique=True, null=True)

    themes = models.ManyToManyField(Theme, blank=True, through=Inventaire_Theme)
    photographies = models.ManyToManyField(Photographie, through=CommentairePhoto)
    matieres = models.ManyToManyField(Matiere, blank=True, verbose_name='matière', through=Inventaire_Matiere)
    contacts = models.ManyToManyField(Contact, through=RelationContact)

    def description_du_modèle(self):
        if self.inventaire_parent:
            return self.inventaire_parent.description_du_modèle() + self.format_parent_description() + "\n "
        return ""

    def notes_marie_jo_parent(self):
        if self.inventaire_parent:
            return self.inventaire_parent.notes_marie_jo_parent() + self.format_parent_notes() + "\n "
        return ""

    def format_parent_description(self):
        return (str(self.inventaire_parent) + ": " + self.inventaire_parent.description_modele) if self.inventaire_parent.description_modele else ""

    def format_parent_notes(self):
        return (str(self.inventaire_parent) + ": " + self.inventaire_parent.notes_mjb) if self.inventaire_parent.notes_mjb else ""

    def couverture(self):
        dernier_com_photo = CommentairePhoto.objects.filter(inventaire=self).exclude(photographie__image_ok=False).order_by("-id").first()
        if dernier_com_photo:
            return dernier_com_photo
        elif self.inventaire_parent:
            dernier_com_photo_dune_soeur = \
                CommentairePhoto.objects.filter(inventaire__inventaire_parent=
                                            self.inventaire_parent).exclude(photographie__image_ok=False).order_by("-id").first()
            if dernier_com_photo_dune_soeur:
                return dernier_com_photo_dune_soeur
            else:
                dernier_com_photo_du_parent = \
                    CommentairePhoto.objects.filter(inventaire=
                                            self.inventaire_parent).exclude(photographie__image_ok=False).order_by("-id").first()
                return dernier_com_photo_du_parent
        else:
            dernier_com_photo_denfant = \
                CommentairePhoto.objects.filter(inventaire__inventaire_parent=
                                            self).exclude(photographie__image_ok=False).order_by("-id").first()
            if dernier_com_photo_denfant:
                return dernier_com_photo_denfant
        return None

    def vignette(self):
        couverture = self.couverture()
        if couverture:
            if couverture.inventaire != self:
                return self.__superpose__(50, couverture.photographie.vignette50(), couverture.inventaire.lien(texte="*"))
            else:
                return couverture.photographie.vignette50()
        return None

    def __superpose__(self, taille, texte, image):
        return mark_safe("""<div style="position:relative; height:%dpx">
               <div style="position:absolute;z-index:1">
                  %s
               </div>
               <div style="position:absolute;top:34px;z-index:2;font-size:xx-small;background-color:#FFFFFF66;">
                  %s
                </div> 
            </div>""" % (taille, texte, image))

    def lien(self, texte=""):
        url = reverse("admin:mjb_inventaire_change", args=[self.id])
        link = '<a href="%s">%s%s</a>' % (url, texte, self.num_mgg)
        return mark_safe(link)

    def __str__(self):
        return self.num_mgg + " (" + self.num_mjb1 + (", " + self.num_mjb2 if self.num_mjb2 else "") + ") - " + self.nom
