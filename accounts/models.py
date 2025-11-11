# accounts/models.py

from django.db import models
from django.utils import timezone
import re


class Outlet(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class RetailAsset(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Draft', 'Draft'),
    ]
    
    # Custom Asset ID
    asset_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Asset ID")
    
    # User field
    user = models.CharField(max_length=100, blank=True, null=True, verbose_name="Assigned User")
    
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    power_input = models.CharField(max_length=100)
    sn = models.CharField(max_length=100, unique=True)
    date_purchase = models.DateField(null=True, blank=True)
    allocation = models.CharField(max_length=255, blank=True, null=True)  # ← NEW FIELD ADDED
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Draft')
    remark = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.asset_id} - {self.item}" if self.asset_id else self.item
    
    @staticmethod
    def generate_asset_id(item_name):
        """
        Generate the next asset ID based on item name
        e.g., CHILLER01, CHILLER02, PRINTER01, etc.
        """
        # Extract the base name (remove numbers and special chars, keep only letters)
        base_name = re.sub(r'[^A-Za-z]', '', item_name).upper()
        
        if not base_name:
            base_name = "ASSET"
        
        # Find all existing asset IDs with this base name
        existing_assets = RetailAsset.objects.filter(
            asset_id__startswith=base_name
        ).values_list('asset_id', flat=True)
        
        if not existing_assets:
            # First asset of this type
            return f"{base_name}01"
        
        # Extract numbers from existing IDs and find the max
        max_num = 0
        for asset_id in existing_assets:
            match = re.search(r'\d+$', asset_id)
            if match:
                num = int(match.group())
                max_num = max(max_num, num)
        
        # Generate next number
        next_num = max_num + 1
        return f"{base_name}{next_num:02d}"


class ITAsset(models.Model):
    ITEM_TYPE_CHOICES = [
        ('cpu', 'CPU'),
        ('cctv', 'CCTV'),
        ('network', 'Network Device'),
        ('printer', 'Printer'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Draft', 'Draft'),
    ]
    
    # Custom Asset ID
    asset_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Asset ID")
    
    # User field
    user = models.CharField(max_length=100, blank=True, null=True, verbose_name="Assigned User")
    
    # P2P QR Image (NEW - Changed from CharField to ImageField)
    p2p_qr = models.ImageField(upload_to='p2p_qr/', blank=True, null=True, verbose_name='P2P QR Code')
    
    # ========== BASIC INFORMATION ==========
    item = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True)
    date_purchase = models.DateField(null=True, blank=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, default='cpu')
    allocation = models.CharField(max_length=255, blank=True, null=True)  # ← NEW FIELD ADDED
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Draft')
    active = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)
    
    # ========== COMPUTER/CPU FIELDS ==========
    cpu = models.CharField(max_length=100, blank=True, null=True)
    gpu = models.CharField(max_length=100, blank=True, null=True)
    memory = models.CharField(max_length=100, blank=True, null=True)
    disk = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    hostname = models.CharField(max_length=100, blank=True, null=True)
    
    # ========== NETWORK FIELDS ==========
    network = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    mac_address = models.CharField(max_length=100, blank=True, null=True)
    local_ip = models.CharField(max_length=100, blank=True, null=True)
    nic_speed = models.CharField(max_length=100, blank=True, null=True)
    gpon_sn = models.CharField(max_length=100, blank=True, null=True)
    wifi_type = models.CharField(max_length=100, blank=True, null=True)
    
    # ========== CCTV SPECIFIC FIELDS ==========
    port = models.CharField(max_length=50, blank=True, null=True, verbose_name='Port')
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Version')
    device_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='Device Type')
    device_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='Device Model')
    build = models.CharField(max_length=100, blank=True, null=True, verbose_name='Build')
    power_adapter = models.CharField(max_length=100, blank=True, null=True, verbose_name='Power Adapter/Cord')
    video_input = models.CharField(max_length=100, blank=True, null=True, verbose_name='Video Input')
    total_channel = models.CharField(max_length=100, blank=True, null=True, verbose_name='Total Channel')
    hdd_total_space = models.CharField(max_length=100, blank=True, null=True, verbose_name='HDD Total Space')
    hardware_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Hardware Version')
    software_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Software Version')
    system_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='System Version')
    web_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Web Version')
    onvif_server_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='ONVIF Server Version')
    onvif_client_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='ONVIF Client Version')
    security_baseline_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Security Baseline Version')
    firmware_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='Firmware Version')
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name='Location')
    hybrid = models.BooleanField(default=False, verbose_name='Hybrid')
    wip = models.CharField(max_length=100, blank=True, null=True, verbose_name='WIP')
    
    # ========== METADATA ==========
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.asset_id} - {self.item}" if self.asset_id else f"{self.item} - {self.serial_number}"
    
    @staticmethod
    def generate_asset_id(asset_type):
        """
        Generate the next asset ID based on asset type
        e.g., CPU01, CPU02, CCTV01, CCTV02, etc.
        """
        # Map asset type to prefix
        prefix_map = {
            'cpu': 'CPU',
            'cctv': 'CCTV',
            'network': 'NET',
            'printer': 'PRINT',
            'other': 'OTHER'
        }
        
        prefix = prefix_map.get(asset_type, 'IT').upper()
        
        # Find all existing asset IDs with this prefix
        existing_assets = ITAsset.objects.filter(
            asset_id__startswith=prefix
        ).values_list('asset_id', flat=True)
        
        if not existing_assets:
            # First asset of this type
            return f"{prefix}01"
        
        # Extract numbers from existing IDs and find the max
        max_num = 0
        for asset_id in existing_assets:
            match = re.search(r'\d+$', asset_id)
            if match:
                num = int(match.group())
                max_num = max(max_num, num)
        
        # Generate next number
        next_num = max_num + 1
        return f"{prefix}{next_num:02d}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'IT Asset'
        verbose_name_plural = 'IT Assets'


class NetworkAsset(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Maintenance', 'Under Maintenance'),
    ]
    
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, null=True, default='Unknown')
    model = models.CharField(max_length=100)
    power_rating = models.CharField(max_length=100)
    wifi_type = models.CharField(max_length=100)
    gpon_sn = models.CharField(max_length=100)
    sn = models.CharField(max_length=100)
    date_purchase = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    
    def __str__(self):
        return self.item


class Service(models.Model):
    asset = models.ForeignKey(RetailAsset, on_delete=models.CASCADE)
    service_date = models.DateField()
    description = models.TextField()
    technician = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Service for {self.asset.item} on {self.service_date}"
    
    class Meta:
        ordering = ['-service_date']