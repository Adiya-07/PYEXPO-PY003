"""
AstroGuy AI — Flask Backend (v2, clean rebuild)
================================================
Run: python app.py
"""
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os, json, traceback

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

@app.route("/horoscope")
def horoscope():
    uc = chart()
    hdata = None
    if uc:
        hdata = HOROSCOPE.get(uc["rasi"]["englishName"],{}).get(lang(),{})
    return render_template("horoscope.html", translations=t(), language=lang(),
                           user_chart=uc, horoscope=hdata, rasis=RASIS)

@app.route("/compatibility")
def compatibility():
    return render_template("compatibility.html", translations=t(), language=lang())

@app.route("/birthchart")
def birthchart():
    uc  = chart()
    svg = generate_birth_chart_svg(uc) if uc else None
    return render_template("birthchart.html", translations=t(), language=lang(),
                           user_chart=uc, svg_chart=svg)

@app.route("/predictions")
def predictions():
    uc    = chart()
    pdata = None
    if uc:
        pdata = HOROSCOPE.get(uc["rasi"]["englishName"],{}).get(lang(),{})
    return render_template("predictions.html", translations=t(), language=lang(),
                           user_chart=uc, predictions=pdata)

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
