from django.contrib import admin
from .models import Crop  # adjust if it's a different model

admin.site.register(Crop)


# @admin.register(Crop)
# class CropAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description', 'image')  # or thumbnail preview
