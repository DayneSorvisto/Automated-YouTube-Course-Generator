from django.contrib import admin
from .models import Course 

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "is_premium", "is_approved")
#admin.site.unregister(User)
admin.site.register(Course, CourseAdmin)