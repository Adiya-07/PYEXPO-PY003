"""
Horoscope data for all 12 Rasis (Zodiac Signs)
Contains predictions in English and Tamil
"""

HOROSCOPE_DATA = {
    "Mesham": {
        "ruler": "Mars",
        "element": "Fire",
        "exalted": "Sun",
        "debilitated": "Saturn",
        "en": {
            "general": "With Mars as your ruler, you possess natural leadership qualities and boundless energy. Today, focus your dynamic nature on constructive pursuits. Avoid impulsive decisions.",
            "career": "Leadership opportunities emerge. Your assertiveness will be recognized by superiors. Good day for initiating new projects.",
            "love": "Passion runs high. Express your feelings directly but with sensitivity. Singles may encounter someone exciting.",
            "health": "High energy levels. Channel into physical exercise. Avoid accidents and inflammations.",
            "finance": "Favorable for bold investments. Real estate and metals show promise. Avoid lending money.",
            "lucky": {"color": "Red", "number": 9, "day": "Tuesday"}
        },
        "ta": {
            "general": "செவ்வாய் உங்கள் அதிபதி என்பதால், இயற்கையான தலைமைப் பண்புகள் மற்றும் எல்லையற்ற சக்தி உங்களிடம் உள்ளது. இன்று, உங்கள் சக்திவாய்ந்த இயல்பை உருவாக்கும் முயற்சிகளில் கவனம் செலுத்துங்கள்.",
            "career": "தலைமை வாய்ப்புகள் எழுகின்றன. உங்கள் உறுதிப்பாடு மேலதிகாரிகளால் அங்கீகரிக்கப்படும். புதிய திட்டங்களைத் தொடங்க நல்ல நாள்.",
            "love": "உணர்ச்சி அதிகமாக உள்ளது. உங்கள் உணர்வுகளை நேரடியாகவும் உணர்ச்சிப்பூர்வமாகவும் வெளிப்படுத்துங்கள்.",
            "health": "உயர்ந்த சக்தி நிலைகள். உடற்பயிற்சியில் கவனம் செலுத்துங்கள். விபத்துகள் மற்றும் அழற்சிகளைத் தவிர்க்கவும்.",
            "finance": "துணிச்சலான முதலீடுகளுக்கு சாதகமானது. நிலம் மற்றும் உலோகங்கள் வாய்ப்பைக் காட்டுகின்றன.",
            "lucky": {"color": "சிவப்பு", "number": 9, "day": "செவ்வாய்"}
        }
    },
    "Rishabam": {
        "ruler": "Venus",
        "element": "Earth",
        "exalted": "Moon",
        "debilitated": "None",
        "en": {
            "general": "Venus blesses you with stability and appreciation for beauty. Today favors artistic pursuits and financial planning.",
            "career": "Steady progress through patience. Creative solutions to workplace challenges. Good for negotiations.",
            "love": "Romance deepens through shared experiences. Existing relationships strengthen. Good day for commitments.",
            "health": "Focus on throat and neck area. Gentle exercise recommended. Avoid overindulgence in food.",
            "finance": "Excellent for long-term investments. Savings grow steadily. Avoid speculative trading.",
            "lucky": {"color": "Green", "number": 6, "day": "Friday"}
        },
        "ta": {
            "general": "சுக்ரன் உங்களுக்கு நிலைத்தன்மை மற்றும் அழகியல் பாராட்டும் தன்மையை அருள்கிறார். இன்று கலை முயற்சிகள் மற்றும் நிதி திட்டமிடலுக்கு சாதகமானது.",
            "career": "பொறுமையின் மூலம் நிலையான முன்னேற்றம். படைப்பாற்றல் தீர்வுகள். பேச்சுவார்த்தைகளுக்கு நல்லது.",
            "love": "பகிர்வு அனுபவங்கள் மூலம் காதல் ஆழமடைகிறது. தற்போதைய உறவுகள் வலுப்படுகின்றன.",
            "health": "தொண்டை மற்றும் கழுத்து பகுதியில் கவனம் செலுத்துங்கள். மென்மையான உடற்பயிற்சி பரிந்துரைக்கப்படுகிறது.",
            "finance": "நீண்டகால முதலீடுகளுக்கு சிறந்தது. சேமிப்பு வளர்ச்சி. ஊக வணிகத்தைத் தவிர்க்கவும்.",
            "lucky": {"color": "பச்சை", "number": 6, "day": "வெள்ளி"}
        }
    },
    "Midhunam": {
        "ruler": "Mercury",
        "element": "Air",
        "exalted": "None",
        "debilitated": "Jupiter",
        "en": {
            "general": "Mercury grants you quick wit and excellent communication. Today favors learning, writing, and social connections.",
            "career": "Networking brings opportunities. Your ideas gain traction. Good for presentations and negotiations.",
            "love": "Intellectual connection matters most. Engaging conversations spark romance. Be honest in communication.",
            "health": "Nervous system needs care. Meditation helps. Avoid mental stress and overthinking.",
            "finance": "Multiple income sources possible. Good for trading and short-term investments. Research thoroughly.",
            "lucky": {"color": "Yellow", "number": 5, "day": "Wednesday"}
        },
        "ta": {
            "general": "புதன் உங்களுக்கு விரைவான அறிவு மற்றும் சிறந்த தகவல்தொடர்பு திறனை அளிக்கிறார். இன்று கற்றல், எழுதுதல் மற்றும் சமூக தொடர்புகளுக்கு சாதகமானது.",
            "career": "பிணைப்பு வாய்ப்புகளைத் தருகிறது. உங்கள் யோசனைகள் கவனம் பெறுகின்றன. விளக்கவுரைகளுக்கு நல்லது.",
            "love": "அறிவுசார் இணைப்பு மிகவும் முக்கியம். ஈடுபாடுள்ள உரையாடல்கள் காதலைத் தூண்டுகின்றன.",
            "health": "நரம்பு மண்டலம் பராமரிப்பு தேவை. தியானம் உதவுகிறது. மன அழுத்தம் மற்றும் அதிக சிந்தனையைத் தவிர்க்கவும்.",
            "finance": "பல வருமான ஆதாரங்கள் சாத்தியம். வணிகம் மற்றும் குறுகியகால முதலீடுகளுக்கு நல்லது.",
            "lucky": {"color": "மஞ்சள்", "number": 5, "day": "புதன்"}
        }
    },
    "Katakam": {
        "ruler": "Moon",
        "element": "Water",
        "exalted": "Jupiter",
        "debilitated": "Mars",
        "en": {
            "general": "The Moon governs your emotions and intuition. Today your sensitivity is heightened. Trust your instincts.",
            "career": "Emotional intelligence serves you well. Good for caregiving professions. Avoid confrontations.",
            "love": "Deep emotional bonds form. Nurturing behavior attracts love. Family matters need attention.",
            "health": "Digestive system sensitive. Eat light, nourishing foods. Stay hydrated. Emotional health important.",
            "finance": "Conservative approach favored. Property investments show promise. Avoid risky ventures.",
            "lucky": {"color": "White", "number": 2, "day": "Monday"}
        },
        "ta": {
            "general": "சந்திரன் உங்கள் உணர்வுகள் மற்றும் உள்ளுணர்வை ஆளுகிறார். இன்று உங்கள் உணர்திறன் அதிகரிக்கப்பட்டுள்ளது.",
            "career": "உணர்ச்சி நுண்ணறிவு உங்களுக்கு நன்மை பயக்கும். பராமரிப்பு தொழில்களுக்கு நல்லது.",
            "love": "ஆழமான உணர்ச்சி பிணைப்புகள் உருவாகின்றன. பராமரிப்பு நடத்தை காதலை ஈர்க்கிறது.",
            "health": "செரிமான மண்டலம் உணர்திறன். இலேசான, ஊட்டச்சத்து உணவுகளை சாப்பிடுங்கள். நீரேற்றம் முக்கியம்.",
            "finance": "பாதுகாப்பு அணுகுமுறை ஆதரிக்கப்படுகிறது. சொத்து முதலீடுகள் வாய்ப்பைக் காட்டுகின்றன.",
            "lucky": {"color": "வெள்ளை", "number": 2, "day": "திங்கள்"}
        }
    },
    "Simmam": {
        "ruler": "Sun",
        "element": "Fire",
        "exalted": "None",
        "debilitated": "Saturn",
        "en": {
            "general": "The Sun illuminates your path with confidence and vitality. Your natural charisma shines today.",
            "career": "Recognition and authority come your way. Leadership roles favored. Creative projects succeed.",
            "love": "Romance flourishes with grand gestures. Your warmth attracts admirers. Express love generously.",
            "health": "Heart and spine need attention. Cardiovascular exercise beneficial. Maintain good posture.",
            "finance": "Speculative investments may pay off. Gold and government bonds favorable. Avoid borrowing.",
            "lucky": {"color": "Gold", "number": 1, "day": "Sunday"}
        },
        "ta": {
            "general": "சூரியன் நம்பிக்கை மற்றும் உயிர்ப்புடன் உங்கள் பாதையை விளக்குகிறார். உங்கள் இயற்கையான கவர்ச்சி இன்று பிரகாசிக்கிறது.",
            "career": "அங்கீகாரம் மற்றும் அதிகாரம் உங்களை நோக்கி வருகிறது. தலைமை பாத்திரங்கள் ஆதரிக்கப்படுகின்றன.",
            "love": "பிரம்மாண்டமான சைகைகளுடன் காதல் செழிக்கிறது. உங்கள் வெப்பம் ரசிகர்களை ஈர்க்கிறது.",
            "health": "இதயம் மற்றும் முதுகெலும்பு கவனம் தேவை. கார்டியோவாஸ்குலர் உடற்பயிற்சி பயனளிக்கும்.",
            "finance": "ஊக முதலீடுகள் பலனளிக்கலாம். தங்கம் மற்றும் அரசு பத்திரங்கள் சாதகமானவை.",
            "lucky": {"color": "தங்கம்", "number": 1, "day": "ஞாயிறு"}
        }
    },
    "Kanni": {
        "ruler": "Mercury",
        "element": "Earth",
        "exalted": "Mercury",
        "debilitated": "Venus",
        "en": {
            "general": "Mercury blesses you with analytical precision and attention to detail. Perfect day for organization.",
            "career": "Your meticulous work gets noticed. Problem-solving skills shine. Good for health-related professions.",
            "love": "Practical expressions of love matter. Service and helpfulness attract partners. Communication is key.",
            "health": "Digestive health focus. Eat clean, organic foods. Regular exercise routine beneficial.",
            "finance": "Detailed financial planning pays off. Healthcare stocks favorable. Avoid impulsive purchases.",
            "lucky": {"color": "Navy Blue", "number": 5, "day": "Wednesday"}
        },
        "ta": {
            "general": "புதன் பகுப்பாய்வு துல்லியம் மற்றும் விவரங்களுக்கு கவனம் செலுத்தும் தன்மையுடன் உங்களை ஆசீர்வதிக்கிறார்.",
            "career": "உங்கள் சிரத்தையான வேலை கவனிக்கப்படுகிறது. பிரச்சனை தீர்க்கும் திறன்கள் பிரகாசிக்கின்றன.",
            "love": "காதலின் யதார்த்தமான வெளிப்பாடுகள் முக்கியம். சேவை மற்றும் உதவியானது துணையை ஈர்க்கிறது.",
            "health": "செரிமான ஆரோக்கிய கவனம். சுத்தமான, இயற்கை உணவுகளை சாப்பிடுங்கள்.",
            "finance": "விரிவான நிதி திட்டமிடல் பலனளிக்கிறது. சுகாதார பங்குகள் சாதகமானவை.",
            "lucky": {"color": "கடற்படை நீலம்", "number": 5, "day": "புதன்"}
        }
    },
    "Thulam": {
        "ruler": "Venus",
        "element": "Air",
        "exalted": "Saturn",
        "debilitated": "Sun",
        "en": {
            "general": "Venus brings harmony and balance to your life. Today favors partnerships and artistic pursuits.",
            "career": "Diplomatic skills resolve conflicts. Partnerships thrive. Legal matters favor you.",
            "love": "Relationships reach equilibrium. Compromise strengthens bonds. Romantic gestures appreciated.",
            "health": "Kidneys and lower back need care. Balance work and rest. Yoga and meditation beneficial.",
            "finance": "Joint ventures profitable. Luxury items and art investments favorable. Balance income and expenses.",
            "lucky": {"color": "Pink", "number": 6, "day": "Friday"}
        },
        "ta": {
            "general": "சுக்ரன் உங்கள் வாழ்க்கைக்கு நல்லிணக்கம் மற்றும் சமநிலையைத் தருகிறார். இன்று கூட்டாண்மைகள் மற்றும் கலை முயற்சிகளுக்கு சாதகமானது.",
            "career": "தூதுவர் திறன்கள் முரண்பாடுகளைத் தீர்க்கின்றன. கூட்டாண்மைகள் செழிக்கின்றன.",
            "love": "உறவுகள் சமநிலையை அடைகின்றன. சமரசம் பிணைப்புகளை வலுப்படுத்துகிறது.",
            "health": "சிறுநீரகங்கள் மற்றும் கீழ் முதுகு பராமரிப்பு தேவை. வேலை மற்றும் ஓய்வை சமநிலைப்படுத்துங்கள்.",
            "finance": "கூட்டு முயற்சிகள் இலாபகரமானவை. ஆடம்பர பொருட்கள் மற்றும் கலை முதலீடுகள் சாதகமானவை.",
            "lucky": {"color": "இளஞ்சிவப்பு", "number": 6, "day": "வெள்ளி"}
        }
    },
    "Viruchigam": {
        "ruler": "Mars",
        "element": "Water",
        "exalted": "None",
        "debilitated": "Moon",
        "en": {
            "general": "Mars intensifies your focus and passion. Transformation is possible through deep introspection.",
            "career": "Research and investigation favored. Secrets may be revealed. Use power wisely.",
            "love": "Intense emotions surface. Deep connections form. Jealousy must be managed.",
            "health": "Reproductive organs and excretory system need care. Stay hydrated. Avoid toxins.",
            "finance": "Hidden sources of income possible. Inheritance matters may arise. Investigate thoroughly.",
            "lucky": {"color": "Maroon", "number": 9, "day": "Tuesday"}
        },
        "ta": {
            "general": "செவ்வாய் உங்கள் கவனம் மற்றும் உணர்ச்சிப்பூர்வமான தன்மையை தீவிரப்படுத்துகிறார்.",
            "career": "ஆராய்ச்சி மற்றும் விசாரணை ஆதரிக்கப்படுகிறது. ரகசியங்கள் வெளிப்படலாம்.",
            "love": "தீவிரமான உணர்வுகள் மேல்படுகின்றன. ஆழமான இணைப்புகள் உருவாகின்றன.",
            "health": "இனப்பெருக்க உறுப்புகள் மற்றும் வெளியேற்று மண்டலம் பராமரிப்பு தேவை.",
            "finance": "மறைக்கப்பட்ட வருமான ஆதாரங்கள் சாத்தியம். மரபுரிமை விஷயங்கள் எழலாம்.",
            "lucky": {"color": "மெரூன்", "number": 9, "day": "செவ்வாய்"}
        }
    },
    "Dhanusu": {
        "ruler": "Jupiter",
        "element": "Fire",
        "exalted": "None",
        "debilitated": "Mercury",
        "en": {
            "general": "Jupiter expands your horizons through wisdom and adventure. Optimism attracts fortune.",
            "career": "Teaching and mentoring roles favored. Higher education benefits. Travel for work possible.",
            "love": "Shared beliefs strengthen relationships. Adventure brings couples closer. Honesty essential.",
            "health": "Liver and thighs need attention. Moderation in food and drink. Outdoor exercise beneficial.",
            "finance": "Long-term investments prosper. Education and travel expenses worthwhile. Philanthropy rewarded.",
            "lucky": {"color": "Purple", "number": 3, "day": "Thursday"}
        },
        "ta": {
            "general": "குரு ஞானம் மற்றும் சாகசம் மூலம் உங்கள் எல்லைகளை விரிவுபடுத்துகிறார்.",
            "career": "கற்பித்தல் மற்றும் வழிகாட்டும் பாத்திரங்கள் ஆதரிக்கப்படுகின்றன. உயர் கல்வி பயனளிக்கும்.",
            "love": "பகிர்ந்த நம்பிக்கைகள் உறவுகளை வலுப்படுத்துகின்றன. சாகசம் இணையர்களை நெருக்கமாக்குகிறது.",
            "health": "கல்லீரல் மற்றும் தொடைகள் கவனம் தேவை. உணவு மற்றும் பானத்தில் மிதமானம்.",
            "finance": "நீண்டகால முதலீடுகள் செழிக்கின்றன. கல்வி மற்றும் பயண செலவுகள் பயனுள்ளவை.",
            "lucky": {"color": "ஊதா", "number": 3, "day": "வியாழன்"}
        }
    },
    "Makaram": {
        "ruler": "Saturn",
        "element": "Earth",
        "exalted": "Mars",
        "debilitated": "Jupiter",
        "en": {
            "general": "Saturn rewards disciplined efforts with steady progress. Patience is your greatest virtue.",
            "career": "Hard work finally recognized. Authority positions attainable. Long-term planning essential.",
            "love": "Commitment and loyalty valued. Mature relationships thrive. Age differences acceptable.",
            "health": "Bones, joints, and teeth need care. Calcium-rich diet important. Regular exercise crucial.",
            "finance": "Conservative investments pay off. Real estate and land favorable. Avoid speculation.",
            "lucky": {"color": "Brown", "number": 8, "day": "Saturday"}
        },
        "ta": {
            "general": "சனி கட்டுப்பாடான முயற்சிகளை நிலையான முன்னேற்றத்துடன் பரிசளிக்கிறார்.",
            "career": "கடின உழைப்பு இறுதியாக அங்கீகரிக்கப்படுகிறது. அதிகாரம் பதவிகள் அடையக்கூடியவை.",
            "love": "அர்ப்பணிப்பு மற்றும் உண்மை மதிக்கப்படுகிறது. முதிர்ந்த உறவுகள் செழிக்கின்றன.",
            "health": "எலும்புகள், மூட்டுகள் மற்றும் பற்கள் பராமரிப்பு தேவை. கால்சியம் நிறைந்த உணவு முக்கியம்.",
            "finance": "பாதுகாப்பு முதலீடுகள் பலனளிக்கின்றன. நிலம் மற்றும் நிலப்பரப்பு சாதகமானவை.",
            "lucky": {"color": "பழுப்பு", "number": 8, "day": "சனி"}
        }
    },
    "Kumbam": {
        "ruler": "Saturn",
        "element": "Air",
        "exalted": "None",
        "debilitated": "None",
        "en": {
            "general": "Saturn supports innovative thinking and humanitarian causes. Your uniqueness is your strength.",
            "career": "Technology and social reform favored. Group projects succeed. Unconventional approaches work.",
            "love": "Friendship forms foundation of love. Independence valued in relationships. Open communication.",
            "health": "Circulation and ankles need attention. Regular movement important. Avoid sedentary lifestyle.",
            "finance": "Technology investments favorable. Cryptocurrency shows promise. Support social causes.",
            "lucky": {"color": "Electric Blue", "number": 4, "day": "Saturday"}
        },
        "ta": {
            "general": "சனி புதுமையான சிந்தனை மற்றும் மனிதநேயமான காரியங்களை ஆதரிக்கிறார்.",
            "career": "தொழில்நுட்பம் மற்றும் சமூக சீர்திருத்தம் ஆதரிக்கப்படுகிறது. குழு திட்டங்கள் வெற்றி பெறுகின்றன.",
            "love": "நட்பு காதலின் அடித்தளமாக அமைகிறது. சுயாதீனம் உறவுகளில் மதிக்கப்படுகிறது.",
            "health": "இரத்த ஓட்டம் மற்றும் கணுக்கள் கவனம் தேவை. தொடர் இயக்கம் முக்கியம்.",
            "finance": "தொழில்நுட்ப முதலீடுகள் சாதகமானவை. கிரிப்டோகரன்சி வாய்ப்பைக் காட்டுகிறது.",
            "lucky": {"color": "எலக்ட்ரிக் நீலம்", "number": 4, "day": "சனி"}
        }
    },
    "Meenam": {
        "ruler": "Jupiter",
        "element": "Water",
        "exalted": "Venus",
        "debilitated": "Mercury",
        "en": {
            "general": "Jupiter enhances spiritual awareness and creative imagination. Compassion is your gift.",
            "career": "Creative and healing professions favored. Spiritual guidance benefits others. Intuition guides decisions.",
            "love": "Soul connections form. Spiritual compatibility matters. Unconditional love expressed.",
            "health": "Feet and immune system need care. Grounding exercises important. Avoid escapism through substances.",
            "finance": "Charitable giving brings prosperity. Arts and spirituality investments favorable. Trust intuition.",
            "lucky": {"color": "Sea Green", "number": 7, "day": "Thursday"}
        },
        "ta": {
            "general": "குரு ஆன்மீக விழிப்புணர்வு மற்றும் படைப்பாற்றல் கற்பனையை மேம்படுத்துகிறார்.",
            "career": "படைப்பாற்றல் மற்றும் குணப்படுத்தும் தொழில்கள் ஆதரிக்கப்படுகின்றன. ஆன்மீக வழிகாட்டுதல் மற்றவர்களுக்கு பயனளிக்கிறது.",
            "love": "ஆன்மா இணைப்புகள் உருவாகின்றன. ஆன்மீக பொருத்தம் முக்கியம்.",
            "health": "கால்கள் மற்றும் நோய் எதிர்ப்பு மண்டலம் பராமரிப்பு தேவை. தரையிறங்கும் பயிற்சிகள் முக்கியம்.",
            "finance": "தொண்டு வழங்குதல் செழிப்பைத் தருகிறது. கலைகள் மற்றும் ஆன்மீக முதலீடுகள் சாதகமானவை.",
            "lucky": {"color": "கடல் பச்சை", "number": 7, "day": "வியாழன்"}
        }
    }
}

# Rasi symbols mapping
RASI_SYMBOLS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']

# Rasi names in different languages
RASI_NAMES = {
    0: ['Mesham', 'மேஷம்', 'Aries'],
    1: ['Rishabam', 'ரிஷபம்', 'Taurus'],
    2: ['Midhunam', 'மிதுனம்', 'Gemini'],
    3: ['Katakam', 'கடகம்', 'Cancer'],
    4: ['Simmam', 'சிம்மம்', 'Leo'],
    5: ['Kanni', 'கன்னி', 'Virgo'],
    6: ['Thulam', 'துலாம்', 'Libra'],
    7: ['Viruchigam', 'விருச்சிகம்', 'Scorpio'],
    8: ['Dhanusu', 'தனுசு', 'Sagittarius'],
    9: ['Makaram', 'மகரம்', 'Capricorn'],
    10: ['Kumbam', 'கும்பம்', 'Aquarius'],
    11: ['Meenam', 'மீனம்', 'Pisces']
}
