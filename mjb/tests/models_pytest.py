from mjb.models import Photographie

def test_lien_vignette():
    photo = Photographie()
    photo.nom_fichier="ho.ho.jpg"
    assert photo.lien_vignette() == "https://www.mariejobourron.com/wp-content/uploads/inventaire/ho.ho-150x150.jpg"

def test_lien_vignette_sans_extension():
    photo = Photographie()
    photo.nom_fichier="hoho"
    assert photo.lien_vignette() == "https://www.mariejobourron.com/wp-content/uploads/inventaire/hoho-150x150"

