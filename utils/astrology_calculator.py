"""
Vedic Astrology Calculator
Ported from JavaScript to Python
Performs authentic Vedic astronomical calculations
"""

import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.nakshatra_data import (
    NAKSHATRAS, GANA_GROUPS, NADI_GROUPS, 
    RASI_LORDS, PLANET_FRIENDS, YONI_MAP,
    FRIENDLY_YONI_PAIRS, ENEMY_YONI_PAIRS
)
from data.horoscope_data import RASI_NAMES, RASI_SYMBOLS


class VedicAstroCalculator:
    """Main class for Vedic astrology calculations"""
    
    def __init__(self):
        self.julian_day_2000 = 2451545.0
        self.ayanamsa_2000 = 23.85
        self.ayanamsa_rate = 0.01397
        
    def to_radians(self, degrees: float) -> float:
        """Convert degrees to radians"""
        return degrees * math.pi / 180
    
    def to_degrees(self, radians: float) -> float:
        """Convert radians to degrees"""
        return radians * 180 / math.pi
    
    def calculate_ayanamsa(self, year: float) -> float:
        """Calculate Lahiri Ayanamsa for a given year"""
        years_since_2000 = year - 2000
        return self.ayanamsa_2000 + (years_since_2000 * self.ayanamsa_rate)
    
    def date_to_julian_day(self, year: int, month: int, day: int, 
                           hour: int = 0, minute: int = 0, 
                           second: int = 0, timezone_offset: float = 5.5) -> float:
        """Convert date/time to Julian Day"""
        utc_hour = hour - timezone_offset
        
        y, m = year, month
        if m <= 2:
            y -= 1
            m += 12
        
        A = math.floor(y / 100)
        B = 2 - A + math.floor(A / 4)
        day_fraction = (utc_hour + minute/60 + second/3600) / 24
        
        JD = (math.floor(365.25 * (y + 4716)) + 
              math.floor(30.6001 * (m + 1)) + 
              day + day_fraction + B - 1524.5)
        return JD
    
    def calculate_moon_longitude(self, jd: float) -> float:
        """Calculate Moon's tropical longitude using simplified VSOP87"""
        T = (jd - self.julian_day_2000) / 36525.0
        
        # Mean longitude of Moon
        L = (218.3164477 + 481267.88123421 * T - 
             0.0015786 * T * T + T**3 / 538841 - T**4 / 65194000)
        
        # Mean anomaly of Moon
        M = (134.9633964 + 477198.8675055 * T + 
             0.0087414 * T * T + T**3 / 69699 - T**4 / 14712000)
        
        # Mean elongation of Moon
        D = (297.8501921 + 445267.1114034 * T - 
             0.0018819 * T * T + T**3 / 545868 - T**4 / 113065000)
        
        # Mean anomaly of Sun
        Ms = (357.5291092 + 35999.0502909 * T - 
              0.0001536 * T * T + T**3 / 24490000)
        
        # Argument of latitude
        F = (93.2720950 + 483202.0175233 * T - 
             0.0036539 * T * T - T**3 / 3526000 + T**4 / 863310000)
        
        # Longitude corrections
        dL = 0
        dL += 6.289 * math.sin(self.to_radians(M))
        dL += 1.274 * math.sin(self.to_radians(2*D - M))
        dL += 0.658 * math.sin(self.to_radians(2*D))
        dL += 0.214 * math.sin(self.to_radians(2*M))
        dL -= 0.186 * math.sin(self.to_radians(Ms))
        dL -= 0.114 * math.sin(self.to_radians(2*F))
        
        longitude = (L + dL) % 360
        if longitude < 0:
            longitude += 360
        return longitude
    
    def calculate_sun_longitude(self, jd: float) -> float:
        """Calculate Sun's tropical longitude"""
        T = (jd - self.julian_day_2000) / 36525.0
        
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T
        
        C = ((1.914602 - 0.004817 * T - 0.000014 * T * T) * 
             math.sin(self.to_radians(M)))
        C += ((0.019993 - 0.000101 * T) * 
              math.sin(self.to_radians(2 * M)))
        C += 0.000289 * math.sin(self.to_radians(3 * M))
        
        longitude = (L0 + C) % 360
        if longitude < 0:
            longitude += 360
        return longitude
    
    def get_rasi_from_longitude(self, longitude: float, ayanamsa: float) -> Tuple[int, float]:
        """Get Rasi (zodiac sign) from longitude"""
        sidereal_long = (longitude - ayanamsa + 360) % 360
        rasi = math.floor(sidereal_long / 30)
        degrees_in_rasi = sidereal_long % 30
        return (rasi, degrees_in_rasi)
    
    def get_nakshatra_from_longitude(self, longitude: float, ayanamsa: float) -> Tuple[int, int, float]:
        """Get Nakshatra from longitude - returns (nakshatra_index, pada, remainder)"""
        sidereal_long = (longitude - ayanamsa + 360) % 360
        nakshatra = math.floor(sidereal_long / 13.333333)
        remainder = sidereal_long % 13.333333
        pada = math.floor(remainder / 3.333333) + 1
        return (nakshatra, pada, remainder)
    
    def get_nakshatra_gana(self, nakshatra_index: int) -> str:
        """Get Gana (temperament) for a nakshatra"""
        for gana, nakshatras in GANA_GROUPS.items():
            if nakshatra_index in nakshatras:
                return gana
        return "Manushya"
    
    def get_nakshatra_nadi(self, nakshatra_index: int) -> str:
        """Get Nadi (dosha type) for a nakshatra"""
        for nadi, nakshatras in NADI_GROUPS.items():
            if nakshatra_index in nakshatras:
                return nadi
        return "Vata"
    
    def calculate_birth_chart(self, year: int, month: int, day: int, 
                              hour: int, minute: int, 
                              birthplace: str = "Chennai") -> Dict:
        """Calculate complete birth chart"""
        jd = self.date_to_julian_day(year, month, day, hour, minute)
        ayanamsa = self.calculate_ayanamsa(year + (month-1)/12 + day/365)
        
        # Calculate Moon position (most important for Rasi)
        moon_tropical = self.calculate_moon_longitude(jd)
        moon_sidereal = (moon_tropical - ayanamsa + 360) % 360
        
        # Get Rasi from Moon position
        rasi_num, rasi_deg = self.get_rasi_from_longitude(moon_tropical, ayanamsa)
        rasi_name = RASI_NAMES[rasi_num]
        
        # Get Nakshatra
        nak_num, nak_pada, nak_deg = self.get_nakshatra_from_longitude(moon_tropical, ayanamsa)
        nakshatra = NAKSHATRAS[nak_num]
        
        # Calculate Sun position
        sun_tropical = self.calculate_sun_longitude(jd)
        sun_sidereal = (sun_tropical - ayanamsa + 360) % 360
        sun_rasi, _ = self.get_rasi_from_longitude(sun_tropical, ayanamsa)
        
        # Determine Lagna (Ascendant) - simplified calculation
        lagna_approx = (sun_sidereal + (hour - 6) * 15) % 360
        lagna_rasi, _ = self.get_rasi_from_longitude(lagna_approx + ayanamsa, ayanamsa)
        
        return {
            "moon_longitude": round(moon_sidereal, 4),
            "sun_longitude": round(sun_sidereal, 4),
            "rasi": {
                "number": rasi_num,
                "tamil_name": rasi_name[1],
                "english_name": rasi_name[0],
                "western_name": rasi_name[2],
                "degrees": round(rasi_deg, 2)
            },
            "nakshatra": {
                "name": nakshatra[0],
                "tamil_name": nakshatra[1],
                "lord": nakshatra[2],
                "pada": nak_pada,
                "degrees": round(nak_deg, 2),
                "gana": self.get_nakshatra_gana(nak_num),
                "nadi": self.get_nakshatra_nadi(nak_num)
            },
            "lagna": {
                "number": lagna_rasi,
                "name": RASI_NAMES[lagna_rasi][1]
            },
            "ayanamsa": round(ayanamsa, 4),
            "julian_day": jd
        }


class CompatibilityCalculator:
    """Dashakoota (10 Porutham) Compatibility Matching Calculator"""
    
    def __init__(self):
        self.astro_calc = VedicAstroCalculator()
    
    # ==================== 10 PORUTHAM CALCULATIONS ====================
    
    def calculate_dina_porutham(self, nak1: int, nak2: int) -> List:
        """Dina Porutham (Tara) - 3 points - Health and longevity"""
        diff = ((nak2 - nak1) % 27 + 27) % 27
        good_dinas = [2, 4, 6, 8, 9, 11, 13, 15, 18, 20, 24, 26]
        secondary_dinas = [1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 22, 23, 25]
        
        if diff in good_dinas:
            return [3, "Excellent - Good health and longevity"]
        elif diff in secondary_dinas:
            return [1.5, "Average - Acceptable"]
        return [0, "Poor - Health concerns possible"]
    
    def calculate_gana_porutham(self, nak1: int, nak2: int) -> List:
        """Gana Porutham - 4 points - Temperament compatibility"""
        gana1 = self.astro_calc.get_nakshatra_gana(nak1)
        gana2 = self.astro_calc.get_nakshatra_gana(nak2)
        
        if gana1 == gana2:
            return [4, f"Excellent - Same Gana ({gana1})"]
        if (gana1 == "Deva" and gana2 == "Manushya") or (gana1 == "Manushya" and gana2 == "Deva"):
            return [3, "Good - Deva-Manushya combination"]
        if (gana1 == "Manushya" and gana2 == "Rakshasa") or (gana1 == "Rakshasa" and gana2 == "Manushya"):
            return [1, "Average - Manushya-Rakshasa"]
        return [0, "Poor - Deva-Rakshasa (remedies needed)"]
    
    def calculate_yoni_porutham(self, nak1: int, nak2: int) -> List:
        """Yoni Porutham - 4 points - Physical compatibility"""
        yoni1 = YONI_MAP[nak1]
        yoni2 = YONI_MAP[nak2]
        
        if yoni1 == yoni2:
            return [4, "Excellent - Same Yoni"]
        if [yoni1, yoni2] in FRIENDLY_YONI_PAIRS:
            return [3, "Very Good - Friendly Yoni"]
        if [yoni1, yoni2] in ENEMY_YONI_PAIRS:
            return [0, "Poor - Enemy Yoni (challenging)"]
        return [2, "Good - Neutral Yoni"]
    
    def calculate_rasi_porutham(self, rasi1: int, rasi2: int) -> List:
        """Rasi Porutham - 7 points - Family growth and prosperity"""
        diff = ((rasi2 - rasi1) % 12 + 12) % 12
        
        # Good positions: 1, 3, 4, 7, 10, 11
        good_positions = [1, 3, 4, 7, 10, 11]
        # Bad positions: 2, 5, 6, 8, 9, 12
        bad_positions = [2, 5, 6, 8, 9, 12]
        
        if diff == 0:
            # Same Rasi - check exceptions
            if rasi1 in [4, 5, 10, 11]:  # Cancer, Leo, Capricorn, Aquarius
                return [0, "Poor - Same Rasi not favorable"]
            return [7, "Excellent - Same Rasi compatible"]
        
        if diff in good_positions:
            return [7, f"Excellent - {diff}th position from girl"]
        if diff in bad_positions:
            return [0, f"Poor - {diff}th position (challenging)"]
        return [3, "Average - Neutral position"]
    
    def calculate_rasyadhipati_porutham(self, rasi1: int, rasi2: int) -> List:
        """Rasyadhipati Porutham (Graha Maitri) - 5 points - Mental rapport"""
        lord1 = RASI_LORDS[rasi1]
        lord2 = RASI_LORDS[rasi2]
        
        if lord1 == lord2:
            return [5, f"Excellent - Same Lord ({lord1})"]
        if lord2 in PLANET_FRIENDS.get(lord1, []):
            return [5, f"Excellent - Friendly Lords ({lord1} & {lord2})"]
        if lord1 in PLANET_FRIENDS.get(lord2, []):
            return [4, f"Very Good - Friendly Lords"]
        return [0, "Neutral - Lords are neutral/enemies"]
    
    def calculate_rajju_porutham(self, nak1: int, nak2: int) -> List:
        """Rajju Porutham - 5 points - Longevity and stability (MOST IMPORTANT)"""
        # Rajju groups
        head = [4, 11, 18, 25]      # Mrigashira, Chitra, Dhanishta
        neck = [3, 9, 12, 19, 22, 26]  # Rohini, Hasta, Swati, Sravana, Satabhisha
        middle = [2, 6, 8, 14, 20, 23]  # Krittika, Punarvasu, Uttara, Vishakha, Purvashada, Uttarabhadra
        thigh = [1, 7, 10, 16, 21, 24]  # Bharani, Pushya, Purvaphalguni, Anuradha, Uttarashada, Purvabhadra
        foot = [0, 5, 13, 17, 15]   # Ashwini, Ardra, Magha, Jyeshtha, Moola, Revati
        
        def get_rajju(nak):
            if nak in head:
                return ("head", "Head")
            elif nak in neck:
                return ("neck", "Neck")
            elif nak in middle:
                return ("middle", "Middle")
            elif nak in thigh:
                return ("thigh", "Thigh")
            elif nak in foot:
                return ("foot", "Foot")
            return ("none", "None")
        
        rajju1, rajju_name1 = get_rajju(nak1)
        rajju2, rajju_name2 = get_rajju(nak2)
        
        if rajju1 == "none" or rajju2 == "none":
            return [5, "Excellent - No Rajju Dosha"]
        
        if rajju1 != rajju2:
            return [5, f"Excellent - Different Rajju ({rajju_name1} & {rajju_name2})"]
        
        # Same Rajju - Dosha!
        dosha_effect = {
            "head": "Husband's longevity at risk",
            "neck": "Wife's longevity at risk", 
            "middle": "Loss of children possible",
            "thigh": "Extreme poverty",
            "foot": "Pitiable wanderings"
        }
        
        return [0, f"CRITICAL DOSHA - Same Rajju ({rajju_name1}): {dosha_effect.get(rajju1, '')}"]
    
    def calculate_vedha_porutham(self, nak1: int, nak2: int) -> List:
        """Vedha Porutham - 2 points - Obstacles and afflictions"""
        # Vedha pairs (mutually opposing stars)
        vedha_pairs = [
            [5, 20],    # Ardra - Purvashada
            [6, 19],    # Punarvasu - Uttarashada
            [10, 24],   # Purvaphalguni - Uttarabhadra
            [11, 23],   # Uttara - Purvabhadra
            [4, 11, 18] # Mrigashira, Chitra, Dhanishta (mutually opposing)
        ]
        
        # Check if stars are in vedha
        for pair in vedha_pairs:
            if nak1 in pair and nak2 in pair and nak1 != nak2:
                return [0, "Poor - Vedha Dosha (mutual affliction)"]
        
        return [2, "Excellent - No Vedha Dosha"]
    
    def calculate_vashya_porutham(self, rasi1: int, rasi2: int) -> List:
        """Vashya Porutham - 2 points - Mutual attraction and cooperation"""
        # Vashya groups
        manava = [0, 3, 6, 9]       # Aries, Cancer, Libra, Capricorn
        vanachara = [4]              # Leo
        chatushpada = [1, 8, 11]    # Taurus, Sagittarius, Pisces
        jalachara = [10]             # Aquarius
        keeta = [2, 5, 7]           # Gemini, Virgo, Scorpio
        
        def get_vashya(rasi):
            if rasi in manava:
                return "Manava"
            elif rasi in vanachara:
                return "Vanachara"
            elif rasi in chatushpada:
                return "Chatushpada"
            elif rasi in jalachara:
                return "Jalachara"
            elif rasi in keeta:
                return "Keeta"
            return "Unknown"
        
        vashya1 = get_vashya(rasi1)
        vashya2 = get_vashya(rasi2)
        
        if vashya1 == vashya2:
            return [2, f"Excellent - Same Vashya ({vashya1})"]
        
        # Compatible combinations
        compatible = [
            ("Manava", "Vanachara"), ("Manava", "Chatushpada"),
            ("Vanachara", "Manava"), ("Chatushpada", "Manava"),
            ("Jalachara", "Keeta"), ("Keeta", "Jalachara")
        ]
        
        if (vashya1, vashya2) in compatible:
            return [1.5, f"Good - Compatible Vashya ({vashya1} & {vashya2})"]
        
        return [1, f"Average - Different Vashya ({vashya1} & {vashya2})"]
    
    def calculate_mahendra_porutham(self, nak1: int, nak2: int) -> List:
        """Mahendra Porutham - 2 points - Progeny and prosperity"""
        diff = ((nak2 - nak1) % 27 + 27) % 27
        good_positions = [4, 7, 10, 13, 16, 19, 22, 25]
        
        if diff in good_positions:
            return [2, f"Excellent - {diff}th position (progeny blessed)"]
        return [0, "Poor - No Mahendra blessing"]
    
    def calculate_stree_deergha_porutham(self, nak1: int, nak2: int) -> List:
        """Stree Deergha Porutham - 2 points - Wife's wellbeing and longevity"""
        diff = ((nak2 - nak1) % 27 + 27) % 27
        
        # If boy's star is beyond 13th from girl's (or 7th in some traditions)
        if diff > 13:
            return [2, f"Excellent - {diff}th position (wife protected)"]
        elif diff >= 7:
            return [1, f"Average - {diff}th position"]
        return [0, f"Poor - {diff}th position (too close)"]
    
    def calculate_full_compatibility(self, boy_chart: Dict, girl_chart: Dict) -> Dict:
        """Calculate full Dashakoota (10 Porutham) compatibility"""
        boy_rasi = boy_chart["rasi"]["number"]
        girl_rasi = girl_chart["rasi"]["number"]
        
        # Get nakshatra indices
        nak_names = [n[0] for n in NAKSHATRAS]
        boy_nak = nak_names.index(boy_chart["nakshatra"]["name"])
        girl_nak = nak_names.index(girl_chart["nakshatra"]["name"])
        
        # Calculate all 10 poruthams
        results = {
            "dina": self.calculate_dina_porutham(girl_nak, boy_nak),
            "gana": self.calculate_gana_porutham(girl_nak, boy_nak),
            "yoni": self.calculate_yoni_porutham(girl_nak, boy_nak),
            "rasi": self.calculate_rasi_porutham(girl_rasi, boy_rasi),
            "rasyadhipati": self.calculate_rasyadhipati_porutham(girl_rasi, boy_rasi),
            "rajju": self.calculate_rajju_porutham(girl_nak, boy_nak),
            "vedha": self.calculate_vedha_porutham(girl_nak, boy_nak),
            "vashya": self.calculate_vashya_porutham(girl_rasi, boy_rasi),
            "mahendra": self.calculate_mahendra_porutham(girl_nak, boy_nak),
            "streedeergha": self.calculate_stree_deergha_porutham(girl_nak, boy_nak)
        }
        
        total_score = sum(r[0] for r in results.values())
        max_score = 36
        percentage = round((total_score / max_score) * 100, 1)
        
        # Determine verdict
        if total_score >= 28:
            verdict = "Excellent Match" if percentage >= 75 else "Very Good Match"
            description = "Highly blessed union. Marriage will be harmonious and prosperous."
        elif total_score >= 21:
            verdict = "Good Match"
            description = "Compatibility is good. Minor remedies may enhance the relationship."
        elif total_score >= 16:
            verdict = "Average Match"
            description = "Acceptable compatibility. Some challenges exist but can be managed."
        else:
            verdict = "Challenging Match"
            description = "Significant challenges exist. Proper remedies and counseling recommended."
        
        # Check for critical doshas
        doshas = []
        
        if results["rajju"][0] == 0:
            doshas.append({
                "name": "Rajju Dosha",
                "remedy": "Perform Rajju Shanti Puja. Donate to Brahmins. Chant Maha Mrityunjaya Mantra."
            })
        
        if results["vedha"][0] == 0:
            doshas.append({
                "name": "Vedha Dosha",
                "remedy": "Perform Vedha Nivarana Puja. Worship Lord Vishnu."
            })
        
        if results["gana"][0] == 0:
            doshas.append({
                "name": "Gana Dosha",
                "remedy": "Perform Gana Dosha Nivarana. Chant Mahamrityunjaya Mantra 108 times daily."
            })
        
        return {
            **results,
            "total": total_score,
            "max": max_score,
            "percentage": percentage,
            "verdict": verdict,
            "description": description,
            "doshas": doshas
        }


# Helper functions
def get_rasi_symbol(rasi_number: int) -> str:
    """Get the symbol for a Rasi"""
    return RASI_SYMBOLS[rasi_number % 12]


def get_planet_positions() -> List[Dict]:
    """Get sample planet positions for birth chart display"""
    return [
        {"symbol": "☉", "name": "Sun", "x": 320, "y": 100},
        {"symbol": "☽", "name": "Moon", "x": 480, "y": 120},
        {"symbol": "♂", "name": "Mars", "x": 500, "y": 280},
        {"symbol": "☿", "name": "Mercury", "x": 480, "y": 480},
        {"symbol": "♃", "name": "Jupiter", "x": 300, "y": 480},
        {"symbol": "♀", "name": "Venus", "x": 100, "y": 480},
        {"symbol": "♄", "name": "Saturn", "x": 100, "y": 280},
        {"symbol": "☊", "name": "Rahu", "x": 120, "y": 120}
    ]
