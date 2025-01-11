from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,OTP

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'role')
    ordering = ('email',)
    search_fields = ('email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'address', 'weight', 'height', 'dob', 'photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(OTP)
