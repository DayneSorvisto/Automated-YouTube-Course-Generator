"""python_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


from apps.user_app.models import User as U
class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)


from apps.video_app.models import Video
class VideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Video, VideoAdmin)


from apps.quiz_app.models import Question
class QuestionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Question, QuestionAdmin)


from apps.course_app.models import Course
class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)


urlpatterns = [
    url(r'^course/', include('apps.course_app.urls')),
    url(r'^course/', include('apps.video_app.urls')),
    url(r'^course/', include('apps.quiz_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.user_app.urls')),
]
