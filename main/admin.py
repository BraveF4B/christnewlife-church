from django.contrib import admin
from .models import Booking, Pastor, PastorWife, GalleryImage, Event


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'consultation_type', 'preferred_date', 'preferred_time', 'status', 'created_at']
    list_filter = ['status', 'consultation_type']
    search_fields = ['full_name', 'phone', 'email']
    list_editable = ['status']


@admin.register(Pastor)
class PastorAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']


@admin.register(PastorWife)
class PastorWifeAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'status', 'is_active')
    list_filter = ('status', 'is_active')
