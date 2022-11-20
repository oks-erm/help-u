from django.contrib import admin
from .models import Conversation, Message


admin.site.register(Message)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    fields = ('name', 'members')
    list_display = ('name',)
    readonly_fields = ('members',)
    search_fields = ('members',)

    def name(self, obj):
        return f"{obj.name} {obj.members}"

    def id(self, obj):
        return f"{obj.id}"