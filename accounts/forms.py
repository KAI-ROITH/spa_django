# accounts/forms.py

from django import forms
from .models import RetailAsset, ITAsset, Service


class DateInput(forms.DateInput):
    """Custom date input widget with calendar picker"""
    input_type = 'date'
    
    def __init__(self, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
            'placeholder': 'Select date...'
        })
        super().__init__(**kwargs)


class RetailAssetForm(forms.ModelForm):
    class Meta:
        model = RetailAsset
        fields = [
            'asset_id', 'outlet', 'item', 'brand', 'model', 'power_input', 
            'sn', 'date_purchase', 'allocation', 'status', 'remark', 'active'  # ← ADDED 'allocation'
        ]
        widgets = {
            'asset_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50 font-mono font-bold',
                'placeholder': 'e.g., CHILLER01, PRINTER01...',
                'id': 'asset_id_field'
            }),
            'date_purchase': DateInput(),
            'outlet': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50'
            }),
            'item': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'placeholder': 'Enter item name...',
                'id': 'item_field'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'placeholder': 'Enter brand...'
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'placeholder': 'Enter model...'
            }),
            'power_input': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'placeholder': 'e.g., 220V...'
            }),
            'sn': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50 font-mono',
                'placeholder': 'Serial number...'
            }),
            # ↓ NEW FIELD ADDED
            'allocation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'placeholder': 'e.g., Store Room, Kitchen, Counter Area...'
            }),
            # ↑ NEW FIELD ADDED
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50'
            }),
            'remark': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition bg-gray-50',
                'rows': 4,
                'placeholder': 'Add any notes or remarks...'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'sr-only peer'
            }),
        }


class ITAssetForm(forms.ModelForm):
    class Meta:
        model = ITAsset
        fields = [
            # ADD asset_id at the beginning
            'asset_id',
            
            # Basic Info
            'item', 'brand', 'serial_number', 'date_purchase', 'outlet', 'asset_type',
            
            # Computer/CPU Fields
            'cpu', 'gpu', 'memory', 'disk', 'operating_system', 'hostname', 'model',
            
            # Network Fields
            'ip_address', 'mac_address', 'network', 'gpon_sn', 'wifi_type',
            
            # CCTV Fields - Complete List
            'local_ip', 'port', 'version', 'device_type', 'device_model', 'build',
            'power_adapter', 'video_input', 'total_channel', 'nic_speed', 
            'hdd_total_space', 'hardware_version', 'software_version', 
            'system_version', 'web_version', 'onvif_server_version', 
            'onvif_client_version', 'security_baseline_version', 
            'firmware_version', 'location', 'hybrid', 'wip', 'p2p_qr',
            
            # ↓ NEW FIELD ADDED
            'allocation',
            # ↑ NEW FIELD ADDED
            
            # Status
            'status', 'remark', 'active'
        ]
        
        widgets = {
            # Asset ID field
            'asset_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono font-bold',
                'placeholder': 'e.g., CPU01, CCTV01...',
                'id': 'asset_id_field'
            }),
            
            # Date picker with calendar
            'date_purchase': DateInput(),
            
            # Select dropdowns
            'outlet': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50'
            }),
            'asset_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'id': 'asset_type_field'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50'
            }),
            
            # Basic Text Inputs
            'item': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Enter item name...'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Enter brand...'
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Device model (optional)...'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': 'Serial number...'
            }),
            
            # Computer Fields
            'hostname': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': 'e.g., PC-BRANCH01...'
            }),
            'cpu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., Intel Core i5...'
            }),
            'gpu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., NVIDIA GTX 1650...'
            }),
            'memory': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 16GB...'
            }),
            'disk': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 512GB SSD...'
            }),
            'operating_system': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., Windows 11...'
            }),
            
            # Network Fields
            'ip_address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': '192.168.1.1'
            }),
            'mac_address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': '00:1B:44:11:3A:B7'
            }),
            'local_ip': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': '192.168.1.1'
            }),
            'nic_speed': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 1.0 Gbps'
            }),
            'network': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Network name...'
            }),
            'gpon_sn': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': 'GPON serial number...'
            }),
            'wifi_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., WiFi 6...'
            }),
            
            # CCTV Specific Fields
            'port': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50 font-mono',
                'placeholder': 'e.g., 37777, 554'
            }),
            'version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Main version...'
            }),
            'device_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., DVR, NVR, XVR'
            }),
            'device_model': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Device model number...'
            }),
            'build': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Build number...'
            }),
            'power_adapter': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 12V 2A'
            }),
            'video_input': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Video input specifications...'
            }),
            'total_channel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 16/24, 8/16'
            }),
            'hdd_total_space': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., 4TB, 8TB'
            }),
            
            # Version Fields
            'hardware_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Hardware version...'
            }),
            'software_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Software version...'
            }),
            'system_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'System version...'
            }),
            'web_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Web interface version...'
            }),
            'onvif_server_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'ONVIF Server version...'
            }),
            'onvif_client_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'ONVIF Client version...'
            }),
            'security_baseline_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Security Baseline version...'
            }),
            'firmware_version': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Firmware version...'
            }),
            
            # Additional CCTV Fields
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Physical location...'
            }),
            'wip': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'WIP information...'
            }),
            'p2p_qr': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'P2P QR code or ID...'
            }),
            
            # ↓ NEW FIELD ADDED
            'allocation': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'e.g., Server Room, Office Desk 3, Reception...'
            }),
            # ↑ NEW FIELD ADDED
            
            # Remarks
            'remark': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'rows': 4,
                'placeholder': 'Add any notes or remarks...'
            }),
            
            # Checkboxes
            'hybrid': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-5 h-5 cursor-pointer'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'sr-only peer'
            }),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_date', 'description', 'technician']
        widgets = {
            'service_date': DateInput(),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'rows': 4,
                'placeholder': 'Describe the service performed...'
            }),
            'technician': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition bg-gray-50',
                'placeholder': 'Technician name...'
            }),
        }