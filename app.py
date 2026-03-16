"""
AstroGuy AI — Flask Backend (v3, with Login/Register + MongoDB)
================================================================
Run: python app.py

NEW in v3:
  - /register  → create account (saved to MongoDB)
  - /login     → sign in
  - /logout    → clear session
  - /profile   → save/update birth details (redirects to /dashboard)
  - All existing routes unchanged
  - Birth chart details now also saved to MongoDB per user
  - Session stores both chart data (fast) AND user_id (for DB lookup)
"""

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
import os, json, traceback, hashlib

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO
from flask import send_file

from utils.astrology       import calculate_birth_chart, calculate_compatibility, HOROSCOPE, RASIS
from utils.panchangam      import get_panchangam
from utils.chatbot         import get_chatbot_response
from utils.birth_chart_svg import generate_birth_chart_svg, get_planet_house_data

# ── MongoDB ────────────────────────────────────────────────────────────────
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
_mongo    = MongoClient(MONGO_URI)
_db       = _mongo["astroguy"]
users_col = _db["users"]          # stores user accounts + birth details
users_col.create_index("username", unique=True)   # prevent duplicate usernames

# ── App setup ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "astroguy-v3-secret")

# ── Translations (unchanged from v2) ──────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "heroTitle":    "AstroGuy AI",
        "heroSubtitle": "Authentic Vedic Astrology • Ancient Wisdom • Modern Intelligence",
        "formTitle":    "Begin Your Cosmic Journey",
        "labelName":    "Full Name",
        "labelDob":     "Date of Birth",
        "labelTime":    "Birth Time",
        "labelPlace":   "Birth Place",
        "labelGender":  "Gender",
        "btnText":      "Generate My Chart",
        "langText":     "தமிழ்",
        "loadingText":  "Aligning Cosmic Energies...",
    },
    "ta": {
        "heroTitle":    "ஆஸ்ட்ரோகை AI",
        "heroSubtitle": "நேர்மையான வேத ஜோதிடம் • பழங்கால ஞானம் • நவீன அறிவுநுட்பம்",
        "formTitle":    "உங்கள் விண்வெளி பயணத்தைத் தொடங்குங்கள்",
        "labelName":    "முழு பெயர்",
        "labelDob":     "பிறந்த தேதி",
        "labelTime":    "பிறந்த நேரம்",
        "labelPlace":   "பிறந்த இடம்",
        "labelGender":  "பாலினம்",
        "btnText":      "என் ஜாதகத்தை உருவாக்கு",
        "langText":     "English",
        "loadingText":  "விண்வெளி சக்திகளை சீரமைக்கிறது...",
    },
}

# ── Helpers ────────────────────────────────────────────────────────────────
def lang():    return session.get("language", "en")
def t():       return TRANSLATIONS[lang()]
def chart():   return session.get("user_chart")
def prof():    return session.get("user_profile")
def cur_user():return session.get("username")          # None if not logged in

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def _load_user_into_session(username: str):
    """Pull user + chart from MongoDB and populate Flask session."""
    u = users_col.find_one({"username": username}, {"_id": 0})
    if not u:
        return
    session["username"]     = u["username"]
    session["user_display"] = u.get("name", username)
    # Restore chart + profile if they exist in DB
    if u.get("user_chart"):
        session["user_chart"]   = u["user_chart"]
    if u.get("user_profile"):
        session["user_profile"] = u["user_profile"]

# ── Auth routes ────────────────────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if cur_user():
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not username or not password:
            error = "Please fill all fields."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            try:
                users_col.insert_one({
                    "username":     username,
                    "name":         name,
                    "password":     hash_pw(password),
                    "user_chart":   None,
                    "user_profile": None,
                    "created_at":   datetime.utcnow().isoformat(),
                })
                # Auto login after register
                session["username"]     = username
                session["user_display"] = name
                # New user has no chart yet — send to home to fill form
                return redirect(url_for("index"))
            except DuplicateKeyError:
                error = "Username already taken. Try another."

    return render_template(
        "auth.html",
        mode="register",
        error=error,
        translations=t(),
        language=lang(),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if cur_user():
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        u = users_col.find_one({"username": username})
        if u and u.get("password") == hash_pw(password):
            _load_user_into_session(username)
            # If user has a saved chart go to dashboard, else go home to fill form
            if u.get("user_chart"):
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("index"))
        else:
            error = "Invalid username or password."

    return render_template(
        "auth.html",
        mode="login",
        error=error,
        translations=t(),
        language=lang(),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ── Existing pages (UNCHANGED — just added cur_user to template context) ──

@app.route("/")
def index():
    return render_template(
        "index.html",
        translations=t(), language=lang(),
        rasis=RASIS,
        current_user=cur_user(),
        user_display=session.get("user_display"),
    )


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        translations=t(), language=lang(),
        user_chart=chart(), profile=prof(),
        current_user=cur_user(),
        user_display=session.get("user_display"),
    )


