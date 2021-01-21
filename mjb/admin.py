from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

import mjb
from mjb.models import Theme, Contact, Photographie, Matiere, Inventaire, CommentairePhoto, RelationContact

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
    inlines = (CommentairePhotoInline, RelationContactInline, InventaireInline, )
    date_hierarchy = 'date_creation'
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

admin.site.register(Inventaire, InventoryAdmin)
admin.site.register(Theme)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere)
admin.site.register(Contact, ContactAdmin)

