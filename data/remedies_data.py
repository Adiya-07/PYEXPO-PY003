"""
Planetary Remedies (Pariharam) Data
Contains remedies for all 9 planets in English and Tamil
"""

REMEDIES_DATA = [
    {
        "planet": "Sun",
        "planetTa": "சூரியன்",
        "symbol": "☉",
        "day": "Sunday",
        "dayTa": "ஞாயிறு",
        "color": "Orange/Red",
        "colorTa": "ஆரஞ்சு/சிவப்பு",
        "gemstone": "Ruby (Manikkam)",
        "gemstoneTa": "மாணிக்கம்",
        "mantra": "Om Suryaya Namaha (ஓம் சூர்யாய நமஹா)",
        "remedy": "Offer water to rising Sun with red flowers. Donate wheat and jaggery. Fast on Sundays.",
        "remedyTa": "உதிக்கும் சூரியனுக்கு சிவப்பு மலர்களுடன் நீர் அர்ப்பணிக்கவும். கோதுமை மற்றும் வெல்லம் தானம் செய்யவும். ஞாயிற்றுக்கிழமைகளில் விரதம் இருக்கவும்."
    },
    {
        "planet": "Moon",
        "planetTa": "சந்திரன்",
        "symbol": "☽",
        "day": "Monday",
        "dayTa": "திங்கள்",
        "color": "White",
        "colorTa": "வெள்ளை",
        "gemstone": "Pearl (Muthu)",
        "gemstoneTa": "முத்து",
        "mantra": "Om Chandraya Namaha (ஓம் சந்த்ராய நமஹா)",
        "remedy": "Wear white clothes. Donate rice and milk. Chant Chandra mantra 108 times on Mondays.",
        "remedyTa": "வெள்ளை ஆடைகள் அணியவும். அரிசி மற்றும் பால் தானம் செய்யவும். திங்கட்கிழமைகளில் சந்திர மந்திரத்தை 108 முறை ஜெபிக்கவும்."
    },
    {
        "planet": "Mars",
        "planetTa": "செவ்வாய்",
        "symbol": "♂",
        "day": "Tuesday",
        "dayTa": "செவ்வாய்",
        "color": "Red",
        "colorTa": "சிவப்பு",
        "gemstone": "Red Coral (Pavalam)",
        "gemstoneTa": "பவளம்",
        "mantra": "Om Mangalaya Namaha (ஓம் மங்களாய நமஹா)",
        "remedy": "Recite Hanuman Chalisa. Donate red lentils and red cloth. Visit Hanuman temple.",
        "remedyTa": "ஹனுமான் சாலிஸா பாராயணம் செய்யவும். சிவப்பு பருப்பு மற்றும் சிவப்பு துணி தானம் செய்யவும். ஹனுமான் கோவிலுக்குச் செல்லவும்."
    },
    {
        "planet": "Mercury",
        "planetTa": "புதன்",
        "symbol": "☿",
        "day": "Wednesday",
        "dayTa": "புதன்",
        "color": "Green",
        "colorTa": "பச்சை",
        "gemstone": "Emerald (Maragatham)",
        "gemstoneTa": "மரகதம்",
        "mantra": "Om Budhaya Namaha (ஓம் புதாய நமஹா)",
        "remedy": "Feed green vegetables to cows. Wear green clothes. Donate books and stationery.",
        "remedyTa": "பசு மாடுகளுக்கு பச்சை காய்கறிகள் ஊட்டவும். பச்சை ஆடைகள் அணியவும். புத்தகங்கள் மற்றும் எழுதுபொருட்கள் தானம் செய்யவும்."
    },
    {
        "planet": "Jupiter",
        "planetTa": "குரு",
        "symbol": "♃",
        "day": "Thursday",
        "dayTa": "வியாழன்",
        "color": "Yellow",
        "colorTa": "மஞ்சள்",
        "gemstone": "Yellow Sapphire (Pushyaragam)",
        "gemstoneTa": "புஷ்கராஜ்",
        "mantra": "Om Gurave Namaha (ஓம் குரவே நமஹா)",
        "remedy": "Worship banana tree. Donate yellow clothes and turmeric. Serve teachers and elders.",
        "remedyTa": "வாழை மரத்தை வழிபடவும். மஞ்சள் ஆடைகள் மற்றும் மஞ்சள் தானம் செய்யவும். ஆசிரியர்கள் மற்றும் மூத்தோருக்கு சேவை செய்யவும்."
    },
    {
        "planet": "Venus",
        "planetTa": "சுக்ரன்",
        "symbol": "♀",
        "day": "Friday",
        "dayTa": "வெள்ளி",
        "color": "White/Pink",
        "colorTa": "வெள்ளை/இளஞ்சிவப்பு",
        "gemstone": "Diamond (Vairam)",
        "gemstoneTa": "வைரம்",
        "mantra": "Om Shukraya Namaha (ஓம் சுக்ராய நமஹா)",
        "remedy": "Worship Goddess Lakshmi. Donate white sweets and fragrant items. Use perfumes.",
        "remedyTa": "இலக்ஷ்மி தேவியை வழிபடவும். வெள்ளை இனிப்புகள் மற்றும் நறுமணப் பொருட்கள் தானம் செய்யவும்."
    },
    {
        "planet": "Saturn",
        "planetTa": "சனி",
        "symbol": "♄",
        "day": "Saturday",
        "dayTa": "சனி",
        "color": "Black/Blue",
        "colorTa": "கருப்பு/நீலம்",
        "gemstone": "Blue Sapphire (Neelam)",
        "gemstoneTa": "நீலம்",
        "mantra": "Om Shanaye Namaha (ஓம் சனையே நமஹா)",
        "remedy": "Donate black sesame, iron items, and blankets to poor. Light sesame oil lamps.",
        "remedyTa": "ஏழைகளுக்கு கருப்பு எள், இரும்புப் பொருட்கள் மற்றும் விரிப்புகள் தானம் செய்யவும். எள் எண்ணெய் விளக்கேற்றவும்."
    },
    {
        "planet": "Rahu",
        "planetTa": "ராகு",
        "symbol": "☊",
        "day": "Saturday",
        "dayTa": "சனி",
        "color": "Smoke Grey",
        "colorTa": "புகை சாம்பல்",
        "gemstone": "Hessonite (Gomedakam)",
        "gemstoneTa": "கோமேதகம்",
        "mantra": "Om Rahave Namaha (ஓம் ராகவே நமஹா)",
        "remedy": "Feed black dogs. Donate coconuts and blankets. Chant Durga Stotra.",
        "remedyTa": "கருப்பு நாய்களுக்கு உணவளிக்கவும். தேங்காய் மற்றும் விரிப்புகள் தானம் செய்யவும். துர்கா ஸ்தோத்திரம் ஜெபிக்கவும்."
    },
    {
        "planet": "Ketu",
        "planetTa": "கேது",
        "symbol": "☋",
        "day": "Tuesday",
        "dayTa": "செவ்வாய்",
        "color": "Brown",
        "colorTa": "பழுப்பு",
        "gemstone": "Cat's Eye (Vaiduryam)",
        "gemstoneTa": "வைடூரியம்",
        "mantra": "Om Ketave Namaha (ஓம் கேதவே நமஹா)",
        "remedy": "Worship Lord Ganesha. Donate blankets and food to saints. Feed Brahmins.",
        "remedyTa": "விநாயகரை வழிபடவும். சாது முனிவர்களுக்கு விரிப்புகள் மற்றும் உணவு தானம் செய்யவும். பிராமணர்களுக்கு உணவளிக்கவும்."
    }
]