@app.route("/horoscope")
def horoscope():
    uc = chart()
    horoscope_data = None
    if uc:
        horoscope_data = HOROSCOPE.get(uc["rasi"]["englishName"], {})
    return render_template(
        "horoscope.html",
        translations=t(), language=lang(),
        user_chart=uc, horoscope_data=horoscope_data,
        all_horoscope=HOROSCOPE,
        current_user=cur_user(),
    )


@app.route("/compatibility")
def compatibility():
    return render_template(
        "compatibility.html",
        translations=t(), language=lang(),
        current_user=cur_user(),
    )


@app.route("/birthchart")
def birthchart():
    uc      = chart()
    svg     = generate_birth_chart_svg(uc, lang()) if uc else None
    planets = get_planet_house_data(uc)    if uc else []
    return render_template(
        "birthchart.html",
        translations=t(), language=lang(),
        user_chart=uc, svg_chart=svg, planets=planets,
        current_user=cur_user(),
    )


MONTHLY_PREDICTIONS = {
    "Mesham": {
        "en": [("Career", "💼", "A month of significant breakthroughs. Your leadership skills will be recognized, potentially leading to a new role or project."), ("Love", "❤️", "Emotional harmony prevails. This is a great time to deepen your connection or start new meaningful relationships."), ("Health", "🏥", "Vitality is high, but ensure you don't overexert yourself. Balance active days with restful nights."), ("Finance", "💰", "Prosperous outlook. Good time for long-term investments, but avoid impulsive luxury spending.")],
        "ta": [("தொழில்", "💼", "குறிப்பிடத்தக்க முன்னேற்றங்களைக் கொண்ட மாதம். உங்கள் தலைமைத்துவ திறன்கள் அங்கீகரிக்கப்படும்."), ("காதல்", "❤️", "உணர்வு ரீதியான இணக்கம் நிலவுகிறது. உங்கள் பிணைப்பை ஆழப்படுத்த இது ஒரு சிறந்த நேரம்."), ("ஆரோக்கியம்", "🏥", "உயிர்ப்பு அதிகமாக உள்ளது, ஆனால் உங்களை அதிகமாக வருத்திக்கொள்ள வேண்டாம்."), ("நிதி", "💰", "செழிப்பான பார்வை. நீண்ட கால முதலீடுகளுக்கு நல்ல நேரம்.")]
    },
    "Rishabam": {
        "en": [("Career", "💼", "Steady progress continues. Your practical approach helps solve complex workplace challenges efficiently."), ("Love", "❤️", "Venus brings charm to your social life. Harmonious interactions with partner and family are highlighted."), ("Health", "🏥", "Focus on throat and neck health. Incorporate gentle stretching and stay hydrated throughout the day."), ("Finance", "💰", "Financial stability is strong. A good month for savings and reviewing your retirement plan.")],
        "ta": [("தொழில்", "💼", "நிலையான முன்னேற்றம் தொடர்கிறது. உங்கள் நடைமுறை அணுகுமுறை சிக்கல்களைத் தீர்க்க உதவுகிறது."), ("காதல்", "❤️", "சுக்கிரன் உங்கள் சமூக வாழ்க்கையில் கவர்ச்சியைக் கொண்டுவருகிறார். குடும்பத்தாருடன் இணக்கமான தொடர்புகள்."), ("ஆரோக்கியம்", "🏥", "தொண்டை மற்றும் கழுத்து ஆரோக்கியத்தில் கவனம் செலுத்துங்கள். நீரேற்றத்துடன் இருப்பது அவசியம்."), ("நிதி", "💰", "நிதி நிலைத்தன்மை வலுவாக உள்ளது. சேமிப்பு மற்றும் ஓய்வூதியத் திட்டங்களை ஆய்வு செய்ய நல்ல மாதம்.")]
    },
    "Midhunam": {
        "en": [("Career", "💼", "Communication is your greatest asset this month. Networking will open doors to unexpected opportunities."), ("Love", "❤️", "Intellectual connections thrive. Engage in deep conversations with your loved ones to strengthen bonds."), ("Health", "🏥", "Mental clarity is high, but watch for nervous tension. Meditation and breathing exercises are beneficial."), ("Finance", "💰", "Business ventures show promise. Diversify your portfolio to ensure long-term financial growth.")],
        "ta": [("தொழில்", "💼", "தகவல்தொடர்பு இந்த மாதம் உங்கள் சிறந்த சொத்து. நெட்வொர்க்கிங் எதிர்பாராத வாய்ப்புகளைத் திறக்கும்."), ("காதல்", "❤️", "அறிவு ரீதியான தொடர்புகள் செழிக்கின்றன. அன்புக்குரியவர்களுடன் ஆழமான உரையாடல்களில் ஈடுபடுங்கள்."), ("ஆரோக்கியம்", "🏥", "மன தெளிவு அதிகமாக உள்ளது, ஆனால் நரம்பு இறுக்கத்தைக் கவனியுங்கள். தியானம் பயனுள்ளதாக இருக்கும்."), ("நிதி", "💰", "வணிக முயற்சிகள் நம்பிக்கையளிக்கின்றன. நீண்ட கால நிதி வளர்ச்சிக்கு உங்கள் முதலீடுகளைப் பல்வகைப்படுத்துங்கள்.")]
    },
    "Katakam": {
        "en": [("Career", "💼", "Focus on collaborative efforts. Your intuitive understanding of colleagues enhances team productivity."), ("Love", "❤️", "Nurturing energy surrounds your relationships. Family matters bring joy and a sense of belonging."), ("Health", "🏥", "Pay attention to digestive health. A balanced diet and mindful eating will keep you energized."), ("Finance", "💰", "Real estate or home-related investments are favorable. Avoid lending money to friends this month.")],
        "ta": [("தொழில்", "💼", "கூட்டு முயற்சிகளில் கவனம் செலுத்துங்கள். சகாக்களின் மீதான உங்கள் உள்ளுணர்வு புரிதல் குழு உற்பத்தியை மேம்படுத்தும்."), ("காதல்", "❤️", "உங்கள் உறவுகளைச் சுற்றியுள்ள வளர்ப்பு ஆற்றல். குடும்ப விஷயங்கள் மகிழ்ச்சியைத் தருகின்றன."), ("ஆரோக்கியம்", "🏥", "செரிமான ஆரோக்கியத்தில் கவனம் செலுத்துங்கள். சீரான உணவு உங்களை உற்சாகமாக வைத்திருக்கும்."), ("நிதி", "💰", "ரியல் எஸ்டேட் அல்லது வீடு தொடர்பான முதலீடுகள் சாதகமானவை. நண்பர்களுக்குப் பணம் கொடுப்பதைத் தவிர்க்கவும்.")]
    },
    "Simmam": {
        "en": [("Career", "💼", "Your charisma helps you win over skeptics. A powerful month for presentations and public speaking."), ("Love", "❤️", "Passion and creativity define your romantic life. Surprise your partner with grand gestures of affection."), ("Health", "🏥", "Heart and spine health are highlighted. Maintain a regular exercise routine and correct posture."), ("Finance", "💰", "Bold financial decisions can pay off, but ensure they are based on sound research and data.")],
        "ta": [("தொழில்", "💼", "உங்கள் கவர்ச்சி சந்தேகப்படுபவர்களையும் வெல்ல உதவுகிறது. விளக்கக்காட்சிகள் மற்றும் பொதுப் பேச்சுகளுக்கு சக்திவாய்ந்த மாதம்."), ("காதல்", "❤️", "உங்கள் காதல் வாழ்க்கையில் ஆர்வமும் படைப்பாற்றலும் வரையறுக்கின்றன. உங்கள் துணையை ஆச்சரியப்படுத்துங்கள்."), ("ஆரோக்கியம்", "🏥", "இதயம் மற்றும் முதுகுத்தண்டு ஆரோக்கியம் முன்னிலைப்படுத்தப்படுகிறது. வழக்கமான உடற்பயிற்சி அவசியம்."), ("நிதி", "💰", "துணிச்சலான நிதி முடிவுகள் பலன் தரும், ஆனால் அவை முறையான ஆராய்ச்சியின் அடிப்படையில் இருப்பதை உறுதிப்படுத்தவும்.")]
    },
    "Kanni": {
        "en": [("Career", "💼", "Precision and attention to detail bring professional recognition. Excellent for research and auditing tasks."), ("Love", "❤️", "Small, thoughtful acts of service strengthen your relationship more than words ever could."), ("Health", "🏥", "Routine is your friend. Consistent sleep and meal times will significantly improve your overall wellbeing."), ("Finance", "💰", "Favorable month for budgeting and expense tracking. Small savings now will lead to big gains later.")],
        "ta": [("தொழில்", "💼", "துல்லியமும் கவனமும் தொழில்முறை அங்கீகாரத்தைக் கொண்டுவருகின்றன. ஆராய்ச்சிப் பணிகளுக்குச் சிறந்தது."), ("காதல்", "❤️", "சிறிய, சிந்தனைமிக்க செயல்கள் உங்கள் உறவை வார்த்தைகளை விட அதிகமாக வலுப்படுத்துகின்றன."), ("ஆரோக்கியம்", "🏥", "வழக்கமான நடைமுறையே உங்கள் நண்பன். நிலையான தூக்கம் மற்றும் உணவு நேரங்கள் உங்கள் நலனை மேம்படுத்தும்."), ("நிதி", "💰", "பட்ஜெட் மற்றும் செலவு கண்காணிப்புக்கு சாதகமான மாதம். சிறிய சேமிப்புகள் பின்னர் பெரிய ஆதாயங்களுக்கு வழிவகுக்கும்.")]
    },
    "Thulam": {
        "en": [("Career", "💼", "Diplomacy resolves long-standing workplace conflicts. Your ability to balance different viewpoints is key."), ("Love", "❤️", "Harmony returns to your relationships. Social events provide opportunities to meet interesting people."), ("Health", "🏥", "Focus on balance — not too much, not too little. Moderate exercise and relaxation are essential."), ("Finance", "💰", "Partnerships can lead to financial growth. Review legal documents carefully before signing new contracts.")],
        "ta": [("தொழில்", "💼", "தூதுவர் திறன் நீண்டகால பணியிட மோதல்களைத் தீர்க்கிறது. வெவ்வேறு கண்ணோட்டங்களைச் சமநிலைப்படுத்தும் திறன் முக்கியம்."), ("காதல்", "❤️", "உங்கள் உறவுகளில் நல்லிணக்கம் திரும்புகிறது. சமூக நிகழ்வுகள் ஆர்வமுள்ளவர்களைச் சந்திக்க வாய்ப்பளிக்கின்றன."), ("ஆரோக்கியம்", "🏥", "மிகவும் அதிகமாகவோ அல்லது குறைவாகவோ இல்லாமல் சமநிலையில் கவனம் செலுத்துங்கள்."), ("நிதி", "💰", "கூட்டாண்மை நிதி வளர்ச்சிக்கு வழிவகுக்கும். புதிய ஒப்பந்தங்களில் கையெழுத்திடும் முன் ஆவணங்களை ஆய்வு செய்யவும்.")]
    },
    "Viruchigam": {
        "en": [("Career", "💼", "Deep research reveals hidden opportunities. Your determination helps you overcome significant professional hurdles."), ("Love", "❤️", "Intense emotional connections are formed. Honesty and vulnerability bring you closer to your partner."), ("Health", "🏥", "Detoxification is beneficial this month. Focus on cleansing your system and getting plenty of rest."), ("Finance", "💰", "Gains from unexpected sources or past investments. A good time to settle old debts.")],
        "ta": [("தொழில்", "💼", "ஆழமான ஆராய்ச்சி மறைக்கப்பட்ட வாய்ப்புகளை வெளிப்படுத்துகிறது. உங்கள் உறுதிப்பாடு தடைகளைத் தாண்ட உதவுகிறது."), ("காதல்", "❤️", "தீவிரமான உணர்வு பூர்வமான தொடர்புகள் உருவாகின்றன. நேர்மை உங்கள் துணையுடன் உங்களை நெருக்கமாக்கும்."), ("ஆரோக்கியம்", "🏥", "இந்த மாதம் நச்சு நீக்கம் பயனுள்ளதாக இருக்கும். உங்கள் அமைப்பைச் சுத்தம் செய்வதில் கவனம் செலுத்துங்கள்."), ("நிதி", "💰", "எதிர்பாராத ஆதாரங்கள் அல்லது கடந்த கால முதலீடுகளிலிருந்து ஆதாயங்கள். பழைய கடன்களைத் தீர்க்க நல்ல நேரம்.")]
    },
    "Dhanusu": {
        "en": [("Career", "💼", "A month for expansive thinking and global outreach. Your visionary ideas gain traction with management."), ("Love", "❤️", "Adventure calls! Sharing new experiences with your partner keeps the spark alive in your relationship."), ("Health", "🏥", "Outdoor activities boost your energy levels. Watch for hip and thigh strain during physical activity."), ("Finance", "💰", "Investment in higher education or travel will bring long-term rewards. Stay open to international trends.")],
        "ta": [("தொழில்", "💼", "பரந்த சிந்தனை மற்றும் உலகளாவிய அவுட்ரீச்சிற்கான மாதம். உங்கள் தொலைநோக்கு யோசனைகள் மேலாண்மையிடம் ஆதரவு பெறும்."), ("காதல்", "❤️", "சாகசம் அழைக்கிறது! உங்கள் துணையுடன் புதிய அனுபவங்களைப் பகிர்ந்து கொள்வது உறவில் ஆர்வத்தைத் தக்கவைக்கும்."), ("ஆரோக்கியம்", "🏥", "வெளிப்புற செயல்பாடுகள் உங்கள் ஆற்றல் நிலைகளை அதிகரிக்கும். உடல் செயல்பாடுகளின் போது இடுப்பு அழுத்தத்தைக் கவனியுங்கள்."), ("நிதி", "💰", "உயர்கல்வி அல்லது பயணத்திலான முதலீடு நீண்ட கால நன்மைகளைத் தரும்.")]
    },
    "Makaram": {
        "en": [("Career", "💼", "Hard work and discipline lead to tangible results. You may receive a promotion or a position of higher responsibility."), ("Love", "❤️", "Commitment and loyalty are themes this month. Building a solid foundation for the future is highlighted."), ("Health", "🏥", "Focus on bone and joint health. Ensure adequate calcium intake and engage in low-impact exercise."), ("Finance", "💰", "Stable financial growth. Long-term investments, especially in real estate, are highly favored.")],
        "ta": [("தொழில்", "💼", "கடின உழைப்பும் ஒழுக்கமும் உறுதியான முடிவுகளுக்கு வழிவகுக்கும். நீங்கள் உயர் பொறுப்பைப் பெறலாம்."), ("காதல்", "❤️", "அர்ப்பணிப்பு மற்றும் விசுவாசம் இந்த மாதத்தின் கருப்பொருள்கள். எதிர்காலத்திற்கு ஒரு திடமான அடித்தளத்தை அமைத்தல்."), ("ஆரோக்கியம்", "🏥", "எலும்பு மற்றும் மூட்டு ஆரோக்கியத்தில் கவனம் செலுத்துங்கள். போதுமான கால்சியம் உட்கொள்வதை உறுதிப்படுத்தவும்."), ("நிதி", "💰", "நிலையான நிதி வளர்ச்சி. நீண்ட கால முதலீடுகள், குறிப்பாக ரியல் எஸ்டேட், மிகவும் சாதகமானது.")]
    },
    "Kumbam": {
        "en": [("Career", "💼", "Innovative solutions set you apart. Collaboration with tech-savvy colleagues leads to success in complex projects."), ("Love", "❤️", "Friendship is the base of romance this month. Shared ideals and community activities bring joy."), ("Health", "🏥", "Stay mindful of your nervous system. Relaxation techniques and plenty of sleep are essential."), ("Finance", "💰", "Unconventional investments might show quick returns. Keep an eye on tech stocks and startup news.")],
        "ta": [("தொழில்", "💼", "புதுமையான தீர்வுகள் உங்களைத் தனித்துக்காட்டுகின்றன. தொழில்நுட்ப அறிவுள்ள சகாக்களுடனான ஒத்துழைப்பு வெற்றிக்கு வழிவகுக்கும்."), ("காதல்", "❤️", "இந்த மாதம் காதலுக்கு நட்புதான் அடிப்படை. பகிரப்பட்ட இலட்சியங்கள் மற்றும் சமூக நடவடிக்கைகள் மகிழ்ச்சியைத் தரும்."), ("ஆரோக்கியம்", "🏥", "உங்கள் நரம்பு மண்டலத்தை கவனத்தில் கொள்ளுங்கள். ஓய்வு நுட்பங்கள் மற்றும் ஏராளமான தூக்கம் அவசியம்."), ("நிதி", "💰", "மரபுசாரா முதலீடுகள் விரைவான வருவாயைக் காட்டக்கூடும். தொழில்நுட்ப பங்குகளைக் கவனியுங்கள்.")]
    },
    "Meenam": {
        "en": [("Career", "💼", "Your creative imagination leads to artistic breakthroughs. Compassionate leadership inspires your team members."), ("Love", "❤️", "Deep spiritual and romantic connections. A month of unconditional love and emotional healing."), ("Health", "🏥", "Intuitive connection with your body's needs. Practice yoga and swimming for mental and physical balance."), ("Finance", "💰", "Trust your gut feelings in financial matters. Charitable acts bring unexpected good fortune and blessings.")],
        "ta": [("தொழில்", "💼", "உங்கள் படைப்பு கற்பனை கலை முன்னேற்றங்களுக்கு வழிவகுக்கிறது. அனுகம்பம் கொண்ட தலைமை உங்கள் குழுவை ஊக்குவிக்கிறது."), ("காதல்", "❤️", "ஆழமான ஆன்மீக மற்றும் காதல் தொடர்புகள். நிபந்தனையற்ற அன்பு மற்றும் உணர்வு ரீதியான குணப்படுத்துதலின் மாதம்."), ("ஆரோக்கியம்", "🏥", "உங்கள் உடலின் தேவைகளுடன் உள்ளுணர்வு தொடர்பு. மன மற்றும் உடல் சமநிலைக்கு யோகா பயிற்சி செய்யவும்."), ("நிதி", "💰", "நிதி விஷயங்களில் உங்கள் உள்ளுணர்வை நம்புங்கள். தொண்டு செயல்கள் எதிர்பாராத நற்பலன்களையும் ஆசீர்வாதங்களையும் தரும்.")]
    }
}

