from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# region-----------USUARIOS---------------------------------------------------------------------------------------


class ExtendUserInline(admin.StackedInline):
    model = Usuarios
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ExtendUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
