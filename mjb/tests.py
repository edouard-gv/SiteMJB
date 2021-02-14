import django.test

from mjb.models import Inventaire, Photographie, CommentairePhoto


class MappingsTestCaseWithDB(django.test.TestCase):
    # Ordre de recherche d'une mignature : self > soeur > parent > enfant
    # famille A : parent et enfant avec photo sauf un enfant
    # famille B : parent avec photo mais aucun enfant n'en a
    # famille C : parent sans photo mais certains enfant en ont

    def setUp(self):
        photo_1 = Photographie.objects.create(nom_fichier="photo1")
        photo_2 = Photographie.objects.create(nom_fichier="photo2")
        photo_3 = Photographie.objects.create(nom_fichier="photo3")
        photo_4 = Photographie.objects.create(nom_fichier="photo4")

        self.parent_A = Inventaire.objects.create(nom="test", num_mgg="MGG_0001", num_mjb1="001")
        self.fille_A_1 = Inventaire.objects.create(nom="test", num_mgg="MGG_0002", num_mjb1="001",
                                                   inventaire_parent=self.parent_A)
        self.fille_A_2 = Inventaire.objects.create(nom="test", num_mgg="MGG_0003", num_mjb1="001",
                                                   inventaire_parent=self.parent_A)
        self.fille_A_3 = Inventaire.objects.create(nom="test", num_mgg="MGG_0004", num_mjb1="001",
                                                   inventaire_parent=self.parent_A)

        CommentairePhoto.objects.create(inventaire=self.parent_A, photographie=photo_1)
        CommentairePhoto.objects.create(inventaire=self.fille_A_1, photographie=photo_2)
        # A2 en a 2, mais A3 n'en a pas
        CommentairePhoto.objects.create(inventaire=self.fille_A_2, photographie=photo_3)
        CommentairePhoto.objects.create(inventaire=self.fille_A_2, photographie=photo_4)

        self.parent_B = Inventaire.objects.create(nom="test", num_mgg="MGG_0010", num_mjb1="010")
        self.fille_B_1 = Inventaire.objects.create(nom="test", num_mgg="MGG_0011", num_mjb1="010",
                                                   inventaire_parent=self.parent_B)
        self.fille_B_2 = Inventaire.objects.create(nom="test", num_mgg="MGG_0012", num_mjb1="010",
                                                   inventaire_parent=self.parent_B)

        CommentairePhoto.objects.create(inventaire=self.parent_B, photographie=photo_1)
        CommentairePhoto.objects.create(inventaire=self.parent_B, photographie=photo_2)

        self.parent_C = Inventaire.objects.create(nom="test", num_mgg="MGG_0020", num_mjb1="020")
        self.fille_C_1 = Inventaire.objects.create(nom="test", num_mgg="MGG_0021", num_mjb1="020",
                                                   inventaire_parent=self.parent_C)
        self.fille_C_2 = Inventaire.objects.create(nom="test", num_mgg="MGG_0022", num_mjb1="020",
                                                   inventaire_parent=self.parent_C)

        CommentairePhoto.objects.create(inventaire=self.fille_C_1, photographie=photo_1)
        CommentairePhoto.objects.create(inventaire=self.fille_C_2, photographie=photo_2)
        CommentairePhoto.objects.create(inventaire=self.fille_C_1, photographie=photo_3)

    def test_ma_derniere_photo_avant_tout(self):
        self.assertEqual("photo1", self.parent_A.couverture().photographie.nom_fichier)
        self.assertEqual("photo2", self.fille_A_1.couverture().photographie.nom_fichier)
        self.assertEqual("photo4", self.fille_A_2.couverture().photographie.nom_fichier)

    def test_ou_la_plus_recente_de_mes_soeurs(self):
        self.assertEqual("photo4", self.fille_A_3.couverture().photographie.nom_fichier)

    def test_ou_la_plus_recente_de_mon_parent(self):
        self.assertEqual("photo2", self.fille_B_1.couverture().photographie.nom_fichier)
        self.assertEqual("photo2", self.fille_B_2.couverture().photographie.nom_fichier)

    def test_ou_la_plus_recente_de_mes_enfants(self):
        self.assertEqual("photo3", self.parent_C.couverture().photographie.nom_fichier)
