from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'),
              ('email', 'is_staff'),
              ('date_joined', 'last_login'),
              'user_permissions',
              'groups',
              'is_active')
    list_display = ('name', 'email', 'id', 'is_active')

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def id(self, obj):
        return f"{obj.id}"


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(ContactFormMessage)

