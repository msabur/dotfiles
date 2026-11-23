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
    from pyIslam.hijri import HijriDate
except ModuleNotFoundError:
    print("⚠️run pip install islam⚠️")
    import sys
    sys.exit(1)

# Settings
lat, lon = 28.3047, -81.4167 # Kissimmee, FL
fajr_isha_method = 5
madhab = 2
hijri_offset = 0

# https://stackoverflow.com/a/3168394
is_dst = time.daylight and time.localtime().tm_isdst > 0
tz = -1 * time.timezone / 60 / 60

today = datetime.date.today()
now = datetime.datetime.now()

pconf = PrayerConf(lon, lat, tz, fajr_isha_method, madhab, enable_summer_time=is_dst)
pt = Prayer(pconf, today)

timings = {
    "Fajr": pt.fajr_time(),
    "Sunrise": pt.sherook_time(),
    "Dhuhr": pt.dohr_time(),
    "Asr": pt.asr_time(),
    "Maghrib": pt.maghreb_time(),
    "Isha": pt.ishaa_time()
}

timings_dt = { name: datetime.datetime.combine(date=today, time=time)
                   for name, time in timings.items() }

# Determine current and next timing
current_timing = None
next_timing = None
for name, dt in timings_dt.items():
    if dt > now:
        next_timing = (name, dt)
        break
    elif name == "Sunrise":
        current_timing = None
    else:
        current_timing = (name, dt)

# If all timings passed, next is tomorrow's Fajr
if next_timing is None:
    tomorrow = today + datetime.timedelta(days=1)
    pt_tomorrow = Prayer(pconf, tomorrow)
    fajr_tomorrow = pt_tomorrow.fajr_time()
    fajr_dt = datetime.datetime.combine(date=tomorrow, time=fajr_tomorrow)
    next_timing = ("Fajr", fajr_dt)

delta = next_timing[1] - now
hours, remainder = divmod(int(delta.total_seconds()), 3600)
minutes = remainder // 60
time_left = f"{hours}h {minutes}m" if hours else f"{minutes}m"

# Output to Argos

print(f"🕌 {next_timing[0]} in {time_left}")
print("---")

lineSpecs: list[tuple[str, bool]] = [] # [text, shouldHighlight]

heading = f"{HijriDate.today(hijri_offset).format(lang=2)}"

max_name_len = max([len(name) for name in timings_dt])

to_mono = lambda s: f"<span font='monospace'>{s}</span>"
to_bold = lambda s: f"<b>{s}</b>"
to_italics = lambda s: f"<i>{s}</i>"

for name, dt in timings_dt.items():
    line = f"{name:<{max_name_len+5}}: {dt.strftime('%I:%M %p')}"
    if current_timing and name == current_timing[0]:
        lineSpecs.append((line, True))
    else:
        lineSpecs.append((line, False))

max_line_length = max([len(text) for text, _ in lineSpecs])
print(to_mono(heading.center(max_line_length)))

for text, shouldHighlight in lineSpecs:
    if shouldHighlight:
        print(to_mono(to_italics(to_bold(text))))
    else:
        print(to_mono(text))
