from django.contrib import admin
from .models import Gym, GymImage, GymPlan, GymProduct, ProductImage, GymMember


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'address', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'owner__email', 'owner__full_name')
    ordering = ('-id',)


@admin.register(GymImage)
class GymImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'gym', 'image', 'uploaded_at')
    search_fields = ('gym__name',)
    ordering = ('-uploaded_at',)


@admin.register(GymPlan)
class GymPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gym', 'price')
    search_fields = ('name', 'gym__name')
    ordering = ('-id',)


@admin.register(GymProduct)
class GymProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gym', 'price')
    search_fields = ('name', 'gym__name')
    ordering = ('-id',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'gym', 'image', 'uploaded_at')
    search_fields = ('gym__name',)
    ordering = ('-uploaded_at',)


@admin.register(GymMember)
class GymMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'gym', 'status', 'joined_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'user__full_name', 'gym__name')
    ordering = ('-joined_at',)
