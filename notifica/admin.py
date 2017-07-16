from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from notifica.models import *

admin.site.register(Org)
admin.site.register(Activity)
admin.site.register(Notify)
admin.site.register(Position)
admin.site.register(Message)

class MemberOrgInline(admin.TabularInline):
    model = Org.member.through
    extra = 1

class ExtendedUserAdmin(admin.ModelAdmin):
    inlines = [
        MemberOrgInline,
    ]

admin.site.register(ExtendedUser, ExtendedUserAdmin)
