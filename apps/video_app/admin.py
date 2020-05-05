from django.contrib import admin
from .models import Video
# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title",)

#admin.site.unregister(User)
admin.site.register(Video, VideoAdmin)