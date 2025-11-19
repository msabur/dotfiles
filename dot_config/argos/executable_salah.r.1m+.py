#!/usr/bin/env python3
"""
Fajr and Ishaa reference:
-------------------------------------
1 = University of Islamic Sciences, Karachi (UISK) | Ministry of Religious Affaires, Tunisia | France - Angle 18°
2 = Muslim World League (MWL) | Ministry of Religious Affaires and Awqaf, Algeria | Presidency of Religious Affairs, Turkey
3 = Egyptian General Authority of Survey (EGAS)
4 = Umm al-Qura University, Makkah (UMU)
5 = Islamic Society of North America (ISNA) | France - Angle 15°
6 = French Muslims (ex-UOIF)
7 = Islamic Religious Council of Signapore (MUIS) | Department of Islamic Advancements of Malaysia (JAKIM) | Ministry of Religious Affairs of Indonesia (KEMENAG)
8 = Spiritual Administration of Muslims of Russia
9 = Fixed Ishaa Time Interval, 90min

Asr madhab:
-------------------------------------
1 = Shafii, Maliki, Hambali
2 = Hanafi
"""

import datetime
import time

try:
    from pyIslam.praytimes import PrayerConf, Prayer
except ModuleNotFoundError:
    print("⚠️run pip install islam⚠️")
    import sys
    sys.exit(1)

#### Settings
lat = 28.3047    # Kissimmee, FL
lon = -81.4167  # Kissimmee, FL
fajr_isha_method = 5
madhab = 2

# https://stackoverflow.com/a/3168394
is_dst = time.daylight and time.localtime().tm_isdst > 0
tz = -1 * time.timezone / 60 / 60

today = datetime.date.today()
now = datetime.datetime.now()

pconf = PrayerConf(lon, lat, tz, fajr_isha_method, madhab, enable_summer_time=is_dst)
pt = Prayer(pconf, today)

prayers = {
    "Fajr": pt.fajr_time(),
    "Sunrise": pt.sherook_time(),
    "Dhuhr": pt.dohr_time(),
    "Asr": pt.asr_time(),
    "Maghrib": pt.maghreb_time(),
    "Isha": pt.ishaa_time()
}

# Convert prayer times to datetime objects
prayers_dt = { name: datetime.datetime.combine(date=today, time=time)
                   for name, time in prayers.items() }

# Determine next prayer
next_prayer = None
for name, dt in prayers_dt.items():
    if dt > now:
        next_prayer = (name, dt)
        break

# If all prayers passed, next is tomorrow's Fajr
if not next_prayer:
    tomorrow = today + datetime.timedelta(days=1)
    pt_tomorrow = Prayer(pconf, tomorrow)
    fajr_tomorrow = pt_tomorrow.fajr_time()
    fajr_dt = datetime.datetime.combine(date=tomorrow, time=fajr_tomorrow)
    next_prayer = ("Fajr", fajr_dt)

# Time remaining
delta = next_prayer[1] - now
hours, remainder = divmod(int(delta.total_seconds()), 3600)
minutes = remainder // 60
time_left = f"{hours}h {minutes}m" if hours else f"{minutes}m"

# === Output to Argos ===

print(f"🕌 {next_prayer[0]} in {time_left}")
print("---")

max_name_len = max([len(name) for name in prayers_dt])
width = max_name_len + 16

heading = f"📅 {now.strftime('%d %b %Y')}"
print(f"{heading.center(width)}|trim=false font=monospace")

for name, dt in prayers_dt.items():
    line = f"{name:<{max_name_len}}: {dt.strftime('%I:%M %p')}"
    print(f"{line.center(width)}|font=monospace trim=false")
