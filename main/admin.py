from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'),
              ('email', 'is_staff'),
              ('date_joined', 'last_login'),
              'user_permissions',
              'groups',
              'is_active')
    list_display = ('name', 'email', 'id', 'is_active')
    list_filter = ('is_staff', 'date_joined', 'last_login', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def id(self, obj):
        return f"{obj.id}"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = (('user', 'languages'),
              ('country', 'city'),
              'thumbnail_preview',
              'userpic',
              'bio')
    list_display = ('user', 'country', 'languages', 'active', 'id')
    readonly_fields = ('thumbnail_preview',)
    search_fields = ('user', 'bio', 'country', 'city', 'languages')

    def id(self, obj):
        return f"{obj.user.id}"

    def active(self, obj):
        return f"{obj.user.is_active}"

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('user',
              'created_on',
              'post',
              'body',
              'approved')
    list_display = ('user', 'created_on', 'approved')
    readonly_fields = ('user', 'post', 'created_on')
    list_filter = ('approved', 'created_on')
    search_fields = ('user', 'body')
 
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(status=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('author',
              'title',
              'image',
              'thumbnail_preview',
              'text',
              ('country', 'city'),
              'area',
              ('status', 'relevance'),
              ('type', 'category'))
    list_display = ('title', 'author', 'country', 'created_on', 'type', 'status')
    readonly_fields = ('thumbnail_preview',)
    list_filter = ('type', 'status', 'created_on')
    search_fields = ('name', 'email', 'author', 'title')
 
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status=True)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


@admin.register(ContactFormMessage)
class ContactFormAdmin(admin.ModelAdmin):
    fields = (('name', 'email'),
              'subject',
              'message',
              'date',
              'responded')
    list_display = ('subject', 'name', 'email', 'date', 'responded')
    readonly_fields = ('date',)
    list_filter = ('date', 'responded')
    search_fields = ('name', 'email', 'subject', 'message')

    actions = ['mark_as_responded']

    def mark_as_responded(self, request, queryset):
        queryset.update(responded=True)

