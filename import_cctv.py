import os
import django
import csv
from datetime import datetime
from django.utils import timezone

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spa_django.settings")
django.setup()

from accounts.models import ITAsset, Outlet  # Import Outlet too

CSV_FILE_PATH = r"C:\Users\User\spa_django\cctvassetdetail_fixed.csv"

added_count = 0
skipped_count = 0

print("📂 Reading file:", CSV_FILE_PATH)

with open(CSV_FILE_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [name.strip().replace('\ufeff', '') for name in reader.fieldnames]

    print("✅ CSV Headers Detected:", reader.fieldnames)

    for row in reader:
        outlet_name = row.get("Outlet")
        device_model = row.get("Device Model")
        serial_no = row.get("Serial Number")
        location = row.get("Location")
        port = row.get("Port")
        version = row.get("Version")

        # Skip invalid rows
        if not outlet_name or not serial_no:
            print("⚠️ Skipping row (missing outlet or serial):", row)
            skipped_count += 1
            continue

        try:
            outlet_obj, _ = Outlet.objects.get_or_create(name=outlet_name)

            ITAsset.objects.create(
                outlet=outlet_obj,
                item=device_model or "CCTV Device",
                brand="Unknown",
                model=device_model or "Unknown Model",
                serial_number=serial_no,
                asset_type="cctv",
                device_model=device_model or "",
                location=location or "",
                port=port or "",
                version=version or "",
                status="Active",
                created_at=timezone.now(),
            )

            added_count += 1

        except Exception as e:
            print(f"❌ Skipped (duplicate or error): {serial_no} — {e}")
            skipped_count += 1

print(f"\n✅ Import complete! {added_count} CCTV assets added, {skipped_count} skipped ✅")
