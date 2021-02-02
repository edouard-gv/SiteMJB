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
    readonly_fields = ['lien_de_suite', 'vignette', 'date_creation', 'date_modification', ]
    fieldsets = [
        (None, {
            'fields': (('num_mgg', 'nom', 'vignette'), ('num_mjb1', 'num_mjb2'),)
        }),
        (None, {
            'fields': ('description', 'notes_mjb')
        }),
        (None, {
            'fields': ('commande', ('volume', 'dim_hauteur', 'dim_base'))
        }),
        (None, {
            'fields': (('date_creation', 'date_modification'),)
        }),
        ("DE SUITE (PARENT)", {
            'fields': (('type_original_moulage', 'lien_de_suite', 'inventaire_parent'),)
        }),
    ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': INPUT_WIDTH})},
    }

    date_hierarchy = 'date_modification'
    list_display_links = ['num_mgg', ]
    list_filter = ['themes__mot_cle', 'matieres__matiere', 'commande', 'volume', ]
    list_display = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'de_suite', 'vignette',]
    search_fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]
    ordering = ['-num_mgg', ]

    def lien_de_suite(self, inventaire):
        return inventaire.inventaire_parent.lien() if inventaire.inventaire_parent else None

    def de_suite(self, inventaire):
        return self.lien_de_suite(inventaire)


class ContactAdmin(admin.ModelAdmin):
    inlines = (RelationContactInline, )
    exclude = ('import_id',)


class PhotographieAdmin(admin.ModelAdmin):
    readonly_fields = ('image', )
    inlines = (CommentairePhotoInline, )
    exclude = ('import_id',)


class MatiereAdmin(admin.ModelAdmin):
    #inlines = (InventaireMatiereInline, )
    exclude = ('import_id',)

    def get_ordering(self, request):
        return [Lower('matiere')]


class ThemeAdmin(admin.ModelAdmin):
    inlines = (InventaireThemeInline, )
    exclude = ('import_id',)


admin.site.register(Inventaire, InventaireAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Contact, ContactAdmin)

