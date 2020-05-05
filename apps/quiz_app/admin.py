from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('video_title','question')

    def video_title(self, instance):
        return instance.video.title
#admin.site.unregister(User)
admin.site.register(Question, QuestionAdmin)