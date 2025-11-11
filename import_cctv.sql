-- 1. Drop staging table if exists
DROP TABLE IF EXISTS public.staging_cctv;

-- 2. Create staging table matching CSV headers
CREATE TABLE public.staging_cctv (
    Outlet TEXT,
    DVR TEXT,
    "Serial Number" TEXT,
    "Local IP" TEXT,
    port TEXT,
    "MAC Address" TEXT,
    version TEXT,
    "Device Type" TEXT,
    "Device Model" TEXT,
    build TEXT,
    "Power Adapter/Cord" TEXT,
    "Video Input" TEXT,
    "Total Channel" TEXT,
    "NIC Speed" TEXT,
    "HDD Total Space" TEXT,
    "Hardware Version" TEXT,
    "Software Version" TEXT,
    "System version" TEXT,
    "Web version" TEXT,
    "ONVIFServer version" TEXT,
    "ONVIFClient version" TEXT,
    "SecurityBaseline Version" TEXT,
    "Firmware Version" TEXT,
    location TEXT,
    warranty TEXT,
    hybrid TEXT,
    wip TEXT,
    "P2P QR" TEXT
);

-- 3. Import CSV into staging table (client-side)
\copy public.staging_cctv 
FROM 'C:/Users/User/spa_django/cctvassetdetail.csv' 
DELIMITER ',' CSV HEADER;

-- 4. Insert into accounts_itasset, handle nulls, generate serial if missing, skip duplicates
INSERT INTO public.accounts_itasset (
    item, brand, model, serial_number, hostname, operating_system,
    ip_address, mac_address, cpu, memory, gpu, disk, wifi_type,
    gpon_sn, status, date_purchase, remark, outlet_id, asset_type,
    network, device_type, hdd_total_space, local_ip, nic_speed,
    power_adapter, total_channel, version, video_input, active,
    port, device_model, build, hardware_version, software_version,
    system_version, web_version, onvif_server_version, onvif_client_version,
    security_baseline_version, firmware_version, location, wip, p2p_qr,
    hybrid, asset_id, "user", allocation
)
SELECT
    COALESCE(NULLIF(s.DVR,''), 'Unknown') AS item,
    'Unknown' AS brand,
    COALESCE(NULLIF(s."Device Model",''), 'Unknown') AS model,
    COALESCE(NULLIF(s."Serial Number",''), 'CCTV-' || s.DVR || '-' || ROW_NUMBER() OVER()) AS serial_number,
    NULL AS hostname,
    NULL AS operating_system,
    s."Local IP" AS ip_address,
    s."MAC Address" AS mac_address,
    NULL AS cpu,
    NULL AS memory,
    NULL AS gpu,
    NULL AS disk,
    NULL AS wifi_type,
    NULL AS gpon_sn,
    'Active' AS status,
    NULL AS date_purchase,
    NULL AS remark,
    CASE WHEN s.Outlet ~ '^\d+$' THEN s.Outlet::int ELSE NULL END AS outlet_id,
    'CCTV' AS asset_type,
    NULL AS network,
    s."Device Type" AS device_type,
    s."HDD Total Space" AS hdd_total_space,
    s."Local IP" AS local_ip,
    s."NIC Speed" AS nic_speed,
    s."Power Adapter/Cord" AS power_adapter,
    s."Total Channel" AS total_channel,
    s.version AS version,
    s."Video Input" AS video_input,
    TRUE AS active,
    s.port AS port,
    s."Device Model" AS device_model,
    s.build AS build,
    s."Hardware Version" AS hardware_version,
    s."Software Version" AS software_version,
    s."System version" AS system_version,
    s."Web version" AS web_version,
    s."ONVIFServer version" AS onvif_server_version,
    s."ONVIFClient version" AS onvif_client_version,
    s."SecurityBaseline Version" AS security_baseline_version,
    s."Firmware Version" AS firmware_version,
    s.location AS location,
    s.wip AS wip,
    s."P2P QR" AS p2p_qr,
    CASE WHEN LOWER(s.hybrid) IN ('t','true','1') THEN TRUE ELSE FALSE END AS hybrid,
    NULL AS asset_id,
    NULL AS "user",
    NULL AS allocation
FROM public.staging_cctv s
WHERE s."Serial Number" IS NOT NULL
  AND s."Serial Number" <> ''
  AND NOT EXISTS (
      SELECT 1 FROM public.accounts_itasset a
      WHERE a.serial_number = s."Serial Number"
  );

-- 5. Verify insert
SELECT COUNT(*) AS total_assets FROM public.accounts_itasset;
