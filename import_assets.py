import pandas as pd
from accounts.models import ITAsset, RetailAsset, Outlet
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import assets from Excel files into the database'

    def handle(self, *args, **kwargs):
        # Load IT Assets data
        it_assets_df = pd.read_excel('/path/to/itassetdetail.xlsx')  # Replace with your file path
        retail_assets_df = pd.read_excel('/path/to/retailassetdetail.xlsx')  # Replace with your file path

        # Check IT Asset data
        print(f"Loaded {len(it_assets_df)} IT Assets")
        print(it_assets_df.head())

        # Check Retail Asset data
        print(f"Loaded {len(retail_assets_df)} Retail Assets")
        print(retail_assets_df.head())

        # Iterate through IT assets and save them to the database
        for index, row in it_assets_df.iterrows():
            outlet, created = Outlet.objects.get_or_create(name=row['outlet'])  # Assuming outlet exists in the Excel file
            it_asset = ITAsset(
                item=row['item'],
                brand=row['brand'],
                serial_number=row['serial_number'],
                date_purchase=row['date_purchase'],
                network=row['network'],
                cpu=row['cpu'],
                gpu=row['gpu'],
                memory=row['memory'],
                ip_address=row['ip_address'],
                mac_address=row['mac_address'],
                disk=row['disk'],
                status=row['status'],
                operating_system=row['operating_system'],
                gpon_sn=row['gpon_sn'],
                wifi_type=row['wifi_type'],
                model=row['model'],
                hostname=row['hostname'],
                remark=row['remark'],
                outlet=outlet
            )
            it_asset.save()
            print(f"Imported IT Asset: {row['item']}")

        # Iterate through Retail assets and save them to the database
        for index, row in retail_assets_df.iterrows():
            outlet, created = Outlet.objects.get_or_create(name=row['outlet'])  # Assuming outlet exists in the Excel file
            retail_asset = RetailAsset(
                item=row['item'],
                brand=row['brand'],
                serial_number=row['serial_number'],
                date_purchase=row['date_purchase'],
                outlet=outlet
            )
            retail_asset.save()
            print(f"Imported Retail Asset: {row['item']}")

        self.stdout.write(self.style.SUCCESS('Data import completed!'))
