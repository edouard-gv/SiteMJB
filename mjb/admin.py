from django.contrib import admin

from mjb.models import *


class InventaireMatiereInline(admin.TabularInline):
    model = Inventaire_Matiere
    extra = 1


class InventaireThemeInline(admin.TabularInline):
    model = Inventaire_Theme
    extra = 1


class RelationContactInline(admin.TabularInline):
    model = RelationContact
    extra = 1


class CommentairePhotoInline(admin.TabularInline):
    model = CommentairePhoto
    readonly_fields = ('vignette', 'lien', )
    extra = 1


class InventaireInline(admin.TabularInline):
    model = Inventaire
    fields = ['lien', 'vignette', 'nom', 'num_mgg', 'num_mjb1', 'num_mjb2', ]
    readonly_fields = ['vignette', 'lien', ]
    extra = 1


class InventaireAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, RelationContactInline, InventaireInline, InventaireMatiereInline, InventaireThemeInline)
    readonly_fields = ['lien_de_suite', 'vignette', ]
    exclude = ['import_id', ]

    date_hierarchy = 'date_modification'
    list_display_links = ['num_mgg', ]
    list_filter = ['themes__mot_cle', 'matieres__matiere', 'commande', 'volume', ]
    list_display = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'de_suite', 'vignette',]
    search_fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]

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


class ThemeAdmin(admin.ModelAdmin):
    inlines = (InventaireThemeInline, )
    exclude = ('import_id',)


admin.site.register(Inventaire, InventaireAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Contact, ContactAdmin)

