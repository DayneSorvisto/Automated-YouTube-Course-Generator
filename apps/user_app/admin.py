from django.contrib import admin
from .models import User
# Register your models here.
#admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_premium")

#admin.site.unregister(User)
admin.site.register(User, UserAdmin)