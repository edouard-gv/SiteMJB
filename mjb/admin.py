from django.contrib import admin
from mjb.models import Theme, Contact, Photographie, Matiere, Inventaire, CommentairePhoto, RelationContact

class RelationContactInline(admin.TabularInline):
    model = RelationContact
    extra = 1

class CommentairePhotoInline(admin.TabularInline):
    model = CommentairePhoto
    extra = 1

class InventoryAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, RelationContactInline, )

class ContactAdmin(admin.ModelAdmin):
    inlines = (RelationContactInline, )

class PhotographieAdmin(admin.ModelAdmin):
    inlines = (CommentairePhotoInline, )

admin.site.register(Inventaire, InventoryAdmin)
admin.site.register(Theme)
admin.site.register(Photographie, PhotographieAdmin)
admin.site.register(Matiere)
admin.site.register(Contact, ContactAdmin)

