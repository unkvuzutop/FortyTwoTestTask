from django.contrib import admin

# Register your models here.
from apps.hello.models import User, RequestHistory

admin.site.register(User)
admin.site.register(RequestHistory)
