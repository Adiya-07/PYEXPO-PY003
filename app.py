"""
AstroGuy AI — Flask Backend (v2, clean rebuild)
================================================
Run: python app.py
"""
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os, json, traceback
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO
from flask import send_file
from utils.astrology   import calculate_birth_chart, calculate_compatibility, HOROSCOPE, RASIS
from utils.panchangam  import get_panchangam
from utils.chatbot     import get_chatbot_response
from utils.birth_chart_svg import generate_birth_chart_svg

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY','astroguy-v2-secret')

TRANSLATIONS = {
    "en":{"heroTitle":"AstroGuy AI","heroSubtitle":"Authentic Vedic Astrology • Ancient Wisdom • Modern Intelligence",
          "formTitle":"Begin Your Cosmic Journey","labelName":"Full Name","labelDob":"Date of Birth",
          "labelTime":"Birth Time","labelPlace":"Birth Place","labelGender":"Gender",
          "btnText":"Generate My Chart","langText":"தமிழ்","loadingText":"Aligning Cosmic Energies..."},
    "ta":{"heroTitle":"ஆஸ்ட்ரோகை AI","heroSubtitle":"நேர்மையான வேத ஜோதிடம் • பழங்கால ஞானம் • நவீன அறிவுநுட்பம்",
          "formTitle":"உங்கள் விண்வெளி பயணத்தைத் தொடங்குங்கள்","labelName":"முழு பெயர்",
          "labelDob":"பிறந்த தேதி","labelTime":"பிறந்த நேரம்","labelPlace":"பிறந்த இடம்",
          "labelGender":"பாலினம்","btnText":"என் ஜாதகத்தை உருவாக்கு",
          "langText":"English","loadingText":"விண்வெளி சக்திகளை சீரமைக்கிறது..."}
}

def lang(): return session.get("language","en")
def t():    return TRANSLATIONS[lang()]
def chart():return session.get("user_chart")
def prof(): return session.get("user_profile")

# ── Pages ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", translations=t(), language=lang(),
                           rasis=RASIS)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", translations=t(), language=lang(),
                           user_chart=chart(), profile=prof())

@app.route("/horoscope")
def horoscope():
    uc = chart()
    horoscope_data = None
    if uc:
        horoscope_data = HOROSCOPE.get(uc["rasi"]["englishName"], {})
    return render_template("horoscope.html", translations=t(), language=lang(),
                           user_chart=uc, horoscope_data=horoscope_data,
                           all_horoscope=HOROSCOPE)

@app.route("/compatibility")
def compatibility():
    return render_template("compatibility.html", translations=t(), language=lang())

