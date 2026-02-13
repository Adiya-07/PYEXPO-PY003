"""
AstroGuy AI - Vedic Astrology Web Application
Flask Backend Server - Optimized Version with 10 Poruthams
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os
import traceback

# Import utilities
from utils.astrology_calculator import (
    VedicAstroCalculator, CompatibilityCalculator,
    get_rasi_symbol, get_planet_positions
)
from utils.chatbot import get_chatbot_response
from data.horoscope_data import HOROSCOPE_DATA, RASI_NAMES, RASI_SYMBOLS
from data.remedies_data import REMEDIES_DATA
from data.nakshatra_data import NAKSHATRAS

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'astroguy-dev-key-change-in-production')

# Initialize calculators
astro_calc = VedicAstroCalculator()
compat_calc = CompatibilityCalculator()

# ==================== TRANSLATIONS ====================

TRANSLATIONS = {
    "en": {
        "heroTitle": "AstroGuy AI",
        "heroSubtitle": "Authentic Vedic Astrology • Ancient Wisdom • Modern Intelligence",
        "formTitle": "Begin Your Cosmic Journey",
        "labelName": "Full Name",
        "labelDob": "Date of Birth",
        "labelTime": "Birth Time",
        "labelPlace": "Birth Place",
        "labelGender": "Gender",
        "labelPhone": "Phone (Optional)",
        "btnText": "Generate My Chart",
        "feat1": "Daily Rasi",
        "feat2": "Birth Chart",
        "feat3": "Predictions",
        "feat4": "Compatibility",
        "feat5": "Finance",
        "feat6": "Remedies",
        "rasiTitle": "Your Rasi (Moon Sign)",
        "compatTitle": "Dashakoota Compatibility (10 Poruthams)",
        "checkBtn": "Analyze Compatibility",
        "chartTitle": "Vedic Birth Chart (Jathagam)",
        "genChartBtn": "Calculate Positions",
        "predictionsTitle": "Horoscope Predictions",
        "financeTitle": "Financial Astrology",
        "videosTitle": "Astrology Videos",
        "remedyTitle": "Planetary Remedies (Pariharam)",
        "langText": "தமிழ்",
        "loadingText": "Aligning Cosmic Energies...",
        "rasiLabel": "Rasi (Moon Sign)",
        "nakshatraLabel": "Nakshatra",
        "lagnaLabel": "Lagna (Ascendant)",
        "ayanamsaLabel": "Ayanamsa"
    },
    "ta": {
        "heroTitle": "ஆஸ்ட்ரோகை AI",
        "heroSubtitle": "நேர்மையான வேத ஜோதிடம் • பழங்கால ஞானம் • நவீன அறிவுநுட்பம்",
        "formTitle": "உங்கள் விண்வெளி பயணத்தைத் தொடங்குங்கள்",
        "labelName": "முழு பெயர்",
        "labelDob": "பிறந்த தேதி",
        "labelTime": "பிறந்த நேரம்",
        "labelPlace": "பிறந்த இடம்",
        "labelGender": "பாலினம்",
        "labelPhone": "தொலைபேசி (விருப்பம்)",
        "btnText": "என் ஜாதகத்தை உருவாக்கு",
        "feat1": "தினசரி ராசி",
        "feat2": "பிறப்பு சக்கரம்",
        "feat3": "கணிப்புகள்",
        "feat4": "பொருத்தம்",
        "feat5": "நிதி",
        "feat6": "பரிகாரங்கள்",
        "rasiTitle": "உங்கள் ராசி (சந்திர ராசி)",
        "compatTitle": "தசகூட பொருத்தம் (10 பொருத்தங்கள்)",
        "checkBtn": "பொருத்தம் பார்",
        "chartTitle": "வேத பிறப்பு சக்கரம் (ஜாதகம்)",
        "genChartBtn": "கிரக நிலைகளை கணக்கிடு",
        "predictionsTitle": "ராசி பலன்கள்",
        "financeTitle": "நிதி ஜோதிடம்",
        "videosTitle": "ஜோதிட வீடியோக்கள்",
        "remedyTitle": "கிரக பரிகாரங்கள் (பரிகாரம்)",
        "langText": "English",
        "loadingText": "விண்வெளி சக்திகளை சீரமைக்கிறது...",
        "rasiLabel": "ராசி (சந்திர ராசி)",
        "nakshatraLabel": "நட்சத்திரம்",
        "lagnaLabel": "லக்னம்",
        "ayanamsaLabel": "அயனாம்சம்"
    }
}

# ==================== ROUTES ====================

@app.route("/")
def index():
    """Home page"""
    lang = session.get("language", "en")
    return render_template("index.html", 
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          horoscope_data=HOROSCOPE_DATA,
                          rasi_symbols=RASI_SYMBOLS)


@app.route("/horoscope")
def horoscope():
    """Horoscope page"""
    lang = session.get("language", "en")
    user_chart = session.get("user_chart")
    
    horoscope_data = None
    if user_chart:
        rasi_name = user_chart["rasi"]["english_name"]
        horoscope_data = HOROSCOPE_DATA.get(rasi_name, {})
    
    return render_template("horoscope.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          user_chart=user_chart,
                          horoscope_data=horoscope_data,
                          rasi_symbols=RASI_SYMBOLS)


@app.route("/compatibility")
def compatibility():
    """Compatibility matching page - 10 Poruthams"""
    lang = session.get("language", "en")
    return render_template("compatibility.html",
                          translations=TRANSLATIONS[lang],
                          language=lang)


@app.route("/birthchart")
def birthchart():
    """Birth chart page"""
    lang = session.get("language", "en")
    user_chart = session.get("user_chart")
    planets = get_planet_positions()
    
    return render_template("birthchart.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          user_chart=user_chart,
                          planets=planets)


@app.route("/predictions")
def predictions():
    """Predictions page"""
    lang = session.get("language", "en")
    user_chart = session.get("user_chart")
    
    # Generate 7-day predictions
    predictions_list = []
    if user_chart:
        rasi_name = user_chart["rasi"]["english_name"]
        rasi_data = HOROSCOPE_DATA.get(rasi_name, {})
        
        for i in range(7):
            date = datetime.now()
            date = date.replace(day=date.day + i)
            predictions_list.append({
                "date": date,
                "data": rasi_data.get(lang, {})
            })
    
    return render_template("predictions.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          user_chart=user_chart,
                          predictions=predictions_list)


@app.route("/finance")
def finance():
    """Financial astrology page"""
    lang = session.get("language", "en")
    user_chart = session.get("user_chart")
    
    forecasts = []
    if user_chart:
        nakshatra_lord = user_chart["nakshatra"]["lord"]
        rasi_lord = user_chart["rasi"]["number"]
        
        periods = [
            {"en": "This Week", "ta": "இந்த வாரம்"},
            {"en": "This Month", "ta": "இந்த மாதம்"},
            {"en": "Next Quarter", "ta": "அடுத்த காலாண்டு"}
        ]
        
        forecasts = [
            {
                "period": periods[0][lang],
                "prediction": f"{nakshatra_lord}'s influence brings investment opportunities. Real estate and precious metals show positive trends." if lang == "en" else f"{nakshatra_lord} அதிபதியின் செல்வாக்கு முதலீட்டு வாய்ப்புகளைத் தருகிறது.",
                "advice": "Consider SIP investments. Avoid lending money to friends." if lang == "en" else "SIP முதலீடுகளைக் கருத்தில் கொள்ளவும். நண்பர்களுக்கு பணம் கடனாகத் தவிர்க்கவும்."
            },
            {
                "period": periods[1][lang],
                "prediction": f"Planetary positions suggest disciplined spending. Budget review necessary." if lang == "en" else "கிரக நிலைகள் கட்டுப்பாடான செலவைக் குறிக்கின்றன.",
                "advice": "Create emergency fund. Track daily expenses meticulously." if lang == "en" else "அவசரகால நிதியை உருவாக்கவும். தினசரி செலவுகளை கவனமாகக் கண்காணிக்கவும்."
            },
            {
                "period": periods[2][lang],
                "prediction": "Favorable period for long-term investments. Partnership proposals look promising." if lang == "en" else "நீண்டகால முதலீடுகளுக்கு சாதகமான காலம்.",
                "advice": "Due diligence essential. Legal review of contracts recommended." if lang == "en" else "உரிய விசாரணை அவசியம். ஒப்பந்தங்களின் சட்ட ஆய்வு பரிந்துரைக்கப்படுகிறது."
            }
        ]
    
    return render_template("finance.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          user_chart=user_chart,
                          forecasts=forecasts)


@app.route("/videos")
def videos():
    """Videos page"""
    lang = session.get("language", "en")
    
    videos_list = [
        {
            "id": "iw0yxLP0J5E",
            "title": "Understanding Your Birth Chart" if lang == "en" else "உங்கள் பிறப்பு சக்கரத்தைப் புரிந்துகொள்ளுதல்",
            "meta": "Basics of Vedic Astrology" if lang == "en" else "வேத ஜோதிடத்தின் அடிப்படைகள்"
        },
        {
            "id": "5Rj9EoX_QJk",
            "title": "Planetary Remedies" if lang == "en" else "கிரக பரிகாரங்கள்",
            "meta": "Authentic Pariharams" if lang == "en" else "நேர்மையான பரிகாரங்கள்"
        },
        {
            "id": "Hzv4RVRk4Tg",
            "title": "Marriage Compatibility" if lang == "en" else "திருமண பொருத்தம்",
            "meta": "10 Porutham Explained" if lang == "en" else "10 பொருத்தங்கள் விளக்கம்"
        }
    ]
    
    return render_template("videos.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          videos=videos_list)


@app.route("/remedies")
def remedies():
    """Remedies page"""
    lang = session.get("language", "en")
    return render_template("remedies.html",
                          translations=TRANSLATIONS[lang],
                          language=lang,
                          remedies=REMEDIES_DATA)


@app.route("/chat")
def chat():
    """Chat page"""
    lang = session.get("language", "en")
    return render_template("chat.html",
                          translations=TRANSLATIONS[lang],
                          language=lang)


# ==================== API ENDPOINTS ====================

@app.route("/api/calculate-chart", methods=["POST"])
def calculate_chart():
    """API endpoint to calculate birth chart"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Parse date and time
        dob = data.get("dob", "")
        time = data.get("time", "")
        
        if not dob or not time:
            return jsonify({"success": False, "error": "Date and time are required"}), 400
        
        try:
            year, month, day = map(int, dob.split("-"))
            hour, minute = map(int, time.split(":"))
        except ValueError:
            return jsonify({"success": False, "error": "Invalid date or time format"}), 400
        
        # Calculate birth chart
        chart = astro_calc.calculate_birth_chart(
            year, month, day, hour, minute,
            data.get("place", "Chennai")
        )
        
        # Store in session
        session["user_chart"] = chart
        session["user_profile"] = {
            "name": data.get("name", ""),
            "dob": dob,
            "time": time,
            "place": data.get("place", ""),
            "gender": data.get("gender", "")
        }
        
        return jsonify({
            "success": True,
            "chart": chart
        })
    
    except Exception as e:
        app.logger.error(f"Error calculating chart: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.route("/api/calculate-compatibility", methods=["POST"])
def calculate_compatibility():
    """API endpoint to calculate 10 Porutham compatibility"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Parse dates and times
        dob1 = data.get("dob1", "")
        time1 = data.get("time1", "")
        dob2 = data.get("dob2", "")
        time2 = data.get("time2", "")
        
        if not all([dob1, time1, dob2, time2]):
            return jsonify({"success": False, "error": "All dates and times are required"}), 400
        
        try:
            year1, month1, day1 = map(int, dob1.split("-"))
            hour1, minute1 = map(int, time1.split(":"))
            year2, month2, day2 = map(int, dob2.split("-"))
            hour2, minute2 = map(int, time2.split(":"))
        except ValueError:
            return jsonify({"success": False, "error": "Invalid date or time format"}), 400
        
        # Calculate charts
        chart1 = astro_calc.calculate_birth_chart(year1, month1, day1, hour1, minute1)
        chart2 = astro_calc.calculate_birth_chart(year2, month2, day2, hour2, minute2)
        
        # Calculate 10 Porutham compatibility
        result = compat_calc.calculate_full_compatibility(chart1, chart2)
        
        return jsonify({
            "success": True,
            "result": result
        })
    
    except Exception as e:
        app.logger.error(f"Error calculating compatibility: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.route("/api/chat", methods=["POST"])
def chat_api():
    """API endpoint for chatbot"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({"success": False, "error": "Empty message"}), 400
        
        lang = session.get("language", "en")
        user_chart = session.get("user_chart")
        
        response = get_chatbot_response(message, user_chart, lang)
        
        return jsonify({
            "success": True,
            "response": response
        })
    
    except Exception as e:
        app.logger.error(f"Error in chat: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.route("/api/toggle-language", methods=["POST"])
def toggle_language():
    """API endpoint to toggle language"""
    try:
        current_lang = session.get("language", "en")
        new_lang = "ta" if current_lang == "en" else "en"
        session["language"] = new_lang
        
        return jsonify({
            "success": True,
            "language": new_lang
        })
    except Exception as e:
        app.logger.error(f"Error toggling language: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


@app.route("/api/get-user-data")
def get_user_data():
    """API endpoint to get user data"""
    try:
        return jsonify({
            "profile": session.get("user_profile"),
            "chart": session.get("user_chart"),
            "language": session.get("language", "en")
        })
    except Exception as e:
        app.logger.error(f"Error getting user data: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    lang = session.get("language", "en")
    return render_template("index.html", 
                          translations=TRANSLATIONS[lang],
                          language=lang), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    app.logger.error(f"Server error: {str(e)}")
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ==================== MAIN ====================

if __name__ == "__main__":
    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )
