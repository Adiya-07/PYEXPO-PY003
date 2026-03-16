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


@app.route("/predictions")
def predictions():
    from datetime import timedelta
    uc = chart(); preds = []
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