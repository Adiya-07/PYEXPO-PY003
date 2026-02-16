"""
AstroGuy AI — Interactive SVG Birth Chart Generator
====================================================
Generates a South Indian style birth chart as SVG.
Each house is clickable — shows planet info on click.
"""

from typing import Dict, List, Optional


# House positions in South Indian chart layout
# Grid is 4x4, houses numbered 1-12 going clockwise from top-left
# Position = (col, row) in the 4x4 grid, 0-indexed
HOUSE_POSITIONS = {
    1:  (0, 0), 2:  (1, 0), 3:  (2, 0), 4:  (3, 0),
    5:  (3, 1), 6:  (3, 2), 7:  (3, 3),
    8:  (2, 3), 9:  (1, 3), 10: (0, 3),
    11: (0, 2), 12: (0, 1),
}
# Center 2x2 is empty (indices 1,2 in row 1 and 2)

RASI_NAMES = [
    '', 'Mesham','Rishabam','Midhunam','Katakam',
    'Simmam','Kanni','Thulam','Viruchigam',
    'Dhanusu','Makaram','Kumbam','Meenam'
]
RASI_TAMIL = [
    '','மேஷம்','ரிஷபம்','மிதுனம்','கடகம்',
    'சிம்மம்','கன்னி','துலாம்','விருச்சிகம்',
    'தனுசு','மகரம்','கும்பம்','மீனம்'
]

PLANET_SYMBOLS = {
    'Sun':'Su', 'Moon':'Mo', 'Mars':'Ma', 'Mercury':'Me',
    'Jupiter':'Ju', 'Venus':'Ve', 'Saturn':'Sa',
    'Rahu':'Ra', 'Ketu':'Ke', 'Lagna':'La'
}
PLANET_COLORS = {
    'Sun':'#FF8C00', 'Moon':'#C0C0FF', 'Mars':'#FF4444',
    'Mercury':'#44BB44', 'Jupiter':'#FFD700', 'Venus':'#FF69B4',
    'Saturn':'#8888FF', 'Rahu':'#AA44AA', 'Ketu':'#AA8844',
    'Lagna':'#00FFCC'
}
PLANET_INFO = {
    'Sun':     'Soul, ego, father, authority, government service, vitality.',
    'Moon':    'Mind, emotions, mother, water, public life, intuition.',
    'Mars':    'Energy, courage, siblings, property, engineering, surgery.',
    'Mercury': 'Intelligence, communication, business, education, writing.',
    'Jupiter': 'Wisdom, wealth, children, religion, teaching, expansion.',
    'Venus':   'Love, beauty, luxury, arts, marriage, vehicles, comfort.',
    'Saturn':  'Karma, discipline, longevity, service, delays, hard work.',
    'Rahu':    'Obsession, foreign, technology, sudden gains/losses, illusion.',
    'Ketu':    'Spirituality, liberation, past life, detachment, mysticism.',
    'Lagna':   'Ascendant — your body, personality, and life direction.',
}
HOUSE_MEANINGS = {
    1:'Self, personality, body, health, appearance',
    2:'Wealth, family, speech, food, early education',
    3:'Siblings, courage, communication, short journeys',
    4:'Mother, home, property, vehicles, education',
    5:'Children, intelligence, creativity, romance, past life merit',
    6:'Enemies, health issues, debts, service, daily routine',
    7:'Marriage, partnerships, business, foreign travel',
    8:'Longevity, transformation, secrets, inheritance, occult',
    9:'Luck, religion, father, higher education, dharma',
    10:'Career, status, reputation, government, public life',
    11:'Gains, income, elder siblings, social network, desires',
    12:'Expenses, liberation, foreign land, sleep, spirituality',
}


