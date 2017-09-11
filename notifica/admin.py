from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Organization)
admin.site.register(Activity)
admin.site.register(Notify)
admin.site.register(Position)
admin.site.register(Message)


class MemberOrgInline(admin.TabularInline):
    model = ExtendedUser.org.through
    extra = 1


class ExtendedUserAdmin(admin.ModelAdmin):
    inlines = [
        MemberOrgInline,
    ]

admin.site.register(ExtendedUser, ExtendedUserAdmin)
