from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from guardian.admin import GuardedModelAdmin

from .models import Family, Member

class MemberAdminInline(admin.TabularInline):
    model = Member

class FamilyAdmin(GuardedModelAdmin):
    model = Family

class UserAdmin(UserAdmin):
    inlines = (MemberAdminInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Family, FamilyAdmin)
