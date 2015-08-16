from django.contrib import admin
from apps.hello.models import Profile, RequestHistory, EventHistory


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'last_name',
                    'date_of_birth',
                    'bio',
                    'jabber',
                    'skype',
                    'other_contacts',
                    'admin_preview')
    search_fields = ('name', 'last_name', 'email')
    readonly_fields = ('photo_preview', 'photo')


class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = ('path',
                    'host',
                    'method',
                    'ip',
                    'date',
                    'is_viewed')
    list_filter = ('host', 'ip', 'method')


class EventHistoryAdmin(admin.ModelAdmin):
    list_display = ('model', 'event', 'date')

admin.site.register(Profile, UserAdmin)
admin.site.register(RequestHistory, RequestHistoryAdmin)
admin.site.register(EventHistory, EventHistoryAdmin)
