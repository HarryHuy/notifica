from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Activity, ExtendedUser, \
    Organization, Position

admin.site.register(ExtendedUser, UserAdmin)
admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(Position)
