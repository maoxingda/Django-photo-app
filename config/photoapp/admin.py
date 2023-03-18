from django.contrib import admin
from .models import Photo


# Register your models here.
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.submitter_id:
            obj.submitter = request.user
        super().save_model(request, obj, form, change)

    exclude = ('submitter',)
