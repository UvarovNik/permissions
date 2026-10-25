from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

from advertisements.models import Advertisement

admin.site.register(Advertisement)
admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('first_name', 'last_name')
    search_fields = UserAdmin.search_fields + ('first_name', 'last_name')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Token, TokenAdmin)
