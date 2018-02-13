from copy import deepcopy

from django.contrib import admin
from django.contrib.auth import get_user_model
from mezzanine.accounts.admin import UserProfileAdmin
from mezzanine.pages.admin import PageAdmin

User = get_user_model()

# Register your models here.
from .models import Title, Profile, ProfilesPage

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    max_num = 1

class UserAdmin(UserProfileAdmin):
    inlines = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'phone', 'university', 'department', 'country', 'in_participants_page')

admin.site.register(Title)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfilesPage, PageAdmin)

if User in admin.site._registry:
    admin.site.unregister(User)
admin.site.register(User, UserAdmin)