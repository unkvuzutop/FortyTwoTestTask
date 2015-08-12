from django.contrib import admin
from apps.hello.models import Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'last_name',
                    'date_of_birth',
                    'bio',
                    'jabber',
                    'skype',
                    'other_contacts')
    search_fields = ('name', 'last_name', 'email')

admin.site.register(Profile, UserAdmin)
