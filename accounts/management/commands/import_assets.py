from django.core.management.base import BaseCommand
import pandas as pd
from accounts.models import ITAsset, Outlet
from django.db.models import Count

class Command(BaseCommand):
    help = 'Imports data from Excel files into the database'

    def handle(self, *args, **kwargs):
        # Import Network Assets
        self.import_network_assets()
        # Import CPU Assets
        self.import_cpu_assets()
        # Import Retail Assets
        self.import_retail_assets()
        # Import CCTV Assets
        self.import_cctv_assets()

    def import_network_assets(self):
        network_file_path = r'C:\Users\User\Downloads\networkassetdetail.xlsx'
        network_df = pd.read_excel(network_file_path)

        self.stdout.write(self.style.SUCCESS(f"Columns in network asset file: {network_df.columns}"))

        if 'Date Purchase' in network_df.columns:
            network_df['Date Purchase'] = pd.to_datetime(network_df['Date Purchase'], errors='coerce')
        else:
            self.stdout.write(self.style.ERROR("'Date Purchase' column is missing!"))
            return

        network_df['Date Purchase'] = network_df['Date Purchase'].fillna(None)

        for index, row in network_df.iterrows():
            outlet_instance, created = Outlet.objects.get_or_create(name=row['Outlet'])

            network_asset = ITAsset(
                outlet=outlet_instance,
                item=row['Item'],
                ip_address=row['IP Address'],
                mac_address=row['MAC Address'],
                brand=row['Brand'],
                model=row['Model'],
                power_rating=row['Power Rating'],
                wifi_type=row['WiFi_Type'],
                gpon_sn=row['GPON SN'],
                sn=row['SN'],
                date_purchase=row['Date Purchase'],
                status=row['Status']
            )
            network_asset.save()

        self.stdout.write(self.style.SUCCESS("Network assets imported successfully"))

    def import_cpu_assets(self):
        cpu_file_path = r'C:\Users\User\Downloads\cpuassetdetail.xlsx'
        cpu_df = pd.read_excel(cpu_file_path, header=3)

        self.stdout.write(self.style.SUCCESS(f"First few rows in cpu asset file: {cpu_df.head()}"))

        cpu_df.columns = cpu_df.columns.astype(str).str.strip()

        if 'Date Purchase' in cpu_df.columns:
            cpu_df['Date Purchase'] = pd.to_datetime(cpu_df['Date Purchase'], errors='coerce')
        else:
            self.stdout.write(self.style.ERROR("'Date Purchase' column is missing!"))
            return

        for index, row in cpu_df.iterrows():
            cpu_asset = ITAsset(
                outlet=row['Outlet'],
                type=row['TYPE'],
                assigned=row['Assigned'],
                hostname=row['HOSTNAME'],
                serial_number=row['SerialNumber'],
                motherboard_model=row['Motherboard Model'],
                operating_system=row['Operating System'],
                cpu=row['CPU'],
                memory=row['Memory'],
                gpu=row['GPU'],
                ip_address=row['IP Address'],
                mac_address=row['MAC Address'],
                disk=row['Disk'],
                disk_id=row['Disk ID'],
                date_purchase=row['Date Purchase'] if pd.notna(row['Date Purchase']) else None
            )
            cpu_asset.save()

        self.stdout.write(self.style.SUCCESS("CPU assets imported successfully"))

    def import_retail_assets(self):
        retail_file_path = r'C:\Users\User\Downloads\retailassetdetail.xlsx'
        retail_df = pd.read_excel(retail_file_path, header=2)

        self.stdout.write(self.style.SUCCESS(f"First few rows in retail asset file: {retail_df.head()}"))

        retail_df.columns = retail_df.columns.astype(str).str.strip()

        if 'Date Purchase' in retail_df.columns:
            retail_df['Date Purchase'] = pd.to_datetime(retail_df['Date Purchase'], errors='coerce')
        else:
            self.stdout.write(self.style.ERROR("'Date Purchase' column is missing!"))
            return

        for index, row in retail_df.iterrows():
            outlet_instance, created = Outlet.objects.get_or_create(name=row['Outlet'])

            retail_asset = ITAsset(
                outlet=outlet_instance,
                item=row['Item'],
                brand=row['Brand'],
                model=row['Model'],
                power_adapter=row['Power Input'],  # power_input should match model
                serial_number=row['SN'],  # sn should match model
                date_purchase=row['Date Purchase'] if pd.notna(row['Date Purchase']) else None,
                status=row['Status'],
                remark=row['Remark']
            )
            retail_asset.save()

        self.stdout.write(self.style.SUCCESS("Retail assets imported successfully"))

    def import_cctv_assets(self):
        cctv_file_path = r'C:\Users\User\Downloads\cctvassetdetail.xlsx'
        try:
            cctv_df = pd.read_excel(cctv_file_path, header=1)
        except Exception as e:
            self.stderr.write(f"Failed to read CCTV Excel: {e}")
            return

        # Normalize column names
        cctv_df.columns = cctv_df.columns.astype(str).str.strip()
        self.stdout.write(self.style.SUCCESS(f"CCTV columns: {cctv_df.columns.tolist()}"))

        # Forward-fill Outlet because Excel uses blank cells to mean "same as above"
        if 'Outlet' in cctv_df.columns:
            cctv_df['Outlet'] = cctv_df['Outlet'].ffill()
        else:
            self.stderr.write("'Outlet' column missing in CCTV sheet")
            return

        # Parse Build to dates (dayfirst=True for dd-mm-yy)
        if 'Build' in cctv_df.columns:
            cctv_df['Build_parsed'] = pd.to_datetime(cctv_df['Build'], dayfirst=True, errors='coerce')
        else:
            cctv_df['Build_parsed'] = pd.NaT

        # Mapped columns you expect to save into model fields
        mapped = {
            'Outlet', 'DVR', 'Serial Number', 'Local IP', 'MAC Address', 'Version', 'Device Type',
            'Device Model', 'Build', 'Power Adapter/Cord', 'Video Input', 'Total Channel',
            'NIC Speed', 'HDD Total Space', 'Hybrid', 'WIP', 'P2P QR', 'Date Purchase'
        }

        created = updated = skipped = 0
        for idx, row in cctv_df.iterrows():
            # Outlet
            outlet_name = row.get('Outlet')
            if pd.isna(outlet_name) or str(outlet_name).strip() == '':
                self.stdout.write(self.style.WARNING(f"Row {idx} skipped: empty Outlet"))
                skipped += 1
                continue
            outlet_instance, _ = Outlet.objects.get_or_create(name=str(outlet_name).strip())

            # Serial number is our unique key
            serial = row.get('Serial Number')
            if pd.isna(serial) or str(serial).strip() == '':
                self.stdout.write(self.style.WARNING(f"Row {idx} skipped: missing serial number"))
                skipped += 1
                continue
            serial = str(serial).strip()

            # Device model -> model field
            device_model_raw = row.get('Device Model') or ''
            model_val = str(device_model_raw).strip() if pd.notna(device_model_raw) else 'Unknown'

            # Date Purchase: prefer 'Date Purchase' if present, else use Build_parsed
            date_purchase = None
            if 'Date Purchase' in cctv_df.columns:
                dp = row.get('Date Purchase')
                if pd.notna(dp):
                    try:
                        date_purchase = pd.to_datetime(dp, dayfirst=True, errors='coerce').date()
                    except Exception:
                        date_purchase = None
            if date_purchase is None and pd.notna(row.get('Build_parsed')):
                try:
                    date_purchase = row.get('Build_parsed').date()
                except Exception:
                    date_purchase = None

            # Optional fields
            local_ip = row.get('Local IP') if 'Local IP' in cctv_df.columns and pd.notna(row.get('Local IP')) else None
            wip = row.get('WIP') if 'WIP' in cctv_df.columns and pd.notna(row.get('WIP')) else None
            p2p_qr = row.get('P2P QR') if 'P2P QR' in cctv_df.columns and pd.notna(row.get('P2P QR')) else None
            dvr = row.get('DVR') if 'DVR' in cctv_df.columns and pd.notna(row.get('DVR')) else None

            item_name = f"CCTV DVR - {dvr}" if dvr else "CCTV DVR"

            # Collect extras into remark so nothing is lost
            extras = []
            for col in cctv_df.columns:
                if col not in mapped:
                    val = row.get(col)
                    if pd.notna(val):
                        extras.append(f"{col}={val}")
            extras_text = ("; ".join(extras)) if extras else ""

            defaults = {
                'outlet': outlet_instance,
                'item': item_name,
                'model': model_val,
                'serial_number': serial,
                'date_purchase': date_purchase,
                'status': str(wip).strip() if wip is not None else 'Unknown',
                'remark': (str(p2p_qr).strip() if p2p_qr is not None else '') + (("; " + extras_text) if extras_text else ''),
                'asset_type': 'cctv',
                'local_ip': local_ip,
                'version': row.get('Version') if 'Version' in cctv_df.columns and pd.notna(row.get('Version')) else None,
                'device_type': row.get('Device Type') if 'Device Type' in cctv_df.columns and pd.notna(row.get('Device Type')) else None,
                'power_adapter': row.get('Power Adapter/Cord') if 'Power Adapter/Cord' in cctv_df.columns and pd.notna(row.get('Power Adapter/Cord')) else None,
                'video_input': row.get('Video Input') if 'Video Input' in cctv_df.columns and pd.notna(row.get('Video Input')) else None,
                'total_channel': row.get('Total Channel') if 'Total Channel' in cctv_df.columns and pd.notna(row.get('Total Channel')) else None,
                'nic_speed': row.get('NIC Speed') if 'NIC Speed' in cctv_df.columns and pd.notna(row.get('NIC Speed')) else None,
                'hdd_total_space': row.get('HDD Total Space') if 'HDD Total Space' in cctv_df.columns and pd.notna(row.get('HDD Total Space')) else None,
                'hybrid': row.get('Hybrid') if 'Hybrid' in cctv_df.columns and pd.notna(row.get('Hybrid')) else None,
            }

            try:
                obj, created_flag = ITAsset.objects.update_or_create(
                    serial_number=serial,
                    defaults=defaults
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1
            except Exception as e:
                self.stderr.write(f"Failed row {idx} serial={serial}: {e}")
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"CCTV import done — created: {created}, updated: {updated}, skipped: {skipped}"
        ))
