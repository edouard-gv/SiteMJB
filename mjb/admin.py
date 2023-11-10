from django.contrib import admin
from django.db.models.functions import Lower
from django.forms import TextInput

from mjb.models import *

INPUT_WIDTH = '20'


class InventaireMatiereInline(admin.TabularInline):
    model = Inventaire_Matiere
    verbose_name = "lien vers matière"
    verbose_name_plural = "Matières"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }
    extra = 0


class InventaireThemeInline(admin.TabularInline):
    model = Inventaire_Theme
    verbose_name = "lien vers thème"
    verbose_name_plural = "Thèmes"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }
    extra = 0


class RelationContactInline(admin.TabularInline):
    model = RelationContact
    verbose_name = "relation contact"
    verbose_name_plural = "Contacts / Mouvements"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }
    extra = 0


class CommentairePhotoInline(admin.TabularInline):
    model = CommentairePhoto
    verbose_name = "lien vers photo"
    readonly_fields = ('vignette', 'lien', )
    verbose_name_plural = "Photographies"
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }
    extra = 0


class InventaireInline(admin.TabularInline):
    model = Inventaire
    fields = ['lien', 'vignette', 'nom', 'num_mgg', 'num_mjb1', 'num_mjb2', ]
    readonly_fields = ['vignette', 'lien', ]
    verbose_name = "de suite enfant"
    verbose_name_plural = "De suites (enfants) - Modifier les champs ci-dessous modifiera la ou les pièces cibles, et non le lien avec celles-ci."
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }
    extra = 0


class InventaireAdmin(admin.ModelAdmin):
    inlines = (InventaireInline, InventaireMatiereInline, InventaireThemeInline, CommentairePhotoInline, RelationContactInline, )
    readonly_fields = ['lien_original', 'vignette_original', 'de_suite_de', 'vignette', 'date_creation', 'date_modification', 'notes_marie_jo_parent', 'description_du_modèle']
    readonly_fields_modele = ['lien_original', 'vignette_original', 'de_suite_de', 'vignette', 'date_creation', 'date_modification', 'notes_marie_jo_parent', ]
    fieldsets = [
        (None, {
            'fields': (('num_mgg', 'nom', 'vignette'), ('de_suite_de', 'vignette_original', ), ('num_mjb1', 'num_mjb2'),)
        }),
        (None, {
            'fields': ('description_du_modèle', 'description', 'notes_marie_jo_parent', 'notes_mjb')
        }),
        (None, {
            'fields': ('commande', ('volume', 'dim_hauteur', 'dim_base'))
        }),
        (None, {
            'fields': (('date_creation', 'date_modification'),)
        }),
        ("ORIGINAL (PARENT)", {
            'fields': (('type_original_moulage', 'lien_original', 'inventaire_parent'),)
        }),
    ]
    fieldsets_model = [
        (None, {
            'fields': (('num_mgg', 'nom', 'vignette'), ('de_suite_de', 'vignette_original', ), ('num_mjb1', 'num_mjb2'),)
        }),
        (None, {
            'fields': ('description_modele', 'description', 'notes_marie_jo_parent', 'notes_mjb')
        }),
        (None, {
            'fields': ('commande', ('volume', 'dim_hauteur', 'dim_base'))
        }),
        (None, {
            'fields': (('date_creation', 'date_modification'),)
        }),
        ("ORIGINAL (PARENT)", {
            'fields': (('type_original_moulage', 'lien_original', 'inventaire_parent'),)
        }),
    ]

    def get_fieldsets(self, request, obj=None):
        if obj is None or obj.inventaire_parent:
            return self.fieldsets
        else:
            return self.fieldsets_model

    def get_readonly_fields(self, request, obj=None):
        if obj is None or obj.inventaire_parent:
            return self.readonly_fields
        else:
            return self.readonly_fields_modele

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }

    date_hierarchy = 'date_modification'
    list_display_links = ['num_mgg', ]
    list_filter = ['themes__mot_cle', 'matieres__matiere', 'commande', 'volume', ]
    list_display = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'original', 'vignette',]
    search_fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]
    ordering = ['-num_mgg', ]

    def lien_original(self, inventaire):
        return inventaire.inventaire_parent.lien() if inventaire.inventaire_parent else None

    def vignette_original(self, inventaire):
        return inventaire.inventaire_parent.vignette() if inventaire.inventaire_parent else None

    def original(self, inventaire):
        return self.lien_original(inventaire)

    def de_suite_de(self, inventaire):
        return self.lien_original(inventaire)


class ContactAdmin(admin.ModelAdmin):
    #inlines = (RelationContactInline, )
    exclude = ('import_id',)

    ordering = ['institution', 'nom', 'prenom', ]
    #list_filter = ordering
    list_display = ordering
    search_fields = ordering
    list_display_links = ordering


class PhotographieAdmin(admin.ModelAdmin):
    readonly_fields = ('image', )
    inlines = (CommentairePhotoInline, )
    exclude = ('import_id', 'vignette_ok', 'image_ok')

    list_display = ['nom_fichier', 'vignette50', 'liens_inventaires', 'import_auto',]
    list_filter = ['image_ok', 'vignette_ok', 'import_auto', ]

    def liens_inventaires(self, photo):
        return mark_safe(" ".join([com.inventaire.lien()
                                   for com in CommentairePhoto.objects.filter(photographie_id = photo.id)]))


class MatiereAdmin(admin.ModelAdmin):
    #inlines = (InventaireMatiereInline, )
    exclude = ('import_id',)

    def get_ordering(self, request):
        return [Lower('matiere')]


class ThemeAdmin(admin.ModelAdmin):
    #inlines = (InventaireThemeInline, )
    exclude = ('import_id',)

    def get_ordering(self, request):
        return [Lower('mot_cle')]


admin.site.register(Inventaire, InventaireAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Contact, ContactAdmin)

