# 🌟 AstroGuy AI - Vedic Astrology Web Application

A comprehensive Vedic Astrology web application built with **Flask (Python)**. Features authentic **Dashakoota (10 Porutham)** compatibility matching as per South Indian (Tamil) astrology traditions.

## ✨ Features

- 🌙 **Daily Rasi (Moon Sign) Horoscope** - Personalized daily predictions
- 🪐 **Birth Chart (Jathagam)** - Complete Vedic birth chart with planetary positions
- 💑 **Dashakoota Compatibility (10 Porutham)** - Authentic South Indian 10-fold compatibility analysis
- 🔮 **Predictions** - Weekly and monthly forecasts for all life aspects
- 💰 **Financial Astrology** - Wealth predictions and investment guidance
- 🕉️ **Planetary Remedies (Pariharam)** - Authentic Vedic remedies for all 9 planets
- 🤖 **AI Chatbot** - Interactive astrology assistant
- 🎬 **Educational Videos** - Learn Vedic astrology from experts
- 🌐 **Bilingual Support** - English and Tamil languages

## 📿 10 Poruthams (Dashakoota) - 36 Points

The compatibility matching follows the authentic South Indian system:

| # | Porutham | Tamil Name | Max Points | Significance |
|---|----------|------------|------------|--------------|
| 1 | **Dina** (Tara) | தினம் (தாரா) | 3 | Health & Longevity |
| 2 | **Gana** | கணம் | 4 | Temperament & Nature |
| 3 | **Yoni** | யோனி | 4 | Physical Compatibility |
| 4 | **Rasi** | ராசி | 7 | Family Growth & Prosperity |
| 5 | **Rasyadhipati** | ராசியதிபதி | 5 | Mental Rapport |
| 6 | **Rajju** | ரஜ்ஜு | 5 | Longevity (Most Critical) |
| 7 | **Vedha** | வேதா | 2 | Obstacles & Afflictions |
| 8 | **Vashya** | வசியம் | 2 | Mutual Attraction |
| 9 | **Mahendra** | மகேந்திரம் | 2 | Progeny & Children |
| 10 | **Stree Deergha** | ஸ்திரீ தீர்க்கம் | 2 | Wife's Wellbeing |

**Total: 36 Points**

### Score Interpretation
- **28-36**: Excellent Match - Highly blessed union
- **21-27**: Good Match - Compatible with minor remedies
- **16-20**: Average Match - Manageable with effort
- **Below 16**: Challenging - Significant remedies needed

## 🚀 Performance Optimizations

### CSS Optimizations
- Reduced star count from 100 to 50
- Only 20% of stars have animation
- Simplified backdrop effects
- Better paint performance with `contain`
- Support for `prefers-reduced-motion`

### JavaScript Optimizations
- DocumentFragment for batch DOM insertion
- Reduced loading time (1.5s)
- Better memory management
- Debounced event handlers

## 📁 Project Structure

```
astroguy_ai/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore file
│
├── static/                     # Static assets
│   ├── css/style.css          # Optimized CSS styles
│   └── js/main.js             # Optimized JavaScript
│
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html              # Base layout
│   ├── index.html             # Home page
│   ├── horoscope.html         # Horoscope page
│   ├── compatibility.html     # 10 Porutham matching
│   ├── birthchart.html        # Birth chart display
│   ├── predictions.html       # Predictions timeline
│   ├── finance.html           # Financial astrology
│   ├── videos.html            # Videos page
│   ├── remedies.html          # Planetary remedies
│   └── chat.html              # Chat interface
│
├── data/                       # Data modules
│   ├── horoscope_data.py      # Horoscope data for 12 Rasis
│   ├── remedies_data.py       # Planetary remedies
│   ├── chatbot_knowledge.py   # Chatbot responses
│   └── nakshatra_data.py      # Nakshatra information
│
└── utils/                      # Core logic
    ├── astrology_calculator.py # Vedic calculations (10 Poruthams)
    └── chatbot.py              # Chatbot response generator
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd astroguy_ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python app.py
```

Open browser: `http://localhost:5000`

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/horoscope` | GET | Horoscope page |
| `/compatibility` | GET | 10 Porutham compatibility |
| `/birthchart` | GET | Birth chart page |
| `/predictions` | GET | Predictions page |
| `/finance` | GET | Finance page |
| `/videos` | GET | Videos page |
| `/remedies` | GET | Remedies page |
| `/chat` | GET | Chat page |
| `/api/calculate-chart` | POST | Calculate birth chart |
| `/api/calculate-compatibility` | POST | Calculate 10 Porutham compatibility |
| `/api/chat` | POST | Chatbot response |
| `/api/toggle-language` | POST | Toggle language (en/ta) |
| `/api/get-user-data` | GET | Get user session data |

### API Example - 10 Porutham Compatibility

```bash
curl -X POST http://localhost:5000/api/calculate-compatibility \
  -H "Content-Type: application/json" \
  -d '{
    "dob1": "1990-05-15",
    "time1": "10:30",
    "dob2": "1992-08-20",
    "time2": "14:45"
  }'
```

**Response includes all 10 poruthams:**
```json
{
  "success": true,
  "result": {
    "dina": [3, "Excellent"],
    "gana": [4, "Excellent"],
    "yoni": [3, "Very Good"],
    "rasi": [7, "Excellent"],
    "rasyadhipati": [5, "Excellent"],
    "rajju": [5, "Excellent"],
    "vedha": [2, "Excellent"],
    "vashya": [2, "Excellent"],
    "mahendra": [2, "Excellent"],
    "streedeergha": [2, "Excellent"],
    "total": 35,
    "max": 36,
    "percentage": 97.2,
    "verdict": "Excellent Match",
    "doshas": []
  }
}
```

## 🐳 Docker Support

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t astroguy-ai .
docker run -p 5000:5000 astroguy-ai
```

## 🔒 Security Notes

- Uses Flask sessions for user data storage
- Secret key should be changed in production
- No sensitive data stored permanently
- Comprehensive input validation
- Proper error handling

## 🚧 Production Deployment

```bash
export SECRET_KEY="your-secure-secret-key"
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Key Components

### 1. Astrology Calculator (`utils/astrology_calculator.py`)
- **10 Porutham calculations** (Dashakoota)
- Vedic astronomical calculations (VSOP87)
- Birth chart generation with Lahiri Ayanamsa
- Planetary position calculations

### 2. 10 Porutham Details

**Critical Doshas to Watch:**
- **Rajju Dosha**: Same Rajju group (Head, Neck, Middle, Thigh, Foot) - Most dangerous
- **Vedha Dosha**: Mutually opposing stars
- **Gana Dosha**: Deva-Rakshasa combination

### 3. Chatbot (`utils/chatbot.py`)
- Natural language understanding
- Context-aware responses
- Multi-language support (EN/TA)

## 📄 License

Open source. Feel free to use and modify.

## 🙏 Credits

- Framework: Flask (Python)
- Fonts: Google Fonts (Cinzel, Inter, Noto Sans Tamil)
- Icons: Font Awesome

---

**நல்ல பொருத்தம்!** 🌟✨ (Good Matching!)