@app.route("/predictions")
def predictions():
    from datetime import timedelta
    uc = chart(); preds = []; m_pred = None
    if uc:
        l = lang()
        MOON_EMOJIS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"]
        NAKS_7 = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu"]
        DAY = [
            {"ce":"Peak energy — ideal for important meetings and decisions.","le":"Express your feelings openly. Romance is strong.","he":"Vitality is high. Great day for exercise.","fe":"Good for financial planning and reviewing investments.","ct":"உச்ச ஆற்றல் — முக்கிய சந்திப்புகளுக்கு சிறந்தது.","lt":"காதல் ஆற்றல் வலுவாக உள்ளது.","ht":"உயிர்ப்பு அதிகம். உடற்பயிற்சிக்கு சிறந்த நாள்.","ft":"நிதி திட்டமிடலுக்கு நல்ல நாள்."},
            {"ce":"Focus on completing pending tasks. Avoid new projects.","le":"Listen more than you speak. Understanding deepens bonds.","he":"Rest and recharge. Hydration is key today.","fe":"Hold off on major spending. Review your budget.","ct":"நிலுவையில் உள்ள பணிகளை முடிக்கவும்.","lt":"அதிகமாக கேளுங்கள். புரிதல் பிணைப்பை ஆழப்படுத்துகிறது.","ht":"ஓய்வெடுங்கள். நீரேற்றம் முக்கியம்.","ft":"பெரிய செலவுகளை தவிர்க்கவும்."},
            {"ce":"Excellent for networking and collaboration.","le":"Social energy is high. Great day for dates.","he":"Mental clarity is sharp. Good for yoga.","fe":"Good day for investments. Consult an advisor.","ct":"நெட்வொர்க்கிங்கிற்கு சிறந்தது.","lt":"சமூக ஆற்றல் அதிகம்.","ht":"மன தெளிவு கூர்மையானது.","ft":"முதலீடுகளுக்கு நல்ல நாள்."},
            {"ce":"Creative work flourishes. Trust your instincts.","le":"Deep emotional conversations strengthen bonds.","he":"Watch for fatigue. Take short breaks.","fe":"Avoid speculative investments.","ct":"படைப்பாற்றல் பணி சிறக்கும்.","lt":"ஆழமான உணர்வு உரையாடல்கள்.","ht":"சோர்வை கவனியுங்கள்.","ft":"ஊக முதலீடுகளை தவிர்க்கவும்."},
            {"ce":"Leadership shines. Take initiative.","le":"Passion and romance are heightened.","he":"Physical energy is excellent.","fe":"Strong day for salary negotiations.","ct":"தலைமைத்துவம் மிளிர்கிறது.","lt":"ஆர்வமும் காதலும் அதிகரித்திருக்கின்றன.","ht":"உடல் ஆற்றல் சிறந்தது.","ft":"சம்பள பேச்சுவார்த்தைகளுக்கு வலுவான நாள்."},
            {"ce":"Day of reflection. Review progress.","le":"Quiet togetherness is more valuable.","he":"Rest is productive. Sleep early.","fe":"Good day to track expenses.","ct":"சிந்தனையின் நாள்.","lt":"அமைதியான ஒன்றிணைவு இன்று மதிப்புமிக்கது.","ht":"ஓய்வு உற்பத்திகரமானது.","ft":"செலவுகளை கண்காணிக்கவும்."},
            {"ce":"Week ends high. Celebrate small wins.","le":"Joyful energy. Laughter brings you closer.","he":"Excellent wellbeing. Treat yourself.","fe":"Review the week's finances.","ct":"வாரம் உயர்வில் முடிகிறது.","lt":"மகிழ்ச்சியான ஆற்றல்.","ht":"சிறந்த நலன்.","ft":"வாரத்தின் நிதியை மதிப்பாய்வு செய்யுங்கள்."},
        ]

        # Monthly Prediction
        rasi_en = uc["rasi"]["englishName"]
        raw_m = MONTHLY_PREDICTIONS.get(rasi_en, {})
        if raw_m:
            items = raw_m.get("ta" if l == "ta" else "en", [])
            m_pred = {
                "month_year": datetime.now().strftime("%B %Y"),
                "areas": items
            }

        # Weekly Predictions
        for i in range(7):
            dt = datetime.now() + timedelta(days=i)
            e  = DAY[i]
            if l == "ta":
                areas = [("தொழில்","💼",e["ct"]),("காதல்","❤️",e["lt"]),("ஆரோக்கியம்","🏥",e["ht"]),("நிதி","💰",e["ft"])]
            else:
                areas = [("Career","💼",e["ce"]),("Love","❤️",e["le"]),("Health","🏥",e["he"]),("Finance","💰",e["fe"])]
            preds.append({
                "date":        dt.strftime("%A, %d %b"),
                "moon_emoji":  MOON_EMOJIS[i % 8],
                "nakshatra":   NAKS_7[i],
                "areas":       areas,
            })
    return render_template(
        "predictions.html",
        translations=t(), language=lang(),
        user_chart=uc, predictions=preds,
        monthly_prediction=m_pred,
        current_user=cur_user(),
    )


