# accounts/admin.py
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ITAsset, RetailAsset, Outlet

# Create resource classes
class ITAssetResource(resources.ModelResource):
    class Meta:
        model = ITAsset
        fields = ('id', 'asset_id', 'outlet__name', 'item', 'serial_number', 
                  'local_ip', 'port', 'mac_address', 'device_model', 'status')
        export_order = fields

class RetailAssetResource(resources.ModelResource):
    class Meta:
        model = RetailAsset
        fields = ('id', 'asset_id', 'outlet__name', 'item', 'brand', 
                  'model', 'sn', 'status')
        export_order = fields

# Register with export functionality
@admin.register(ITAsset)
class ITAssetAdmin(ImportExportModelAdmin):
    resource_class = ITAssetResource
    list_display = ('asset_id', 'item', 'outlet', 'serial_number', 'status')
    list_filter = ('asset_type', 'status', 'outlet')
    search_fields = ('asset_id', 'serial_number', 'item')

@admin.register(RetailAsset)
class RetailAssetAdmin(ImportExportModelAdmin):
    resource_class = RetailAssetResource
    list_display = ('asset_id', 'item', 'outlet', 'sn', 'status')
    list_filter = ('status', 'outlet')
    search_fields = ('asset_id', 'sn', 'item')

@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ('name',)