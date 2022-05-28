from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class Config(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'last_login')
    list_filter = ('role' ,'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ['id']
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('id', 'date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('last_name', 'first_name', 'middle_initial', 'picture', 'mobile_number')}),
        (("Permissions"), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide'), 'fields': ('email', 'password1', 'password2')}),
    )


admin.site.register(CustomUser, Config)
admin.site.register(Evaluator)
admin.site.register(Student)
admin.site.register(Incident)
admin.site.register(Followup)
admin.site.register(Notification)
admin.site.register(News)
admin.site.register(Event)