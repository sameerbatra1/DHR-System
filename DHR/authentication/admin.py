from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define what fields are displayed in the admin panel
    list_display = ('username', 'first_name', 'last_name', 'user_type', 'last_login', 'access_time')
    search_fields = ('username', 'last_name')
    readonly_fields = ('last_login',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'access_time')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'access_time')}
        ),
    )
    ordering = ('username',)

admin.site.register(User, UserAdmin)
