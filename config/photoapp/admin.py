from django.contrib import admin
from .models import Photo, CnTag, CnTaggedItem


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.submitter_id:
            obj.submitter = request.user
        super().save_model(request, obj, form, change)

    exclude = ('submitter',)


class TaggedItemInline(admin.TabularInline):
    model = CnTaggedItem
    extra = 0

    readonly_fields = ('content_type', 'object_id',)


@admin.register(CnTag)
class CnTagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    exclude = ["slug"]