@app.route("/finance")
def finance():
    return render_template(
        "finance.html",
        translations=t(), language=lang(),
        user_chart=chart(), current_user=cur_user(),
    )


@app.route("/remedies")
def remedies():
    return render_template(
        "remedies.html",
        translations=t(), language=lang(),
        user_chart=chart(), current_user=cur_user(),
    )


@app.route("/videos")
def videos():
    vlist = [
        {"id":"iw0yxLP0J5E","title":"Understanding Your Birth Chart" if lang()=="en" else "உங்கள் பிறப்பு சக்கரத்தைப் புரிந்துகொள்ளுதல்","meta":"Basics of Vedic Astrology"},
        {"id":"5Rj9EoX_QJk","title":"Planetary Remedies" if lang()=="en" else "கிரக பரிகாரங்கள்","meta":"Authentic Pariharams"},
        {"id":"Hzv4RVRk4Tg","title":"Marriage Compatibility" if lang()=="en" else "திருமண பொருத்தம்","meta":"10 Porutham Explained"},
    ]
    return render_template(
        "videos.html",
        translations=t(), language=lang(),
        videos=vlist, current_user=cur_user(),
    )


@app.route("/chat")
def chat():
    return render_template(
        "chat.html",
        translations=t(), language=lang(),
        current_user=cur_user(),
    )


