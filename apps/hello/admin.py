from django.contrib import admin
from apps.hello.models import User, RequestHistory


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'last_name',
                    'date_of_birth',
                    'bio',
                    'jabber',
                    'skype',
                    'other_contacts')
    search_fields = ('name', 'last_name', 'email')


class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = ('path',
                    'host',
                    'method',
                    'ip',
                    'date',
                    'is_viewed')
    list_filter = ('host', 'ip', 'method')

admin.site.register(User, UserAdmin)
admin.site.register(RequestHistory, RequestHistoryAdmin)