def generate_birth_chart_svg(chart: Dict, size: int = 400) -> str:
    """
    Generate a South Indian birth chart SVG from a chart dict.
    Returns SVG string ready to embed in HTML.
    """
    cell  = size // 4
    pad   = 8
    svg   = []

    # ── Background ────────────────────────────────────────────────────────
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 {size} {size}" width="{size}" height="{size}"
        style="font-family:sans-serif;cursor:pointer"
        id="birthChartSvg">
    <defs>
        <style>
            .house-cell {{ fill:rgba(255,255,255,0.04); stroke:rgba(255,215,0,0.4);
                          stroke-width:1.5; transition:fill 0.2s; }}
            .house-cell:hover {{ fill:rgba(255,215,0,0.12); }}
            .house-num {{ fill:rgba(255,215,0,0.5); font-size:{int(cell*0.18)}px; }}
            .rasi-name {{ fill:rgba(255,255,255,0.6); font-size:{int(cell*0.14)}px; }}
            .planet-text {{ font-size:{int(cell*0.17)}px; font-weight:bold; }}
            .center-box {{ fill:rgba(0,0,0,0.3); stroke:rgba(255,215,0,0.25);
                           stroke-width:1; }}
            .center-title {{ fill:#FFD700; font-size:{int(cell*0.22)}px;
                             font-weight:bold; text-anchor:middle; }}
            .center-sub {{ fill:rgba(255,255,255,0.5); font-size:{int(cell*0.13)}px;
                           text-anchor:middle; }}
        </style>
    </defs>''')

    # ── Get lagna rasi number to figure out which house = which rasi ──────
    lagna_rasi = chart.get('lagna', {}).get('number', 0)

    # Build house → rasi mapping (South Indian: house 1 = lagna rasi)
    house_rasi = {}
    for h in range(1, 13):
        house_rasi[h] = ((lagna_rasi - 1 + h - 1) % 12) + 1

    # Build rasi → planets list
    rasi_planets = {r: [] for r in range(1, 13)}

    # Place Lagna
    rasi_planets[lagna_rasi].append('Lagna')

    # Place planets from chart
    planet_map = {
        'Sun':     chart.get('sunRasi',     chart.get('sun_rasi',     -1)),
        'Moon':    chart.get('rasi', {}).get('number', -1),
        'Jupiter': chart.get('jupiterRasi', chart.get('jupiter_rasi', -1)),
        'Venus':   chart.get('venusRasi',   chart.get('venus_rasi',   -1)),
        'Mars':    chart.get('marsRasi',    chart.get('mars_rasi',    -1)),
        'Mercury': chart.get('mercuryRasi', chart.get('mercury_rasi', -1)),
        'Saturn':  chart.get('saturnRasi',  chart.get('saturn_rasi',  -1)),
        'Rahu':    chart.get('rahuRasi',    chart.get('rahu_rasi',    -1)),
        'Ketu':    chart.get('ketuRasi',    chart.get('ketu_rasi',    -1)),
    }
    for planet, rasi_num in planet_map.items():
        if 1 <= rasi_num <= 12:
            rasi_planets[rasi_num].append(planet)

    # ── Draw 12 houses ────────────────────────────────────────────────────
    for house_num, (col, row) in HOUSE_POSITIONS.items():
        x = col * cell
        y = row * cell
        rasi_num = house_rasi[house_num]
        planets  = rasi_planets.get(rasi_num, [])

        house_meaning = HOUSE_MEANINGS[house_num].replace("'", "\\'")
        rasi_en       = RASI_NAMES[rasi_num]
        planets_str   = ', '.join(planets) if planets else 'Empty'
        onclick = (f"showHouseInfo({house_num}, '{rasi_en}', "
                   f"'{rasi_num}', '{planets_str}', '{house_meaning}')")

        svg.append(f'''
    <g onclick="{onclick}" class="chart-house" id="house{house_num}">
        <rect x="{x}" y="{y}" width="{cell}" height="{cell}"
              class="house-cell" rx="3"/>
        <text x="{x+pad}" y="{y+pad+10}" class="house-num">{house_num}</text>
        <text x="{x+cell//2}" y="{y+cell-pad-12}" class="rasi-name"
              text-anchor="middle">{RASI_TAMIL[rasi_num]}</text>''')

        # Draw planets
        planet_y = y + int(cell * 0.38)
        for i, planet in enumerate(planets[:4]):   # max 4 per house
            px     = x + pad + (i % 2) * (cell//2 - pad)
            py     = planet_y + (i // 2) * int(cell * 0.22)
            color  = PLANET_COLORS.get(planet, '#FFFFFF')
            symbol = PLANET_SYMBOLS.get(planet, planet[:2])
            svg.append(f'''        <text x="{px}" y="{py}" class="planet-text"
                  fill="{color}">{symbol}</text>''')

        svg.append('    </g>')

    # ── Center 2×2 box (chart title) ──────────────────────────────────────
    cx = cell
    cy = cell
    svg.append(f'''
    <rect x="{cx}" y="{cy}" width="{cell*2}" height="{cell*2}"
          class="center-box" rx="4"/>
    <text x="{cx + cell}" y="{cy + int(cell*0.55)}" class="center-title">
        ☿ AstroGuy
    </text>
    <text x="{cx + cell}" y="{cy + int(cell*0.80)}" class="center-sub">
        Vedic Chart
    </text>
    <text x="{cx + cell}" y="{cy + int(cell*1.05)}" class="center-sub">
        {RASI_NAMES[lagna_rasi]} Lagna
    </text>''')

    svg.append('</svg>')
    return '\n'.join(svg)


def get_planet_house_data(chart: Dict) -> List[Dict]:
    """Return list of planets with their house positions for JS tooltip."""
    result = []
    for planet, info in PLANET_INFO.items():
        result.append({
            'name':   planet,
            'symbol': PLANET_SYMBOLS[planet],
            'color':  PLANET_COLORS[planet],
            'info':   info,
        })
    return result
