from django.contrib import admin

from .models import GymMembersByOwner

class GymMembersByOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'gym', 'name', 'phone_number', 'email', 'is_archive', 'is_delete')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone_number', 'email')

admin.site.register(GymMembersByOwner,GymMembersByOwnerAdmin)
# Register your models here.
