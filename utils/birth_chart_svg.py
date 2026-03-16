"""
AstroGuy AI — South Indian Birth Chart SVG Generator
=====================================================
CORRECT South Indian chart rules:
- 12 signs are FIXED in their boxes (Pisces always top-left, clockwise)
- Fixed layout: Pi Ar Ta Ge / Aq [  ] Ca / Cp [  ] Le / Sg Sc Li Vi
- Lagna (ascendant) is marked with diagonal lines in its sign box
- Houses are counted clockwise FROM the Lagna sign
- Planets go in their actual sign box (not house number box)
"""
from typing import Dict, List

# ── Fixed South Indian grid layout ──────────────────────────────────────────
# Sign numbers (1=Aries...12=Pisces) in grid position (col, row), 0-indexed
# Top row L→R:    Pisces(12) Aries(1)  Taurus(2)  Gemini(3)
# Right col T→B:  Cancer(4)  Leo(5)    Virgo(6)
# Bot row R→L:    Libra(7)   Scorpio(8) Sagittarius(9) Capricorn(10)
# Left col B→T:   Aquarius(11)
SIGN_POSITIONS = {
    12: (0,0),  1: (1,0),  2: (2,0),  3: (3,0),
    11: (0,1),                          4: (3,1),
    10: (0,2),                          5: (3,2),
     9: (0,3),  8: (1,3),  7: (2,3),  6: (3,3),
}

