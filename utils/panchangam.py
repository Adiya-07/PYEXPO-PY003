"""
AstroGuy AI — Enhanced Panchangam Calculator
==============================================
Features:
  - 360-day calendar generation
  - Daily Panchangam (Tithi, Vara, Nakshatra, Yoga, Karana)
  - Soolam (inauspicious direction by weekday)
  - Ema Kandam (snake direction - risky times)
  - Rahu Kalam, Yamagandam, Gulikai
  - Abhijit Muhurta
  - Major Hindu festivals
  - Auspicious day filtering
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List


# ── Constants ──────────────────────────────────────────────────────────────
J2000 = 2451545.0
AYANAMSA_2000 = 23.8581
AYANAMSA_RATE = 0.013976

# ── Core astronomy helpers ─────────────────────────────────────────────────
def _to_rad(d): return d * math.pi / 180
def _norm360(d): return d % 360

def _julian_day(year, month, day, hour=12, minute=0):
    y, m = year, month
    if m <= 2: y -= 1; m += 12
    A = int(y / 100)
    B = 2 - A + int(A / 4)
    return int(365.25*(y+4716)) + int(30.6001*(m+1)) + day + (hour + minute/60)/24 + B - 1524.5

def _ayanamsa(year):
    return AYANAMSA_2000 + (year - 2000) * AYANAMSA_RATE

def _moon_longitude(jd):
    T = (jd - J2000) / 36525.0
    L = 218.3164477 + 481267.88123421*T - 0.0015786*T*T + T**3/538841
    M = 134.9633964 + 477198.8675055*T + 0.0087414*T*T
    D = 297.8501921 + 445267.1114034*T - 0.0018819*T*T
    Ms = 357.5291092 + 35999.0502909*T - 0.0001536*T*T
    F = 93.2720950 + 483202.0175233*T - 0.0036539*T*T
    dL = (6.289*math.sin(_to_rad(M))
        + 1.274*math.sin(_to_rad(2*D-M))
        + 0.658*math.sin(_to_rad(2*D))
        + 0.214*math.sin(_to_rad(2*M))
        - 0.186*math.sin(_to_rad(Ms))
        - 0.114*math.sin(_to_rad(2*F)))
    return _norm360(L + dL)

def _sun_longitude(jd):
    T = (jd - J2000) / 36525.0
    L0 = 280.46646 + 36000.76983*T
    M = 357.52911 + 35999.05029*T
    C = ((1.914602 - 0.004817*T)*math.sin(_to_rad(M))
        + 0.019993*math.sin(_to_rad(2*M))
        + 0.000289*math.sin(_to_rad(3*M)))
    return _norm360(L0 + C)


# ── Panchangam data ────────────────────────────────────────────────────────
TITHIS = [
    "Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya"
]
TITHI_TAMIL = [
    "பிரதமை","துவிதியை","திரிதியை","சதுர்த்தி","பஞ்சமி",
    "சஷ்டி","சப்தமி","அஷ்டமி","நவமி","தசமி",
    "ஏகாதசி","துவாதசி","த்ரயோதசி","சதுர்தசி","பௌர்ணமி/அமாவாசை"
]
TITHI_TYPE = [
    "Nanda","Bhadra","Jaya","Rikta","Purna",
    "Nanda","Bhadra","Jaya","Rikta","Purna",
    "Nanda","Bhadra","Jaya","Rikta","Purna"
]

VARAS = [
    {"en":"Sunday","ta":"ஞாயிறு","planet":"Sun","symbol":"☀️","color":"#FF6B35"},
    {"en":"Monday","ta":"திங்கள்","planet":"Moon","symbol":"🌙","color":"#C0C0C0"},
    {"en":"Tuesday","ta":"செவ்வாய்","planet":"Mars","symbol":"♂","color":"#FF4444"},
    {"en":"Wednesday","ta":"புதன்","planet":"Mercury","symbol":"☿","color":"#44BB44"},
    {"en":"Thursday","ta":"வியாழன்","planet":"Jupiter","symbol":"♃","color":"#FFD700"},
    {"en":"Friday","ta":"வெள்ளி","planet":"Venus","symbol":"♀","color":"#FF69B4"},
    {"en":"Saturday","ta":"சனி","planet":"Saturn","symbol":"♄","color":"#4444FF"},
]

NAKSHATRAS_27 = [
    ("Ashwini","அஸ்வினி"),("Bharani","பரணி"),("Krittika","கிருத்திகை"),
    ("Rohini","ரோகிணி"),("Mrigashira","மிருகசீரிஷம்"),("Ardra","திருவாதிரை"),
    ("Punarvasu","புனர்பூசம்"),("Pushya","பூசம்"),("Ashlesha","ஆயில்யம்"),
    ("Magha","மகம்"),("Purva Phalguni","பூரம்"),("Uttara Phalguni","உத்திரம்"),
    ("Hasta","ஹஸ்தம்"),("Chitra","சித்திரை"),("Swati","சுவாதி"),
    ("Vishakha","விசாகம்"),("Anuradha","அனுஷம்"),("Jyeshtha","கேட்டை"),
    ("Mula","மூலம்"),("Purva Ashadha","பூராடம்"),("Uttara Ashadha","உத்திராடம்"),
    ("Shravana","திருவோணம்"),("Dhanishta","அவிட்டம்"),("Shatabhisha","சதயம்"),
    ("Purva Bhadrapada","பூரட்டாதி"),("Uttara Bhadrapada","உத்திரட்டாதி"),
    ("Revati","ரேவதி"),
]

YOGAS = [
    ("Vishkambha","விஷ்கம்ப"),("Priti","ப்ரீதி"),("Ayushman","ஆயுஷ்மான்"),
    ("Saubhagya","சௌபாக்கிய"),("Shobhana","சோபன"),("Atiganda","அதிகண்ட"),
    ("Sukarma","சுகர்ம"),("Dhriti","திருதி"),("Shula","சூல"),
    ("Ganda","கண்ட"),("Vriddhi","விருத்தி"),("Dhruva","திருவ"),
    ("Vyaghata","வியாகாத"),("Harshana","ஹர்ஷண"),("Vajra","வஜ்ர"),
    ("Siddhi","சித்தி"),("Vyatipata","வியதீபாத"),("Variyana","வரீயான்"),
    ("Parigha","பரிக"),("Shiva","சிவ"),("Siddha","சித்த"),
    ("Sadhya","சாத்ய"),("Shubha","சுப"),("Shukla","சுக்ல"),
    ("Brahma","பிரம்ம"),("Indra","இந்திர"),("Vaidhriti","வைத்ருதி"),
]
YOGA_QUALITY = [
    "Inauspicious","Auspicious","Auspicious","Auspicious","Auspicious",
    "Inauspicious","Auspicious","Auspicious","Inauspicious","Inauspicious",
    "Auspicious","Auspicious","Inauspicious","Auspicious","Inauspicious",
    "Auspicious","Inauspicious","Auspicious","Inauspicious","Auspicious",
    "Auspicious","Auspicious","Auspicious","Auspicious","Auspicious",
    "Auspicious","Inauspicious",
]

KARANAS = [
    "Bava","Balava","Kaulava","Taitila","Garija",
    "Vanija","Vishti","Shakuni","Chatushpada","Naga","Kimstughna"
]
KARANA_TAMIL = [
    "பவ","பாலவ","கௌலவ","தைதில","கரஜ",
    "வணிஜ","விஷ்டி","சகுனி","சதுஷ்பாத","நாக","கிம்ஸ்துக்ன"
]

# ── NEW: Soolam (inauspicious direction by weekday) ────────────────────────
SOOLAM_DIRECTIONS = [
    {"day": "Sunday", "direction": "East", "direction_ta": "கிழக்கு", "avoid": "Travel or activities in this direction"},
    {"day": "Monday", "direction": "North-East", "direction_ta": "வடகிழக்கு", "avoid": "Avoid starting journeys here"},
    {"day": "Tuesday", "direction": "North", "direction_ta": "வடக்கு", "avoid": "Risky for important tasks"},
    {"day": "Wednesday", "direction": "South", "direction_ta": "தெற்கு", "avoid": "Inauspicious direction today"},
    {"day": "Thursday", "direction": "South-West", "direction_ta": "தென்மேற்கு", "avoid": "Avoid this direction"},
    {"day": "Friday", "direction": "West", "direction_ta": "மேற்கு", "avoid": "Not favorable"},
    {"day": "Saturday", "direction": "South-East", "direction_ta": "தென்கிழக்கு", "avoid": "Avoid activities here"},
]

# ── NEW: Ema Kandam (snake direction - risky times) ────────────────────────
EMA_KANDAM_TIMES = [
    {"day": "Sunday", "direction": "East", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Monday", "direction": "South", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Tuesday", "direction": "West", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Wednesday", "direction": "North", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Thursday", "direction": "South-West", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Friday", "direction": "South-East", "start": "12:00 PM", "end": "1:30 PM"},
    {"day": "Saturday", "direction": "North-West", "start": "12:00 PM", "end": "1:30 PM"},
]

# Rahu Kalam, Yamagandam, Gulikai by weekday (start part out of 8)
RAHU_KALAM_PARTS = [8, 2, 7, 5, 6, 4, 3]  # Sun=8th, Mon=2nd, etc.
YAMAGANDAM_PARTS = [5, 4, 3, 2, 1, 7, 6]
GULIKAI_PARTS = [7, 6, 5, 4, 3, 2, 1]

MOON_PHASES = [
    (0, "🌑 New Moon", "Amavasya"),
    (45, "🌒 Waxing Crescent", "Waxing"),
    (90, "🌓 First Quarter", "First Quarter"),
    (135, "🌔 Waxing Gibbous", "Waxing Gibbous"),
    (180, "🌕 Full Moon", "Purnima"),
    (225, "🌖 Waning Gibbous", "Waning Gibbous"),
    (270, "🌗 Last Quarter", "Last Quarter"),
    (315, "🌘 Waning Crescent", "Waning Crescent"),
]

# ── NEW: Major Hindu Festivals (approximate - needs dynamic calculation) ───
FESTIVALS_2026 = {
    "01-14": "Pongal / Makar Sankranti",
    "01-26": "Republic Day",
    "03-14": "Maha Shivaratri",
    "03-25": "Holi",
    "04-02": "Ugadi / Gudi Padwa",
    "04-06": "Ram Navami",
    "04-21": "Mahavir Jayanti",
    "05-23": "Buddha Purnima",
    "08-15": "Independence Day / Raksha Bandhan",
    "08-27": "Janmashtami",
    "09-17": "Ganesh Chaturthi",
    "10-02": "Gandhi Jayanti",
    "10-24": "Dussehra",
    "11-12": "Diwali",
    "11-14": "Diwali (Day 2)",
    "12-25": "Christmas",
}


def _fmt_time(h):
    """Format hour as 12-hour time"""
    hr = int(h)
    mn = int((h - hr) * 60)
    ap = "AM" if hr < 12 else "PM"
    hr12 = hr if hr <= 12 else hr - 12
    if hr12 == 0: hr12 = 12
    return f"{hr12}:{mn:02d} {ap}"


def get_panchangam(date: datetime = None, lat: float = 13.0827, lon: float = 80.2707) -> Dict:
    """Calculate full Panchangam for a given date"""
    if date is None:
        date = datetime.now()

    year, month, day = date.year, date.month, date.day
    hour = date.hour + date.minute / 60

    jd = _julian_day(year, month, day, hour)
    ayanamsa = _ayanamsa(year + (month-1)/12 + day/365)

    moon_trop = _moon_longitude(jd)
    sun_trop = _sun_longitude(jd)
    moon_sid = _norm360(moon_trop - ayanamsa)
    sun_sid = _norm360(sun_trop - ayanamsa)

    # 1. Tithi
    moon_sun_diff = _norm360(moon_trop - sun_trop)
    tithi_index = int(moon_sun_diff / 12)
    tithi_display = tithi_index % 15
    tithi_elapsed = (moon_sun_diff % 12) / 12 * 100
    paksha = "Shukla Paksha" if tithi_index < 15 else "Krishna Paksha"
    paksha_ta = "சுக்ல பக்ஷம்" if tithi_index < 15 else "கிருஷ்ண பக்ஷம்"

    # 2. Vara
    weekday = date.weekday()
    vara_idx = (weekday + 1) % 7
    vara = VARAS[vara_idx]

    # 3. Nakshatra
    nak_index = int(moon_sid / 13.3333) % 27
    nak_pada = int((moon_sid % 13.3333) / 3.3333) + 1
    nak_elapsed = ((moon_sid % 13.3333) / 13.3333) * 100

    # 4. Yoga
    yoga_long = _norm360(moon_sid + sun_sid)
    yoga_index = int(yoga_long / 13.3333) % 27

    # 5. Karana
    karana_index = int(moon_sun_diff / 6) % 11

    # Inauspicious periods
    sunrise_h, sunset_h = 6.0, 18.0
    day_dur = sunset_h - sunrise_h
    part_dur = day_dur / 8

    # Rahu Kalam
    rk_part = RAHU_KALAM_PARTS[vara_idx] - 1
    rk_start_h = sunrise_h + rk_part * part_dur
    rk_end_h = rk_start_h + part_dur

    # Yamagandam
    yg_part = YAMAGANDAM_PARTS[vara_idx] - 1
    yg_start_h = sunrise_h + yg_part * part_dur
    yg_end_h = yg_start_h + part_dur

    # Gulikai
    gu_part = GULIKAI_PARTS[vara_idx] - 1
    gu_start_h = sunrise_h + gu_part * part_dur
    gu_end_h = gu_start_h + part_dur

    # Abhijit Muhurta
    midday = (sunrise_h + sunset_h) / 2
    abh_start = midday - 0.4
    abh_end = midday + 0.4

    # Soolam & Ema Kandam
    soolam = SOOLAM_DIRECTIONS[vara_idx]
    ema_kandam = EMA_KANDAM_TIMES[vara_idx]

    # Moon phase
    phase_angle = moon_sun_diff
    phase_label, phase_name = MOON_PHASES[-1][1], MOON_PHASES[-1][2]
    for threshold, label, name in MOON_PHASES:
        if phase_angle >= threshold:
            phase_label, phase_name = label, name

    # Auspiciousness
    yoga_good = YOGA_QUALITY[yoga_index] == "Auspicious"
    is_vishti = KARANAS[karana_index] == "Vishti"
    is_amavasya = tithi_display == 14 and tithi_index >= 15
    is_purnima = tithi_display == 14 and tithi_index < 15
    is_ekadashi = tithi_display == 10
    
    overall = "Highly Auspicious ✨" if (yoga_good and not is_vishti and (is_purnima or is_ekadashi)) else \
              "Auspicious" if yoga_good and not is_vishti else \
              "Inauspicious ⚠️" if is_amavasya or is_vishti else "Moderate"

    # Festival
    date_key = date.strftime("%m-%d")
    festival = FESTIVALS_2026.get(date_key, None)

    return {
        "date": date.strftime("%A, %d %B %Y"),
        "date_ta": f"{vara['ta']}, {date.strftime('%d %B %Y')}",
        "date_obj": date,
        "festival": festival,
        
        "tithi": {
            "number": tithi_index + 1,
            "name": TITHIS[tithi_display],
            "name_ta": TITHI_TAMIL[tithi_display],
            "type": TITHI_TYPE[tithi_display],
            "paksha": paksha,
            "paksha_ta": paksha_ta,
            "elapsed": round(tithi_elapsed, 1),
            "is_special": is_ekadashi or is_purnima or is_amavasya,
        },
        "vara": vara,
        "nakshatra": {
            "name": NAKSHATRAS_27[nak_index][0],
            "name_ta": NAKSHATRAS_27[nak_index][1],
            "pada": nak_pada,
            "elapsed": round(nak_elapsed, 1),
        },
        "yoga": {
            "name": YOGAS[yoga_index][0],
            "name_ta": YOGAS[yoga_index][1],
            "quality": YOGA_QUALITY[yoga_index],
        },
        "karana": {
            "name": KARANAS[karana_index],
            "name_ta": KARANA_TAMIL[karana_index],
        },
        "rahu_kalam": {"start": _fmt_time(rk_start_h), "end": _fmt_time(rk_end_h)},
        "yamagandam": {"start": _fmt_time(yg_start_h), "end": _fmt_time(yg_end_h)},
        "gulikai": {"start": _fmt_time(gu_start_h), "end": _fmt_time(gu_end_h)},
        "abhijit": {"start": _fmt_time(abh_start), "end": _fmt_time(abh_end)},
        "soolam": soolam,
        "ema_kandam": ema_kandam,
        "moon_phase": {"label": phase_label, "name": phase_name, "angle": round(phase_angle, 1)},
        "auspicious": overall,
        "sun_long": round(sun_sid, 2),
        "moon_long": round(moon_sid, 2),
        "ayanamsa": round(ayanamsa, 4),
    }


def get_year_panchangam(year: int = None, lat: float = 13.0827, lon: float = 80.2707) -> List[Dict]:
    """Generate Panchangam for 360 days starting from today or given year"""
    start_date = datetime(year, 1, 1) if year else datetime.now()
    calendar = []
    
    for i in range(360):
        date = start_date + timedelta(days=i)
        panchang = get_panchangam(date, lat, lon)
        calendar.append(panchang)
    
    return calendar


def filter_auspicious_days(calendar: List[Dict], criteria: str = "all") -> List[Dict]:
    """Filter calendar by auspiciousness criteria"""
    if criteria == "ekadashi":
        return [d for d in calendar if d['tithi']['is_special'] and "Ekadashi" in d['tithi']['name']]
    elif criteria == "purnima":
        return [d for d in calendar if "Purnima" in d['tithi']['name']]
    elif criteria == "festivals":
        return [d for d in calendar if d['festival']]
    elif criteria == "auspicious":
        return [d for d in calendar if "Auspicious" in d['auspicious']]
    else:
        return calendar