@app.route("/birthchart")
def birthchart():
    from utils.birth_chart_svg import generate_birth_chart_svg, get_planet_house_data
    
    uc = chart()
    svg = generate_birth_chart_svg(uc) if uc else None
    planets = get_planet_house_data(uc) if uc else []  # ← ADD THIS!
    
    return render_template("birthchart.html", 
                          translations=t(), 
                          language=lang(),
                          user_chart=uc, 
                          svg_chart=svg,
                          planets=planets)  # ← ADD THIS!

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
            {"ce":"Excellent for networking and collaboration. New opportunities emerge.","le":"Social energy is high. Great day for dates and outings.","he":"Mental clarity is sharp. Good for yoga and meditation.","fe":"Good day for investments. Consult an advisor.","ct":"நெட்வொர்க்கிங்கிற்கு சிறந்தது. புதிய வாய்ப்புகள் வருகின்றன.","lt":"சமூக ஆற்றல் அதிகம். சந்திப்புகளுக்கு சிறந்த நாள்.","ht":"மன தெளிவு கூர்மையானது. யோகாவிற்கு நல்ல நாள்.","ft":"முதலீடுகளுக்கு நல்ல நாள்."},
            {"ce":"Creative work flourishes. Trust your instincts over analysis.","le":"Deep emotional conversations strengthen your relationship.","he":"Watch for fatigue. Take short breaks throughout the day.","fe":"Avoid speculative investments. Conservative choices safer.","ct":"படைப்பாற்றல் பணி சிறக்கும்.","lt":"ஆழமான உணர்வு உரையாடல்கள் உறவை வலுப்படுத்துகின்றன.","ht":"சோர்வை கவனியுங்கள். சிறிய இடைவெளிகள் எடுங்கள்.","ft":"ஊக முதலீடுகளை தவிர்க்கவும்."},
            {"ce":"Leadership shines. Take initiative on projects you believe in.","le":"Passion and romance are heightened. Plan something special.","he":"Physical energy is excellent. Push yourself a little.","fe":"Strong day for salary negotiations and financial talks.","ct":"தலைமைத்துவம் மிளிர்கிறது.","lt":"ஆர்வமும் காதலும் அதிகரித்திருக்கின்றன.","ht":"உடல் ஆற்றல் சிறந்தது.","ft":"சம்பள பேச்சுவார்த்தைகளுக்கு வலுவான நாள்."},
            {"ce":"Day of reflection. Review progress and set new intentions.","le":"Quiet togetherness is more valuable than grand gestures.","he":"Rest is productive. Sleep early, avoid screens.","fe":"Good day to track expenses and improve savings.","ct":"சிந்தனையின் நாள். முன்னேற்றத்தை மதிப்பீடு செய்யுங்கள்.","lt":"அமைதியான ஒன்றிணைவு இன்று மிகவும் மதிப்புமிக்கது.","ht":"ஓய்வு உற்பத்திகரமானது.","ft":"செலவுகளை கண்காணிக்கவும்."},
            {"ce":"Week ends high. Celebrate small wins and plan ahead.","le":"Joyful energy. Laughter and fun bring you closer.","he":"Excellent wellbeing. Treat yourself to something good.","fe":"Review the week's finances and plan the month ahead.","ct":"வாரம் உயர்வில் முடிகிறது. சிறிய வெற்றிகளை கொண்டாடுங்கள்.","lt":"மகிழ்ச்சியான ஆற்றல். சிரிப்பு உங்களை நெருக்கமாக்குகிறது.","ht":"சிறந்த நலன். ஏதாவது புத்துணர்ச்சிகரமானதை அனுபவியுங்கள்.","ft":"வாரத்தின் நிதியை மதிப்பாய்வு செய்யுங்கள்."},
        ]
        for i in range(7):
            try: dt = datetime.now() + timedelta(days=i)
            except: dt = datetime.now()
            e = DAY[i]
            if l == "ta":
                areas = [("தொழில்","💼",e["ct"]),("காதல்","❤️",e["lt"]),("ஆரோக்கியம்","🏥",e["ht"]),("நிதி","💰",e["ft"])]
            else:
                areas = [("Career","💼",e["ce"]),("Love","❤️",e["le"]),("Health","🏥",e["he"]),("Finance","💰",e["fe"])]
            preds.append({"date":dt.strftime("%A, %d %b"),"moon_emoji":MOON_EMOJIS[i%8],"nakshatra":NAKS_7[i],"areas":areas})
    return render_template("predictions.html", translations=t(), language=lang(),
                           user_chart=uc, predictions=preds)

@app.route("/finance")
def finance():
    uc = chart()
    return render_template("finance.html", translations=t(), language=lang(), user_chart=uc)

@app.route("/remedies")
def remedies():
    return render_template("remedies.html", translations=t(), language=lang(), user_chart=chart())

@app.route("/videos")
def videos():
    vlist = [
        {"id":"iw0yxLP0J5E","title":"Understanding Your Birth Chart" if lang()=="en" else "உங்கள் பிறப்பு சக்கரத்தைப் புரிந்துகொள்ளுதல்","meta":"Basics of Vedic Astrology"},
        {"id":"5Rj9EoX_QJk","title":"Planetary Remedies" if lang()=="en" else "கிரக பரிகாரங்கள்","meta":"Authentic Pariharams"},
        {"id":"Hzv4RVRk4Tg","title":"Marriage Compatibility" if lang()=="en" else "திருமண பொருத்தம்","meta":"10 Porutham Explained"},
    ]
    return render_template("videos.html", translations=t(), language=lang(), videos=vlist)

@app.route("/chat")
def chat():
    return render_template("chat.html", translations=t(), language=lang())

@app.route("/panchangam")
def panchangam():
    pdata = get_panchangam()
    return render_template("panchangam.html", translations=t(), language=lang(), panchangam=pdata)

@app.route("/cosmic-card")
def cosmic_card():
    return render_template("cosmic_card.html", translations=t(), language=lang(),
                           user_chart=chart(), profile=prof())

@app.route("/quiz")
def quiz():
    return render_template("quiz.html", translations=t(), language=lang())

@app.route("/wellness")
def wellness():
    pdata = get_panchangam()
    return render_template("wellness.html", translations=t(), language=lang(),
                           user_chart=chart(), panchangam=pdata)

# ── API ────────────────────────────────────────────────────────────────────
@app.route("/api/calculate-chart", methods=["POST"])
def api_chart():
    try:
        d = request.get_json()
        if not d: return jsonify({"success":False,"error":"No data"}),400
        dob  = d.get("dob",""); time = d.get("time","")
        if not dob or not time: return jsonify({"success":False,"error":"Date/time required"}),400
        y,mo,day = map(int,dob.split("-"))
        h,mi     = map(int,time.split(":"))
        c = calculate_birth_chart(y,mo,day,h,mi,d.get("place","Chennai"))
        session["user_chart"]   = c
        session["user_profile"] = {"name":d.get("name",""),"dob":dob,"time":time,
                                   "place":d.get("place",""),"gender":d.get("gender","")}
        return jsonify({"success":True,"chart":c})
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success":False,"error":str(e)}),500
        