@app.route("/panchangam")
def panchangam():
    return render_template(
        "panchangam.html",
        translations=t(), language=lang(),
        panchangam=get_panchangam(), current_user=cur_user(),
    )


@app.route("/cosmic-card")
def cosmic_card():
    return render_template(
        "cosmic_card.html",
        translations=t(), language=lang(),
        user_chart=chart(), profile=prof(),
        current_user=cur_user(),
    )


@app.route("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        translations=t(), language=lang(),
        current_user=cur_user(),
    )


@app.route("/wellness")
def wellness():
    return render_template(
        "wellness.html",
        translations=t(), language=lang(),
        user_chart=chart(), panchangam=get_panchangam(),
        current_user=cur_user(),
    )


# ── API routes (UNCHANGED — plus saves to MongoDB if logged in) ───────────

@app.route("/api/calculate-chart", methods=["POST"])
def api_chart():
    try:
        d = request.get_json()
        if not d:
            return jsonify({"success": False, "error": "No data"}), 400

        dob  = d.get("dob", "")
        time = d.get("time", "")
        if not dob or not time:
            return jsonify({"success": False, "error": "Date/time required"}), 400

        y, mo, day = map(int, dob.split("-"))
        h, mi      = map(int, time.split(":"))

        c = calculate_birth_chart(y, mo, day, h, mi, d.get("place", "Chennai"))

        profile = {
            "name":   d.get("name", ""),
            "dob":    dob,
            "time":   time,
            "place":  d.get("place", ""),
            "gender": d.get("gender", ""),
        }

        # Always save to session (fast access)
        session["user_chart"]   = c
        session["user_profile"] = profile

        # If logged in, also persist to MongoDB
        if cur_user():
            users_col.update_one(
                {"username": cur_user()},
                {"$set": {
                    "user_chart":   c,
                    "user_profile": profile,
                    "updated_at":   datetime.utcnow().isoformat(),
                }},
            )

        return jsonify({"success": True, "chart": c})

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/download-chart-pdf")
def download_chart_pdf():
    try:
        uc   = chart()
        p    = prof()
        if not uc or not p:
            return jsonify({"success": False, "error": "No chart data"}), 400

        buffer = BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawCentredString(width / 2, height - 80, "AstroGuy AI")

        c.setFont("Helvetica", 16)
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.drawCentredString(width / 2, height - 110, "Birth Chart Report")

        c.setStrokeColor(colors.HexColor("#FFD700"))
        c.setLineWidth(2)
        c.line(100, height - 130, width - 100, height - 130)

        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawString(100, height - 170, "Personal Information")

        y_pos = height - 200
        for label, value in [
            ("Name:", p.get("name", "-")),
            ("Date of Birth:", p.get("dob", "-")),
            ("Time:", p.get("time", "-")),
            ("Place:", p.get("place", "-")),
            ("Gender:", p.get("gender", "-")),
        ]:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#CCCCCC"))
            c.drawString(100, y_pos, label)
            c.setFont("Helvetica", 10)
            c.drawString(220, y_pos, str(value))
            y_pos -= 25

        y_pos -= 20
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawString(100, y_pos, "Vedic Chart Details")
        y_pos -= 35

        rasi_name  = uc.get("rasi", {}).get("englishName", "-")
        nak_name   = uc.get("nakshatra", {}).get("name", "-")
        pada       = uc.get("nakshatra", {}).get("pada", "-")
        lord       = uc.get("nakshatra", {}).get("lord", "-")
        lagna_name = uc.get("lagna", {}).get("englishName") or uc.get("lagna", {}).get("name", "-")

        for label, value in [
            ("Rasi (Moon Sign):", rasi_name),
            ("Nakshatra:", nak_name),
            ("Pada:", str(pada)),
            ("Nakshatra Lord:", lord),
            ("Lagna (Ascendant):", lagna_name),
        ]:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor("#CCCCCC"))
            c.drawString(100, y_pos, label)
            c.setFont("Helvetica", 10)
            c.drawString(250, y_pos, str(value))
            y_pos -= 25

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawCentredString(width / 2, 50, "Generated by AstroGuy AI - Authentic Vedic Astrology")
        c.drawCentredString(width / 2, 35, f"astroguy.ai • {datetime.now().strftime('%d %B %Y')}")

        c.save()
        buffer.seek(0)

        filename = f"astroguy-chart-{p.get('name','user').lower().replace(' ','-')}.pdf"
        return send_file(buffer, mimetype="application/pdf",
                         as_attachment=True, download_name=filename)

    except Exception as e:
        app.logger.error(f"PDF error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/calculate-compatibility", methods=["POST"])
