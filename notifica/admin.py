from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from notifica.models import *

admin.site.register(ExtendedUser, UserAdmin)
admin.site.register(Org)
admin.site.register(Activity)
admin.site.register(Notify)
admin.site.register(Position)
admin.site.register(Message)
