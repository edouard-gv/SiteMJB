# Generated by Django 3.1.5 on 2021-02-13 17:52
import re
import unittest
import requests

from django.db import migrations
from django.db.models import Max, Min

import django.test

from mjb.models import Photographie, Inventaire, CommentairePhoto


def photo_mapping(noms):
    mappings = []
    for nom in noms:
        nom_splitte = nom.split('-')
        if len(nom_splitte) > 1:
            num_mjb_raw = nom_splitte[0]
            # On cherche avec le numéro tel quel, sans chercher à le completer
            num_mgg = cherche_premier_mgg(num_mjb_raw)
            if num_mgg is None:
                nombre_de_chiffres = sum(c.isdigit() for c in num_mjb_raw)
                num_mjb_complet = "0" * max(0, 3 - nombre_de_chiffres) + num_mjb_raw
                num_mgg = cherche_premier_mgg(num_mjb_complet)
            mappings.append((num_mgg, nom))
    return mappings


def cherche_premier_mgg(num_mjb):
    return Inventaire.objects.filter(num_mjb1=num_mjb).aggregate(num=Min("num_mgg"))['num']


def get_liste_nom():
    noms = requests.get("https://www.mariejobourron.com/wp-content/uploads/inventaire/images-inventaire.php").text
    return [nom.strip() for nom in noms.split("<br>") if nom.strip() != '' and not mignature(nom.strip())]


def mignature(nom):
    return True if re.search(r"-\d+x\d+\.\w+$", nom) else False


class Migration(migrations.Migration):
    dependencies = [
        ('mjb', '0014_numero_photo_facultatif'),
    ]

    def import_photo(apps, schema_editor):
        photographie = apps.get_model('mjb', 'Photographie')
        commentairephoto = apps.get_model('mjb', 'CommentairePhoto')
        inventaires = apps.get_model('mjb', 'Inventaire')
        IMPORT_AUTO = "import auto"
        _, nb_lignes_supprimees = photographie.objects.filter(commentairephoto__commentaire=IMPORT_AUTO).delete()

        noms = get_liste_nom()
        inv_introuvables = []
        for num_mgg, nom_fichier in photo_mapping(noms):
            inv = inventaires.objects.filter(num_mgg=num_mgg).first()
            if inv != None:
                photo = photographie(nom_fichier=nom_fichier)
                photo.save()
                commentaire_photo = commentairephoto(inventaire=inv, photographie=photo, commentaire=IMPORT_AUTO)
                commentaire_photo.save();
                print("Photo %d created for %d" % (photo.id, inv.id))
            else:
                inv_introuvables.append((num_mgg, nom_fichier))
        print('nb lignes supprimées: %s' % nb_lignes_supprimees)
        print(inv_introuvables)

    operations = [
        # migrations.RunPython(import_photo),
    ]


class MappingsTestCaseWithDB(django.test.TestCase):
    def setUp(self):
        Inventaire.objects.create(nom="test", num_mgg="MGG_0037", num_mjb1="003")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0047", num_mjb1="004")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0048", num_mjb1="004A")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0068", num_mjb1="010")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0069", num_mjb1="010")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0080", num_mjb1="004F")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0478", num_mjb1="83A")
        Inventaire.objects.create(nom="test", num_mgg="MGG_0479", num_mjb1="83A")

    def test_mapp_vide(self):
        assert photo_mapping([]) == []

    def test_mapp_nominal(self):
        self.assertEqual(photo_mapping(['003-xxx.jpeg', ]), [('MGG_0037', '003-xxx.jpeg'), ])

    def test_mapp_mjb_incomplet_dans_nom(self):
        self.assertEqual(photo_mapping(['3-xxx.jpeg', ]), [('MGG_0037', '3-xxx.jpeg'), ])
        self.assertEqual(photo_mapping(['04F-xxx.jpeg', ]), [('MGG_0080', '04F-xxx.jpeg'), ])

    def test_mapp_mjb_incomplet_en_base(self):
        self.assertEqual(photo_mapping(['83A-xxx.jpeg', ]), [('MGG_0478', '83A-xxx.jpeg'), ])

    def test_num_mjb_multiple_en_base(self):
        self.assertEqual(photo_mapping(['10-xxx.jpeg', ]), [('MGG_0068', '10-xxx.jpeg'), ])
        self.assertEqual(photo_mapping(['010-xxx.jpeg', ]), [('MGG_0068', '010-xxx.jpeg'), ])

    def test_mapp_ordre_maintenu(self):
        self.assertEqual(photo_mapping(['03-xxx.jpeg',
                                        '010-xxx.jpeg',
                                        '004A-xxx.jpeg', ]), [('MGG_0037', '03-xxx.jpeg'),
                                                              ('MGG_0068', '010-xxx.jpeg'),
                                                              ('MGG_0048', '004A-xxx.jpeg')])

    def test_mapp_NA(self):
        self.assertEqual(photo_mapping(['xxx']), [])


class UtilsTestCase(unittest.TestCase):
    def ko_test_noms_reels(self):
        self.assertEqual(
            [
               '3-petite-femme-boule-marron.jpeg',
               '1-F1-apparition-platre-MG.jpg',
               '1-F2-Gr-Valerie.jpeg',
               '3-petite-femme-boule-bleu.jpeg',
               '2-Grosse-femme-boule_terre.jpg',
                '147-Eva-page68-vente-Sadde-Dijon2017-140€.png',
               'images-inventaire.php',
               '1-Petite-Valérie-platre-CBG2.jpg',
               '01-Grande-Valérie-plâtre-MG.jpg'],
            get_liste_nom())

    def test_mignature(self):
        tests = ['1-F2-Gr-Valerie-150x150.jpeg',
                 '1-F2-Gr-Valerie-205x300.jpeg',
                 '1-F2-Gr-Valerie-700x1024.jpeg',
                 '1-F2-Gr-Valerie-768x1124.jpeg',
                 '1-F2-Gr-Valerie.jpeg',
                 '147-Eva-page68-vente-Sadde-Dijon2017-140%E2%82%AC-768x471.png',
                 '147-Eva-page68-vente-Sadde-Dijon2017-140%E2%82%AC.png']
        attendu = [True, True, True, True, False, True, False]
        self.assertEqual(attendu, [mignature(nom) for nom in tests])
