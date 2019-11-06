"""Register models to django admin."""
from django.contrib import admin
from django.contrib.auth.models import Group

from api.models import User


MODELS = []#TODO: add other models


class UserAdmin(admin.ModelAdmin):
    """Customize user/admin view on djano admin."""

    search_fields = ('email', 'username' )
    list_display = ('username', 'email', 'admin')
    list_filter = ('active', 'admin')
    orderimng = ('username', 'email')
    # filter_horizontal = ('user_type','bio') many to many with profile/roles

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('admin',)}),
        ('Primary personal information', {
            'fields': ('user_type',)}),
        ('Status', {'fields': ('active', )}),
    )


admin.site.register(User, UserAdmin)

for model in MODELS:
    admin.site.register(model)

admin.site.unregister(Group)