@app.route("/api/download-chart-pdf")
def download_chart_pdf():
    """Generate and download birth chart as PDF"""
    try:
        uc = chart()
        prof = session.get("user_profile")
        
        if not uc or not prof:
            return jsonify({"success": False, "error": "No chart data"}), 400
        
        # Create PDF in memory
        buffer = BytesIO()
        c = pdf_canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawCentredString(width/2, height - 80, "AstroGuy AI")
        
        c.setFont("Helvetica", 16)
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.drawCentredString(width/2, height - 110, "Birth Chart Report")
        
        # Horizontal line
        c.setStrokeColor(colors.HexColor("#FFD700"))
        c.setLineWidth(2)
        c.line(100, height - 130, width - 100, height - 130)
        
        # Personal Info
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawString(100, height - 170, "Personal Information")
        
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#CCCCCC"))
        y = height - 200
        
        info_data = [
            ("Name:", prof.get("name", "-")),
            ("Date of Birth:", prof.get("dob", "-")),
            ("Time:", prof.get("time", "-")),
            ("Place:", prof.get("place", "-")),
            ("Gender:", prof.get("gender", "-"))
        ]
        
        for label, value in info_data:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(100, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(220, y, str(value))
            y -= 25
        
        # Chart Details
        y -= 20
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#FFD700"))
        c.drawString(100, y, "Vedic Chart Details")
        
        y -= 35
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#CCCCCC"))
        
        rasi_name = uc.get("rasi", {}).get("english_name") or uc.get("rasi", {}).get("englishName", "-")
        nak_name = uc.get("nakshatra", {}).get("name", "-")
        pada = uc.get("nakshatra", {}).get("pada", "-")
        lord = uc.get("nakshatra", {}).get("lord", "-")
        lagna_name = uc.get("lagna", {}).get("english_name") or uc.get("lagna", {}).get("englishName") or uc.get("lagna", {}).get("name", "-")
        
        chart_data = [
            ("Rasi (Moon Sign):", rasi_name),
            ("Nakshatra:", nak_name),
            ("Pada:", str(pada)),
            ("Nakshatra Lord:", lord),
            ("Lagna (Ascendant):", lagna_name)
        ]
        
        for label, value in chart_data:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(100, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(250, y, str(value))
            y -= 25
        
        # Footer
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawCentredString(width/2, 50, "Generated by AstroGuy AI - Authentic Vedic Astrology")
        c.drawCentredString(width/2, 35, f"astroguy.ai • {datetime.now().strftime('%d %B %Y')}")
        
        # Save PDF
        c.save()
        buffer.seek(0)
        
        filename = f"astroguy-chart-{prof.get('name', 'user').lower().replace(' ', '-')}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        app.logger.error(f"PDF generation error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/calculate-compatibility", methods=["POST"])
def api_compat():
    try:
        d = request.get_json()
        y1,mo1,d1 = map(int,d["dob1"].split("-")); h1,m1 = map(int,d["time1"].split(":"))
        y2,mo2,d2 = map(int,d["dob2"].split("-")); h2,m2 = map(int,d["time2"].split(":"))
        c1 = calculate_birth_chart(y1,mo1,d1,h1,m1,d.get("place1","Chennai"))
        c2 = calculate_birth_chart(y2,mo2,d2,h2,m2,d.get("place2","Chennai"))
        result = calculate_compatibility(c1,c2)
        return jsonify({"success":True,"result":result,"chart1":c1,"chart2":c2})
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        d   = request.get_json()
        msg = d.get("message","").strip()
        if not msg: return jsonify({"success":False,"error":"Empty"}),400
        l   = d.get("lang") or lang()
        uc  = d.get("userChart") or chart()
        resp= get_chatbot_response(msg, uc, l)
        return jsonify({"success":True,"response":resp})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/toggle-language", methods=["POST"])
def api_lang():
    session["language"] = "ta" if lang()=="en" else "en"
    return jsonify({"success":True,"language":session["language"]})

@app.route("/api/get-user-data")
def api_user():
    return jsonify({"chart":chart(),"profile":prof(),"language":lang()})

@app.route("/api/panchangam")
def api_panchangam():
    return jsonify({"success":True,"data":get_panchangam()})

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html",translations=t(),language=lang()),404

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True,threaded=True)
