from django.contrib import admin

# Register your models here.
from apps.hello.models import User

admin.site.register(User)