RASI_EN = {
    1:'Mesham',2:'Rishabam',3:'Midhunam',4:'Katakam',
    5:'Simmam',6:'Kanni',7:'Thulam',8:'Viruchigam',
    9:'Dhanusu',10:'Makaram',11:'Kumbam',12:'Meenam'
}
RASI_TA = {
    1:'மேஷம்',2:'ரிஷபம்',3:'மிதுனம்',4:'கடகம்',
    5:'சிம்மம்',6:'கன்னி',7:'துலாம்',8:'விருச்சிகம்',
    9:'தனுசு',10:'மகரம்',11:'கும்பம்',12:'மீனம்'
}
PLANET_SYM = {
    'Sun':'Su','Moon':'Mo','Mars':'Ma','Mercury':'Me',
    'Jupiter':'Ju','Venus':'Ve','Saturn':'Sa',
    'Rahu':'Ra','Ketu':'Ke','Lagna':'Lg'
}
PLANET_COL = {
    'Sun':'#FF8C00','Moon':'#C0C0FF','Mars':'#FF4444',
    'Mercury':'#44BB44','Jupiter':'#FFD700','Venus':'#FF69B4',
    'Saturn':'#8888FF','Rahu':'#AA44AA','Ketu':'#AA8844',
    'Lagna':'#00FFCC'
}
PLANET_INFO = {
    'Sun':    'Soul, ego, father, authority, vitality, government service.',
    'Moon':   'Mind, emotions, mother, water, public life, intuition.',
    'Mars':   'Energy, courage, siblings, property, engineering, surgery.',
    'Mercury':'Intelligence, communication, business, education, writing.',
    'Jupiter':'Wisdom, wealth, children, religion, teaching, expansion.',
    'Venus':  'Love, beauty, luxury, arts, marriage, vehicles, comfort.',
    'Saturn': 'Karma, discipline, longevity, service, delays, hard work.',
    'Rahu':   'Obsession, foreign, technology, sudden gains/losses, illusion.',
    'Ketu':   'Spirituality, liberation, past life, detachment, mysticism.',
    'Lagna':  'Ascendant — your body, personality, and life direction.',
}
PLANET_INFO_TA = {
    'Sun':    'ஆன்மா, எகோ, தந்தை, அதிகாரம், உயிர்ப்பு, அரசாங்க சேவை.',
    'Moon':   'மனம், உணர்வுகள், தாய், நீர், பொது வாழ்க்கை, உள்நுணர்வு.',
    'Mars':   'ஆற்றல், தைரியம், சகோதரர்கள், சொத்து, பொறியியல், அறுவை சிகிச்சை.',
    'Mercury':'புத்திசாலித்தனம், தொடர்பு, வணிகம், கல்வி, எழுத்து.',
    'Jupiter':'ஞானம், செல்வம், குழந்தைகள், மதம், கற்பித்தல், விரிவாக்கம்.',
    'Venus':  'காதல், அழகு, சொகுசு, கலைகள், திருமணம், வாகனங்கள், வசதி.',
    'Saturn': 'கர்மா, ஒழுக்கம், நீடித்த வாழ்க்கை, சேவை, தாமதங்கள், கடின உழைப்பு.',
    'Rahu':   'ஆசை, வெளிநாடு, தொழில்நுட்பம், திடீர் ஆதாயங்கள்/இழப்புகள், மாயை.',
    'Ketu':   'ஆன்மீகம், விடுவிப்பு, முந்தைய வாழ்க்கை, விலகல், மர்மம்.',
    'Lagna':  'அஸ்கண்டன்ட் — உங்கள் உடல், ஆளுமை, மற்றும் வாழ்க்கை திசை.',
}
PLANET_HOUSE_MEANINGS = {
    ('Sun', 1): "Sun in the 1st house bestows strong leadership, vitality, and a commanding presence. The native has good health, self-confidence, and often holds authoritative positions. This placement enhances physical strength, promotes a positive outlook on life, and attracts respect and admiration from peers and subordinates alike.",
    ('Sun', 2): "Sun in the 2nd house brings wealth through family or government, strong speech, and family status. It may indicate fame or wealth accumulation from paternal side. Natives often have a powerful voice, enjoy financial stability, and are respected for their family values and contributions to society.",
    ('Sun', 3): "Sun in the 3rd house enhances courage, communication, and sibling relationships. The native is bold, adventurous, and may excel in writing or short journeys. This position fosters bravery in expressing ideas, strengthens bonds with siblings, and encourages pursuits in media, travel, or competitive activities.",
    ('Sun', 4): "Sun in the 4th house indicates strong motherly influence, property ownership, and emotional stability. It brings success in real estate and domestic happiness. Individuals with this placement often have a nurturing home environment, achieve property gains, and find emotional fulfillment through family and home-related endeavors.",
    ('Sun', 5): "Sun in the 5th house promotes creativity, intelligence, and children. The native may have leadership in education, arts, or speculative ventures. This house placement encourages artistic expression, intellectual pursuits, and joyful experiences with children, leading to success in creative fields and speculative investments.",
    ('Sun', 6): "Sun in the 6th house gives strength in overcoming enemies, service, and health issues. It can lead to careers in medicine, law, or competitive fields. Natives exhibit resilience in daily challenges, excel in service-oriented professions, and maintain good health through disciplined routines and overcoming obstacles.",
    ('Sun', 7): "Sun in the 7th house affects partnerships and marriage. It may bring a dominant spouse or success in business partnerships and foreign relations. This placement influences harmonious alliances, attracts powerful partners, and promotes success in collaborative ventures and international dealings.",
    ('Sun', 8): "Sun in the 8th house deals with transformation, secrets, and longevity. It can indicate interest in occult, inheritance, or sudden changes in life. Individuals may experience profound personal growth, uncover hidden knowledge, and benefit from legacies or transformative experiences that extend their lifespan.",
    ('Sun', 9): "Sun in the 9th house enhances luck, religion, and higher education. The native may travel abroad, follow spiritual paths, or have a wise father figure. This position brings fortunate opportunities, deepens philosophical understanding, and encourages exploration of distant lands and spiritual teachings.",
    ('Sun', 10): "Sun in the 10th house is excellent for career and reputation. It brings success in government, leadership roles, and public recognition. Natives achieve high status, gain public acclaim, and excel in authoritative positions that allow them to influence society and lead with honor.",
    ('Sun', 11): "Sun in the 11th house fulfills desires, gains, and social networks. The native achieves goals, has influential friends, and gains from elder siblings. This placement attracts supportive networks, enables goal realization, and brings financial and social benefits through community and elder family members.",
    ('Sun', 12): "Sun in the 12th house indicates expenses, spirituality, and foreign lands. It may lead to charitable work, isolation, or losses due to ego. Natives often engage in humanitarian efforts, seek spiritual enlightenment, and may experience expenditures related to foreign travels or personal growth journeys.",
    ('Moon', 1): "Moon in the 1st house makes the native emotional, intuitive, and sensitive. It affects appearance, health, and public image, often bringing popularity. This placement enhances emotional intelligence, fosters nurturing qualities, and attracts public attention through a gentle and approachable demeanor.",
    ('Moon', 2): "Moon in the 2nd house influences family wealth, speech, and food. The native may have fluctuating finances and strong family bonds. It promotes emotional attachment to material possessions, encourages culinary interests, and can lead to income through family businesses or emotional support roles.",
    ('Moon', 3): "Moon in the 3rd house enhances communication, siblings, and short travels. It brings creativity in writing and adaptability. Natives are emotionally expressive, form deep bonds with siblings, and find comfort in short journeys that stimulate their imagination and social interactions.",
    ('Moon', 4): "Moon in the 4th house strengthens motherly ties, home life, and emotions. It indicates property gains and emotional security. Individuals experience a strong connection to their roots, achieve domestic stability, and find emotional fulfillment in creating a nurturing home environment.",
    ('Moon', 5): "Moon in the 5th house boosts creativity, children, and romance. The native is artistic, loving towards children, and enjoys speculative activities. This position fosters emotional involvement in creative pursuits, deepens romantic experiences, and brings joy through interactions with children and artistic endeavors.",
    ('Moon', 6): "Moon in the 6th house affects health, service, and daily routine. It may cause emotional stress from work or health issues. Natives are empathetic in service roles, may experience mood swings related to health, and find emotional balance through routine and caring for others.",
    ('Moon', 7): "Moon in the 7th house influences marriage and partnerships. It brings emotional harmony in relationships and success in business. This placement promotes deep emotional connections in partnerships, attracts caring spouses, and enhances success in collaborative business ventures through intuitive understanding.",
    ('Moon', 8): "Moon in the 8th house deals with emotional transformations and secrets. It can indicate psychic abilities or sudden emotional changes. Individuals undergo profound emotional growth, develop intuitive insights, and may explore hidden aspects of life through transformative experiences.",
    ('Moon', 9): "Moon in the 9th house promotes intuition, travel, and spirituality. The native may have foreign connections and philosophical interests. This position enhances emotional exploration of philosophy, encourages travel for emotional enrichment, and fosters spiritual growth through intuitive understanding.",
    ('Moon', 10): "Moon in the 10th house affects career through emotions and public. It brings fluctuating reputation and careers in public service. Natives excel in roles requiring emotional intelligence, experience career changes influenced by public mood, and achieve success in nurturing professions.",
    ('Moon', 11): "Moon in the 11th house fulfills emotional desires and gains. The native has supportive friends and gains from social networks. This placement attracts emotionally fulfilling friendships, enables achievement of heartfelt goals, and brings benefits through community involvement and social connections.",
    ('Moon', 12): "Moon in the 12th house indicates emotional expenses and isolation. It may lead to foreign residence or spiritual retreats. Natives seek emotional solitude for introspection, may experience expenditures on spiritual pursuits, and find emotional healing in distant lands or meditative practices.",
    ('Mars', 1): "Mars in the 1st house gives energy, courage, and physical strength. The native is bold, competitive, and may have scars or injuries. This placement fuels ambition, promotes athletic pursuits, and instills a warrior-like spirit that drives success in competitive environments.",
    ('Mars', 2): "Mars in the 2nd house brings wealth through hard work, strong speech, and family conflicts. It indicates property acquisition. Natives accumulate assets via determination, may face familial disputes, and develop a forceful communication style that commands attention.",
    ('Mars', 3): "Mars in the 3rd house enhances courage, siblings, and communication. The native is adventurous, may have younger siblings, and excels in sports. This position encourages bold expression, fosters sibling rivalries or support, and leads to success in physical activities and courageous endeavors.",
    ('Mars', 4): "Mars in the 4th house affects home and property. It may bring disputes over land or strong maternal influence. Individuals experience dynamic home life, pursue property aggressively, and may have intense relationships with mothers or domestic conflicts.",
    ('Mars', 5): "Mars in the 5th house promotes creativity and children. The native is passionate, may have male children, and enjoys competitive sports. This placement ignites creative energy, encourages passionate romances, and brings enthusiasm to parenting and recreational pursuits.",
    ('Mars', 6): "Mars in the 6th house is strong for overcoming enemies and health. It leads to careers in medicine, army, or competitive fields. Natives combat health challenges vigorously, excel in service professions, and demonstrate resilience in daily struggles and professional rivalries.",
    ('Mars', 7): "Mars in the 7th house affects marriage and partnerships. It may bring a dynamic spouse or business rivalries. This position attracts energetic partners, may cause marital conflicts, and promotes success in competitive business alliances and assertive negotiations.",
    ('Mars', 8): "Mars in the 8th house deals with transformation and secrets. It can indicate surgical procedures or intense experiences. Individuals undergo powerful transformations, explore hidden energies, and may face life-threatening situations that lead to profound personal growth.",
    ('Mars', 9): "Mars in the 9th house enhances courage in religion and travel. The native may be adventurous in spiritual pursuits. This placement fuels bold exploration of philosophy, encourages daring travels, and promotes assertive approaches to higher learning and spiritual journeys.",
    ('Mars', 10): "Mars in the 10th house brings career success through hard work. It indicates leadership in military, engineering, or politics. Natives achieve professional prominence via determination, excel in authoritative roles, and demonstrate leadership in fields requiring strength and strategy.",
    ('Mars', 11): "Mars in the 11th house fulfills desires and gains. The native achieves goals through effort and has courageous friends. This position attracts ambitious social circles, enables goal attainment through persistence, and brings gains from group activities and bold initiatives.",
    ('Mars', 12): "Mars in the 12th house indicates expenses and foreign lands. It may lead to isolation or losses from enemies. Natives may expend energy on hidden matters, face isolation due to conflicts, and find release through foreign adventures or spiritual battles.",
    ('Mercury', 1): "Mercury in the 1st house makes the native intelligent and communicative. It affects appearance and brings wit, adaptability. This placement sharpens mental acuity, enhances verbal skills, and promotes a youthful, agile demeanor that attracts intellectual connections.",
    ('Mercury', 2): "Mercury in the 2nd house influences wealth through business, speech, and education. The native is good at negotiations. It fosters financial gains via communication, encourages educational pursuits, and develops persuasive speech for business success.",
    ('Mercury', 3): "Mercury in the 3rd house enhances communication and siblings. It brings skills in writing, teaching, and short journeys. Natives excel in expressive arts, maintain close sibling bonds, and thrive in environments requiring quick thinking and adaptability.",
    ('Mercury', 4): "Mercury in the 4th house affects education and home. The native may have multiple properties or interests in learning. This position promotes intellectual home life, encourages property investments, and fosters a love for knowledge and domestic discussions.",
    ('Mercury', 5): "Mercury in the 5th house boosts intelligence and creativity. It indicates success in education, arts, and speculation. Individuals shine in intellectual pursuits, enjoy creative expression, and find success in educational fields, artistic ventures, and speculative activities.",
    ('Mercury', 6): "Mercury in the 6th house helps in service and health. The native may work in healthcare, law, or daily routines. This placement aids in analytical work, promotes health through mental discipline, and leads to careers in service industries requiring precision.",
    ('Mercury', 7): "Mercury in the 7th house influences partnerships. It brings business acumen and harmonious relationships. Natives excel in negotiations, attract communicative partners, and achieve success in business collaborations through intellectual synergy.",
    ('Mercury', 8): "Mercury in the 8th house deals with secrets and research. It can indicate interest in occult or investigative work. Individuals delve into hidden knowledge, pursue research, and may uncover secrets through analytical thinking and transformative studies.",
    ('Mercury', 9): "Mercury in the 9th house promotes higher education and travel. The native is philosophical and may teach or write. This position encourages intellectual exploration, fosters philosophical thinking, and leads to success in teaching, writing, and international communications.",
    ('Mercury', 10): "Mercury in the 10th house brings career in communication. It indicates success in business, writing, or public speaking. Natives achieve professional recognition through verbal skills, excel in communicative professions, and build careers on intellectual reputation.",
    ('Mercury', 11): "Mercury in the 11th house fulfills intellectual desires. The native gains through networks and has communicative friends. This placement attracts like-minded social circles, enables goal achievement via networking, and brings gains from intellectual and communicative pursuits.",
    ('Mercury', 12): "Mercury in the 12th house indicates expenses on education. It may lead to foreign studies or spiritual communication. Natives invest in higher learning, explore spiritual concepts intellectually, and may pursue education in distant lands or through introspective studies.",
    ('Jupiter', 1): "Jupiter in the 1st house gives wisdom and optimism. The native is generous, healthy, and has a positive outlook. This placement expands personal growth, attracts good fortune, and promotes a benevolent personality that inspires trust and admiration.",
    ('Jupiter', 2): "Jupiter in the 2nd house brings wealth and family prosperity. It indicates gains from family and strong values. Natives accumulate abundance through ethical means, strengthen family bonds, and develop a generous approach to financial matters.",
    ('Jupiter', 3): "Jupiter in the 3rd house enhances knowledge and siblings. The native is learned, has good relations with siblings. This position broadens intellectual horizons, fosters sibling harmony, and encourages pursuits in teaching, writing, and expansive communications.",
    ('Jupiter', 4): "Jupiter in the 4th house strengthens home and education. It brings property and emotional happiness. Individuals enjoy abundant home life, acquire properties, and find joy in educational and familial expansions.",
    ('Jupiter', 5): "Jupiter in the 5th house promotes children and wisdom. The native is creative, has good children, and enjoys teaching. This placement blesses with progeny, enhances creative wisdom, and brings success in educational and artistic fields.",
    ('Jupiter', 6): "Jupiter in the 6th house helps in overcoming obstacles. It indicates service to others and health recovery. Natives overcome challenges with optimism, excel in service professions, and maintain health through positive routines and charitable acts.",
    ('Jupiter', 7): "Jupiter in the 7th house brings good partnerships. The native has a wise spouse and successful business. This position attracts benevolent partners, promotes harmonious marriages, and ensures success in collaborative ventures through mutual respect.",
    ('Jupiter', 8): "Jupiter in the 8th house deals with transformation and wealth. It can indicate inheritance or spiritual growth. Individuals experience profound transformations, receive legacies, and grow spiritually through deep insights and shared resources.",
    ('Jupiter', 9): "Jupiter in the 9th house is excellent for luck and religion. The native is fortunate, travels, and follows dharma. This placement brings divine favor, encourages pilgrimages, and promotes adherence to righteous paths and philosophical teachings.",
    ('Jupiter', 10): "Jupiter in the 10th house brings career success. It indicates leadership in teaching, law, or religion. Natives achieve high status through wisdom, excel in authoritative roles, and gain public recognition for their benevolent leadership.",
    ('Jupiter', 11): "Jupiter in the 11th house fulfills desires and gains. The native has wise friends and achieves goals. This position attracts supportive networks, enables abundant gains, and brings fulfillment through community involvement and wise associations.",
    ('Jupiter', 12): "Jupiter in the 12th house indicates spiritual expenses. It may lead to foreign charity or liberation. Natives invest in spiritual pursuits, engage in charitable work abroad, and achieve liberation through expansive spiritual practices.",
    ('Venus', 1): "Venus in the 1st house gives beauty and charm. The native is attractive, artistic, and enjoys luxury. This placement enhances physical allure, fosters artistic talents, and promotes a love for refined pleasures and harmonious interactions.",
    ('Venus', 2): "Venus in the 2nd house brings wealth through arts, family, and speech. It indicates luxury and good food. Natives accumulate wealth via creative pursuits, enjoy culinary delights, and develop a melodious voice for financial success.",
    ('Venus', 3): "Venus in the 3rd house enhances creativity and communication. The native is artistic and has harmonious siblings. This position inspires poetic expression, fosters sibling affection, and encourages pursuits in arts, music, and pleasant communications.",
    ('Venus', 4): "Venus in the 4th house affects home and comfort. It brings beautiful home and emotional pleasure. Individuals create aesthetically pleasing homes, find emotional bliss in domestic settings, and enjoy comforts that enhance family harmony.",
    ('Venus', 5): "Venus in the 5th house promotes love and arts. The native is romantic, creative, and enjoys entertainment. This placement deepens romantic experiences, boosts artistic creativity, and brings joy through children, romance, and leisure activities.",
    ('Venus', 6): "Venus in the 6th house helps in service and health. It may indicate artistic careers or health through diet. Natives excel in service with grace, maintain health via balanced diets, and pursue careers in healing arts or aesthetic services.",
    ('Venus', 7): "Venus in the 7th house brings harmonious marriage. The native has a loving spouse and business success. This position attracts beautiful partners, promotes marital bliss, and ensures success in partnerships through mutual affection and cooperation.",
    ('Venus', 8): "Venus in the 8th house deals with luxury and secrets. It can indicate gains from partnerships or occult. Individuals enjoy sensual pleasures in hidden realms, receive inheritances, and explore esoteric arts for personal transformation.",
    ('Venus', 9): "Venus in the 9th house promotes beauty in religion. The native travels for pleasure and has artistic interests. This placement beautifies spiritual pursuits, encourages pleasurable travels, and fosters appreciation for cultural and religious arts.",
    ('Venus', 10): "Venus in the 10th house brings career in arts. It indicates success in entertainment, fashion, or public. Natives achieve fame through beauty, excel in creative professions, and gain public adoration for their aesthetic contributions.",
    ('Venus', 11): "Venus in the 11th house fulfills desires for luxury. The native gains through friends and social networks. This position attracts affluent social circles, enables fulfillment of material wishes, and brings gains from artistic and social collaborations.",
    ('Venus', 12): "Venus in the 12th house indicates expenses on luxury. It may lead to foreign romance or spiritual beauty. Natives indulge in luxurious expenditures, experience romantic connections abroad, and find beauty in spiritual or secluded pleasures.",
    ('Saturn', 1): "Saturn in the 1st house gives discipline and longevity. The native is serious, hardworking, and may have delayed success. This placement instills responsibility, promotes enduring health, and teaches life lessons through perseverance and structured personal development.",
    ('Saturn', 2): "Saturn in the 2nd house brings slow wealth accumulation. It indicates family responsibilities and speech delays. Natives build wealth gradually, shoulder family duties, and develop measured speech that gains respect over time.",
    ('Saturn', 3): "Saturn in the 3rd house affects siblings and communication. The native is cautious and may have sibling issues. This position encourages careful expression, may bring sibling separations, and fosters disciplined approaches to learning and short travels.",
    ('Saturn', 4): "Saturn in the 4th house influences home and mother. It may bring property delays or emotional restraint. Individuals experience structured home life, face maternal challenges, and achieve property ownership through persistent efforts.",
    ('Saturn', 5): "Saturn in the 5th house affects children and creativity. It indicates delayed children or disciplined arts. Natives approach creativity seriously, may have later progeny, and find success in structured artistic or educational pursuits.",
    ('Saturn', 6): "Saturn in the 6th house helps in service and health. The native overcomes enemies through hard work. This placement promotes diligent service, aids in health management, and leads to success in overcoming obstacles via discipline.",
    ('Saturn', 7): "Saturn in the 7th house brings serious partnerships. It may indicate delayed marriage or business discipline. Natives form enduring alliances, may experience marital delays, and achieve business success through responsible partnerships.",
    ('Saturn', 8): "Saturn in the 8th house deals with longevity and secrets. It can indicate long life or karmic transformations. Individuals undergo deep karmic lessons, maintain longevity through discipline, and explore hidden aspects with serious intent.",
    ('Saturn', 9): "Saturn in the 9th house promotes disciplined religion. The native is philosophical and may have foreign hardships. This position encourages structured spiritual growth, may bring challenges abroad, and fosters wisdom through philosophical discipline.",
    ('Saturn', 10): "Saturn in the 10th house brings career through hard work. It indicates success in government or structured fields. Natives achieve professional prominence via perseverance, excel in authoritative roles, and gain reputation through consistent effort.",
    ('Saturn', 11): "Saturn in the 11th house fulfills desires slowly. The native achieves goals through persistence and has reliable friends. This placement attracts steadfast social networks, enables gradual goal attainment, and brings enduring gains from disciplined efforts.",
    ('Saturn', 12): "Saturn in the 12th house indicates isolation and expenses. It may lead to spiritual discipline or foreign losses. Natives seek solitude for introspection, may face expenditures abroad, and achieve spiritual growth through disciplined seclusion.",
    ('Rahu', 1): "Rahu in the 1st house brings obsession and foreign influence. The native is ambitious but may have unconventional appearance. This placement fuels intense ambitions, attracts foreign elements, and promotes a unique persona that challenges conventional norms.",
    ('Rahu', 2): "Rahu in the 2nd house affects wealth suddenly. It indicates gains from foreign or unusual sources. Natives experience fluctuating finances, may inherit unconventional wealth, and develop speech influenced by foreign cultures.",
    ('Rahu', 3): "Rahu in the 3rd house enhances communication and travel. The native is adventurous and may have sibling issues. This position encourages bold explorations, may disrupt sibling relationships, and fosters innovative communication styles.",
    ('Rahu', 4): "Rahu in the 4th house influences home and emotions. It may bring foreign property or emotional instability. Individuals seek unconventional homes, experience emotional upheavals, and may acquire properties abroad.",
    ('Rahu', 5): "Rahu in the 5th house promotes creativity and speculation. The native is innovative but may have risky ventures. This placement ignites unconventional creativity, encourages speculative risks, and may affect progeny in unique ways.",
    ('Rahu', 6): "Rahu in the 6th house helps in overcoming enemies. It indicates success in foreign service or health issues. Natives combat adversaries cunningly, may work in international service, and face health challenges requiring innovative treatments.",
    ('Rahu', 7): "Rahu in the 7th house affects partnerships. It may bring foreign spouse or business illusions. This position attracts exotic partners, may lead to deceptive alliances, and promotes international business ventures.",
    ('Rahu', 8): "Rahu in the 8th house deals with secrets and transformation. It can indicate occult interests or sudden changes. Individuals delve into hidden mysteries, undergo radical transformations, and may experience unexpected gains or losses.",
    ('Rahu', 9): "Rahu in the 9th house promotes foreign travel and religion. The native may follow unconventional beliefs. This placement encourages global explorations, fosters eclectic spiritual paths, and promotes philosophical innovations.",
    ('Rahu', 10): "Rahu in the 10th house brings career in technology. It indicates success in foreign or innovative fields. Natives achieve fame in cutting-edge professions, may work internationally, and gain reputation through unconventional career paths.",
    ('Rahu', 11): "Rahu in the 11th house fulfills desires unusually. The native gains from networks but may have illusions. This position attracts diverse social circles, enables unexpected gains, and may involve deceptive group activities.",
    ('Rahu', 12): "Rahu in the 12th house indicates foreign expenses. It may lead to isolation or spiritual illusions. Natives incur costs abroad, seek seclusion for mystical pursuits, and may experience deceptive spiritual experiences.",
    ('Ketu', 1): "Ketu in the 1st house brings detachment and spirituality. The native is introspective and may have health issues. This placement promotes spiritual detachment, encourages self-reflection, and may lead to unconventional health approaches or mystical experiences.",
    ('Ketu', 2): "Ketu in the 2nd house affects family wealth. It indicates detachment from material possessions. Natives renounce material attachments, may experience family wealth fluctuations, and develop a detached approach to financial matters.",
    ('Ketu', 3): "Ketu in the 3rd house influences siblings and communication. The native is detached from worldly pursuits. This position fosters spiritual communication, may separate from siblings, and encourages detachment from superficial interactions.",
    ('Ketu', 4): "Ketu in the 4th house affects home and emotions. It may bring detachment from family or property. Individuals seek spiritual homes, experience emotional detachment, and may renounce traditional family structures.",
    ('Ketu', 5): "Ketu in the 5th house promotes spiritual creativity. The native is detached from children or arts. This placement ignites mystical creativity, may lead to detachment from progeny, and fosters spiritual approaches to artistic expression.",
    ('Ketu', 6): "Ketu in the 6th house helps in service. It indicates detachment from enemies and health routines. Natives serve selflessly, overcome adversaries spiritually, and maintain health through detached, mindful practices.",
    ('Ketu', 7): "Ketu in the 7th house affects partnerships. It may bring detachment in marriage or business. This position promotes spiritual partnerships, may lead to unconventional marriages, and encourages detachment from material alliances.",
    ('Ketu', 8): "Ketu in the 8th house deals with liberation. It can indicate interest in occult or past life karma. Individuals pursue spiritual liberation, explore esoteric knowledge, and resolve karmic debts through transformative experiences.",
    ('Ketu', 9): "Ketu in the 9th house promotes spiritual travel. The native is detached from religion or foreign lands. This placement encourages mystical journeys, fosters detachment from dogmatic beliefs, and promotes spiritual exploration abroad.",
    ('Ketu', 10): "Ketu in the 10th house brings career detachment. It indicates success in spiritual or unconventional fields. Natives achieve fame through selfless service, may renounce worldly careers, and find success in humanitarian or spiritual professions.",
    ('Ketu', 11): "Ketu in the 11th house fulfills spiritual desires. The native is detached from gains and friends. This position attracts spiritually aligned networks, enables fulfillment of higher desires, and promotes detachment from material gains.",
    ('Ketu', 12): "Ketu in the 12th house indicates liberation. It may lead to spiritual isolation or foreign detachment. Natives achieve moksha through seclusion, may reside abroad spiritually, and experience detachment from worldly illusions.",
}
PLANET_HOUSE_MEANINGS_TA = {
    ('Sun', 1): "சூரியன் 1வது வீட்டில் இருப்பது வலிமையான தலைமைத்துவம், உயிர்ப்பு மற்றும் கட்டளையிடும் தோற்றத்தை வழங்குகிறது. சொந்தக்காரர் நல்ல ஆரோக்கியம், சுயநம்பிக்கை கொண்டவராக இருப்பார், மேலும் பெரும்பாலும் அதிகாரப்பூர்வ நிலைகளை வகிப்பார். இந்த நிலை உடல் வலிமையை மேம்படுத்துகிறது, வாழ்க்கையில் நேர்மறையான பார்வையை ஊக்குவிக்கிறது, மேலும் சகாக்கள் மற்றும் துணை அதிகாரிகளிடமிருந்து மரியாதை மற்றும் பாராட்டத்தை ஈர்க்கிறது.",
    ('Sun', 2): "சூரியன் 2வது வீட்டில் இருப்பது குடும்பம் அல்லது அரசாங்கத்திலிருந்து செல்வத்தை கொண்டுவருகிறது, வலிமையான பேச்சு, மற்றும் குடும்ப நிலை. இது தந்தை பக்கத்திலிருந்து புகழ் அல்லது செல்வம் சேர்ப்பை குறிக்கலாம்.",
    ('Sun', 3): "சூரியன் 3வது வீட்டில் இருப்பது தைரியம், தொடர்பு, மற்றும் சகோதரர் உறவுகளை மேம்படுத்துகிறது. சொந்தக்காரர் தைரியமான, சாகசக்காரரான, மற்றும் எழுத்து அல்லது குறுகிய பயணங்களில் சிறந்தவராக இருக்கலாம்.",
    ('Sun', 4): "சூரியன் 4வது வீட்டில் இருப்பது வலிமையான தாய் செல்வாக்கு, சொத்து உரிமை, மற்றும் உணர்வு நிலைத்தன்மையை குறிக்கிறது. இது ரியல் எஸ்டேட் மற்றும் உள்நாட்டு மகிழ்ச்சியில் வெற்றியை கொண்டுவருகிறது.",
    ('Sun', 5): "சூரியன் 5வது வீட்டில் இருப்பது படைப்பாற்றல், புத்திசாலித்தனம், மற்றும் குழந்தைகளை ஊக்குவிக்கிறது. சொந்தக்காரர் கல்வி, கலைகள், அல்லது ஸ்பெகுலேட்டிவ் திட்டங்களில் தலைமை வகிக்கலாம்.",
    ('Sun', 6): "சூரியன் 6வது வீட்டில் இருப்பது எதிரிகளை வெல்லும் வலிமை, சேவை, மற்றும் ஆரோக்கிய சிக்கல்களை கொடுக்கிறது. இது மருத்துவம், சட்டம், அல்லது போட்டித்தன்மை கொண்ட துறைகளில் தொழில்களுக்கு வழிவகுக்கும்.",
    ('Sun', 7): "சூரியன் 7வது வீட்டில் இருப்பது கூட்டாண்மை மற்றும் திருமணத்தை பாதிக்கிறது. இது ஒரு ஆதிக்கமான துணை அல்லது வணிக கூட்டாண்மை மற்றும் வெளிநாட்டு உறவுகளில் வெற்றியை கொண்டுவரலாம்.",
    ('Sun', 8): "சூரியன் 8வது வீட்டில் இருப்பது மாற்றம், ரகசியங்கள், மற்றும் நீடித்த வாழ்க்கையை கையாளுகிறது. இது ஆக்ட் ஆர்வம், மரபு, அல்லது வாழ்க்கையில் திடீர் மாற்றங்களை குறிக்கலாம்.",
    ('Sun', 9): "சூரியன் 9வது வீட்டில் இருப்பது அதிர்ஷ்டம், மதம், மற்றும் உயர் கல்வியை மேம்படுத்துகிறது. சொந்தக்காரர் வெளிநாட்டுக்கு பயணம் செய்யலாம், ஆன்மீக பாதைகளை பின்பற்றலாம், அல்லது ஒரு ஞானமான தந்தை நபரை கொண்டிருக்கலாம்.",
    ('Sun', 10): "சூரியன் 10வது வீட்டில் இருப்பது தொழில் மற்றும் நற்பெயருக்கு சிறந்தது. இது அரசாங்கம், தலைமை நிலைகள், மற்றும் பொது அங்கீகாரத்தில் வெற்றியை கொண்டுவருகிறது.",
    ('Sun', 11): "சூரியன் 11வது வீட்டில் இருப்பது விருப்பங்களை நிறைவேற்றுகிறது, ஆதாயங்கள், மற்றும் சமூக வலைப்பின்னல்கள். சொந்தக்காரர் இலக்குகளை அடைகிறார், செல்வாக்குமிக்க நண்பர்களை கொண்டிருக்கிறார், மற்றும் மூத்த சகோதரர்களிடமிருந்து ஆதாயங்களை பெறுகிறார்.",
    ('Sun', 12): "சூரியன் 12வது வீட்டில் இருப்பது செலவுகள், ஆன்மீகம், மற்றும் வெளிநாட்டு நாடுகளை குறிக்கிறது. இது தொண்டு வேலை, ஒதுக்கம், அல்லது எகோ காரணமான இழப்புகளுக்கு வழிவகுக்கும்.",
    ('Moon', 1): "சந்திரன் 1வது வீட்டில் இருப்பது சொந்தக்காரரை உணர்வுபூர்வமான, உள்நுணர்வு கொண்ட, மற்றும் உணர்திறன் கொண்டவராக ஆக்குகிறது. இது தோற்றம், ஆரோக்கியம், மற்றும் பொது பிம்பத்தை பாதிக்கிறது, பெரும்பாலும் பிரபலத்தை கொண்டுவருகிறது.",
    ('Moon', 2): "சந்திரன் 2வது வீட்டில் இருப்பது குடும்ப செல்வம், பேச்சு, மற்றும் உணவை பாதிக்கிறது. சொந்தக்காரர் மாறும் நிதிகளை கொண்டிருக்கலாம் மற்றும் வலிமையான குடும்ப பிணைப்புகளை கொண்டிருக்கலாம்.",
    ('Moon', 3): "சந்திரன் 3வது வீட்டில் இருப்பது தொடர்பு, சகோதரர்கள், மற்றும் குறுகிய பயணங்களை மேம்படுத்துகிறது. இது எழுத்தில் படைப்பாற்றலை கொண்டுவருகிறது மற்றும் தகவமைப்பை கொண்டுவருகிறது.",
    ('Moon', 4): "சந்திரன் 4வது வீட்டில் இருப்பது தாய் பிணைப்புகளை வலுப்படுத்துகிறது, வீடு வாழ்க்கை, மற்றும் உணர்வுகள். இது சொத்து ஆதாயங்களை குறிக்கிறது மற்றும் உணர்வு பாதுகாப்பை கொண்டுவருகிறது.",
    ('Moon', 5): "சந்திரன் 5வது வீட்டில் இருப்பது படைப்பாற்றல், குழந்தைகள், மற்றும் காதலை மேம்படுத்துகிறது. சொந்தக்காரர் கலைஞரான, குழந்தைகளிடம் அன்பான, மற்றும் ஸ்பெகுலேட்டிவ் செயல்பாடுகளில் ஆர்வமானவராக இருக்கிறார்.",
    ('Moon', 6): "சந்திரன் 6வது வீட்டில் இருப்பது ஆரோக்கியம், சேவை, மற்றும் தினசரி வழக்கத்தை பாதிக்கிறது. இது வேலை அல்லது ஆரோக்கிய சிக்கல்களிலிருந்து உணர்வு மன அழுத்தத்தை கொண்டுவரலாம்.",
    ('Moon', 7): "சந்திரன் 7வது வீட்டில் இருப்பது திருமணம் மற்றும் கூட்டாண்மையை பாதிக்கிறது. இது உறவுகளில் உணர்வு ஒருமைப்பாட்டை கொண்டுவருகிறது மற்றும் வணிகத்தில் வெற்றியை கொண்டுவருகிறது.",
    ('Moon', 8): "சந்திரன் 8வது வீட்டில் இருப்பது உணர்வு மாற்றங்கள் மற்றும் ரகசியங்களை கையாளுகிறது. இது உள்நுணர்வு திறன்கள் அல்லது திடீர் உணர்வு மாற்றங்களை குறிக்கலாம்.",
    ('Moon', 9): "சந்திரன் 9வது வீட்டில் இருப்பது உள்நுணர்வு, பயணம், மற்றும் ஆன்மீகத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் வெளிநாட்டு இணைப்புகளை கொண்டிருக்கலாம் மற்றும் தத்துவார்த்த ஆர்வங்களை கொண்டிருக்கலாம்.",
    ('Moon', 10): "சந்திரன் 10வது வீட்டில் இருப்பது உணர்வுகள் மூலம் தொழிலை பாதிக்கிறது மற்றும் பொது. இது மாறும் நற்பெயரை கொண்டுவருகிறது மற்றும் பொது சேவை தொழில்களில் வெற்றியை கொண்டுவருகிறது.",
    ('Moon', 11): "சந்திரன் 11வது வீட்டில் இருப்பது உணர்வு விருப்பங்களை நிறைவேற்றுகிறது மற்றும் ஆதாயங்களை கொண்டுவருகிறது. சொந்தக்காரர் ஆதரவான நண்பர்களை கொண்டிருக்கிறார் மற்றும் சமூக வலைப்பின்னல்களிலிருந்து ஆதாயங்களை பெறுகிறார்.",
    ('Moon', 12): "சந்திரன் 12வது வீட்டில் இருப்பது உணர்வு செலவுகள் மற்றும் ஒதுக்கத்தை குறிக்கிறது. இது வெளிநாட்டு குடியிருப்பு அல்லது ஆன்மீக ஒதுக்கங்களுக்கு வழிவகுக்கும்.",
    ('Mars', 1): "செவ்வாய் 1வது வீட்டில் இருப்பது ஆற்றல், தைரியம், மற்றும் உடல் வலிமையை கொடுக்கிறது. சொந்தக்காரர் தைரியமான, போட்டித்தன்மை கொண்ட, மற்றும் காயங்கள் அல்லது குறைகளை கொண்டிருக்கலாம்.",
    ('Mars', 2): "செவ்வாய் 2வது வீட்டில் இருப்பது கடின உழைப்பு மூலம் செல்வத்தை கொண்டுவருகிறது, வலிமையான பேச்சு, மற்றும் குடும்ப மோதல்கள். இது சொத்து கையகப்படுத்தலை குறிக்கிறது.",
    ('Mars', 3): "செவ்வாய் 3வது வீட்டில் இருப்பது தைரியம், சகோதரர்கள், மற்றும் தொடர்பை மேம்படுத்துகிறது. சொந்தக்காரர் சாகசக்காரரான, இளைய சகோதரர்களை கொண்டிருக்கலாம், மற்றும் விளையாட்டுகளில் சிறந்தவராக இருக்கிறார்.",
    ('Mars', 4): "செவ்வாய் 4வது வீட்டில் இருப்பது வீடு மற்றும் சொத்தை பாதிக்கிறது. இது நிலம் மீது மோதல்களை கொண்டுவரலாம் அல்லது வலிமையான தாய் செல்வாக்கை கொண்டுவரலாம்.",
    ('Mars', 5): "செவ்வாய் 5வது வீட்டில் இருப்பது படைப்பாற்றல் மற்றும் குழந்தைகளை ஊக்குவிக்கிறது. சொந்தக்காரர் ஆர்வமான, ஆண் குழந்தைகளை கொண்டிருக்கலாம், மற்றும் போட்டித்தன்மை கொண்ட விளையாட்டுகளில் ஆர்வமானவராக இருக்கிறார்.",
    ('Mars', 6): "செவ்வாய் 6வது வீட்டில் இருப்பது எதிரிகளை வெல்ல மற்றும் ஆரோக்கியத்திற்கு வலிமையானது. இது மருத்துவம், இராணுவம், அல்லது போட்டித்தன்மை கொண்ட துறைகளில் தொழில்களுக்கு வழிவகுக்கிறது.",
    ('Mars', 7): "செவ்வாய் 7வது வீட்டில் இருப்பது திருமணம் மற்றும் கூட்டாண்மையை பாதிக்கிறது. இது ஒரு மாறுபட்ட துணை அல்லது வணிக போட்டித்தன்மையை கொண்டுவரலாம்.",
    ('Mars', 8): "செவ்வாய் 8வது வீட்டில் இருப்பது மாற்றம் மற்றும் ரகசியங்களை கையாளுகிறது. இது அறுவை சிகிச்சை நடைமுறைகள் அல்லது தீவிர அனுபவங்களை குறிக்கலாம்.",
    ('Mars', 9): "செவ்வாய் 9வது வீட்டில் இருப்பது மதம் மற்றும் பயணத்தில் தைரியத்தை மேம்படுத்துகிறது. சொந்தக்காரர் ஆன்மீக பயணங்களில் சாகசக்காரராக இருக்கலாம்.",
    ('Mars', 10): "செவ்வாய் 10வது வீட்டில் இருப்பது கடின உழைப்பு மூலம் தொழில் வெற்றியை கொண்டுவருகிறது. இது இராணுவம், பொறியியல், அல்லது அரசியலில் தலைமையை குறிக்கிறது.",
    ('Mars', 11): "செவ்வாய் 11வது வீட்டில் இருப்பது விருப்பங்களை நிறைவேற்றுகிறது மற்றும் ஆதாயங்களை கொண்டுவருகிறது. சொந்தக்காரர் முயற்சி மூலம் இலக்குகளை அடைகிறார் மற்றும் தைரியமான நண்பர்களை கொண்டிருக்கிறார்.",
    ('Mars', 12): "செவ்வாய் 12வது வீட்டில் இருப்பது செலவுகள் மற்றும் வெளிநாட்டு நாடுகளை குறிக்கிறது. இது ஒதுக்கம் அல்லது எதிரிகளிடமிருந்து இழப்புகளுக்கு வழிவகுக்கும்.",
    ('Mercury', 1): "புதன் 1வது வீட்டில் இருப்பது சொந்தக்காரரை புத்திசாலி மற்றும் தொடர்பு கொண்டவராக ஆக்குகிறது. இது தோற்றத்தை பாதிக்கிறது மற்றும் நகைச்சுவை, தகவமைப்பை கொண்டுவருகிறது.",
    ('Mercury', 2): "புதன் 2வது வீட்டில் இருப்பது வணிகம், பேச்சு, மற்றும் கல்வி மூலம் செல்வத்தை பாதிக்கிறது. சொந்தக்காரர் பேச்சுவார்த்தைகளில் நல்லவராக இருக்கிறார்.",
    ('Mercury', 3): "புதன் 3வது வீட்டில் இருப்பது தொடர்பு மற்றும் சகோதரர்களை மேம்படுத்துகிறது. இது எழுத்து, கற்பித்தல், மற்றும் குறுகிய பயணங்களில் திறன்களை கொண்டுவருகிறது.",
    ('Mercury', 4): "புதன் 4வது வீட்டில் இருப்பது கல்வி மற்றும் வீட்டை பாதிக்கிறது. சொந்தக்காரர் பல சொத்துகளை கொண்டிருக்கலாம் அல்லது கற்றலில் ஆர்வங்களை கொண்டிருக்கலாம்.",
    ('Mercury', 5): "புதன் 5வது வீட்டில் இருப்பது புத்திசாலித்தனம் மற்றும் படைப்பாற்றலை மேம்படுத்துகிறது. இது கல்வி, கலைகள், மற்றும் ஸ்பெகுலேஷனில் வெற்றியை குறிக்கிறது.",
    ('Mercury', 6): "புதன் 6வது வீட்டில் இருப்பது சேவை மற்றும் ஆரோக்கியத்தில் உதவுகிறது. சொந்தக்காரர் ஆரோக்கிய சிகிச்சை, சட்டம், அல்லது தினசரி வழக்கங்களில் வேலை செய்யலாம்.",
    ('Mercury', 7): "புதன் 7வது வீட்டில் இருப்பது கூட்டாண்மையை பாதிக்கிறது. இது வணிக அறிவை கொண்டுவருகிறது மற்றும் ஒருமைப்பாட்டான உறவுகளை கொண்டுவருகிறது.",
    ('Mercury', 8): "புதன் 8வது வீட்டில் இருப்பது ரகசியங்கள் மற்றும் ஆராய்ச்சியை கையாளுகிறது. இது ஆக்ட் அல்லது விசாரணை வேலைக்கு ஆர்வத்தை குறிக்கலாம்.",
    ('Mercury', 9): "புதன் 9வது வீட்டில் இருப்பது உயர் கல்வி மற்றும் பயணத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் தத்துவார்த்தமான மற்றும் கற்பிக்க அல்லது எழுதலாம்.",
    ('Mercury', 10): "புதன் 10வது வீட்டில் இருப்பது தொடர்பு துறையில் தொழிலை கொண்டுவருகிறது. இது வணிகம், எழுத்து, அல்லது பொது பேச்சில் வெற்றியை குறிக்கிறது.",
    ('Mercury', 11): "புதன் 11வது வீட்டில் இருப்பது புத்திசாலி விருப்பங்களை நிறைவேற்றுகிறது. சொந்தக்காரர் வலைப்பின்னல்களிலிருந்து ஆதாயங்களை பெறுகிறார் மற்றும் தொடர்பு கொண்ட நண்பர்களை கொண்டிருக்கிறார்.",
    ('Mercury', 12): "புதன் 12வது வீட்டில் இருப்பது கல்வியில் செலவுகளை குறிக்கிறது. இது வெளிநாட்டு கல்வி அல்லது ஆன்மீக தொடர்புக்கு வழிவகுக்கும்.",
    ('Jupiter', 1): "குரு 1வது வீட்டில் இருப்பது ஞானம் மற்றும் ஆப்டிமிஸத்தை கொடுக்கிறது. சொந்தக்காரர் தாராளமான, ஆரோக்கியமான, மற்றும் நேர்மறையான பார்வை கொண்டவராக இருக்கிறார்.",
    ('Jupiter', 2): "குரு 2வது வீட்டில் இருப்பது செல்வம் மற்றும் குடும்ப வளர்ச்சியை கொண்டுவருகிறது. இது குடும்பத்திலிருந்து ஆதாயங்களை குறிக்கிறது மற்றும் வலிமையான மதிப்புகளை கொண்டுவருகிறது.",
    ('Jupiter', 3): "குரு 3வது வீட்டில் இருப்பது அறிவை மேம்படுத்துகிறது மற்றும் சகோதரர்களை கொண்டுவருகிறது. சொந்தக்காரர் கற்றவரான, சகோதரர்களுடன் நல்ல உறவுகளை கொண்டிருக்கிறார்.",
    ('Jupiter', 4): "குரு 4வது வீட்டில் இருப்பது வீடு மற்றும் கல்வியை வலுப்படுத்துகிறது. இது சொத்து மற்றும் உணர்வு மகிழ்ச்சியை கொண்டுவருகிறது.",
    ('Jupiter', 5): "குரு 5வது வீட்டில் இருப்பது குழந்தைகள் மற்றும் ஞானத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் படைப்பாற்றலான, நல்ல குழந்தைகளை கொண்டிருக்கிறார், மற்றும் கற்பித்தலில் ஆர்வமானவராக இருக்கிறார்.",
    ('Jupiter', 6): "குரு 6வது வீட்டில் இருப்பது தடைகளை வெல்ல உதவுகிறது. இது மற்றவர்களுக்கு சேவை செய்தல் மற்றும் ஆரோக்கிய மீட்சியை குறிக்கிறது.",
    ('Jupiter', 7): "குரு 7வது வீட்டில் இருப்பது நல்ல கூட்டாண்மையை கொண்டுவருகிறது. சொந்தக்காரர் ஒரு ஞானமான துணை மற்றும் வெற்றிகரமான வணிகத்தை கொண்டிருக்கிறார்.",
    ('Jupiter', 8): "குரு 8வது வீட்டில் இருப்பது மாற்றம் மற்றும் செல்வத்தை கையாளுகிறது. இது மரபு அல்லது ஆன்மீக வளர்ச்சியை குறிக்கலாம்.",
    ('Jupiter', 9): "குரு 9வது வீட்டில் இருப்பது அதிர்ஷ்டம் மற்றும் மதத்திற்கு சிறந்தது. சொந்தக்காரர் அதிர்ஷ்டசாலி, பயணம் செய்கிறார், மற்றும் தர்மத்தை பின்பற்றுகிறார்.",
    ('Jupiter', 10): "குரு 10வது வீட்டில் இருப்பது தொழில் வெற்றியை கொண்டுவருகிறது. இது கற்பித்தல், சட்டம், அல்லது மதத்தில் தலைமையை குறிக்கிறது.",
    ('Jupiter', 11): "குரு 11வது வீட்டில் இருப்பது விருப்பங்களை நிறைவேற்றுகிறது மற்றும் ஆதாயங்களை கொண்டுவருகிறது. சொந்தக்காரர் ஞானமான நண்பர்களை கொண்டிருக்கிறார் மற்றும் இலக்குகளை அடைகிறார்.",
    ('Jupiter', 12): "குரு 12வது வீட்டில் இருப்பது ஆன்மீக செலவுகளை குறிக்கிறது. இது வெளிநாட்டு தொண்டு அல்லது விடுவிப்புக்கு வழிவகுக்கும்.",
    ('Venus', 1): "சுக்கிரன் 1வது வீட்டில் இருப்பது அழகு மற்றும் கவர்ச்சியை கொடுக்கிறது. சொந்தக்காரர் கவர்ச்சியான, கலைஞரான, மற்றும் சொகுசில் ஆர்வமானவராக இருக்கிறார்.",
    ('Venus', 2): "சுக்கிரன் 2வது வீட்டில் இருப்பது கலைகள், குடும்பம், மற்றும் பேச்சு மூலம் செல்வத்தை கொண்டுவருகிறது. இது சொகுசு மற்றும் நல்ல உணவை குறிக்கிறது.",
    ('Venus', 3): "சுக்கிரன் 3வது வீட்டில் இருப்பது படைப்பாற்றல் மற்றும் தொடர்பை மேம்படுத்துகிறது. சொந்தக்காரர் கலைஞரான மற்றும் ஒருமைப்பாட்டான சகோதரர்களை கொண்டிருக்கிறார்.",
    ('Venus', 4): "சுக்கிரன் 4வது வீட்டில் இருப்பது வசதி மற்றும் வீட்டை பாதிக்கிறது. இது அழகான வீடு மற்றும் உணர்வு இன்பத்தை கொண்டுவருகிறது.",
    ('Venus', 5): "சுக்கிரன் 5வது வீட்டில் இருப்பது காதல் மற்றும் கலைகளை ஊக்குவிக்கிறது. சொந்தக்காரர் காதலான, படைப்பாற்றலான, மற்றும் பொழுதுபோக்கில் ஆர்வமானவராக இருக்கிறார்.",
    ('Venus', 6): "சுக்கிரன் 6வது வீட்டில் இருப்பது சேவை மற்றும் ஆரோக்கியத்தில் உதவுகிறது. இது கலைஞரான தொழில்கள் அல்லது உணவு மூலம் ஆரோக்கியத்தை குறிக்கலாம்.",
    ('Venus', 7): "சுக்கிரன் 7வது வீட்டில் இருப்பது ஒருமைப்பாட்டான திருமணத்தை கொண்டுவருகிறது. சொந்தக்காரர் ஒரு அன்பான துணை மற்றும் வணிக வெற்றியை கொண்டிருக்கிறார்.",
    ('Venus', 8): "சுக்கிரன் 8வது வீட்டில் இருப்பது சொகுசு மற்றும் ரகசியங்களை கையாளுகிறது. இது கூட்டாண்மையிலிருந்து ஆதாயங்கள் அல்லது ஆக்ட் ஆர்வத்தை குறிக்கலாம்.",
    ('Venus', 9): "சுக்கிரன் 9வது வீட்டில் இருப்பது மதத்தில் அழகை ஊக்குவிக்கிறது. சொந்தக்காரர் இன்பத்திற்கு பயணம் செய்கிறார் மற்றும் கலைஞரான ஆர்வங்களை கொண்டிருக்கிறார்.",
    ('Venus', 10): "சுக்கிரன் 10வது வீட்டில் இருப்பது கலைகளில் தொழிலை கொண்டுவருகிறது. இது பொழுதுபோக்கு, ஃபேஷன், அல்லது பொதுவில் வெற்றியை குறிக்கிறது.",
    ('Venus', 11): "சுக்கிரன் 11வது வீட்டில் இருப்பது சொகுசு விருப்பங்களை நிறைவேற்றுகிறது. சொந்தக்காரர் நண்பர்களிலிருந்து ஆதாயங்களை பெறுகிறார் மற்றும் சமூக வலைப்பின்னல்களை கொண்டிருக்கிறார்.",
    ('Venus', 12): "சுக்கிரன் 12வது வீட்டில் இருப்பது சொகுசில் செலவுகளை குறிக்கிறது. இது வெளிநாட்டு காதல் அல்லது ஆன்மீக அழகுக்கு வழிவகுக்கும்.",
    ('Saturn', 1): "சனி 1வது வீட்டில் இருப்பது ஒழுக்கம் மற்றும் நீடித்த வாழ்க்கையை கொடுக்கிறது. சொந்தக்காரர் தீவிரமான, கடின உழைப்பு கொண்ட, மற்றும் தாமதமான வெற்றியை கொண்டிருக்கலாம்.",
    ('Saturn', 2): "சனி 2வது வீட்டில் இருப்பது மெதுவான செல்வம் சேர்ப்பை கொண்டுவருகிறது. இது குடும்ப பொறுப்புகள் மற்றும் பேச்சு தாமதங்களை குறிக்கிறது.",
    ('Saturn', 3): "சனி 3வது வீட்டில் இருப்பது சகோதரர்கள் மற்றும் தொடர்பை பாதிக்கிறது. சொந்தக்காரர் எச்சரிக்கையான மற்றும் சகோதரர் சிக்கல்களை கொண்டிருக்கலாம்.",
    ('Saturn', 4): "சனி 4வது வீட்டில் இருப்பது வீடு மற்றும் தாயை பாதிக்கிறது. இது சொத்து தாமதங்கள் அல்லது உணர்வு கட்டுப்பாட்டை கொண்டுவரலாம்.",
    ('Saturn', 5): "சனி 5வது வீட்டில் இருப்பது குழந்தைகள் மற்றும் படைப்பாற்றலை பாதிக்கிறது. இது தாமதமான குழந்தைகள் அல்லது ஒழுக்கமான கலைகளை குறிக்கிறது.",
    ('Saturn', 6): "சனி 6வது வீட்டில் இருப்பது சேவை மற்றும் ஆரோக்கியத்தில் உதவுகிறது. சொந்தக்காரர் கடின உழைப்பு மூலம் எதிரிகளை வெல்கிறார்.",
    ('Saturn', 7): "சனி 7வது வீட்டில் இருப்பது தீவிரமான கூட்டாண்மையை கொண்டுவருகிறது. இது தாமதமான திருமணம் அல்லது வணிக ஒழுக்கத்தை குறிக்கலாம்.",
    ('Saturn', 8): "சனி 8வது வீட்டில் இருப்பது நீடித்த வாழ்க்கை மற்றும் ரகசியங்களை கையாளுகிறது. இது நீண்ட வாழ்க்கை அல்லது கர்மிக் மாற்றங்களை குறிக்கலாம்.",
    ('Saturn', 9): "சனி 9வது வீட்டில் இருப்பது ஒழுக்கமான மதத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் தத்துவார்த்தமான மற்றும் வெளிநாட்டு கடினங்களை கொண்டிருக்கலாம்.",
    ('Saturn', 10): "சனி 10வது வீட்டில் இருப்பது கடின உழைப்பு மூலம் தொழிலை கொண்டுவருகிறது. இது அரசாங்கம் அல்லது கட்டமைக்கப்பட்ட துறைகளில் வெற்றியை குறிக்கிறது.",
    ('Saturn', 11): "சனி 11வது வீட்டில் இருப்பது விருப்பங்களை மெதுவாக நிறைவேற்றுகிறது. சொந்தக்காரர் நிலைத்தன்மை கொண்ட நண்பர்களை கொண்டிருக்கிறார் மற்றும் முயற்சி மூலம் இலக்குகளை அடைகிறார்.",
    ('Saturn', 12): "சனி 12வது வீட்டில் இருப்பது ஒதுக்கம் மற்றும் செலவுகளை குறிக்கிறது. இது ஆன்மீக ஒழுக்கம் அல்லது வெளிநாட்டு இழப்புகளுக்கு வழிவகுக்கும்.",
    ('Rahu', 1): "ராகு 1வது வீட்டில் இருப்பது ஆசை மற்றும் வெளிநாட்டு செல்வாக்கை கொண்டுவருகிறது. சொந்தக்காரர் ஆர்வமான மற்றும் வழக்கமற்ற தோற்றத்தை கொண்டிருக்கலாம்.",
    ('Rahu', 2): "ராகு 2வது வீட்டில் இருப்பது செல்வத்தை திடீரென பாதிக்கிறது. இது வெளிநாட்டு அல்லது வழக்கமற்ற மூலங்களிலிருந்து ஆதாயங்களை குறிக்கிறது.",
    ('Rahu', 3): "ராகு 3வது வீட்டில் இருப்பது தொடர்பு மற்றும் பயணத்தை மேம்படுத்துகிறது. சொந்தக்காரர் சாகசக்காரரான மற்றும் சகோதரர் சிக்கல்களை கொண்டிருக்கலாம்.",
    ('Rahu', 4): "ராகு 4வது வீட்டில் இருப்பது வீடு மற்றும் உணர்வுகளை பாதிக்கிறது. இது வெளிநாட்டு சொத்து அல்லது உணர்வு நிலைத்தன்மையின்மையை கொண்டுவரலாம்.",
    ('Rahu', 5): "ராகு 5வது வீட்டில் இருப்பது படைப்பாற்றல் மற்றும் ஸ்பெகுலேஷனை ஊக்குவிக்கிறது. சொந்தக்காரர் புதுமையான மற்றும் ஆபத்தான திட்டங்களை கொண்டிருக்கலாம்.",
    ('Rahu', 6): "ராகு 6வது வீட்டில் இருப்பது எதிரிகளை வெல்ல உதவுகிறது. இது வெளிநாட்டு சேவை அல்லது ஆரோக்கிய சிக்கல்களில் வெற்றியை குறிக்கிறது.",
    ('Rahu', 7): "ராகு 7வது வீட்டில் இருப்பது கூட்டாண்மையை பாதிக்கிறது. இது வெளிநாட்டு துணை அல்லது வணிக மாயைகளை கொண்டுவரலாம்.",
    ('Rahu', 8): "ராகு 8வது வீட்டில் இருப்பது ரகசியங்கள் மற்றும் மாற்றத்தை கையாளுகிறது. இது ஆக்ட் ஆர்வம் அல்லது திடீர் மாற்றங்களை குறிக்கலாம்.",
    ('Rahu', 9): "ராகு 9வது வீட்டில் இருப்பது வெளிநாட்டு பயணம் மற்றும் மதத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் வழக்கமற்ற நம்பிக்கைகளை பின்பற்றலாம்.",
    ('Rahu', 10): "ராகு 10வது வீட்டில் இருப்பது தொழில்நுட்பத்தில் தொழிலை கொண்டுவருகிறது. இது வெளிநாட்டு அல்லது புதுமையான துறைகளில் வெற்றியை குறிக்கிறது.",
    ('Rahu', 11): "ராகு 11வது வீட்டில் இருப்பது விருப்பங்களை வழக்கமற்ற முறையில் நிறைவேற்றுகிறது. சொந்தக்காரர் வலைப்பின்னல்களிலிருந்து ஆதாயங்களை பெறுகிறார் ஆனால் மாயைகளை கொண்டிருக்கலாம்.",
    ('Rahu', 12): "ராகு 12வது வீட்டில் இருப்பது வெளிநாட்டு செலவுகளை குறிக்கிறது. இது ஒதுக்கம் அல்லது ஆன்மீக மாயைகளுக்கு வழிவகுக்கும்.",
    ('Ketu', 1): "கேது 1வது வீட்டில் இருப்பது விலகல் மற்றும் ஆன்மீகத்தை கொண்டுவருகிறது. சொந்தக்காரர் உள்முகமான மற்றும் ஆரோக்கிய சிக்கல்களை கொண்டிருக்கலாம்.",
    ('Ketu', 2): "கேது 2வது வீட்டில் இருப்பது குடும்ப செல்வத்தை பாதிக்கிறது. இது பொருள் உரிமைகளிலிருந்து விலகலை குறிக்கிறது.",
    ('Ketu', 3): "கேது 3வது வீட்டில் இருப்பது சகோதரர்கள் மற்றும் தொடர்பை பாதிக்கிறது. சொந்தக்காரர் உலகியல் பயணங்களிலிருந்து விலகியவராக இருக்கிறார்.",
    ('Ketu', 4): "கேது 4வது வீட்டில் இருப்பது வீடு மற்றும் உணர்வுகளை பாதிக்கிறது. இது குடும்பம் அல்லது சொத்திலிருந்து விலகலை கொண்டுவரலாம்.",
    ('Ketu', 5): "கேது 5வது வீட்டில் இருப்பது ஆன்மீக படைப்பாற்றலை ஊக்குவிக்கிறது. சொந்தக்காரர் குழந்தைகள் அல்லது கலைகளிலிருந்து விலகியவராக இருக்கிறார்.",
    ('Ketu', 6): "கேது 6வது வீட்டில் இருப்பது சேவையில் உதவுகிறது. இது எதிரிகள் மற்றும் ஆரோக்கிய வழக்கங்களிலிருந்து விலகலை குறிக்கிறது.",
    ('Ketu', 7): "கேது 7வது வீட்டில் இருப்பது கூட்டாண்மையை பாதிக்கிறது. இது திருமணம் அல்லது வணிகத்தில் விலகலை கொண்டுவரலாம்.",
    ('Ketu', 8): "கேது 8வது வீட்டில் இருப்பது விடுவிப்பை கையாளுகிறது. இது ஆக்ட் அல்லது முந்தைய வாழ்க்கை கர்மாவுக்கு ஆர்வத்தை குறிக்கலாம்.",
    ('Ketu', 9): "கேது 9வது வீட்டில் இருப்பது ஆன்மீக பயணத்தை ஊக்குவிக்கிறது. சொந்தக்காரர் மதம் அல்லது வெளிநாட்டு நாடுகளிலிருந்து விலகியவராக இருக்கிறார்.",
    ('Ketu', 10): "கேது 10வது வீட்டில் இருப்பது தொழில் விலகலை கொண்டுவருகிறது. இது ஆன்மீக அல்லது வழக்கமற்ற துறைகளில் வெற்றியை குறிக்கிறது.",
    ('Ketu', 11): "கேது 11வது வீட்டில் இருப்பது ஆன்மீக விருப்பங்களை நிறைவேற்றுகிறது. சொந்தக்காரர் ஆதாயங்கள் மற்றும் நண்பர்களிலிருந்து விலகியவராக இருக்கிறார்.",
    ('Ketu', 12): "கேது 12வது வீட்டில் இருப்பது விடுவிப்பை குறிக்கிறது. இது ஆன்மீக ஒதுக்கம் அல்லது வெளிநாட்டு விலகலுக்கு வழிவகுக்கும்.",
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


def _house_num(lagna_rasi: int, sign: int) -> int:
    """Return the house number for a given sign, counting clockwise from lagna."""
    return ((sign - lagna_rasi) % 12) + 1


def generate_birth_chart_svg(chart: Dict, language: str = 'en', size: int = 420) -> str:
    if language == 'ta':
        planet_house_meanings = PLANET_HOUSE_MEANINGS_TA
        planet_info = PLANET_INFO_TA
    else:
        planet_house_meanings = PLANET_HOUSE_MEANINGS
        planet_info = PLANET_INFO
    cell = size // 4
    pad  = 6
    svg  = []

    lagna_rasi = chart.get('lagna', {}).get('number', 1)

    # Build sign → list of planets
    sign_planets: Dict[int, List[str]] = {s: [] for s in range(1, 13)}
    sign_planets[lagna_rasi].append('Lagna')

    # Planet → sign number from chart dict
    
    sign_planets[chart.get('sun',{}).get('rasi',0)].append('Sun') if chart.get('sun',{}).get('rasi',0) else None
    sign_planets[chart.get('moon',{}).get('rasi',0)].append('Moon') if chart.get('moon',{}).get('rasi',0) else None
    sign_planets[chart.get('mars',{}).get('rasi',0)].append('Mars') if chart.get('mars',{}).get('rasi',0) else None
    sign_planets[chart.get('mercury',{}).get('rasi',0)].append('Mercury') if chart.get('mercury',{}).get('rasi',0) else None
    sign_planets[chart.get('jupiter',{}).get('rasi',0)].append('Jupiter') if chart.get('jupiter',{}).get('rasi',0) else None
    sign_planets[chart.get('venus',{}).get('rasi',0)].append('Venus') if chart.get('venus',{}).get('rasi',0) else None
    sign_planets[chart.get('saturn',{}).get('rasi',0)].append('Saturn') if chart.get('saturn',{}).get('rasi',0) else None
    sign_planets[chart.get('rahu',{}).get('rasi',0)].append('Rahu') if chart.get('rahu',{}).get('rasi',0) else None
    sign_planets[chart.get('ketu',{}).get('rasi',0)].append('Ketu') if chart.get('ketu',{}).get('rasi',0) else None

    # Remove 0 entries
    sign_planets.pop(0, None)

    fs = int(cell * 0.16)  # font size

    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 {size} {size}" width="{size}" height="{size}"
      style="font-family:sans-serif;cursor:pointer" id="birthChartSvg">
  <defs><style>
    .hc{{fill:rgba(255,255,255,.04);stroke:rgba(255,215,0,.35);stroke-width:1.5;transition:fill .2s}}
    .hc:hover{{fill:rgba(255,215,0,.10)}}
    .hn{{fill:rgba(255,215,0,.45);font-size:{int(fs*.85)}px}}
    .rn{{fill:rgba(255,255,255,.55);font-size:{int(fs*.9)}px}}
    .pt{{font-size:{fs}px;font-weight:700}}
    .cb{{fill:rgba(0,0,0,.35);stroke:rgba(255,215,0,.2);stroke-width:1}}
    .ct{{fill:#FFD700;font-size:{int(fs*1.1)}px;font-weight:700;text-anchor:middle}}
    .cs{{fill:rgba(255,255,255,.45);font-size:{int(fs*.8)}px;text-anchor:middle}}
  </style></defs>''')

    for sign_num, (col, row) in SIGN_POSITIONS.items():
        x = col * cell
        y = row * cell
        house = _house_num(lagna_rasi, sign_num)
        planets = [p for p in sign_planets.get(sign_num, []) if p]
        is_lagna = (sign_num == lagna_rasi)
        hmean = HOUSE_MEANINGS[house].replace("'","\\'")
        rasi_name = RASI_TA[sign_num] if language == 'ta' else RASI_EN[sign_num]
        planet_str = ', '.join(p for p in planets if p != 'Lagna') or 'Empty'
        planet_meanings = '; '.join(f"{p}: {planet_house_meanings.get((p, house), planet_info.get(p, ''))}" for p in planets if p != 'Lagna') or 'No planets in this house.'
        onclick = f"showHouseInfo({house},'{rasi_name}',{house},'{planet_str}','{planet_meanings}')"

        svg.append(f'  <g onclick="{onclick}">')
        # Cell background
        lagna_stroke = 'rgba(0,255,204,.6)' if is_lagna else 'rgba(255,215,0,.35)'
        lagna_fill   = 'rgba(0,255,204,.06)' if is_lagna else 'rgba(255,255,255,.04)'
        svg.append(f'    <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" class="hc" style="fill:{lagna_fill};stroke:{lagna_stroke}"/>')

        # Lagna diagonal lines
        if is_lagna:
            svg.append(f'    <line x1="{x}" y1="{y}" x2="{x+cell}" y2="{y+cell}" stroke="rgba(0,255,204,.4)" stroke-width="1"/>')
            svg.append(f'    <line x1="{x+cell}" y1="{y}" x2="{x}" y2="{y+cell}" stroke="rgba(0,255,204,.4)" stroke-width="1"/>')

        # House number (small, top-left)
        svg.append(f'    <text x="{x+4}" y="{y+int(fs*1.1)}" class="hn">{house}</text>')

        # Rasi name (small, bottom-center)
        svg.append(f'    <text x="{x+cell//2}" y="{y+cell-5}" class="rn" text-anchor="middle">{RASI_TA[sign_num]}</text>')

        # Planets
        non_lagna = [p for p in planets if p != 'Lagna']
        for i, planet in enumerate(non_lagna[:4]):
            px = x + pad + (i % 2) * (cell // 2 - pad + 2)
            py = y + int(cell * 0.35) + (i // 2) * int(cell * 0.26)
            color = PLANET_COL.get(planet, '#FFF')
            sym   = PLANET_SYM.get(planet, planet[:2])
            svg.append(f'    <text x="{px}" y="{py}" class="pt" fill="{color}">{sym}</text>')

        # Show "Lg" label if lagna
        if is_lagna:
            svg.append(f'    <text x="{x+cell-4}" y="{y+int(fs*1.1)}" class="hn" text-anchor="end" style="fill:rgba(0,255,204,.8)">Lg</text>')

        svg.append('  </g>')

    # Center 2x2 box
    cx, cy = cell, cell
    svg.append(f'''  <rect x="{cx}" y="{cy}" width="{cell*2}" height="{cell*2}" class="cb" rx="4"/>
  <text x="{cx+cell}" y="{cy+int(cell*.42)}" class="ct">🪐</text>
  <text x="{cx+cell}" y="{cy+int(cell*.62)}" class="ct">AstroGuy</text>
  <text x="{cx+cell}" y="{cy+int(cell*.78)}" class="cs">Vedic Birth Chart</text>
  <text x="{cx+cell}" y="{cy+int(cell*.93)}" class="cs">{RASI_EN.get(lagna_rasi,'')} Lagna</text>
  <text x="{cx+cell}" y="{cy+int(cell*1.07)}" class="cs" style="fill:rgba(0,255,204,.6)">Houses count clockwise ↻</text>''')

    svg.append('</svg>')
    return '\n'.join(svg)


def get_planet_house_data(chart: Dict) -> List[Dict]:
    """Return planets with house positions for sidebar display."""
    lagna_rasi = chart.get('lagna', {}).get('number', 1)
    result = []
    planet_sign_map = {
        'Sun':     chart.get('sun',{}).get('rasi',0),
        'Moon':    chart.get('moon',{}).get('rasi',0),
        'Mars':    chart.get('mars',{}).get('rasi',0),
        'Mercury': chart.get('mercury',{}).get('rasi',0),
        'Jupiter': chart.get('jupiter',{}).get('rasi',0),
        'Venus':   chart.get('venus',{}).get('rasi',0),
        'Saturn':  chart.get('saturn',{}).get('rasi',0),
        'Rahu':    chart.get('rahu',{}).get('rasi',0),
        'Ketu':    chart.get('ketu',{}).get('rasi',0),
        'Lagna':   lagna_rasi,
    }
    for planet, sign in planet_sign_map.items():
        if not sign: continue
        house = _house_num(lagna_rasi, sign)
        result.append({
            'name':   planet,
            'symbol': PLANET_SYM.get(planet, planet[:2]),
            'color':  PLANET_COL.get(planet, '#FFF'),
            'sign':   RASI_EN.get(sign, ''),
            'sign_ta':RASI_TA.get(sign, ''),
            'house':  house,
            'info':   PLANET_INFO.get(planet, ''),
        })
    return result
