from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Message,User,Session,Group,UserGroup,GroupMessage


# class SessionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'other_user', 'timestamp')
#     search_fields = ('user__username', 'other_user__username')
#     readonly_fields = ('timestamp',)  # Make the timestamp field read-only

# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'timestamp', 'session')
#     search_fields = ('sender__username', 'receiver__username', 'session__id')
#     readonly_fields = ('timestamp',)  # Make the timestamp field read-only

# admin.site.register(Session, SessionAdmin)
# admin.site.register(Message, MessageAdmin)

admin.site.register(get_user_model())
admin.site.register(Message)
admin.site.register(Session)
admin.site.register(Group)
admin.site.register(UserGroup)
admin.site.register(GroupMessage)
