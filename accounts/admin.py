from django.contrib import admin
from accounts.models import CustomUser, OtpCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, Group
from accounts.forms import UserCreationForm, UserChangeForm

admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    add_form = UserChangeForm
    list_display = ('phone_number', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login', 'created')

    fieldsets = (
        ('Main', {'fields': ('phone_number', 'password')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'is_baker')}),

    )

    add_fieldsets = (
        ('None', {'fields': ('phone_number', 'password')})
    )
    search_fields = ('phone_number',)
    ordering = ('is_admin',)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(OtpCode)
