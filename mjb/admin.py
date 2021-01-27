from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    readonly_fields = ('vignette', 'inventaire_' )
    extra = 1

    def inventaire_(self, commentairePhoto):
        url = reverse("admin:mjb_inventaire_change", args=[commentairePhoto.inventaire.id])
        link = '<a href="%s">%s</a>' % (url, commentairePhoto.inventaire)
        return mark_safe(link)


class InventaireInline(admin.TabularInline):
    model = Inventaire
    fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', ]
    show_change_link = True
    extra = 1


class InventaireAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, RelationContactInline, InventaireInline, InventaireMatiereInline, InventaireThemeInline)
    readonly_fields = ('inventaire_parent_',)

    date_hierarchy = 'date_modification'
    list_display_links = ['num_mgg', ]
    list_filter = ['themes__mot_cle', 'matieres__matiere', 'commande', 'volume', ]
    list_display = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', 'inventaire_parent_', 'vignette']
    search_fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]

    def inventaire_parent_(self, inventaire):
        if (inventaire.inventaire_parent):
            url = reverse("admin:mjb_inventaire_change", args=[inventaire.inventaire_parent.id])
            link = '<a href="%s">%s</a>' % (url, inventaire.inventaire_parent)
            return mark_safe(link)
        else:
            return None

    def vignette(self, inventaire):
        if inventaire.photographies.count() >= 1:
            return inventaire.photographies.all()[0].vignette50()
        else:
            return None


class ContactAdmin(admin.ModelAdmin):
    inlines = (RelationContactInline, )


class PhotographieAdmin(admin.ModelAdmin):
    readonly_fields = ('image', )
    inlines = (CommentairePhotoInline, )


class MatiereAdmin(admin.ModelAdmin):
    #inlines = (InventaireMatiereInline, )
    pass


class ThemeAdmin(admin.ModelAdmin):
    inlines = (InventaireThemeInline, )


admin.site.register(Inventaire, InventaireAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Contact, ContactAdmin)

