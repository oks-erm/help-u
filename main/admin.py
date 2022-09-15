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


class UserProfileAdmin(admin.ModelAdmin):
    fields = (('user', 'languages'),
              ('country', 'city'),
              'userpic',
              'bio')
    list_display = ('user', 'country', 'id')

    def id(self, obj):
        return f"{obj.user.id}"


class PostAdmin(admin.ModelAdmin):
    fields = ('author',
              'title',
              'slug',
              'image',
              'text',
              ('country', 'city'),
              ('status', 'relevance'),
              ('type', 'category'))
    list_display = ('title', 'author', 'created_on', 'status')


class ContactFormAdmin(admin.ModelAdmin):
    fields = (('name', 'email'),
              'subject',
              'message',
              'date')
    list_display = ('subject', 'name', 'email', 'date')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ContactFormMessage, ContactFormAdmin)

