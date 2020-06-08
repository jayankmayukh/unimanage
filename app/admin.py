from django.contrib import admin

# Register your models here.
from .models import (Person, Asset, SoftwareAsset, PhysicalAsset, Location)

# admin.site.register(Person)
# admin.site.register(SoftwareAsset)
# admin.site.register(PhysicalAsset)
# admin.site.register(Location)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number')

@admin.register(SoftwareAsset)
class SoftwareAssetAdmin(admin.ModelAdmin):
    list_display = ('name','contact_person', 'version','license_key','expiry_date', 'vendor', 'details')
    list_filter = ('contact_person', 'expiry_date', 'vendor')

@admin.register(PhysicalAsset)
class PhysicalAssetAdmin(admin.ModelAdmin):
    list_display = ('name','contact_person', 'location', 'expiry_date', 'vendor', 'details')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'caretaker')