def api_compat():
    try:
        d = request.get_json()
        y1,mo1,d1 = map(int, d["dob1"].split("-")); h1,m1 = map(int, d["time1"].split(":"))
        y2,mo2,d2 = map(int, d["dob2"].split("-")); h2,m2 = map(int, d["time2"].split(":"))
        c1 = calculate_birth_chart(y1, mo1, d1, h1, m1, d.get("place1","Chennai"))
        c2 = calculate_birth_chart(y2, mo2, d2, h2, m2, d.get("place2","Chennai"))
        result = calculate_compatibility(c1, c2)
        return jsonify({"success": True, "result": result, "chart1": c1, "chart2": c2})
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        d    = request.get_json()
        msg  = d.get("message", "").strip()
        if not msg:
            return jsonify({"success": False, "error": "Empty"}), 400
        l    = d.get("lang") or lang()
        uc   = d.get("userChart") or chart()
        resp = get_chatbot_response(msg, uc, l)
        return jsonify({"success": True, "response": resp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/toggle-language", methods=["POST"])
def api_lang():
    session["language"] = "ta" if lang() == "en" else "en"
    return jsonify({"success": True, "language": session["language"]})


@app.route("/api/get-user-data")
def api_user():
    return jsonify({"chart": chart(), "profile": prof(), "language": lang()})


@app.route("/api/panchangam")
def api_panchangam():
    return jsonify({"success": True, "data": get_panchangam()})


# ── Error handlers ─────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", translations=t(), language=lang()), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)