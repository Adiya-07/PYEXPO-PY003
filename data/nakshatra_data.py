"""
Nakshatra (Lunar Mansion) Data
Contains information about all 27 nakshatras
"""

# Nakshatra data: [English Name, Tamil Name, Lord, Starting Longitude]
NAKSHATRAS = [
    ["Ashwini", "அஸ்வினி", "Ketu", 0],
    ["Bharani", "பரணி", "Venus", 13.3333],
    ["Krittika", "கிருத்திகை", "Sun", 26.6667],
    ["Rohini", "ரோகிணி", "Moon", 40.0],
    ["Mrigashira", "மிருகசீரிஷம்", "Mars", 53.3333],
    ["Ardra", "திருவாதிரை", "Rahu", 66.6667],
    ["Punarvasu", "புனர்பூசம்", "Jupiter", 80.0],
    ["Pushya", "பூசம்", "Saturn", 93.3333],
    ["Ashlesha", "ஆயில்யம்", "Mercury", 106.6667],
    ["Magha", "மகம்", "Ketu", 120.0],
    ["Purva Phalguni", "பூரம்", "Venus", 133.3333],
    ["Uttara Phalguni", "உத்திரம்", "Sun", 146.6667],
    ["Hasta", "ஹஸ்தம்", "Moon", 160.0],
    ["Chitra", "சித்திரை", "Mars", 173.3333],
    ["Swati", "சுவாதி", "Rahu", 186.6667],
    ["Vishakha", "விசாகம்", "Jupiter", 200.0],
    ["Anuradha", "அனுஷம்", "Saturn", 213.3333],
    ["Jyeshtha", "கேட்டை", "Mercury", 226.6667],
    ["Mula", "மூலம்", "Ketu", 240.0],
    ["Purva Ashadha", "பூராடம்", "Venus", 253.3333],
    ["Uttara Ashadha", "உத்திராடம்", "Sun", 266.6667],
    ["Shravana", "திருவோணம்", "Moon", 280.0],
    ["Dhanishta", "அவிட்டம்", "Mars", 293.3333],
    ["Shatabhisha", "சதயம்", "Rahu", 306.6667],
    ["Purva Bhadrapada", "பூரட்டாதி", "Jupiter", 320.0],
    ["Uttara Bhadrapada", "உத்திரட்டாதி", "Saturn", 333.3333],
    ["Revati", "ரேவதி", "Mercury", 346.6667]
]

# Gana (temperament) groups for each nakshatra
GANA_GROUPS = {
    "Deva": [0, 3, 6, 10, 12, 15, 18, 21, 24],
    "Manushya": [1, 4, 7, 11, 13, 16, 19, 22, 25],
    "Rakshasa": [2, 5, 8, 9, 14, 17, 20, 23, 26]
}

# Nadi (dosha) groups for each nakshatra
NADI_GROUPS = {
    "Vata": [0, 6, 12, 18, 24],
    "Pitta": [1, 7, 13, 19, 25],
    "Kapha": [2, 8, 14, 20, 26]
}

# Rasi lords
RASI_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

# Planet friendships
PLANET_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Venus", "Mercury"]
}

# Yoni mapping for compatibility
YONI_MAP = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]

# Friendly Yoni pairs
FRIENDLY_YONI_PAIRS = [
    [0, 3], [3, 0], [1, 4], [4, 1], [2, 5], [5, 2],
    [6, 9], [9, 6], [7, 10], [10, 7], [8, 11], [11, 8]
]

# Enemy Yoni pairs
ENEMY_YONI_PAIRS = [
    [0, 4], [4, 0], [1, 5], [5, 1], [2, 6], [6, 2]
]
