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
    extra = 1


class InventaireInline(admin.TabularInline):
    model = Inventaire
    fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]
    show_change_link = True
    extra = 1


class InventoryAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, RelationContactInline, InventaireInline, InventaireMatiereInline, InventaireThemeInline)
    date_hierarchy = 'date_modification'
    list_display_links = ['num_mgg', ]
    list_filter = ['themes__mot_cle', 'matieres__matiere', 'commande', 'volume', ]
    list_display = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', 'parent_link', ]
    search_fields = ['nom', 'num_mgg', 'num_mjb1', 'num_mjb2', 'description', ]

    def parent_link(self, inventaire):
        if (inventaire.inventaire_parent):
            url = reverse("admin:mjb_inventaire_change", args=[inventaire.inventaire_parent.id])
            link = '<a href="%s">%s</a>' % (url, inventaire.inventaire_parent)
            return mark_safe(link)
        else:
            return None


class ContactAdmin(admin.ModelAdmin):
    inlines = (RelationContactInline, )


class PhotographieAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, )


class MatiereAdmin(admin.ModelAdmin):
    inlines = (InventaireMatiereInline, )


class ThemeAdmin(admin.ModelAdmin):
    inlines = (InventaireThemeInline, )


admin.site.register(Inventaire, InventoryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Contact, ContactAdmin)

