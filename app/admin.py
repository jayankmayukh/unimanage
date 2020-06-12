from django.contrib import admin

# Register your models here.
from .models import (SoftwareAsset, PhysicalAsset, Location, AssetRequest)

admin.site.register(AssetRequest)
admin.site.register(SoftwareAsset)
admin.site.register(PhysicalAsset)
admin.site.register(Location)

# @admin.register(SoftwareAsset)
# class SoftwareAssetAdmin(admin.ModelAdmin):
#     list_display = ('name','contact_person', 'version','license_key','expiry_date', 'vendor', 'details')
#     list_filter = ('contact_person', 'expiry_date', 'vendor')

# @admin.register(PhysicalAsset)
# class PhysicalAssetAdmin(admin.ModelAdmin):
#     list_display = ('name','contact_person', 'location', 'expiry_date', 'vendor', 'details')

# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ('room_number', 'caretaker')