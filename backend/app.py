from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from urllib.parse import quote
import math

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

TERM_NAMES = {
    "en": {
        "alluvial": "alluvial",
        "black": "black",
        "red": "red / laterite",
        "loamy": "loamy",
        "clay": "clay",
        "sandy": "sandy",
        "kharif": "Kharif",
        "rabi": "Rabi",
        "zaid": "Zaid",
        "annual": "annual",
        "monsoon": "monsoon",
        "winter": "winter",
        "high": "high",
        "medium": "medium",
        "low": "low",
    },
    "kn": {
        "alluvial": "ಮೆಕ್ಕಲು",
        "black": "ಕಪ್ಪು",
        "red": "ಕೆಂಪು / ಲ್ಯಾಟರೈಟ್",
        "loamy": "ಗೋಡು",
        "clay": "ಜೇಡಿ",
        "sandy": "ಮರಳು",
        "kharif": "ಮುಂಗಾರು (ಖಾರಿಫ್)",
        "rabi": "ಹಿಂಗಾರು (ರಬಿ)",
        "zaid": "ಬೇಸಿಗೆ (ಜೈದ್)",
        "annual": "ವಾರ್ಷಿಕ",
        "monsoon": "ಮಳೆಗಾಲ",
        "winter": "ಚಳಿಗಾಲ",
        "high": "ಹೆಚ್ಚಿನ",
        "medium": "ಮಧ್ಯಮ",
        "low": "ಕಡಿಮೆ",
    },
    "hi": {
        "alluvial": "जलोढ़",
        "black": "काली",
        "red": "लाल / लेटराइट",
        "loamy": "दोमट",
        "clay": "चिकनी",
        "sandy": "बलुई",
        "kharif": "खरीफ",
        "rabi": "रबी",
        "zaid": "जायद",
        "annual": "वार्षिक",
        "monsoon": "मानसून",
        "winter": "सर्दी",
        "high": "अधिक",
        "medium": "मध्यम",
        "low": "कम",
    },
    "ta": {
        "alluvial": "வண்டல்",
        "black": "கரிசல்",
        "red": "செம்மண்",
        "loamy": "களிமண் கலந்த",
        "clay": "களிமண்",
        "sandy": "மணல்",
        "kharif": "கரீஃப்",
        "rabi": "ரபி",
        "zaid": "சையத்",
        "annual": "ஆண்டு முழுவதும்",
        "monsoon": "மழைக்காலம்",
        "winter": "குளிர்காலம்",
        "high": "அதிக",
        "medium": "நடுத்தர",
        "low": "குறைந்த",
    },
    "te": {
        "alluvial": "ఒండ్రు",
        "black": "నల్ల రేగడి",
        "red": "ఎర్ర / లాటరైట్",
        "loamy": "లోమీ",
        "clay": "బంకమట్టి",
        "sandy": "ఇసుక",
        "kharif": "ఖరీఫ్",
        "rabi": "రబీ",
        "zaid": "జైద్",
        "annual": "వార్షిక",
        "monsoon": "వర్షాకాలం",
        "winter": "చలికాలం",
        "high": "ఎక్కువ",
        "medium": "మధ్యస్థ",
        "low": "తక్కువ",
    },
}

UI_TEXT = {
    "en": {
        "soil_ok": "Ideal {soil} soil",
        "soil_sec": "Compatible {soil} soil",
        "soil_bad": "{soil} soil is less suitable",
        "season_ok": "prime {season} season",
        "season_sec": "viable {season} season",
        "season_bad": "{season} season is off-peak",
        "water_ok": "matching {water} water availability",
        "water_sec": "manageable {water} water availability",
        "water_bad": "{water} water level poses stress",
        "rain_ok": "rainfall ({rain} mm) fits ideal range ({min_r}-{max_r} mm)",
        "rain_bad": "rainfall ({rain} mm) is outside ideal range ({min_r}-{max_r} mm)",
        "temp_ok": "temperature ({temp}°C) is optimal ({min_t}-{max_t}°C)",
        "temp_bad": "temperature ({temp}°C) is outside ideal range ({min_t}-{max_t}°C)",
        "ph_ok": "soil pH ({ph}) is suitable ({min_p}-{max_p})",
        "ph_bad": "soil pH ({ph}) is outside ideal range ({min_p}-{max_p})",
        "note": "Note: ",
        "high": "Highly Recommended",
        "med": "Moderately Suitable (Requires Care)",
        "low": "Not Recommended / High Risk",
    },
    "kn": {
        "soil_ok": "ಸೂಕ್ತವಾದ {soil} ಮಣ್ಣು",
        "soil_sec": "ಹೊಂದಿಕೊಳ್ಳುವ {soil} ಮಣ್ಣು",
        "soil_bad": "{soil} ಮಣ್ಣು ಕಡಿಮೆ ಸೂಕ್ತವಾಗಿದೆ",
        "season_ok": "ಪ್ರಮುಖ {season} ಋತು",
        "season_sec": "ಪರ್ಯಾಯ {season} ಋತು",
        "season_bad": "{season} ಋತು ಸೂಕ್ತವಲ್ಲ",
        "water_ok": "ಸರಿಹೊಂದುವ {water} ನೀರಿನ ಲಭ್ಯತೆ",
        "water_sec": "ನಿರ್ವಹಿಸಬಹುದಾದ {water} ನೀರಿನ ಲಭ್ಯತೆ",
        "water_bad": "{water} ನೀರಿನ ಮಟ್ಟ ಅಪಾಯಕಾರಿ",
        "rain_ok": "ಮಳೆ ({rain} mm) ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಲ್ಲಿದೆ ({min_r}-{max_r} mm)",
        "rain_bad": "ಮಳೆ ({rain} mm) ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಿಂದ ({min_r}-{max_r} mm) ಹೊರಗಿದೆ",
        "temp_ok": "ತಾಪಮಾನ ({temp}°C) ಸೂಕ್ತವಾಗಿದೆ ({min_t}-{max_t}°C)",
        "temp_bad": "ತಾಪಮಾನ ({temp}°C) ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಿಂದ ({min_t}-{max_t}°C) ಹೊರಗಿದೆ",
        "ph_ok": "ಮಣ್ಣಿನ pH ({ph}) ಸೂಕ್ತವಾಗಿದೆ ({min_p}-{max_p})",
        "ph_bad": "ಮಣ್ಣಿನ pH ({ph}) ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಿಂದ ({min_p}-{max_p}) ಹೊರಗಿದೆ",
        "note": "ಗಮನಿಸಿ: ",
        "high": "ಅತ್ಯಂತ ಸೂಕ್ತವಾಗಿದೆ",
        "med": "ಮಧ್ಯಮ ಸೂಕ್ತ (ಹೆಚ್ಚಿನ ಕಾಳಜಿ ಅಗತ್ಯ)",
        "low": "ಸೂಕ್ತವಲ್ಲ / ಹೆಚ್ಚಿನ ಅಪಾಯ",
    },
    "hi": {
        "soil_ok": "आदर्श {soil} मिट्टी",
        "soil_sec": "उपयुक्त {soil} मिट्टी",
        "soil_bad": "{soil} मिट्टी कम उपयुक्त है",
        "season_ok": "मुख्य {season} मौसम",
        "season_sec": "वैकल्पिक {season} मौसम",
        "season_bad": "{season} मौसम उपयुक्त नहीं है",
        "water_ok": "सही {water} पानी की उपलब्धता",
        "water_sec": "प्रबंधनीय {water} पानी की उपलब्धता",
        "water_bad": "{water} पानी का स्तर जोखिम भरा है",
        "rain_ok": "वर्षा ({rain} mm) आदर्श सीमा ({min_r}-{max_r} mm) में है",
        "rain_bad": "वर्षा ({rain} mm) आदर्श सीमा ({min_r}-{max_r} mm) से बाहर है",
        "temp_ok": "तापमान ({temp}°C) उपयुक्त है ({min_t}-{max_t}°C)",
        "temp_bad": "तापमान ({temp}°C) आदर्श सीमा ({min_t}-{max_t}°C) से बाहर है",
        "ph_ok": "मिट्टी का pH ({ph}) उपयुक्त है ({min_p}-{max_p})",
        "ph_bad": "मिट्टी का pH ({ph}) आदर्श सीमा ({min_p}-{max_p}) से बाहर है",
        "note": "नोट: ",
        "high": "अत्यधिक अनुशंसित",
        "med": "मध्यम रूप से उपयुक्त (देखभाल आवश्यक)",
        "low": "अनुशंसित नहीं / उच्च जोखिम",
    },
    "ta": {
        "soil_ok": "சிறந்த {soil} மண்",
        "soil_sec": "பொருந்தக்கூடிய {soil} மண்",
        "soil_bad": "{soil} மண் குறைந்த பொருத்தம் கொண்டது",
        "season_ok": "முதன்மை {season} பருவம்",
        "season_sec": "மாற்று {season} பருவம்",
        "season_bad": "{season} பருவம் ஏற்றதல்ல",
        "water_ok": "சரியான {water} நீர் இருப்பு",
        "water_sec": "சமாளிக்கக்கூடிய {water} நீர் இருப்பு",
        "water_bad": "{water} நீர் அளவு சவாலானது",
        "rain_ok": "மழை ({rain} mm) சிறந்த அளவில் உள்ளது ({min_r}-{max_r} mm)",
        "rain_bad": "மழை ({rain} mm) சிறந்த அளவிற்கு ({min_r}-{max_r} mm) வெளியே உள்ளது",
        "temp_ok": "வெப்பநிலை ({temp}°C) சிறந்தது ({min_t}-{max_t}°C)",
        "temp_bad": "வெப்பநிலை ({temp}°C) சிறந்த அளவிற்கு ({min_t}-{max_t}°C) வெளியே உள்ளது",
        "ph_ok": "மண் pH ({ph}) ஏற்றது ({min_p}-{max_p})",
        "ph_bad": "மண் pH ({ph}) சிறந்த அளவிற்கு ({min_p}-{max_p}) வெளியே உள்ளது",
        "note": "குறிப்பு: ",
        "high": "மிகவும் பரிந்துரைக்கப்படுகிறது",
        "med": "மிதமான பொருத்தம் (கவனம் தேவை)",
        "low": "பரிந்துரைக்கப்படவில்லை / அதிக ஆபத்து",
    },
    "te": {
        "soil_ok": "అనువైన {soil} నేల",
        "soil_sec": "సరిపోయే {soil} నేల",
        "soil_bad": "{soil} నేల తక్కువ అనుకూలం",
        "season_ok": "ప్రధాన {season} సీజన్",
        "season_sec": "ప్రత్యామ్నాయ {season} సీజన్",
        "season_bad": "{season} సీజన్ అనుకూలం కాదు",
        "water_ok": "సరైన {water} నీటి లభ్యత",
        "water_sec": "నిర్వహించగల {water} నీటి లభ్యత",
        "water_bad": "{water} నీటి స్థాయి ఇబ్బందికరం",
        "rain_ok": "వర్షపాతం ({rain} mm) అనువైన పరిధిలో ({min_r}-{max_r} mm) ఉంది",
        "rain_bad": "వర్షపాతం ({rain} mm) అనువైన పరిధి ({min_r}-{max_r} mm) బయట ఉంది",
        "temp_ok": "ఉష్ణోగ్రత ({temp}°C) అనుకూలంగా ఉంది ({min_t}-{max_t}°C)",
        "temp_bad": "ఉష్ణోగ్రత ({temp}°C) అనువైన పరిధి ({min_t}-{max_t}°C) బయట ఉంది",
        "ph_ok": "నేల pH ({ph}) అనుకూలం ({min_p}-{max_p})",
        "ph_bad": "నేల pH ({ph}) అనువైన పరిధి ({min_p}-{max_p}) బయట ఉంది",
        "note": "గమనిక: ",
        "high": "అత్యధికంగా సిఫార్సు చేయబడింది",
        "med": "మధ్యస్థంగా అనుకూలం (జాగ్రత్త అవసరం)",
        "low": "సిఫార్సు చేయబడదు / అధిక ప్రమాదం",
    },
}

RESOURCE_LABELS = {
    "en": {"video": "Video Guide", "research": "Scientific Report", "wiki": "Wikipedia"},
    "kn": {"video": "ವೀಡಿಯೊ ಮಾರ್ಗದರ್ಶಿ", "research": "ವಿಜ್ಞಾನ ವರದಿ", "wiki": "ವಿಕಿಪೀಡಿಯಾ"},
    "hi": {"video": "वीडियो गाइड", "research": "वैज्ञानिक रिपोर्ट", "wiki": "विकिपीडिया"},
    "ta": {"video": "வீடியோ வழிகாட்டி", "research": "அறிவியல் அறிக்கை", "wiki": "விக்கிப்பீடியா"},
    "te": {"video": "వీడియో గైడ్", "research": "శాస్త్రీయ నివేదిక", "wiki": "వికీపీడియా"},
}

CROP_RESOURCES = {
    "Rice (Paddy)": {
        "videos": {"en": "https://www.youtube.com/watch?v=J_mMS3EkHok", "kn": "https://www.youtube.com/watch?v=-EJwp3qvuZU"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Rice", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%AD%E0%B2%A4%E0%B3%8D%E0%B2%A4"},
        "research": "https://openknowledge.fao.org/bitstreams/7e995fe6-73f6-4ea9-a0c3-2f29d2393983/download",
    },
    "Wheat": {
        "videos": {"en": "https://www.youtube.com/watch?v=JN0ICendQns", "kn": "https://www.youtube.com/watch?v=UARltcbc5v0", "hi": "https://www.youtube.com/watch?v=xlycr_068Ls"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Wheat", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%97%E0%B3%8B%E0%B2%A7%E0%B2%BF"},
        "research": "https://iiwbr.org.in/wp-content/uploads/2023/08/EB-52-Wheat-Cultivation-in-India-Pocket-Guide.pdf",
    },
    "Maize (Corn)": {
        "videos": {"en": "https://www.youtube.com/watch?v=Fq-IsAOqvM0", "kn": "https://www.youtube.com/watch?v=d3xybMIkI_o"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Maize", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%AE%E0%B3%86%E0%B2%95%E0%B3%8D%E0%B2%95%E0%B3%86_%E0%B2%9C%E0%B3%8B%E0%B2%B3"},
        "research": "https://agritech.tnau.ac.in/agriculture/agri_irrigationmgt_maize.html",
    },
    "Cotton": {
        "videos": {"en": "https://www.youtube.com/watch?v=eN-TqqBQOAk", "kn": "https://www.youtube.com/watch?v=AdZGyD0ShTA"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Cotton", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%B9%E0%B2%A4%E0%B3%8D%E0%B2%A4%E0%B2%BF"},
        "research": "https://www.nfsm.gov.in/BriefNote/BN_Cotton.pdf",
    },
    "Sugarcane": {
        "videos": {"en": "https://www.youtube.com/watch?v=ZfTIyrGQ8Fc", "kn": "https://www.youtube.com/watch?v=G1b56-Zw020"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Sugarcane"},
        "research": "https://www.nfsm.gov.in/BriefNote/BN_Sugarcane.pdf",
    },
    "Millets (Ragi / Bajra / Jowar)": {
        "videos": {"en": "https://www.youtube.com/watch?v=t_q4FNgZ1GQ", "kn": "https://www.youtube.com/watch?v=KYpVejs8NCI"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Finger_millet"},
        "research": "https://agritech.tnau.ac.in/agriculture/millets_sorghum.html",
    },
    "Groundnut (Peanut)": {
        "videos": {"en": "https://www.youtube.com/watch?v=Xfuudi5yo38", "kn": "https://www.youtube.com/watch?v=raqrPWJc5vI"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Peanut", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%B6%E0%B3%87%E0%B2%82%E0%B2%97%E0%B2%BE_%E0%B2%8E%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%86"},
        "research": "https://icar.org.in/en/crop-science/groundnut",
    },
    "Soybean": {
        "videos": {"en": "https://www.youtube.com/watch?v=Nw3zJnjtI34", "kn": "https://www.youtube.com/watch?v=TcMv9jODKTg"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Soybean"},
        "research": "https://icar-nsri.res.in/pdfdoc/ExtensionBulletin2023E_2.pdf",
    },
    "Chickpea (Bengal Gram / Chana)": {
        "videos": {"en": "https://www.youtube.com/watch?v=QBOtu4zCYGo", "kn": "https://www.youtube.com/watch?v=CHVuXqqZkUE", "te": "https://www.youtube.com/watch?v=VCXqrH974FI"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Chickpea"},
        "research": "https://www.icar-crida.res.in/assets/img/Books/2005-06/chickpea.pdf",
    },
    "Potato": {
        "videos": {"en": "https://www.youtube.com/watch?v=UqCRiJ6yL9g", "kn": "https://www.youtube.com/watch?v=zA0fSfB24Uk"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Potato"},
        "research": "https://agriculture.vikaspedia.in/viewcontent/agriculture/crop-production/package-of-practices/vegetables-1/potato?lgn=en",
    },
    "Mustard (Rapeseed-Mustard)": {
        "videos": {"kn": "https://www.youtube.com/watch?v=zaKzs-DMNds"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Brassica_juncea", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%B8%E0%B2%BE%E0%B2%B8%E0%B2%BF%E0%B2%B5%E0%B3%86"},
        "research": "https://pdfs.semanticscholar.org/51cd/f2a466bebd227cd84ef15e4a7a7d203de10e.pdf",
    },
    "Pigeon Pea (Tur / Arhar)": {
        "videos": {"kn": "https://www.youtube.com/watch?v=2UJnpIPuzVI"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Pigeon_pea"},
        "research": "https://agriculture.vikaspedia.in/viewcontent/agriculture/crop-production/package-of-practices/pulses/pigeon-pea?lgn=en",
    },
    "Sunflower": {
        "videos": {"kn": "https://www.youtube.com/watch?v=D9qVXUY3MXI"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Common_sunflower", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%B8%E0%B3%82%E0%B2%B0%E0%B3%8D%E0%B2%AF%E0%B2%95%E0%B2%BE%E0%B2%82%E0%B2%A4%E0%B2%BF"},
        "research": "https://www.apnikheti.com/en/pn/agriculture/crops/oilseeds/sunflower",
    },
    "Onion": {
        "videos": {"kn": "https://www.youtube.com/watch?v=KKjaHqcpjuU"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Onion"},
        "research": "https://agriculture.vikaspedia.in/viewcontent/agriculture/crop-production/package-of-practices/vegetables-1/onion-allium-cepa?lgn=en",
    },
    "Tomato": {
        "videos": {"kn": "https://www.youtube.com/watch?v=EfL5aABjTnY"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Tomato", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%9F%E0%B3%8A%E0%B2%AE%E0%B3%87%E0%B2%9F%E0%B3%8A"},
        "research": "https://icl-growingsolutions.com/agriculture/crops/tomato/",
    },
    "Green Gram (Moong)": {
        "videos": {"kn": "https://www.youtube.com/watch?v=t3Pt2aTzLQQ"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Mung_bean"},
        "research": "https://www.agrifarming.in/summer-green-gram-cultivation-varieties-of-mung-beans-and-irrigation-management",
    },
    "Banana": {
        "videos": {"kn": "https://www.youtube.com/watch?v=CZ_ff_sa-Kg"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Banana", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%AC%E0%B2%BE%E0%B2%B3%E0%B3%86_%E0%B2%B9%E0%B2%A3%E0%B3%8D%E0%B2%A3%E0%B3%81"},
        "research": "https://agritech.tnau.ac.in/expert_system/banana/cultivation.html",
    },
    "Coconut": {
        "videos": {"kn": "https://www.youtube.com/watch?v=1x16RhUg8hc"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Coconut"},
        "research": "https://agriculture.vikaspedia.in/viewcontent/agriculture/crop-production/package-of-practices/plantation-crops/coconut/coconut-cultivation-practices?lgn=en",
    },
    "Tea": {
        "videos": {"en": "https://www.youtube.com/watch?v=dTHansLrH0M", "kn": "https://www.youtube.com/watch?v=iUUNgk2IlzA"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Tea"},
        "research": "https://agriculture.institute/crop-production-technology/optimizing-soil-conditions-for-tea-cultivation/",
    },
    "Coffee": {
        "videos": {"kn": "https://www.youtube.com/watch?v=O_-yK2yVyuE"},
        "wiki": {"en": "https://en.wikipedia.org/wiki/Coffee_production_in_India", "kn": "https://kn.wikipedia.org/wiki/%E0%B2%95%E0%B2%BE%E0%B2%AB%E0%B2%BF"},
        "research": "https://agriculture.institute/crop-production-technology/ideal-soil-conditions-coffee-cultivation-india/",
    },
}


def build_resources(crop_name, lang):
    res = CROP_RESOURCES.get(crop_name, {})
    lbl = RESOURCE_LABELS.get(lang, RESOURCE_LABELS["en"])
    videos = res.get("videos", {})
    video_url = videos.get(lang) or videos.get("en") or videos.get("kn")

    wiki_map = res.get("wiki", {})
    en_wiki = wiki_map.get("en", "https://en.wikipedia.org/wiki/Agriculture_in_India")
    if lang == "en":
        wiki_url = en_wiki
    elif lang in wiki_map:
        wiki_url = wiki_map[lang]
    else:
        wiki_url = f"https://translate.google.com/translate?sl=en&tl={lang}&u={quote(en_wiki, safe='')}"

    research_url = res.get("research", en_wiki)
    if lang != "en":
        research_url = f"https://translate.google.com/translate?sl=en&tl={lang}&u={quote(research_url, safe='')}"

    items = []
    if video_url:
        items.append({"type": "video", "label": lbl["video"], "url": video_url})
    items.append({"type": "research", "label": lbl["research"], "url": research_url})
    items.append({"type": "wiki", "label": lbl["wiki"], "url": wiki_url})
    return items


CROPS = [
    {
        "name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "primary_soil": ["clay", "alluvial"],
        "secondary_soil": ["loamy"],
        "primary_season": ["kharif"],
        "secondary_season": ["monsoon", "rabi"],
        "ideal_rain": 1600,
        "min_rain": 1150,
        "max_rain": 3000,
        "min_temp": 21,
        "max_temp": 37,
        "min_ph": 5.5,
        "max_ph": 6.5,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "120 - 150 days",
        "temp": "21°C - 37°C",
        "ph_range": "5.5 - 6.5",
        "image_url": "https://cdn.britannica.com/33/125833-050-3C90801C/Paddy-field-Minamiuonuma-Japan.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Rice",
        "overview": {
            "en": "Rice (Oryza sativa) is India's primary staple cereal grass, thriving in warm, humid climates with assured water supply or puddled paddy fields.",
            "kn": "ಭತ್ತ (Oryza sativa) ಭಾರತದ ಪ್ರಮುಖ ಆಹಾರ ಧಾನ್ಯವಾಗಿದ್ದು, ಬೆಚ್ಚಗಿನ, ತೇವಾಂಶವುಳ್ಳ ಹವಾಮಾನ ಮತ್ತು ಉತ್ತಮ ನೀರಾವರಿ ಇರುವ ಗದ್ದೆಗಳಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತದೆ.",
            "hi": "धान (Oryza sativa) भारत की प्रमुख मुख्य फसल है, जो गर्म, आर्द्र जलवायु और पर्याप्त पानी वाले खेतों में अच्छी तरह उगती है।",
            "ta": "நெல் (Oryza sativa) இந்தியாவின் முக்கிய உணவுப் பயிராகும்; இது வெப்பமான, ஈரப்பதமான காலநிலை மற்றும் நீர் வசதி உள்ள வயல்களில் நன்கு வளரும்.",
            "te": "వరి (Oryza sativa) భారతదేశపు ప్రధాన ఆహార పంట; ఇది వెచ్చని, తేమతో కూడిన వాతావరణం మరియు నీటి వసతి ఉన్న పొలాల్లో బాగా పెరుగుతుంది.",
        },
        "fertilizer": {
            "en": "NPK 120:60:60 kg/ha; apply Nitrogen in 3 split doses (basal, tillering, panicle initiation).",
            "kn": "NPK 120:60:60 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಸಾರಜನಕವನ್ನು 3 ಹಂತಗಳಲ್ಲಿ (ಬಿತ್ತನೆ, ಕವಲೊಡೆಯುವಿಕೆ, ತೆನೆ ಹಂತ) ನೀಡಿ.",
            "hi": "NPK 120:60:60 किग्रा/हेक्टेयर; नाइट्रोजन को 3 भागों (बुवाई, कल्ले निकलने, बाली अवस्था) में दें।",
            "ta": "NPK 120:60:60 கிலோ/எக்டர்; தழைச்சத்தை 3 பிரிவுகளாக இடவும்.",
            "te": "NPK 120:60:60 కిలోలు/హెక్టారుకు; నత్రజనిని 3 దఫాలుగా వేయండి.",
        },
        "tip": {
            "en": "Maintain 2-5 cm standing water during vegetative growth and drain 10 days before harvest.",
            "kn": "ಬೆಳವಣಿಗೆಯ ಹಂತದಲ್ಲಿ 2-5 ಸೆಂ.ಮೀ ನೀರು ನಿಲ್ಲಿಸಿ, ಕಟಾವಿಗೆ 10 ದಿನಗಳ ಮೊದಲು ನೀರು ಬಸಿದುಹೋಗುವಂತೆ ಮಾಡಿ.",
            "hi": "बढ़वार के समय 2-5 सेमी पानी बनाए रखें और कटाई से 10 दिन पहले पानी निकाल दें।",
            "ta": "வளர்ச்சிப் பருவத்தில் 2-5 செ.மீ நீர் நிறுத்தி, அறுவடைக்கு 10 நாட்களுக்கு முன் நீரை வடிக்கவும்.",
            "te": "పెరుగుదల దశలో 2-5 సెం.మీ నీరు నిల్వ ఉంచి, కోతకు 10 రోజుల ముందు నీటిని తీసివేయండి.",
        },
        "guidelines": {
            "en": [
                "1. Nursery & Soil Prep: Puddle field 2-3 times and level properly for uniform water depth.",
                "2. Transplanting: Transplant 21-25 day old seedlings at 20x15 cm spacing.",
                "3. Water Management: Keep 2-5 cm standing water; avoid moisture stress at flowering.",
                "4. Weed & Pest Control: Apply pre-emergence herbicide within 3 DAT and monitor stem borer.",
                "5. Harvest: Harvest when 80-85% of panicles turn golden yellow.",
            ],
            "kn": [
                "1. ಸಸಿಮಡಿ ಮತ್ತು ಭೂಮಿ ಸಿದ್ಧತೆ: ಗದ್ದೆಯನ್ನು 2-3 ಬಾರಿ ಉಳುಮೆ ಮಾಡಿ ಸಮತಟ್ಟು ಮಾಡಿ.",
                "2. ನಾಟಿ ಮಾಡುವುದು: 21-25 ದಿನದ ಸಸಿಗಳನ್ನು 20x15 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ನಾಟಿ ಮಾಡಿ.",
                "3. ನೀರಿನ ನಿರ್ವಹಣೆ: 2-5 ಸೆಂ.ಮೀ ನೀರು ನಿಲ್ಲಿಸಿ; ಹೂ ಬಿಡುವ ಹಂತದಲ್ಲಿ ನೀರಿನ ಕೊರತೆಯಾಗದಂತೆ ನೋಡಿ.",
                "4. ಕಳೆ ಮತ್ತು ಕೀಟ ನಿಯಂತ್ರಣ: ನಾಟಿ ಮಾಡಿದ 3 ದಿನಗಳಲ್ಲಿ ಕಳೆ ನಿಯಂತ್ರಿಸಿ ಮತ್ತು ಕಾಂಡ ಕೊರಕ ಹುಳುವನ್ನು ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ಶೇ. 80-85 ರಷ್ಟು ತೆನೆಗಳು ಬಂಗಾರದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. नर्सरी और खेत तैयारी: खेत की 2-3 बार जुताई कर समतल और कीचड़युक्त बनाएं।",
                "2. रोपाई: 21-25 दिन की पौध को 20x15 सेमी की दूरी पर रोपें।",
                "3. सिंचाई प्रबंधन: खेत में 2-5 सेमी पानी रखें; फूल आते समय नमी कम न होने दें।",
                "4. खरपतवार व कीट नियंत्रण: रोपाई के 3 दिन में खरपतवार प्रबंधन करें और तना छेदक पर नजर रखें।",
                "5. कटाई: जब 80-85% बालियां सुनहरी हो जाएं तब कटाई करें।",
            ],
            "ta": [
                "1. நாற்றங்கால் மற்றும் நிலம் தயாரித்தல்: வயலை 2-3 முறை சேறு கலக்கி சமப்படுத்தவும்.",
                "2. நடவு: 21-25 நாட்கள் ஆன நாற்றுகளை 20x15 செ.மீ இடைவெளியில் நடவும்.",
                "3. நீர் மேலாண்மை: 2-5 செ.மீ நீர் நிறுத்தவும்; பூக்கும் பருவத்தில் வறட்சி தவிர்க்கவும்.",
                "4. களை மற்றும் பூச்சி கட்டுப்பாடு: நட்ட 3 நாட்களில் களைக்கொல்லி இட்டு தண்டு துளைப்பானைக் கண்காணிக்கவும்.",
                "5. அறுவடை: 80-85% கதிர்கள் பொன்னிறமானதும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. నారుమడి మరియు పొలం తయారీ: పొలాన్ని 2-3 సార్లు దమ్ము చేసి సమం చేయండి.",
                "2. నాట్లు: 21-25 రోజుల నారును 20x15 సెం.మీ దూరంలో నాటండి.",
                "3. నీటి యాజమాన్యం: 2-5 సెం.మీ నీరు నిల్వ ఉంచి, పూత దశలో నీటి ఎద్దడి లేకుండా చూడండి.",
                "4. కలుపు & పురుగుల నివారణ: నాటిన 3 రోజుల్లో కలుపు మందు వాడి కాండం తొలుచు పురుగును గమనించండి.",
                "5. కోత: 80-85% వెన్నులు బంగారు రంగులోకి మారినప్పుడు కోత కోయండి.",
            ],
        },
    },
    {
        "name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "primary_soil": ["loamy", "alluvial"],
        "secondary_soil": ["clay", "black"],
        "primary_season": ["rabi"],
        "secondary_season": ["winter"],
        "ideal_rain": 550,
        "min_rain": 300,
        "max_rain": 1000,
        "min_temp": 10,
        "max_temp": 25,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["medium"],
        "secondary_water": ["high"],
        "duration": "110 - 130 days",
        "temp": "10°C - 25°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://www.farmatma.in/wp-content/uploads/2019/05/wheat-cultivation-india.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Wheat",
        "overview": {
            "en": "Wheat (Triticum aestivum) is India's premier Rabi cereal crop, needing cool temperatures during tillering and warm, dry weather for grain ripening.",
            "kn": "ಗೋಧಿ (Triticum aestivum) ಭಾರತದ ಪ್ರಮುಖ ಹಿಂಗಾರು (ರಬಿ) ಧಾನ್ಯವಾಗಿದ್ದು, ಬೆಳವಣಿಗೆಗೆ ತಂಪಾದ ವಾತಾವರಣ ಮತ್ತು ಕಾಳು ಮಾಗಲು ಒಣ ಹವಾಮಾನ ಬೇಕಾಗುತ್ತದೆ.",
            "hi": "गेहूं (Triticum aestivum) भारत की प्रमुख रबी फसल है, जिसे बढ़वार के लिए ठंडा मौसम और पकने के समय गर्म व शुष्क मौसम चाहिए।",
            "ta": "கோதுமை (Triticum aestivum) இந்தியாவின் முக்கிய ரபி தானியப் பயிராகும்; வளர்ச்சிக்கு குளிர்ந்த காலநிலையும், கதிர் முதிர்ச்சிக்கு வறண்ட வானிலையும் தேவை.",
            "te": "గోధుమ (Triticum aestivum) భారతదేశపు ప్రధాన రబీ పంట; పెరుగుదలకు చల్లని వాతావరణం మరియు గింజలు పండేందుకు పొడి వాతావరణం అవసరం.",
        },
        "fertilizer": {
            "en": "NPK 120:60:40 kg/ha; apply full Phosphorus and Potash at sowing and split Nitrogen.",
            "kn": "NPK 120:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಬಿತ್ತನೆ ವೇಳೆ ರಂಜಕ, ಪೊಟ್ಯಾಶ್ ಮತ್ತು ಸಾರಜನಕವನ್ನು ಹಂತ ಹಂತವಾಗಿ ನೀಡಿ.",
            "hi": "NPK 120:60:40 किग्रा/हेक्टेयर; बुवाई के समय पूरा फास्फोरस-पोटाश और नाइट्रोजन को विभाजित कर दें।",
            "ta": "NPK 120:60:40 கிலோ/எக்டர்; விதைப்பின்போது மணிச்சத்து, சாம்பல் சத்து இட்டு தழைச்சத்தை பிரித்து இடவும்.",
            "te": "NPK 120:60:40 కిలోలు/హెక్టారుకు; విత్తేటప్పుడు భాస్వరం, పొటాష్ వేసి నత్రజనిని దఫాలుగా వేయండి.",
        },
        "tip": {
            "en": "Ensure critical irrigation at Crown Root Initiation (CRI) stage around 21 days after sowing.",
            "kn": "ಬಿತ್ತನೆ ಮಾಡಿದ 21 ದಿನಗಳ ನಂತರ ಬೇರು ಬಿಡುವ (CRI) ಹಂತದಲ್ಲಿ ತಪ್ಪದೇ ನೀರು ಹಾಯಿಸಿ.",
            "hi": "बुवाई के लगभग 21 दिन बाद शीर्ष जड़ जमने (CRI) की अवस्था में सिंचाई जरूर करें।",
            "ta": "விதைத்த 21 நாட்களில் வேர் பிடிக்கும் (CRI) பருவத்தில் தவறாமல் நீர் பாய்ச்சவும்.",
            "te": "విత్తిన 21 రోజుల తర్వాత వేర్లు వచ్చే (CRI) దశలో తప్పనిసరిగా నీరు పెట్టండి.",
        },
        "guidelines": {
            "en": [
                "1. Seedbed & Sowing: Sow 100-125 kg/ha certified seed at 20-22.5 cm row spacing in November.",
                "2. CRI Irrigation: Give first irrigation at 21 DAS, then at tillering, jointing, flowering, and milking.",
                "3. Weed Management: Control Phalaris minor and broadleaf weeds at 30-35 DAS.",
                "4. Disease Watch: Monitor for yellow and brown rust; use resistant varieties.",
                "5. Harvest: Harvest when grain moisture drops below 14% and straw turns golden.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನವೆಂಬರ್‌ನಲ್ಲಿ ಹೆಕ್ಟೇರ್‌ಗೆ 100-125 ಕೆಜಿ ಬೀಜವನ್ನು 20-22.5 ಸೆಂ.ಮೀ ಸಾಲಿನಲ್ಲಿ ಬಿತ್ತನೆ ಮಾಡಿ.",
                "2. ನೀರಾವರಿ: ಬಿತ್ತಿದ 21 ದಿನಕ್ಕೆ (CRI) ಮೊದಲ ನೀರು, ನಂತರ ತೆನೆ ಹಾಗೂ ಹಾಲು ತುಂಬುವ ಹಂತದಲ್ಲಿ ನೀರು ಕೊಡಿ.",
                "3. ಕಳೆ ನಿರ್ವಹಣೆ: ಬಿತ್ತಿದ 30-35 ದಿನಗಳಲ್ಲಿ ಕಳೆಗಳನ್ನು ತೆಗೆಯಿರಿ.",
                "4. ರೋಗ ನಿಗಾ: ಹಳದಿ ಮತ್ತು ಕಂದು ತುಕ್ಕು ರೋಗದ ಬಗ್ಗೆ ನಿಗಾ ವಹಿಸಿ.",
                "5. ಕಟಾವು: ಕಾಳು ಗಟ್ಟಿಯಾಗಿ ಹುಲ್ಲು ಒಣಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: नवंबर में 100-125 किग्रा/हेक्टेयर बीज 20-22.5 सेमी कतार में बोएं।",
                "2. सिंचाई: 21 दिन पर पहली सिंचाई (CRI), फिर कल्ले, गांठ, फूल और दूधिया अवस्था में पानी दें।",
                "3. खरपतवार नियंत्रण: बुवाई के 30-35 दिन बाद गेहूंसा और चौड़ी पत्ती के खरपतवार हटाएं।",
                "4. रोग निगरानी: पीले और भूरे रतुआ रोग से बचाव के लिए प्रतिरोधी किस्में चुनें।",
                "5. कटाई: दाने सख्त होने और बालियां सूखने पर कटाई करें।",
            ],
            "ta": [
                "1. விதைப்பு: நவம்பரில் 100-125 கிலோ/எக்டர் விதையை 20-22.5 செ.மீ வரிசை இடைவெளியில் விதைக்கவும்.",
                "2. நீர்ப்பாசனம்: விதைத்த 21வது நாளில் (CRI) முதல் நீர் மற்றும் பூக்கும் பருவத்தில் நீர் பாய்ச்சவும்.",
                "3. களை மேலாண்மை: 30-35 நாட்களில் களைகளை அகற்றவும்.",
                "4. நோய் கண்காணிப்பு: துரு நோயைக் கண்காணித்து எதிர்ப்பு ரகங்களைப் பயன்படுத்தவும்.",
                "5. அறுவடை: தானியங்கள் காய்ந்து பொன்னிறமானதும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: నవంబర్‌లో ఎకరాకు 100-125 కిలోల/హెక్టార్ విత్తనాన్ని 20-22.5 సెం.మీ వరుసల్లో విత్తండి.",
                "2. నీటిపారుదల: విత్తిన 21 రోజులకు (CRI) మొదటి తడి, ఆపై పూత మరియు పాలు పోసుకునే దశలో నీరు ఇవ్వండి.",
                "3. కలుపు నియంత్రణ: 30-35 రోజులలో కలుపును నివారించండి.",
                "4. తెగుళ్ల పర్యవేక్షణ: కుంకుమ తెగులును గమనించి నిరోధక రకాలను వాడండి.",
                "5. కోత: గింజలు గట్టిపడి కంకులు బంగారు రంగులోకి వచ్చినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "primary_soil": ["loamy", "alluvial"],
        "secondary_soil": ["sandy", "red", "black"],
        "primary_season": ["kharif", "rabi"],
        "secondary_season": ["zaid"],
        "ideal_rain": 750,
        "min_rain": 500,
        "max_rain": 1200,
        "min_temp": 18,
        "max_temp": 32,
        "min_ph": 5.5,
        "max_ph": 7.5,
        "primary_water": ["medium"],
        "secondary_water": ["high", "low"],
        "duration": "90 - 110 days",
        "temp": "18°C - 32°C",
        "ph_range": "5.5 - 7.5",
        "image_url": "https://cdn.britannica.com/33/75933-050-826C8817/Rows-corn-field-Nebraska.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Maize",
        "overview": {
            "en": "Maize (Zea mays) is a versatile C4 cereal grown across Kharif and Rabi seasons in India for food, poultry feed, and starch.",
            "kn": "ಮೆಕ್ಕೆಜೋಳ (Zea mays) ಆಹಾರ, ಪಶು ಆಹಾರ ಮತ್ತು ಪಿಷ್ಟಕ್ಕಾಗಿ ಮುಂಗಾರು ಹಾಗೂ ಹಿಂಗಾರು ಋತುಗಳಲ್ಲಿ ಬೆಳೆಯುವ ಬಹುಮುಖ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "मक्का (Zea mays) भोजन, चारे और स्टार्च के लिए खरीफ और रबी दोनों मौसम में उगाई जाने वाली बहुमुखी फसल है।",
            "ta": "மக்காச்சோளம் (Zea mays) உணவு, தீவனம் மற்றும் மாவுச்சத்துக்காக கரீஃப், ரபி பருவங்களில் வளர்க்கப்படும் பல்துறைப் பயிராகும்.",
            "te": "మొక్కజొన్న (Zea mays) ఆహారం, పశుగ్రాసం మరియు స్టార్చ్ కోసం ఖరీఫ్, రబీ సీజన్లలో పండించే బహుళ ప్రయోజన పంట.",
        },
        "fertilizer": {
            "en": "NPK 120:60:40 kg/ha plus Zinc Sulphate (25 kg/ha) for higher grain yield.",
            "kn": "ಹೆಚ್ಚಿನ ಇಳುವರಿಗಾಗಿ NPK 120:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಸತುವಿನ ಸಲ್ಫೇಟ್ (25 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) ನೀಡಿ.",
            "hi": "अधिक उपज के लिए NPK 120:60:40 किग्रा/हेक्टेयर के साथ जिंक सल्फेट (25 किग्रा) डालें।",
            "ta": "அதிக மகசூலுக்கு NPK 120:60:40 கிலோ/எக்டர் உடன் துத்தநாக சல்பேட் (25 கிலோ) இடவும்.",
            "te": "అధిక దిగుబడి కోసం NPK 120:60:40 కిలోలతో పాటు జింక్ సల్ఫేట్ (25 కిలోలు) వేయండి.",
        },
        "tip": {
            "en": "Avoid waterlogging at seedling stage and ensure moisture during tasseling and silking.",
            "kn": "ಮೊಳಕೆ ಹಂತದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು ಹೂವು ಬಿಡುವ ಹಂತದಲ್ಲಿ ತೇವಾಂಶ ಕಾಪಾಡಿ.",
            "hi": "शुरुआती अवस्था में जलभराव से बचें और फूल आते समय खेत में नमी बनाए रखें।",
            "ta": "ஆரம்ப நிலையில் நீர் தேங்குவதைத் தவிர்த்து, பூக்கும் பருவத்தில் ஈரப்பதம் காக்கவும்.",
            "te": "ప్రారంభ దశలో నీరు నిల్వకుండా చూసి, పూత సమయంలో తగిన తేమ ఉండేలా చూడండి.",
        },
        "guidelines": {
            "en": [
                "1. Ridge & Furrow Sowing: Sow seeds at 60x20 cm spacing on well-drained ridges.",
                "2. Weed Control: Keep field weed-free for the first 30-40 days.",
                "3. Top Dressing: Apply Nitrogen splits at knee-high and pre-tasseling stages.",
                "4. Pest Watch: Monitor for Fall Armyworm in whorl leaves early.",
                "5. Harvest: Harvest when husks dry and kernels show a black layer at the base.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನೀರು ಬಸಿದುಹೋಗುವ ಸಾಲುಗಳಲ್ಲಿ 60x20 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಬೀಜ ಬಿತ್ತನೆ ಮಾಡಿ.",
                "2. ಕಳೆ ನಿಯಂತ್ರಣ: ಮೊದಲ 30-40 ದಿನಗಳವರೆಗೆ ಹೊಲವನ್ನು ಕಳೆರಹಿತವಾಗಿ ಇಡಿ.",
                "3. ಮೇಲುಗೊಬ್ಬರ: ಮೊಳಕಾಲು ಎತ್ತರ ಮತ್ತು ತೆನೆ ಬರುವ ಮುನ್ನ ಸಾರಜನಕ ನೀಡಿ.",
                "4. ಕೀಟ ನಿಗಾ: ಸೈನಿಕ ಹುಳುವಿನ (Fall Armyworm) ಬಾಧೆಯನ್ನು ಆರಂಭದಲ್ಲೇ ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ತೆನೆಯ ಸಿಪ್ಪೆ ಒಣಗಿ ಕಾಳು ಗಟ್ಟಿಯಾದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. मेड़ पर बुवाई: जल निकासी वाली मेड़ों पर 60x20 सेमी दूरी पर बुवाई करें।",
                "2. निराई-गुड़ाई: शुरुआती 30-40 दिनों तक खेत को खरपतवार मुक्त रखें।",
                "3. टॉप ड्रेसिंग: घुटने तक ऊंचाई और मंजरी निकलने से पहले नाइट्रोजन डालें।",
                "4. कीट प्रबंधन: फॉल आर्मीवर्म कीट की शुरुआत में ही निगरानी करें।",
                "5. कटाई: भुट्टे के छिलके सूखने और दाने सख्त होने पर कटाई करें।",
            ],
            "ta": [
                "1. பார் அமைத்து விதைப்பு: வடிகால் வசதியுள்ள பார்களில் 60x20 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "2. களை கட்டுப்பாடு: முதல் 30-40 நாட்களுக்கு வயலைக் களையின்றி வைத்திருக்கவும்.",
                "3. மேலுரம்: முழங்கால் உயரத்திலும் பூக்கும் முன்பும் தழைச்சத்து இடவும்.",
                "4. பூச்சி கண்காணிப்பு: படைப்புழு தாக்குதலை ஆரம்பத்திலேயே கண்காணிக்கவும்.",
                "5. அறுவடை: கதிர் உறை காய்ந்து மணிகள் முற்றியதும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. బోదెలపై విత్తడం: నీరు నిలవని బోదెలపై 60x20 సెం.మీ దూరంలో విత్తండి.",
                "2. కలుపు నియంత్రణ: మొదటి 30-40 రోజులు పొలాన్ని కలుపు లేకుండా ఉంచండి.",
                "3. పైపాటు ఎరువులు: మోకాలు ఎత్తు మరియు పూతకు ముందు నత్రజని వేయండి.",
                "4. పురుగుల పర్యవేక్షణ: కత్తెర పురుగు (Fall Armyworm) ఉధృతిని ముందే గమనించండి.",
                "5. కోత: కంకి పొరలు ఎండి గింజలు గట్టిపడినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "primary_soil": ["black"],
        "secondary_soil": ["alluvial", "loamy"],
        "primary_season": ["kharif"],
        "secondary_season": ["annual"],
        "ideal_rain": 800,
        "min_rain": 500,
        "max_rain": 1300,
        "min_temp": 21,
        "max_temp": 35,
        "min_ph": 5.8,
        "max_ph": 7.5,
        "primary_water": ["medium"],
        "secondary_water": ["low", "high"],
        "duration": "150 - 180 days",
        "temp": "21°C - 35°C",
        "ph_range": "5.8 - 7.5",
        "image_url": "https://www.moderndane.com/cdn/shop/articles/29b303c6537f5db5c6478c3ed851aa7f.jpg?v=1776046671&width=2048",
        "source_url": "https://en.wikipedia.org/wiki/Cotton",
        "overview": {
            "en": "Cotton (Gossypium hirsutum) is India's leading natural fiber cash crop, ideally suited to deep black cotton soils with bright sunshine at boll opening.",
            "kn": "ಹತ್ತಿ (Gossypium hirsutum) ಭಾರತದ ಪ್ರಮುಖ ನಾರಿನ ವಾಣಿಜ್ಯ ಬೆಳೆಯಾಗಿದ್ದು, ಕಪ್ಪು ಮಣ್ಣು ಮತ್ತು ಕಾಯಿ ಬಿರಿಯುವಾಗ ಬಿಸಿಲಿನ ವಾತಾವರಣದಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತದೆ.",
            "hi": "कपास (Gossypium hirsutum) भारत की प्रमुख रेशेदार नकदी फसल है, जो काली मिट्टी और टिंडे खुलते समय तेज धूप में अच्छी उपज देती है।",
            "ta": "பருத்தி (Gossypium hirsutum) இந்தியாவின் முக்கிய நார் பணப்பயிராகும்; கரிசல் மண் மற்றும் காய் வெடிக்கும்போது வெயிலில் நன்கு விளையும்.",
            "te": "పత్తి (Gossypium hirsutum) భారతదేశపు ప్రధాన వాణిజ్య పంట; నల్ల రేగడి నేలలు మరియు కాయలు పగిలే సమయంలో పొడి వాతావరణం దీనికి అనుకూలం.",
        },
        "fertilizer": {
            "en": "NPK 100:50:50 kg/ha; spray 2% DAP or 19:19:19 during flowering and boll development.",
            "kn": "NPK 100:50:50 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಹೂವು ಮತ್ತು ಕಾಯಿ ಕಟ್ಟುವ ಹಂತದಲ್ಲಿ 2% DAP ಸಿಂಪಡಿಸಿ.",
            "hi": "NPK 100:50:50 किग्रा/हेक्टेयर; फूल और टिंडे बनते समय 2% DAP का छिड़काव करें।",
            "ta": "NPK 100:50:50 கிலோ/எக்டர்; பூக்கும் மற்றும் காய் பிடிக்கும் பருவத்தில் 2% DAP தெளிக்கவும்.",
            "te": "NPK 100:50:50 కిలోలు/హెక్టారుకు; పూత మరియు కాయ దశలో 2% DAP పిచికారీ చేయండి.",
        },
        "tip": {
            "en": "Install pheromone traps to monitor pink bollworm and avoid excess nitrogen that triggers sucking pests.",
            "kn": "ಗುಲಾಬಿ ಕಾಯಿಕೊರಕ ಹುಳು ನಿಯಂತ್ರಣಕ್ಕೆ ಮೋಹಕ ಬಲೆಗಳನ್ನು (pheromone traps) ಬಳಸಿ.",
            "hi": "गुलाबी सुंडी की निगरानी के लिए फेरोमोन ट्रैप लगाएं और अतिरिक्त नाइट्रोजन से बचें।",
            "ta": "இளஞ்சிவப்பு காய்ப்புழுவைக் கண்காணிக்க இனக்கவர்ச்சிப் பொறிகளைப் பொருத்தவும்.",
            "te": "గులాబీ రంగు పురుగును గమనించేందుకు ఫెరమోన్ ఎరలను అమర్చండి.",
        },
        "guidelines": {
            "en": [
                "1. Deep Ploughing & Sowing: Deep-plough in summer and sow hybrids at 90x60 cm spacing.",
                "2. Thinning & Gap Filling: Maintain one healthy plant per hill within 15-20 DAS.",
                "3. Intercultivation: Perform hoeing at 30 and 50 DAS to conserve soil moisture.",
                "4. Bollworm & Pest Control: Use yellow sticky traps and pheromone traps from 45 DAS.",
                "5. Picking: Pick clean, dry cotton bolls in 3-4 pickings without trash.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ಬೇಸಿಗೆಯಲ್ಲಿ ಆಳವಾದ ಉಳುಮೆ ಮಾಡಿ 90x60 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಹೈಬ್ರಿಡ್ ಬೀಜ ಬಿತ್ತಿ.",
                "2. ಸಸಿ ತೆಳುಗೊಳಿಸುವಿಕೆ: 15-20 ದಿನಗಳಲ್ಲಿ ಗುಣಿಗೆ ಒಂದು ಆರೋಗ್ಯಕರ ಗಿಡ ಉಳಿಸಿ.",
                "3. ಎಡೆಕುಂಟೆ: ಮಣ್ಣಿನ ತೇವಾಂಶ ಉಳಿಸಲು 30 ಮತ್ತು 50 ದಿನಗಳಲ್ಲಿ ಎಡೆಕುಂಟೆ ಹೊಡೆಯಿರಿ.",
                "4. ಕೀಟ ನಿಯಂತ್ರಣ: 45 ದಿನದಿಂದ ಹಳದಿ ಅಂಟು ಬಲೆ ಮತ್ತು ಮೋಹಕ ಬಲೆ ಬಳಸಿ.",
                "5. ಹತ್ತಿ ಬಿಡಿಸುವುದು: ಕಾಯಿಗಳು ಚೆನ್ನಾಗಿ ಬಿರಿದಾಗ 3-4 ಹಂತಗಳಲ್ಲಿ ಸ್ವಚ್ಛವಾಗಿ ಬಿಡಿಸಿ.",
            ],
            "hi": [
                "1. गहरी जुताई व बुवाई: गर्मियों में गहरी जुताई कर 90x60 सेमी पर हाइब्रिड बीज बोएं।",
                "2. छंटाई: 15-20 दिन में प्रति स्थान एक स्वस्थ पौधा रखें।",
                "3. निंदाई-गुड़ाई: नमी बचाने के लिए 30 और 50 दिन पर गुड़ाई करें।",
                "4. कीट प्रबंधन: 45 दिन से पीले चिपचिपे व फेरोमोन ट्रैप लगाएं।",
                "5. चुनाई: टिंडे पूरी तरह खिलने पर 3-4 बार में साफ कपास चुनें।",
            ],
            "ta": [
                "1. ஆழ உழவு & விதைப்பு: கோடையில் ஆழ உழவு செய்து 90x60 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "2. செடி களைதல்: 15-20 நாட்களில் குழிக்கு ஒரு ஆரோக்கியமான செடியை விடவும்.",
                "3. இடை உழவு: ஈரப்பதத்தைக் காக்க 30 மற்றும் 50 நாட்களில் களைக்கொத்து செய்யவும்.",
                "4. பூச்சி கட்டுப்பாடு: 45வது நாளில் மஞ்சள் ஒட்டும் மற்றும் இனக்கவர்ச்சிப் பொறிகள் வைக்கவும்.",
                "5. பறிப்பு: காய் நன்கு வெடித்ததும் 3-4 முறை சுத்தமாகப் பஞ்சு எடுக்கவும்.",
            ],
            "te": [
                "1. లోతు దుక్కి & విత్తడం: వేసవిలో లోతు దుక్కి చేసి 90x60 సెం.మీ దూరంలో విత్తండి.",
                "2. మొక్కల సర్దుబాటు: 15-20 రోజుల్లో పాదుకు ఒక ఆరోగ్యకరమైన మొక్కను ఉంచండి.",
                "3. అంతర కృషి: తేమను కాపాడేందుకు 30, 50 రోజుల్లో గొర్రు తోలండి.",
                "4. పురుగుల నియంత్రణ: 45వ రోజు నుండి పసుపు అట్టలు, ఫెరమోన్ ఎరలు పెట్టండి.",
                "5. తీత: కాయలు పూర్తిగా పగిలిన తర్వాత 3-4 విడతలుగా శుభ్రంగా పత్తి తీయండి.",
            ],
        },
    },
    {
        "name": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "primary_soil": ["alluvial", "loamy", "black"],
        "secondary_soil": ["clay", "red"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif", "rabi"],
        "ideal_rain": 1500,
        "min_rain": 1000,
        "max_rain": 2600,
        "min_temp": 20,
        "max_temp": 35,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "300 - 365 days",
        "temp": "20°C - 35°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://cdn.britannica.com/23/126823-050-820B0A1F/Field-sugarcane-St-George-Parish-Barbados.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Sugarcane",
        "overview": {
            "en": "Sugarcane (Saccharum officinarum) is a long-duration tropical grass grown across India for sugar, jaggery, and ethanol production.",
            "kn": "ಕಬ್ಬು (Saccharum officinarum) ಸಕ್ಕರೆ, ಬೆಲ್ಲ ಮತ್ತು ಎಥೆನಾಲ್ ಉತ್ಪಾದನೆಗಾಗಿ ಬೆಳೆಯುವ ದೀರ್ಘಾವಧಿಯ ಪ್ರಮುಖ ವಾಣಿಜ್ಯ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "गन्ना (Saccharum officinarum) चीनी, गुड़ और एथेनॉल उत्पादन के लिए उगाई जाने वाली प्रमुख दीर्घकालिक नकदी फसल है।",
            "ta": "கரும்பு (Saccharum officinarum) சர்க்கரை, வெல்லம் மற்றும் எத்தனால் உற்பத்திக்காகப் பயிரிடப்படும் நீண்டகாலப் பயிராகும்.",
            "te": "చెరకు (Saccharum officinarum) చక్కెర, బెల్లం మరియు ఇథనాల్ ఉత్పత్తి కోసం పండించే దీర్ఘకాలిక వాణిజ్య పంట.",
        },
        "fertilizer": {
            "en": "NPK 250:115:115 kg/ha; apply Nitrogen in 3-4 splits up to 120 days and add organic compost.",
            "kn": "NPK 250:115:115 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; 120 ದಿನಗಳವರೆಗೆ 3-4 ಹಂತಗಳಲ್ಲಿ ಸಾರಜನಕ ಮತ್ತು ಸಾವಯವ ಗೊಬ್ಬರ ನೀಡಿ.",
            "hi": "NPK 250:115:115 किग्रा/हेक्टेयर; 120 दिनों तक 3-4 बार में नाइट्रोजन और जैविक खाद दें।",
            "ta": "NPK 250:115:115 கிலோ/எக்டர்; 120 நாட்கள் வரை 3-4 முறை தழைச்சத்து மற்றும் தொழுவுரம் இடவும்.",
            "te": "NPK 250:115:115 కిలోలు/హెక్టారుకు; 120 రోజుల వరకు 3-4 దఫాలుగా నత్రజని మరియు సేంద్రియ ఎరువు వేయండి.",
        },
        "tip": {
            "en": "Earthing-up at 120 days prevents lodging, and trash mulching conserves irrigation water.",
            "kn": "120 ದಿನಗಳಲ್ಲಿ ಬುಡಕ್ಕೆ ಮಣ್ಣು ಏರಿಸುವುದರಿಂದ ಗಿಡ ಬೀಳುವುದಿಲ್ಲ; ತರಗು ಹೊದಿಕೆ ನೀರು ಉಳಿಸುತ್ತದೆ.",
            "hi": "120 दिन पर मिट्टी चढ़ाने से गन्ना गिरता नहीं है और सूखी पत्तियों की मल्चिंग नमी बचाती है।",
            "ta": "120வது நாளில் மண் அணைப்பது கரும்பு சாய்வதைத் தடுக்கும்; சருகு மூடாக்கு நீரைச் சேமிக்கும்.",
            "te": "120 రోజుల్లో మట్టి ఎగదోయడం వల్ల చెరకు పడిపోదు; ఆకు మల్చింగ్ తేమను కాపాడుతుంది.",
        },
        "guidelines": {
            "en": [
                "1. Sett Treatment & Planting: Plant 2-3 budded treated setts in furrows spaced 90-120 cm apart.",
                "2. Mulching: Spread sugarcane trash between rows to suppress weeds and conserve moisture.",
                "3. Earthing-up: Perform partial earthing-up at 45 days and full earthing-up at 120 days.",
                "4. Detrashing & Propping: Remove dry lower leaves at 5th and 7th months and prop canes.",
                "5. Harvest: Cut canes close to ground level when Brix reading reaches 18-20%.",
            ],
            "kn": [
                "1. ನಾಟಿ: ಬೀಜೋಪಚಾರ ಮಾಡಿದ 2-3 ಕಣ್ಣಿನ ತುಂಡುಗಳನ್ನು 90-120 ಸೆಂ.ಮೀ ಅಂತರದ ಸಾಲುಗಳಲ್ಲಿ ನಾಟಿ ಮಾಡಿ.",
                "2. ಹೊದಿಕೆ: ಕಳೆ ತಡೆಯಲು ಮತ್ತು ತೇವಾಂಶ ಉಳಿಸಲು ಸಾಲುಗಳ ಮಧ್ಯೆ ಕಬ್ಬಿನ ತರಗು ಹರಡಿ.",
                "3. ಮಣ್ಣು ಏರಿಸುವುದು: 45 ಮತ್ತು 120 ದಿನಗಳಲ್ಲಿ ಬುಡಕ್ಕೆ ಮಣ್ಣು ಏರಿಸಿ.",
                "4. ಒಣಗಿದ ಎಲೆ ತೆಗೆಯುವುದು: 5 ಮತ್ತು 7ನೇ ತಿಂಗಳಲ್ಲಿ ಒಣಗಿದ ಕೆಳ ಎಲೆಗಳನ್ನು ತೆಗೆದು ಕಬ್ಬು ಕಟ್ಟಿ.",
                "5. ಕಟಾವು: ಬ್ರಿಕ್ಸ್ ಪ್ರಮಾಣ 18-20% ತಲುಪಿದಾಗ ನೆಲಮಟ್ಟಕ್ಕೆ ಸಮೀಪವಾಗಿ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: उपचारित 2-3 आंख वाले टुकड़ों को 90-120 सेमी की दूरी वाली नालियों में बोएं।",
                "2. मल्चिंग: खरपतवार रोकने और नमी बचाने के लिए कतारों में सूखी पत्तियां बिछाएं।",
                "3. मिट्टी चढ़ाना: 45 दिन पर हल्की और 120 दिन पर पूरी मिट्टी चढ़ाएं।",
                "4. बंधाई: 5वें और 7वें महीने में सूखी निचली पत्तियां हटाकर गन्ने बांधें।",
                "5. कटाई: ब्रिक्स मान 18-20% पहुंचने पर जमीन की सतह के पास से कटाई करें।",
            ],
            "ta": [
                "1. நடவு: விதை நேர்த்தி செய்த 2-3 பரு கரணைகளை 90-120 செ.மீ பார்களில் நடவும்.",
                "2. மூடாக்கு: களை கட்டுப்படுத்த மற்றும் ஈரப்பதம் காக்க வரிசைகளுக்கு இடையே சருகு பரப்பவும்.",
                "3. மண் அணைத்தல்: 45 மற்றும் 120வது நாட்களில் மண் அணைக்கவும்.",
                "4. சோகை உரித்தல்: 5 மற்றும் 7வது மாதங்களில் காய்ந்த இலைகளை நீக்கி விட்டம் கட்டவும்.",
                "5. அறுவடை: சர்க்கரை அளவு (Brix) 18-20% எட்டும்போது அடியோடு வெட்டி அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. నాటు: శుద్ధి చేసిన 2-3 కణుపుల ముక్కలను 90-120 సెం.మీ సాళ్లలో నాటండి.",
                "2. మల్చింగ్: కలుపు నివారణకు, తేమకు వరుసల మధ్య చెరకు చెత్త పరచండి.",
                "3. మట్టి ఎగదోత: 45 మరియు 120 రోజుల్లో మొక్కల మొదళ్లకు మట్టి ఎగదోయండి.",
                "4. జడలు కట్టడం: 5, 7 నెలల్లో ఎండిన ఆకులు తీసి చెరకును ఊతమిచ్చి కట్టండి.",
                "5. కోత: బ్రిక్స్ విలువ 18-20% చేరినప్పుడు నేల మట్టానికి దగ్గరగా కోయండి.",
            ],
        },
    },
    {
        "name": "Millets (Ragi / Bajra / Jowar)",
        "scientific_name": "Eleusine coracana / Sorghum bicolor",
        "primary_soil": ["red", "sandy", "loamy"],
        "secondary_soil": ["black", "alluvial"],
        "primary_season": ["kharif", "zaid"],
        "secondary_season": ["rabi"],
        "ideal_rain": 500,
        "min_rain": 250,
        "max_rain": 850,
        "min_temp": 18,
        "max_temp": 35,
        "min_ph": 5.0,
        "max_ph": 8.2,
        "primary_water": ["low"],
        "secondary_water": ["medium"],
        "duration": "85 - 115 days",
        "temp": "18°C - 35°C",
        "ph_range": "5.0 - 8.2",
        "image_url": "https://agritech.tnau.ac.in/agriculture/CropProduction/Millets/millets_ragi_clip_image006.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Finger_millet",
        "overview": {
            "en": "Millets (Ragi, Bajra, Jowar) are hardy, climate-resilient Nutri-Cereals suited to low-rainfall dryland regions across India.",
            "kn": "ಸಿರಿಧಾನ್ಯಗಳು (ರಾಗಿ, ಸಜ್ಜೆ, ಜೋಳ) ಕಡಿಮೆ ಮಳೆ ಬೀಳುವ ಒಣಭೂಮಿ ಪ್ರದೇಶಗಳಿಗೆ ಅತ್ಯಂತ ಸೂಕ್ತವಾದ ಪೌಷ್ಟಿಕ ಬೆಳೆಗಳಾಗಿವೆ.",
            "hi": "मोटे अनाज (रागी, बाजरा, ज्वार) कम वर्षा वाले शुष्क क्षेत्रों के लिए अत्यंत सहनशील और पौष्टिक फसलें हैं।",
            "ta": "சிறுதானியங்கள் (ராகி, கம்பு, சோளம்) குறைந்த மழை பெறும் வறண்ட நிலங்களுக்கு ஏற்ற சத்தான பயிர்களாகும்.",
            "te": "చిరుధాన్యాలు (రాగి, సజ్జ, జొన్న) తక్కువ వర్షపాతం ఉన్న మెట్ట ప్రాంతాలకు అనువైన పోషక పంటలు.",
        },
        "fertilizer": {
            "en": "NPK 50:40:25 kg/ha with 5-7 tonnes FYM/ha; split Nitrogen once at 30 DAS.",
            "kn": "NPK 50:40:25 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ನೀಡಿ; 30 ದಿನಗಳಲ್ಲಿ ಅರ್ಧ ಸಾರಜನಕ ಕೊಡಿ.",
            "hi": "NPK 50:40:25 किग्रा/हेक्टेयर के साथ गोबर की खाद दें; 30 दिन पर आधा नाइट्रोजन डालें।",
            "ta": "NPK 50:40:25 கிலோ/எக்டர் உடன் தொழுவுரம் இடவும்; 30வது நாளில் பாதி தழைச்சத்து இடவும்.",
            "te": "NPK 50:40:25 కిలోలతో పాటు పశువుల ఎరువు వేసి, 30 రోజులకు సగం నత్రజని వేయండి.",
        },
        "tip": {
            "en": "Drought-tolerant by nature, but one protective irrigation at grain-filling boosts yield markedly.",
            "kn": "ಬರ ನಿರೋಧಕ ಬೆಳೆಯಾಗಿದ್ದರೂ ಕಾಳು ತುಂಬುವ ಹಂತದಲ್ಲಿ ಒಂದು ನೀರು ಕೊಟ್ಟರೆ ಇಳುವರಿ ಹೆಚ್ಚುತ್ತದೆ.",
            "hi": "यह सूखा सहनशील फसल है, लेकिन दाने भरते समय एक सिंचाई से उपज काफी बढ़ती है।",
            "ta": "வறட்சியைத் தாங்கும்; எனினும் மணி பிடிக்கும் பருவத்தில் ஒரு பாசனம் மகசூலை அதிகரிக்கும்.",
            "te": "ఇది కరువును తట్టుకుంటుంది, కానీ గింజలు నిండే దశలో ఒక తడి ఇస్తే దిగుబడి పెరుగుతుంది.",
        },
        "guidelines": {
            "en": [
                "1. Seedbed & Sowing: Sow treated seeds at 22.5-30 cm row spacing with onset of rain.",
                "2. Thinning: Thin crowded seedlings at 15-20 DAS to avoid competition.",
                "3. Intercultivation: Give one hoeing at 25-30 DAS to retain moisture and suppress weeds.",
                "4. Protective Irrigation: Provide life-saving irrigation if dry spell exceeds 20 days at flowering.",
                "5. Harvest: Harvest earheads when grains turn hard and moisture drops below 15%.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ಮಳೆ ಪ್ರಾರಂಭವಾದಾಗ ಬೀಜೋಪಚಾರ ಮಾಡಿದ ಬೀಜಗಳನ್ನು 22.5-30 ಸೆಂ.ಮೀ ಸಾಲಿನಲ್ಲಿ ಬಿತ್ತಿ.",
                "2. ಸಸಿ ತೆಳುಗೊಳಿಸುವಿಕೆ: 15-20 ದಿನಗಳಲ್ಲಿ ಒತ್ತಾದ ಸಸಿಗಳನ್ನು ತೆಳುಗೊಳಿಸಿ.",
                "3. ಎಡೆಕುಂಟೆ: 25-30 ದಿನಗಳಲ್ಲಿ ಎಡೆಕುಂಟೆ ಹೊಡೆದು ಕಳೆ ತೆಗೆಯಿರಿ.",
                "4. ರಕ್ಷಣಾತ್ಮಕ ನೀರಾವರಿ: ಹೂ ಬಿಡುವಾಗ ದೀರ್ಘ ಬರ ಬಂದರೆ ಒಂದು ಬಾರಿ ನೀರು ಕೊಡಿ.",
                "5. ಕಟಾವು: ತೆನೆಗಳಲ್ಲಿ ಕಾಳು ಗಟ್ಟಿಯಾದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: मानसून शुरू होने पर उपचारित बीज 22.5-30 सेमी कतार में बोएं।",
                "2. छंटाई: 15-20 दिन में घने पौधों की छंटाई करें।",
                "3. गुड़ाई: नमी बनाए रखने के लिए 25-30 दिन में निराई-गुड़ाई करें।",
                "4. रक्षक सिंचाई: फूल आते समय लंबा सूखा पड़ने पर एक सिंचाई दें।",
                "5. कटाई: दाने सख्त होने पर बालियां काट लें।",
            ],
            "ta": [
                "1. விதைப்பு: மழை தொடங்கியதும் 22.5-30 செ.மீ வரிசை இடைவெளியில் விதைக்கவும்.",
                "2. பயிர் களைதல்: 15-20 நாட்களில் நெருக்கமான செடிகளைக் களைந்து விடவும்.",
                "3. இடை உழவு: 25-30 நாட்களில் களை எடுத்து ஈரப்பதம் காக்கவும்.",
                "4. உயிர் தண்ணீர்: பூக்கும்போது வறட்சி நீடித்தால் ஒரு முறை நீர் பாய்ச்சவும்.",
                "5. அறுவடை: மணிகள் கடினமானதும் கதிர்களை அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: వర్షాలు పడిన వెంటనే 22.5-30 సెం.మీ వరుసల్లో విత్తండి.",
                "2. మొక్కల పలుచన: 15-20 రోజుల్లో దగ్గరగా ఉన్న మొక్కలను తీసివేయండి.",
                "3. అంతర కృషి: 25-30 రోజుల్లో గొర్రు తోలి కలుపు నివారించండి.",
                "4. రక్షక తడి: పూత సమయంలో ఎక్కువ రోజులు వర్షం లేకుంటే ఒక తడి ఇవ్వండి.",
                "5. కోత: కంకుల్లో గింజలు గట్టిపడినప్పుడు కోత కోయండి.",
            ],
        },
    },
    {
        "name": "Groundnut (Peanut)",
        "scientific_name": "Arachis hypogaea",
        "primary_soil": ["sandy", "loamy", "red"],
        "secondary_soil": ["alluvial"],
        "primary_season": ["kharif"],
        "secondary_season": ["rabi", "zaid"],
        "ideal_rain": 700,
        "min_rain": 500,
        "max_rain": 1000,
        "min_temp": 20,
        "max_temp": 35,
        "min_ph": 6.0,
        "max_ph": 6.5,
        "primary_water": ["medium"],
        "secondary_water": ["low"],
        "duration": "100 - 130 days",
        "temp": "20°C - 35°C",
        "ph_range": "6.0 - 6.5",
        "image_url": "https://media.bighaat.com/kvplus/articles/ba051c05-c4f7-47eb-97d3-67daf0ed189d.jpg?w=3840&q=80&format=webp&compress=true",
        "source_url": "https://en.wikipedia.org/wiki/Peanut",
        "overview": {
            "en": "Groundnut (Arachis hypogaea) is a major oilseed and legume crop that thrives in friable, well-drained sandy-loam and red soils for easy peg penetration.",
            "kn": "ಶೇಂಗಾ (Arachis hypogaea) ಪ್ರಮುಖ ಎಣ್ಣೆಕಾಳು ಬೆಳೆಯಾಗಿದ್ದು, ಸಡಿಲವಾದ ಮರಳು ಮಿಶ್ರಿತ ಗೋಡು ಮತ್ತು ಕೆಂಪು ಮಣ್ಣಿನಲ್ಲಿ ಉತ್ತಮವಾಗಿ ಬೆಳೆಯುತ್ತದೆ.",
            "hi": "मूंगफली (Arachis hypogaea) प्रमुख तिलहनी और दलहनी फसल है, जो भुरभुरी बलुई दोमट और लाल मिट्टी में खूब फलती है।",
            "ta": "நிலக்கடலை (Arachis hypogaea) முக்கிய எண்ணெய் வித்துப் பயிராகும்; விழுதுகள் இறங்க தளர்வான மணல் கலந்த செம்மண் சிறந்தது.",
            "te": "వేరుశనగ (Arachis hypogaea) ప్రధాన నూనెగింజల పంట; ఊడలు దిగడానికి గుల్లగా ఉండే ఇసుక లోమీ, ఎర్ర నేలలు చాలా అనుకూలం.",
        },
        "fertilizer": {
            "en": "NPK 20:40:40 kg/ha plus Gypsum (400-500 kg/ha) at flowering for proper pod filling.",
            "kn": "NPK 20:40:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಹೂ ಬಿಡುವಾಗ ಜಿಪ್ಸಂ (400-500 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) ನೀಡಿ.",
            "hi": "NPK 20:40:40 किग्रा/हेक्टेयर के साथ फूल आते समय जिप्सम (400-500 किग्रा/हेक्टेयर) डालें।",
            "ta": "NPK 20:40:40 கிலோ/எக்டர் உடன் பூக்கும் பருவத்தில் ஜிப்சம் (400-500 கிலோ) இடவும்.",
            "te": "NPK 20:40:40 కిలోలతో పాటు పూత దశలో జిప్సం (400-500 కిలోలు/హెక్టార్) వేయండి.",
        },
        "tip": {
            "en": "Avoid deep weeding after pegging starts (40-45 DAS) so developing pegs are not disturbed.",
            "kn": "40-45 ದಿನಗಳ ನಂತರ ಕಾಯಿ ಇಳಿಯುವ ಹಂತದಲ್ಲಿ ಆಳವಾಗಿ ಕಳೆ ತೆಗೆಯಬೇಡಿ.",
            "hi": "40-45 दिन बाद खूंटियां (pegs) बनते समय गहरी गुड़ाई न करें।",
            "ta": "40-45 நாட்களில் விழுது இறங்கும் போது ஆழமாகக் களை எடுக்க வேண்டாம்.",
            "te": "40-45 రోజుల తర్వాత ఊడలు దిగే సమయంలో లోతుగా కలుపు తీయవద్దు.",
        },
        "guidelines": {
            "en": [
                "1. Seed Treatment: Treat kernels with Rhizobium culture and fungicide before sowing.",
                "2. Sowing: Sow at 30x10 cm spacing at 4-5 cm depth in friable soil.",
                "3. Gypsum & Earthing: Apply gypsum at 35-40 DAS around root zone and lightly earth up.",
                "4. Irrigation: Keep soil moist during flowering and pegging; avoid standing water.",
                "5. Harvest: Pull plants when inner shells show dark veins and 75% pods mature.",
            ],
            "kn": [
                "1. ಬೀಜೋಪಚಾರ: ಬಿತ್ತನೆಗೆ ಮುನ್ನ ರೈಜೋಬಿಯಂ ಮತ್ತು ಶಿಲೀಂಧ್ರನಾಶಕದಿಂದ ಬೀಜೋಪಚಾರ ಮಾಡಿ.",
                "2. ಬಿತ್ತನೆ: ಸಡಿಲ ಮಣ್ಣಿನಲ್ಲಿ 30x10 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ 4-5 ಸೆಂ.ಮೀ ಆಳದಲ್ಲಿ ಬಿತ್ತಿ.",
                "3. ಜಿಪ್ಸಂ ಬಳಕೆ: 35-40 ದಿನಗಳಲ್ಲಿ ಗಿಡದ ಬುಡಕ್ಕೆ ಜಿಪ್ಸಂ ಹಾಕಿ ಹಗುರವಾಗಿ ಮಣ್ಣು ಏರಿಸಿ.",
                "4. ನೀರಾವರಿ: ಹೂವು ಮತ್ತು ಕಾಯಿ ಕಟ್ಟುವಾಗ ತೇವಾಂಶ ಕಾಪಾಡಿ; ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿ.",
                "5. ಕಟಾವು: ಶೇ. 75 ರಷ್ಟು ಕಾಯಿಗಳು ಬಲಿತಾಗ ಮತ್ತು ಒಳಭಾಗ ಕಪ್ಪಾದಾಗ ಕಿತ್ತು ಒಣಗಿಸಿ.",
            ],
            "hi": [
                "1. बीज उपचार: बुवाई से पहले बीजों को राइजोबियम और फफूंदनाशी से उपचारित करें।",
                "2. बुवाई: भुरभुरी मिट्टी में 30x10 सेमी की दूरी पर 4-5 सेमी गहराई में बोएं।",
                "3. जिप्सम व मिट्टी चढ़ाना: 35-40 दिन पर जड़ों के पास जिप्सम डालकर हल्की मिट्टी चढ़ाएं।",
                "4. सिंचाई: फूल व खूंटी बनते समय नमी बनाए रखें; जलभराव से बचें।",
                "5. कटाई: 75% फलियां पकने और छिलके के अंदर गहरे निशान दिखने पर खुदाई करें।",
            ],
            "ta": [
                "1. விதை நேர்த்தி: விதைப்பதற்கு முன் ரைசோபியம் மற்றும் பூஞ்சாணக் கொல்லி கொண்டு நேர்த்தி செய்யவும்.",
                "2. விதைப்பு: 30x10 செ.மீ இடைவெளியில் 4-5 செ.மீ ஆழத்தில் விதைக்கவும்.",
                "3. ஜிப்சம் & மண் அணைத்தல்: 35-40 நாட்களில் ஜிப்சம் இட்டு மண் அணைக்கவும்.",
                "4. நீர்ப்பாசனம்: பூக்கும் மற்றும் விழுது இறங்கும் போது ஈரப்பதம் காக்கவும்.",
                "5. அறுவடை: 75% காய்கள் முற்றி ஓட்டின் உட்புறம் கருமையாகும் போது அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తన శుద్ధి: విత్తే ముందు రైజోబియం మరియు శిలీంధ్రనాశనితో శుద్ధి చేయండి.",
                "2. విత్తడం: గుల్ల నేలలో 30x10 సెం.మీ దూరంలో 4-5 సెం.మీ లోతులో విత్తండి.",
                "3. జిప్సం: 35-40 రోజుల్లో మొక్కల వద్ద జిప్సం వేసి తేలికగా మట్టి ఎగదోయండి.",
                "4. నీటిపారుదల: పూత, ఊడల దశలో తేమ ఉండేలా చూడండి; నీరు నిలవనీయవద్దు.",
                "5. కోత: 75% కాయలు ముదిరి లోపలి పొర నల్లబడినప్పుడు తవ్వి తీయండి.",
            ],
        },
    },
    {
        "name": "Soybean",
        "scientific_name": "Glycine max",
        "primary_soil": ["black", "loamy"],
        "secondary_soil": ["alluvial", "clay"],
        "primary_season": ["kharif"],
        "secondary_season": ["monsoon"],
        "ideal_rain": 700,
        "min_rain": 500,
        "max_rain": 900,
        "min_temp": 15,
        "max_temp": 32,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["medium"],
        "secondary_water": ["low", "high"],
        "duration": "90 - 110 days",
        "temp": "15°C - 32°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://www.aces.edu/wp-content/uploads/2022/05/Figure-illustrative.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Soybean",
        "overview": {
            "en": "Soybean (Glycine max) is India's premier Kharif oilseed and protein crop, widely cultivated in Madhya Pradesh, Maharashtra, and Karnataka.",
            "kn": "ಸೋಯಾಬೀನ್ (Glycine max) ಪ್ರಮುಖ ಖಾರಿಫ್ ಎಣ್ಣೆಕಾಳು ಮತ್ತು ಪ್ರೋಟೀನ್ ಬೆಳೆಯಾಗಿದ್ದು, ಕಪ್ಪು ಮತ್ತು ಗೋಡು ಮಣ್ಣಿನಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತದೆ.",
            "hi": "सोयाबीन (Glycine max) भारत की प्रमुख खरीफ तिलहनी व प्रोटीन फसल है, जो काली और दोमट मिट्टी में खूब होती है।",
            "ta": "சோயாபீன்ஸ் (Glycine max) முக்கிய கரீஃப் எண்ணெய் வித்து மற்றும் புரதப் பயிராகும்; கரிசல் மற்றும் வண்டல் மண்ணில் நன்கு வளரும்.",
            "te": "సోయాబీన్ (Glycine max) ప్రధాన ఖరీఫ్ నూనెగింజ మరియు ప్రోటీన్ పంట; నల్ల రేగడి, లోమీ నేలల్లో బాగా పండుతుంది.",
        },
        "fertilizer": {
            "en": "NPK 20:60:40 kg/ha plus Sulphur (20 kg/ha) and Rhizobium seed inoculation.",
            "kn": "NPK 20:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಗಂಧಕ (20 ಕೆಜಿ) ಮತ್ತು ರೈಜೋಬಿಯಂ ಬೀಜೋಪಚಾರ ಮಾಡಿ.",
            "hi": "NPK 20:60:40 किग्रा/हेक्टेयर के साथ सल्फर (20 किग्रा) और राइजोबियम बीज उपचार करें।",
            "ta": "NPK 20:60:40 கிலோ/எக்டர் உடன் கந்தகம் (20 கிலோ) மற்றும் ரைசோபியம் விதை நேர்த்தி செய்யவும்.",
            "te": "NPK 20:60:40 కిలోలతో పాటు సల్ఫర్ (20 కిలోలు) మరియు రైజోబియం విత్తన శుద్ధి చేయండి.",
        },
        "tip": {
            "en": "Ensure good drainage in black soil; harvest promptly when pods turn golden brown to prevent shattering.",
            "kn": "ಕಪ್ಪು ಮಣ್ಣಿನಲ್ಲಿ ನೀರು ಬಸಿದುಹೋಗುವಂತೆ ನೋಡಿ; ಕಾಯಿ ಒಣಗಿ ಸಿಡಿಯುವ ಮುನ್ನ ಕಟಾವು ಮಾಡಿ.",
            "hi": "काली मिट्टी में जल निकासी रखें और फलियां भूरे रंग की होते ही कटाई करें ताकि दाने न झड़ें।",
            "ta": "கரிசல் மண்ணில் நீர் தேங்காமல் பார்த்து, காய்கள் வெடிக்கும் முன் அறுவடை செய்யவும்.",
            "te": "నల్ల నేలల్లో నీరు నిలవకుండా చూసి, కాయలు పగిలిపోకముందే కోత కోయండి.",
        },
        "guidelines": {
            "en": [
                "1. Ridge/Broad-bed Planting: Plant at 45x5 cm spacing on broad-bed furrows to prevent waterlogging.",
                "2. Seed Inoculation: Treat with Rhizobium japonicum before sowing for nitrogen fixation.",
                "3. Weed Management: Control weeds between 20 and 35 DAS.",
                "4. Pest Watch: Monitor for girdle beetle and leaf-eating caterpillars.",
                "5. Harvest: Harvest when leaves yellow and drop and pods rattle.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನೀರು ನಿಲ್ಲದಂತೆ ಏರುಮಡಿಗಳಲ್ಲಿ 45x5 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಬಿತ್ತಿ.",
                "2. ಬೀಜೋಪಚಾರ: ಸಾರಜನಕ ಸ್ಥಿರೀಕರಣಕ್ಕಾಗಿ ರೈಜೋಬಿಯಂ ಲೇಪನ ಮಾಡಿ.",
                "3. ಕಳೆ ನಿಯಂತ್ರಣ: 20 ರಿಂದ 35 ದಿನಗಳ ಒಳಗೆ ಕಳೆ ತೆಗೆಯಿರಿ.",
                "4. ಕೀಟ ನಿಗಾ: ಎಲೆ ತಿನ್ನುವ ಹುಳು ಮತ್ತು ಕಾಂಡದ ಕೀಟಗಳನ್ನು ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ಎಲೆಗಳು ಹಳದಿಯಾಗಿ ಉದುರಿದಾಗ ಮತ್ತು ಕಾಯಿ ಗಟ್ಟಿಯಾದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. मेड़ बुवाई: जलभराव से बचने के लिए चौड़ी मेड़ पर 45x5 सेमी दूरी पर बोएं।",
                "2. बीज उपचार: राइजोबियम जैपोनिकम से बीज उपचारित करें।",
                "3. खरपतवार प्रबंधन: 20 से 35 दिन के बीच निराई-गुड़ाई करें।",
                "4. कीट नियंत्रण: गर्डल बीटल और पत्ती खाने वाली इल्ली पर नजर रखें।",
                "5. कटाई: पत्तियां पीली होकर गिरने और फलियां सूखने पर कटाई करें।",
            ],
            "ta": [
                "1. பார் விதைப்பு: நீர் தேங்காமல் அகலப் பார்களில் 45x5 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "2. விதை நேர்த்தி: ரைசோபியம் உயிர் உரத்துடன் விதை நேர்த்தி செய்யவும்.",
                "3. களை மேலாண்மை: 20 முதல் 35 நாட்களுக்குள் களைகளைக் கட்டுப்படுத்தவும்.",
                "4. பூச்சி கண்காணிப்பு: தண்டு வண்டு மற்றும் இலை உண்ணும் புழுக்களைக் கண்காணிக்கவும்.",
                "5. அறுவடை: இலைகள் உதிர்ந்து காய்கள் காய்ந்ததும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. వెడల్పు బోదెలు: నీరు నిలవకుండా వెడల్పు బోదెలపై 45x5 సెం.మీ దూరంలో విత్తండి.",
                "2. విత్తన శుద్ధి: నత్రజని కోసం రైజోబియంతో విత్తన శుద్ధి చేయండి.",
                "3. కలుపు నియంత్రణ: 20 నుండి 35 రోజుల మధ్య కలుపు తీయండి.",
                "4. పురుగుల పర్యవేక్షణ: ఆకు తినే పురుగులు, గర్డిల్ బీటిల్‌ను గమనించండి.",
                "5. కోత: ఆకులు పసుపు రంగులోకి మారి రాలినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Chickpea (Bengal Gram / Chana)",
        "scientific_name": "Cicer arietinum",
        "primary_soil": ["black", "loamy"],
        "secondary_soil": ["alluvial", "clay"],
        "primary_season": ["rabi"],
        "secondary_season": ["winter"],
        "ideal_rain": 450,
        "min_rain": 300,
        "max_rain": 700,
        "min_temp": 15,
        "max_temp": 30,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["low"],
        "secondary_water": ["medium"],
        "duration": "95 - 120 days",
        "temp": "15°C - 30°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://mapmycrop.com/wp-content/uploads/2026/10/chickpea-plant-with-pods-wikimedia-commons.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Chickpea",
        "overview": {
            "en": "Chickpea (Cicer arietinum) is India's largest Rabi pulse crop, grown mainly on residual soil moisture in cool, dry winters.",
            "kn": "ಕಡಲೆ (Cicer arietinum) ಭಾರತದ ಪ್ರಮುಖ ಹಿಂಗಾರು ದ್ವಿದಳ ಧಾನ್ಯವಾಗಿದ್ದು, ಮಣ್ಣಿನ ಉಳಿದ ತೇವಾಂಶದಲ್ಲಿ ತಂಪಾದ ಚಳಿಗಾಲದಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತದೆ.",
            "hi": "चना (Cicer arietinum) भारत की प्रमुख रबी दलहन फसल है, जो ठंडे और शुष्क मौसम में मिट्टी की बची नमी पर उगती है।",
            "ta": "கொண்டைக்கடலை (Cicer arietinum) குளிர்காலத்தில் மண்ணின் ஈரப்பதத்தில் வளரும் முக்கிய ரபி பயறு வகை பயிராகும்.",
            "te": "శనగ (Cicer arietinum) చలికాలంలో నేలలోని మిగిలిన తేమతో పండే భారతదేశపు ప్రధాన రబీ పప్పుధాన్య పంట.",
        },
        "fertilizer": {
            "en": "NPK 20:40:20 kg/ha plus 20 kg Sulphur/ha at sowing; spray 2% Urea at flowering if dry.",
            "kn": "NPK 20:40:20 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಗಂಧಕ (20 ಕೆಜಿ); ಹೂ ಬಿಡುವಾಗ ಒಣ ವಾತಾವರಣವಿದ್ದರೆ 2% ಯೂರಿಯಾ ಸಿಂಪಡಿಸಿ.",
            "hi": "NPK 20:40:20 किग्रा/हेक्टेयर व 20 किग्रा सल्फर बुवाई में दें; सूखे में फूल पर 2% यूरिया छिड़कें।",
            "ta": "NPK 20:40:20 கிலோ/எக்டர் உடன் கந்தகம் (20 கிலோ) இடவும்.",
            "te": "NPK 20:40:20 కిలోలతో పాటు 20 కిలోల సల్ఫర్ విత్తేటప్పుడు వేయండి.",
        },
        "tip": {
            "en": "Nipping terminal buds at 30-35 DAS increases branching and pod count; avoid excess irrigation.",
            "kn": "30-35 ದಿನಗಳಲ್ಲಿ ಕುಡಿ ಚಿವುಟುವುದರಿಂದ (nipping) ಹೆಚ್ಚು ಕವಲುಗಳು ಮತ್ತು ಕಾಯಿಗಳು ಬರುತ್ತವೆ.",
            "hi": "30-35 दिन पर ऊपरी कोंपलें तोड़ने (निपिंग) से शाखाएं और फलियां बढ़ती हैं; अधिक सिंचाई न करें।",
            "ta": "30-35 நாட்களில் நுனி கிள்ளுதல் (Nipping) செய்வதால் கிளைகள் மற்றும் காய்கள் அதிகரிக்கும்.",
            "te": "30-35 రోజుల్లో కొసలు తుంచడం (Nipping) వల్ల కొమ్మలు, కాయలు ఎక్కువగా వస్తాయి.",
        },
        "guidelines": {
            "en": [
                "1. Seed Treatment: Treat seeds with Trichoderma and Rhizobium to prevent wilt.",
                "2. Sowing: Sow at 30x10 cm spacing at 7-10 cm depth in October-November.",
                "3. Nipping: Nip top shoots at 30-35 DAS to promote lateral branches.",
                "4. Pod Borer Control: Install bird perches (15/ha) and pheromone traps for Helicoverpa.",
                "5. Harvest: Harvest when pods turn straw-brown and seeds rattle.",
            ],
            "kn": [
                "1. ಬೀಜೋಪಚಾರ: ಬಾಡು ರೋಗ ತಡೆಯಲು ಟ್ರೈಕೋಡರ್ಮಾ ಮತ್ತು ರೈಜೋಬಿಯಂ ಲೇಪನ ಮಾಡಿ.",
                "2. ಬಿತ್ತನೆ: ಅಕ್ಟೋಬರ್-ನವೆಂಬರ್‌ನಲ್ಲಿ 30x10 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಬಿತ್ತಿ.",
                "3. ಕುಡಿ ಚಿವುಟುವಿಕೆ: 30-35 ದಿನಗಳಲ್ಲಿ ಗಿಡದ ಮೇಲ್ಭಾಗದ ಕುಡಿ ಚಿವುಟಿ.",
                "4. ಕಾಯಿಕೊರಕ ನಿಯಂತ್ರಣ: ಹಕ್ಕಿ ಕೂರುವ ಕಂಬಗಳು ಮತ್ತು ಮೋಹಕ ಬಲೆಗಳನ್ನು ಅಳವಡಿಸಿ.",
                "5. ಕಟಾವು: ಕಾಯಿಗಳು ಕಂದು ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बीज उपचार: उकठा रोग से बचाव के लिए ट्राइकोडर्मा व राइजोबियम से उपचार करें।",
                "2. बुवाई: अक्टूबर-नवंबर में 30x10 सेमी दूरी पर 7-10 सेमी गहराई में बोएं।",
                "3. निपिंग: अधिक शाखाओं के लिए 30-35 दिन पर ऊपरी कोंपल तोड़ें।",
                "4. फली छेदक नियंत्रण: पक्षी बैठने की खूंटियां (15/हेक्टेयर) व फेरोमोन ट्रैप लगाएं।",
                "5. कटाई: फलियां भूरे रंग की होने पर कटाई करें।",
            ],
            "ta": [
                "1. விதை நேர்த்தி: வாடல் நோயைத் தடுக்க டிரைக்கோடெர்மா மற்றும் ரைசோபியம் கொண்டு நேர்த்தி செய்யவும்.",
                "2. விதைப்பு: அக்டோபர்-நவம்பரில் 30x10 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "3. நுனி கிள்ளுதல்: கிளைகள் அதிகரிக்க 30-35 நாட்களில் நுனியைக் கிள்ளவும்.",
                "4. காய்ப்புழு கட்டுப்பாடு: பறவை இருக்கைகள் மற்றும் இனக்கவர்ச்சிப் பொறிகளைப் பயன்படுத்தவும்.",
                "5. அறுவடை: காய்கள் பழுப்பு நிறமாக மாறியதும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తన శుద్ధి: ఎండు తెగులు నివారణకు ట్రైకోడెర్మా, రైజోబియంతో శుద్ధి చేయండి.",
                "2. విత్తడం: అక్టోబర్-నవంబర్‌లో 30x10 సెం.మీ దూరంలో విత్తండి.",
                "3. కొసలు తుంచడం: కొమ్మలు పెరిగేందుకు 30-35 రోజుల్లో కొసలు తుంచండి.",
                "4. శనగపచ్చ పురుగు నియంత్రణ: పక్షి స్థావరాలు, ఫెరమోన్ ఎరలు అమర్చండి.",
                "5. కోత: కాయలు ఎండి గోధుమ రంగులోకి మారినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Potato",
        "scientific_name": "Solanum tuberosum",
        "primary_soil": ["loamy", "sandy", "alluvial"],
        "secondary_soil": ["red"],
        "primary_season": ["rabi"],
        "secondary_season": ["kharif"],
        "ideal_rain": 500,
        "min_rain": 350,
        "max_rain": 750,
        "min_temp": 12,
        "max_temp": 25,
        "min_ph": 5.2,
        "max_ph": 6.4,
        "primary_water": ["medium", "high"],
        "secondary_water": ["low"],
        "duration": "85 - 110 days",
        "temp": "12°C - 25°C",
        "ph_range": "5.2 - 6.4",
        "image_url": "https://plantix.net/en/library/assets/custom/crop-images/potato.jpeg",
        "source_url": "https://en.wikipedia.org/wiki/Potato",
        "overview": {
            "en": "Potato (Solanum tuberosum) is a high-yielding cool-season tuber crop preferring loose, well-drained sandy-loam soils.",
            "kn": "ಆಲೂಗಡ್ಡೆ (Solanum tuberosum) ತಂಪಾದ ಹವಾಮಾನ ಮತ್ತು ಸಡಿಲವಾದ ಮರಳು ಮಿಶ್ರಿತ ಗೋಡು ಮಣ್ಣಿನಲ್ಲಿ ಹೆಚ್ಚಿನ ಇಳುವರಿ ನೀಡುವ ಗೆಡ್ಡೆ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "आलू (Solanum tuberosum) ठंडे मौसम की अधिक उपज देने वाली कंद फसल है, जिसे भुरभुरी बलुई दोमट मिट्टी पसंद है।",
            "ta": "உருளைக்கிழங்கு (Solanum tuberosum) குளிர்காலத்தில் தளர்வான மணல் கலந்த மண்ணில் அதிக மகசூல் தரும் கிழங்குப் பயிராகும்.",
            "te": "బంగాళాదుంప (Solanum tuberosum) చల్లని వాతావరణంలో, గుల్లగా ఉండే ఇసుక లోమీ నేలల్లో అధిక దిగుబడినిచ్చే దుంప పంట.",
        },
        "fertilizer": {
            "en": "NPK 150:80:100 kg/ha with 20 tonnes well-rotted FYM/ha; apply Potash for tuber quality.",
            "kn": "NPK 150:80:100 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ; ಗೆಡ್ಡೆ ಗುಣಮಟ್ಟಕ್ಕೆ ಪೊಟ್ಯಾಶ್ ಅಗತ್ಯ.",
            "hi": "NPK 150:80:100 किग्रा/हेक्टेयर व गोबर खाद दें; कंद की गुणवत्ता के लिए पोटाश जरूरी है।",
            "ta": "NPK 150:80:100 கிலோ/எக்டர் உடன் தொழுவுரம் இடவும்; கிழங்கு தரத்திற்கு சாம்பல் சத்து அவசியம்.",
            "te": "NPK 150:80:100 కిలోలతో పాటు పశువుల ఎరువు వేయండి; దుంప నాణ్యతకు పొటాష్ అవసరం.",
        },
        "tip": {
            "en": "Perform earthing-up at 25-30 days so developing tubers are not exposed to sunlight and turn green.",
            "kn": "25-30 ದಿನಗಳಲ್ಲಿ ಮಣ್ಣು ಏರಿಸುವುದರಿಂದ ಗೆಡ್ಡೆಗಳು ಬಿಸಿಲಿಗೆ ಹಸಿರು ಬಣ್ಣಕ್ಕೆ ತಿರುಗುವುದಿಲ್ಲ.",
            "hi": "25-30 दिन पर मिट्टी चढ़ाएं ताकि कंद धूप के संपर्क में आकर हरे न पड़ें।",
            "ta": "25-30 நாட்களில் மண் அணைப்பதால் கிழங்குகள் வெயிலில் பச்சையாக மாறாது.",
            "te": "25-30 రోజుల్లో మట్టి ఎగదోస్తే దుంపలు ఎండకు పచ్చగా మారవు.",
        },
        "guidelines": {
            "en": [
                "1. Tuber Prep: Plant disease-free sprouted seed tubers (25-40 g) at 60x20 cm spacing.",
                "2. Earthing-up: Earth up ridges at 25-30 DAP along with top-dressed Nitrogen.",
                "3. Light Irrigation: Give light, frequent irrigations; stop watering 10 days before harvest.",
                "4. Blight Protection: Watch for Late Blight in foggy, cool weather.",
                "5. Dehaulming & Harvest: Cut haulms 10 days before digging so tuber skin sets firmly.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ಮೊಳಕೆಯೊಡೆದ ರೋಗಮುಕ್ತ ಬೀಜದ ಗೆಡ್ಡೆಗಳನ್ನು 60x20 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ನೆಡಿ.",
                "2. ಮಣ್ಣು ಏರಿಸುವುದು: 25-30 ದಿನಗಳಲ್ಲಿ ಸಾರಜನಕ ನೀಡಿ ಬುಡಕ್ಕೆ ಮಣ್ಣು ಏರಿಸಿ.",
                "3. ನೀರಾವರಿ: ಲಘುವಾಗಿ ನಿಯಮಿತ ನೀರು ಕೊಡಿ; ಕಟಾವಿಗೆ 10 ದಿನ ಮೊದಲು ನೀರು ನಿಲ್ಲಿಸಿ.",
                "4. ರೋಗ ನಿಗಾ: ಮಂಜು ಮತ್ತು ತಂಪು ಹವಾಮಾನದಲ್ಲಿ ಅಂಗಮಾರಿ (Late Blight) ರೋಗ ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ಅಗೆಯುವ 10 ದಿನ ಮೊದಲು ಗಿಡ ಕತ್ತರಿಸಿ ಗೆಡ್ಡೆಯ ಸಿಪ್ಪೆ ಗಟ್ಟಿಯಾಗಲು ಬಿಡಿ.",
            ],
            "hi": [
                "1. बुवाई: अंकुरित रोग-मुक्त बीज कंद 60x20 सेमी दूरी पर मेड़ों में लगाएं।",
                "2. मिट्टी चढ़ाना: 25-30 दिन पर नाइट्रोजन देकर मिट्टी चढ़ाएं।",
                "3. हल्की सिंचाई: नियमित हल्की सिंचाई करें; खुदाई से 10 दिन पहले पानी बंद करें।",
                "4. झुलसा बचाव: कोहरे व ठंड में पछेती झुलसा रोग की निगरानी करें।",
                "5. कटाई: खुदाई से 10 दिन पहले पत्तियां काट दें ताकि छिलका सख्त हो जाए।",
            ],
            "ta": [
                "1. நடவு: நோயற்ற முளைத்த விதைக்கிழங்குகளை 60x20 செ.மீ இடைவெளியில் நடவும்.",
                "2. மண் அணைத்தல்: 25-30 நாட்களில் தழைச்சத்து இட்டு மண் அணைக்கவும்.",
                "3. நீர்ப்பாசனம்: அடிக்கடி லேசான பாசனம் செய்து அறுவடைக்கு 10 நாட்கள் முன் நிறுத்தவும்.",
                "4. கருகல் நோய்: பனி மற்றும் குளிரில் பின்பருவ கருகல் நோயைக் கண்காணிக்கவும்.",
                "5. அறுவடை: தோண்டுவதற்கு 10 நாட்களுக்கு முன் தண்டுகளை வெட்டி தோலை கெட்டிப்படுத்தவும்.",
            ],
            "te": [
                "1. విత్తడం: మొలకెత్తిన ఆరోగ్యకరమైన విత్తన దుంపలను 60x20 సెం.మీ దూరంలో నాటండి.",
                "2. మట్టి ఎగదోత: 25-30 రోజుల్లో నత్రజని వేసి మట్టి ఎగదోయండి.",
                "3. నీటిపారుదల: తేలికపాటి తడులు ఇచ్చి తవ్వకానికి 10 రోజుల ముందు ఆపండి.",
                "4. ఆకు మాడు తెగులు: చలి, మంచు వాతావరణంలో లేట్ బ్లైట్ తెగులును గమనించండి.",
                "5. తవ్వకం: తవ్వడానికి 10 రోజుల ముందు కాండాలు కోసి దుంప తొక్క గట్టిపడేలా చూడండి.",
            ],
        },
    },
    {
        "name": "Mustard (Rapeseed-Mustard)",
        "scientific_name": "Brassica juncea",
        "primary_soil": ["loamy", "alluvial"],
        "secondary_soil": ["sandy", "black"],
        "primary_season": ["rabi"],
        "secondary_season": ["winter"],
        "ideal_rain": 400,
        "min_rain": 240,
        "max_rain": 750,
        "min_temp": 10,
        "max_temp": 25,
        "min_ph": 5.5,
        "max_ph": 6.8,
        "primary_water": ["low", "medium"],
        "secondary_water": ["high"],
        "duration": "110 - 135 days",
        "temp": "10°C - 25°C",
        "ph_range": "5.5 - 6.8",
        "image_url": "https://weedsofmelbourne.org/wp-content/uploads/2021/10/field-mustard-brassica-rapa-a-yellow-flowering-turnip-sometimes-grown-as-a-fallow-or-forage-crop.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Brassica_juncea",
        "overview": {
            "en": "Indian Mustard (Brassica juncea) is a vital Rabi oilseed crop requiring cool weather during growth and clear skies during pod maturity.",
            "kn": "ಸಾಸಿವೆ (Brassica juncea) ಪ್ರಮುಖ ಹಿಂಗಾರು ಎಣ್ಣೆಕಾಳು ಬೆಳೆಯಾಗಿದ್ದು, ಬೆಳವಣಿಗೆಗೆ ತಂಪು ಮತ್ತು ಕಾಯಿ ಮಾಗಲು ಶುಭ್ರ ಆಕಾಶ ಬಯಸುತ್ತದೆ.",
            "hi": "सरसों (Brassica juncea) भारत की प्रमुख रबी तिलहनी फसल है, जिसे बढ़वार में ठंड और पकते समय साफ मौसम चाहिए।",
            "ta": "கடுகு (Brassica juncea) குளிர்காலத்தில் நன்கு வளரும் முக்கிய ரபி எண்ணெய் வித்துப் பயிராகும்.",
            "te": "ఆవాలు (Brassica juncea) చలికాలంలో పెరిగి, కాయలు పండేటప్పుడు స్వచ్ఛమైన వాతావరణాన్ని కోరుకునే రబీ నూనెగింజ పంట.",
        },
        "fertilizer": {
            "en": "NPK 80:40:40 kg/ha plus 40 kg Sulphur/ha to boost oil content.",
            "kn": "ಎಣ್ಣೆ ಅಂಶ ಹೆಚ್ಚಿಸಲು NPK 80:40:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಗಂಧಕ (40 ಕೆಜಿ) ನೀಡಿ.",
            "hi": "तेल की मात्रा बढ़ाने के लिए NPK 80:40:40 किग्रा/हेक्टेयर के साथ 40 किग्रा सल्फर दें।",
            "ta": "எண்ணெய் சத்தை அதிகரிக்க NPK 80:40:40 கிலோ/எக்டர் உடன் 40 கிலோ கந்தகம் இடவும்.",
            "te": "నూనె శాతం పెరిగేందుకు NPK 80:40:40 కిలోలతో పాటు 40 కిలోల సల్ఫర్ వేయండి.",
        },
        "tip": {
            "en": "Timely sowing in October minimizes aphid attack; give two irrigations at pre-flowering and pod filling.",
            "kn": "ಅಕ್ಟೋಬರ್‌ನಲ್ಲಿ ಸಕಾಲಕ್ಕೆ ಬಿತ್ತನೆ ಮಾಡಿದರೆ ಹೇನು ಬಾಧೆ ಕಡಿಮೆ; ಹೂವು ಮತ್ತು ಕಾಯಿ ಹಂತದಲ್ಲಿ ನೀರು ಕೊಡಿ.",
            "hi": "अक्टूबर में समय पर बुवाई से माहू (चेपा) का प्रकोप कम होता है; फूल व फली अवस्था में सिंचाई करें।",
            "ta": "அக்டோபரில் சரியான நேரத்தில் விதைத்தால் அசுவினி தாக்குதல் குறையும்.",
            "te": "అక్టోబర్‌లో సకాలంలో విత్తితే పేనుబంక బెడద తగ్గుతుంది; పూత, కాయ దశలో నీరు ఇవ్వండి.",
        },
        "guidelines": {
            "en": [
                "1. Fine Seedbed: Prepare a fine seedbed and sow 4-5 kg/ha seed at 30-45 cm row spacing.",
                "2. Thinning: Thin plants to 10-15 cm apart at 15-20 DAS.",
                "3. Irrigation: Irrigate at pre-flowering (30-35 DAS) and pod development (60-70 DAS).",
                "4. Aphid Control: Monitor yellow mustard aphids in January-February.",
                "5. Harvest: Harvest when 75-80% of siliquae (pods) turn yellow.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನುಣ್ಣಗಿನ ಮಣ್ಣಿನಲ್ಲಿ ಹೆಕ್ಟೇರ್‌ಗೆ 4-5 ಕೆಜಿ ಬೀಜವನ್ನು 30-45 ಸೆಂ.ಮೀ ಸಾಲಿನಲ್ಲಿ ಬಿತ್ತಿ.",
                "2. ಸಸಿ ತೆಳುಗೊಳಿಸುವಿಕೆ: 15-20 ದಿನಗಳಲ್ಲಿ ಸಸಿಗಳ ನಡುವೆ 10-15 ಸೆಂ.ಮೀ ಅಂತರ ಕಾಪಾಡಿ.",
                "3. ನೀರಾವರಿ: ಹೂ ಬಿಡುವ ಮುನ್ನ (30-35 ದಿನ) ಮತ್ತು ಕಾಯಿ ಕಟ್ಟುವಾಗ (60-70 ದಿನ) ನೀರು ಕೊಡಿ.",
                "4. ಹೇನು ನಿಯಂತ್ರಣ: ಜನವರಿ-ಫೆಬ್ರವರಿಯಲ್ಲಿ ಹೇನು ಬಾಧೆಯನ್ನು ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ಶೇ. 75-80 ಕಾಯಿಗಳು ಹಳದಿ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: भुरभुरी मिट्टी में 4-5 किग्रा/हेक्टेयर बीज 30-45 सेमी कतार में बोएं।",
                "2. छंटाई: 15-20 दिन में पौधों के बीच 10-15 सेमी दूरी रखें।",
                "3. सिंचाई: फूल आने से पहले (30-35 दिन) और फली भरते समय (60-70 दिन) पानी दें।",
                "4. माहू नियंत्रण: जनवरी-फरवरी में चेपा (माहू) कीट की निगरानी करें।",
                "5. कटाई: 75-80% फलियां पीली पड़ने पर कटाई करें।",
            ],
            "ta": [
                "1. விதைப்பு: 4-5 கிலோ/எக்டர் விதையை 30-45 செ.மீ வரிசை இடைவெளியில் விதைக்கவும்.",
                "2. பயிர் களைதல்: 15-20 நாட்களில் செடிகளுக்கு இடையே 10-15 செ.மீ இடைவெளி விடவும்.",
                "3. நீர்ப்பாசனம்: பூக்கும் முன் (30-35 நாள்) மற்றும் காய் பிடிக்கும்போது (60-70 நாள்) நீர் பாய்ச்சவும்.",
                "4. அசுவினி கட்டுப்பாடு: ஜனவரி-பிப்ரவரியில் அசுவினிப் பூச்சிகளைக் கண்காணிக்கவும்.",
                "5. அறுவடை: 75-80% காய்கள் மஞ்சளாக மாறியதும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: హెక్టారుకు 4-5 కిలోల విత్తనాన్ని 30-45 సెం.మీ వరుసల్లో విత్తండి.",
                "2. పలుచన: 15-20 రోజుల్లో మొక్కల మధ్య 10-15 సెం.మీ దూరం ఉండేలా చూడండి.",
                "3. నీటిపారుదల: పూతకు ముందు (30-35 రోజులు) మరియు కాయ దశలో (60-70 రోజులు) నీరు పెట్టండి.",
                "4. పేనుబంక నివారణ: జనవరి-ఫిబ్రవరిలో పేనుబంకను గమనించండి.",
                "5. కోత: 75-80% కాయలు పసుపు రంగులోకి మారినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Pigeon Pea (Tur / Arhar)",
        "scientific_name": "Cajanus cajan",
        "primary_soil": ["loamy", "red", "black"],
        "secondary_soil": ["alluvial"],
        "primary_season": ["kharif"],
        "secondary_season": ["annual"],
        "ideal_rain": 850,
        "min_rain": 600,
        "max_rain": 1400,
        "min_temp": 18,
        "max_temp": 35,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["low", "medium"],
        "secondary_water": ["high"],
        "duration": "150 - 180 days",
        "temp": "18°C - 35°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://media.bighaat.com/kvplus/articles/8b7423f3-3541-4586-8bbd-d98f105863ad.png?w=3840&q=80&format=webp&compress=true",
        "source_url": "https://en.wikipedia.org/wiki/Pigeon_pea",
        "overview": {
            "en": "Pigeon Pea (Tur / Arhar) is a deep-rooted Kharif pulse crop that fixes atmospheric nitrogen and withstands mid-season dry spells.",
            "kn": "ತೊಗರಿ (Cajanus cajan) ಆಳವಾದ ಬೇರು ಹೊಂದಿರುವ ಪ್ರಮುಖ ಖಾರಿಫ್ ಬೇಳೆಕಾಳು ಬೆಳೆಯಾಗಿದ್ದು, ಬರವನ್ನು ತట్టుಿಕೊಳ್ಳುತ್ತದೆ.",
            "hi": "अरहर / तुअर (Cajanus cajan) गहरी जड़ों वाली खरीफ दलहन फसल है, जो सूखे को सहन करती है और मिट्टी की उर्वरता बढ़ाती है।",
            "ta": "துவரை (Cajanus cajan) ஆழமான வேர்களைக் கொண்ட வறட்சி தாங்கும் முக்கிய கரீஃப் பயறுப் பயிராகும்.",
            "te": "కంది (Cajanus cajan) లోతైన వేర్లు కలిగి, కరువును తట్టుకునే ప్రధాన ఖరీఫ్ పప్పుధాన్య పంట.",
        },
        "fertilizer": {
            "en": "NPK 20:50:20 kg/ha plus 20 kg Sulphur/ha as basal dose; Rhizobium seed treatment.",
            "kn": "ಬಿತ್ತನೆ ವೇಳೆ NPK 20:50:20 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಗಂಧಕ (20 ಕೆಜಿ) ಮತ್ತು ರೈಜೋಬಿಯಂ ನೀಡಿ.",
            "hi": "बुवाई पर NPK 20:50:20 किग्रा/हेक्टेयर व 20 किग्रा सल्फर दें; राइजोबियम से बीज उपचार करें।",
            "ta": "அடியுரமாக NPK 20:50:20 கிலோ/எக்டர் உடன் 20 கிலோ கந்தகம் இடவும்.",
            "te": "విత్తేటప్పుడు NPK 20:50:20 కిలోలతో పాటు 20 కిలోల సల్ఫర్ వేయండి.",
        },
        "tip": {
            "en": "Avoid waterlogging completely; intercropping with green gram or soybean maximizes land returns.",
            "kn": "ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿ; ಹೆಸರು ಅಥವಾ ಸೋಯಾಬೀನ್ ಜೊತೆ ಮಿಶ್ರಬೆಳೆ ಮಾಡಿದರೆ ಹೆಚ್ಚಿನ ಆದಾಯ ಸಿಗುತ್ತದೆ.",
            "hi": "खेत में जलभराव बिल्कुल न होने दें; मूंग या सोयाबीन के साथ सह-फसली खेती लाभदायक है।",
            "ta": "வயலில் நீர் தேங்காமல் பார்க்கவும்; பாசிப்பயறுடன் ஊடுபயிராகப் பயிரிடலாம்.",
            "te": "పొలంలో నీరు నిలవకుండా చూడండి; పెసర లేదా సోయాతో అంతరపంటగా వేస్తే అధిక లాభం వస్తుంది.",
        },
        "guidelines": {
            "en": [
                "1. Ridge Planting: Sow at 60-90 cm row spacing on ridges to protect roots from waterlogging.",
                "2. Weed Control: Keep crop weed-free during the first 45-60 days.",
                "3. Topping: Lightly prune tips at 50-60 DAS to encourage side branching.",
                "4. Pod Borer & Fly Watch: Monitor at flowering and podding stages.",
                "5. Harvest: Harvest when 80% of pods turn brown and dry.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನೀರು ನಿಲ್ಲದಂತೆ 60-90 ಸೆಂ.ಮೀ ಸಾಲಿನಲ್ಲಿ ಬಿತ್ತನೆ ಮಾಡಿ.",
                "2. ಕಳೆ ನಿಯಂತ್ರಣ: ಮೊದಲ 45-60 ದಿನಗಳಲ್ಲಿ ಕಳೆ ತೆಗೆದು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
                "3. ಕುಡಿ ಚಿವುಟುವುದು: ಹೆಚ್ಚು ಕೊಂಬೆಗಳಿಗೆ 50-60 ದಿನಗಳಲ್ಲಿ ಮೇಲ್ಭಾಗ ಚಿವುಟಿ.",
                "4. ಕಾಯಿಕೊರಕ ನಿಗಾ: ಹೂವು ಮತ್ತು ಕಾಯಿ ಹಂತದಲ್ಲಿ ಕೀಟ ನಿಯಂತ್ರಣ ಮಾಡಿ.",
                "5. ಕಟಾವು: ಶೇ. 80 ಕಾಯಿಗಳು ಕಂದು ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿ ಒಣಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: जलभराव से बचने के लिए मेड़ों पर 60-90 सेमी कतार में बुवाई करें।",
                "2. निराई: शुरुआती 45-60 दिनों तक खेत को खरपतवार मुक्त रखें।",
                "3. छंटाई: अधिक शाखाओं के लिए 50-60 दिन पर हल्की कटाई-छंटाई करें।",
                "4. कीट निगरानी: फूल और फली अवस्था में फली छेदक व फली मक्खी से बचाव करें।",
                "5. कटाई: 80% फलियां भूरी व सूखी होने पर कटाई करें।",
            ],
            "ta": [
                "1. விதைப்பு: நீர் தேங்காமல் 60-90 செ.மீ வரிசை இடைவெளியில் பார்களில் விதைக்கவும்.",
                "2. களை கட்டுப்பாடு: முதல் 45-60 நாட்களுக்குக் களையின்றி பராமரிக்கவும்.",
                "3. நுனி கிள்ளுதல்: பக்கக் கிளைகள் வளர 50-60 நாட்களில் நுனியைக் கிள்ளவும்.",
                "4. காய்ப்புழு கண்காணிப்பு: பூக்கும் மற்றும் காய் பிடிக்கும் பருவத்தில் கண்காணிக்கவும்.",
                "5. அறுவடை: 80% காய்கள் பழுப்பு நிறமாகக் காய்ந்ததும் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: నీరు నిలవకుండా బోదెలపై 60-90 సెం.మీ వరుసల్లో విత్తండి.",
                "2. కలుపు నియంత్రణ: మొదటి 45-60 రోజులు పొలాన్ని కలుపు లేకుండా ఉంచండి.",
                "3. కొసలు కత్తిరింపు: కొమ్మలు పెరిగేందుకు 50-60 రోజుల్లో కొసలు కత్తిరించండి.",
                "4. పురుగుల పర్యవేక్షణ: పూత మరియు కాయ దశలో శనగపచ్చ పురుగును నివారించండి.",
                "5. కోత: 80% కాయలు గోధుమ రంగులోకి మారి ఎండినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Sunflower",
        "scientific_name": "Helianthus annuus",
        "primary_soil": ["black", "loamy"],
        "secondary_soil": ["alluvial", "red"],
        "primary_season": ["rabi", "zaid"],
        "secondary_season": ["kharif"],
        "ideal_rain": 500,
        "min_rain": 300,
        "max_rain": 750,
        "min_temp": 15,
        "max_temp": 32,
        "min_ph": 6.5,
        "max_ph": 8.0,
        "primary_water": ["medium"],
        "secondary_water": ["low"],
        "duration": "90 - 105 days",
        "temp": "15°C - 32°C",
        "ph_range": "6.5 - 8.0",
        "image_url": "https://www.apnikheti.com/upload/crops/2135idea99sunflowe.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Common_sunflower",
        "overview": {
            "en": "Sunflower (Helianthus annuus) is a day-neutral oilseed crop grown across Kharif, Rabi, and Zaid seasons in Karnataka and across India.",
            "kn": "ಸೂರ್ಯಕಾಂತಿ (Helianthus annuus) ಕರ್ನಾಟಕ ಸೇರಿದಂತೆ ಭಾರತದಾದ್ಯಂತ ಎಲ್ಲಾ ಋತುಗಳಲ್ಲಿ ಬೆಳೆಯಬಹುದಾದ ಪ್ರಮುಖ ಎಣ್ಣೆಕಾಳು ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "सूरजमुखी (Helianthus annuus) खरीफ, रबी और जायद तीनों मौसम में उगाई जाने वाली महत्वपूर्ण तिलहनी फसल है।",
            "ta": "சூரியகாந்தி (Helianthus annuus) அனைத்துப் பருவங்களிலும் வளரக்கூடிய முக்கிய எண்ணெய் வித்துப் பயிராகும்.",
            "te": "పొద్దుతిరుగుడు (Helianthus annuus) ఖరీఫ్, రబీ, జైద్ సీజన్లలో పండించే ప్రధాన నూనెగింజ పంట.",
        },
        "fertilizer": {
            "en": "NPK 60:60:40 kg/ha plus Boron (2 kg/ha) and Sulphur for better seed setting.",
            "kn": "ಉತ್ತಮ ಕಾಳು ಕಟ್ಟಲು NPK 60:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಬೋರಾನ್ (2 ಕೆಜಿ) ಮತ್ತು ಗಂಧಕ ನೀಡಿ.",
            "hi": "अच्छे दाने बनने के लिए NPK 60:60:40 किग्रा/हेक्टेयर के साथ बोरोन (2 किग्रा) व सल्फर दें।",
            "ta": "நல்ல விதை பிடிக்க NPK 60:60:40 கிலோ/எக்டர் உடன் போரான் (2 கிலோ) மற்றும் கந்தகம் இடவும்.",
            "te": "గింజలు బాగా కట్టేందుకు NPK 60:60:40 కిలోలతో పాటు బోరాన్ (2 కిలోలు) మరియు సల్ఫర్ వేయండి.",
        },
        "tip": {
            "en": "Conserve honeybees during flowering and gently rub flower heads in the morning to boost pollination.",
            "kn": "ಹೂ ಬಿಡುವ ಸಮಯದಲ್ಲಿ ಜೇನುನೊಣಗಳನ್ನು ರಕ್ಷಿಸಿ ಮತ್ತು ಪರಾಗಸ್ಪರ್ಶ ಹೆಚ್ಚಿಸಲು ಬೆಳಿಗ್ಗೆ ಹೂವುಗಳನ್ನು ಮೃದುವಾಗಿ ಉಜ್ಜಿ.",
            "hi": "फूल आते समय मधुमक्खियों को बचाएं और परागण बढ़ाने के लिए सुबह फूलों को हल्के हाथ से सहलाएं।",
            "ta": "பூக்கும் போது தேனீக்களைப் பாதுகாத்து, மகரந்தச் சேர்க்கைக்கு காலை வேளையில் பூக்களை மெதுவாகத் தடவவும்.",
            "te": "పూత సమయంలో తేనెటీగలను సంరక్షించి, ఉదయం పూలను మెల్లగా తాకడం ద్వారా పరాగసంపర్కం పెంచండి.",
        },
        "guidelines": {
            "en": [
                "1. Sowing: Sow hybrid seeds at 60x30 cm spacing in well-drained soil.",
                "2. Thinning: Retain one vigorous plant per hill at 15 DAS.",
                "3. Critical Irrigation: Ensure moisture at bud initiation, flowering, and seed filling.",
                "4. Pollination Care: Avoid spraying insecticides during peak bee foraging hours.",
                "5. Harvest: Harvest when back of the flower head turns lemon-yellow.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ನೀರು ಬಸಿದುಹೋಗುವ ಮಣ್ಣಿನಲ್ಲಿ 60x30 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಹೈಬ್ರಿಡ್ ಬೀಜ ಬಿತ್ತಿ.",
                "2. ಸಸಿ ತೆಳುಗೊಳಿಸುವಿಕೆ: 15 ದಿನಗಳಲ್ಲಿ ಗುಣಿಗೆ ಒಂದು ಬಲವಾದ ಸಸಿ ಉಳಿಸಿ.",
                "3. ನೀರಾವರಿ: ಮೊಗ್ಗು, ಹೂವು ಮತ್ತು ಕಾಳು ತುಂಬುವ ಹಂತದಲ್ಲಿ ತೇವಾಂಶ ಕಾಪಾಡಿ.",
                "4. ಪರಾಗಸ್ಪರ್ಶ ರಕ್ಷಣೆ: ಹೂ ಬಿಡುವ ಸಮಯದಲ್ಲಿ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ.",
                "5. ಕಟಾವು: ಹೂವಿನ ಹಿಂಭಾಗ ನಿಂಬೆ ಹಳದಿ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: अच्छी जल निकासी वाली मिट्टी में 60x30 सेमी दूरी पर हाइब्रिड बीज बोएं।",
                "2. छंटाई: 15 दिन में प्रति स्थान एक स्वस्थ पौधा रखें।",
                "3. सिंचाई: कली बनते, फूल आते और दाना भरते समय नमी बनाए रखें।",
                "4. परागण सुरक्षा: फूल अवस्था में मधुमक्खियों के समय कीटनाशक न छिड़कें।",
                "5. कटाई: फूल के पीछे का भाग नींबू-पीला होने पर कटाई करें।",
            ],
            "ta": [
                "1. விதைப்பு: வடிகால் வசதியுள்ள மண்ணில் 60x30 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "2. பயிர் களைதல்: 15 நாட்களில் குழிக்கு ஒரு திடமான செடியை விடவும்.",
                "3. நீர்ப்பாசனம்: மொட்டு, பூ மற்றும் விதை பிடிக்கும் பருவத்தில் ஈரப்பதம் காக்கவும்.",
                "4. மகரந்தப் பாதுகாப்பு: பூக்கும் பருவத்தில் பூச்சிக்கொல்லி தெளிப்பதைத் தவிர்க்கவும்.",
                "5. அறுவடை: பூவின் பின்புறம் எலுமிச்சை மஞ்சள் நிறமாக மாறும்போது அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: నీరు నిలవని నేలలో 60x30 సెం.మీ దూరంలో హైబ్రిడ్ విత్తనాలు నాటండి.",
                "2. పలుచన: 15 రోజుల్లో పాదుకు ఒక ఆరోగ్యకరమైన మొక్కను ఉంచండి.",
                "3. నీటిపారుదల: మొగ్గ, పూత మరియు గింజ నిండే దశలో తేమ ఉండేలా చూడండి.",
                "4. పరాగసంపర్క రక్షణ: పూత సమయంలో పురుగుమందులు పిచికారీ చేయవద్దు.",
                "5. కోత: పువ్వు వెనుక భాగం నిమ్మ పసుపు రంగులోకి మారినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Onion",
        "scientific_name": "Allium cepa",
        "primary_soil": ["loamy", "alluvial", "black"],
        "secondary_soil": ["red"],
        "primary_season": ["rabi", "kharif"],
        "secondary_season": ["zaid"],
        "ideal_rain": 600,
        "min_rain": 400,
        "max_rain": 900,
        "min_temp": 15,
        "max_temp": 30,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["medium"],
        "secondary_water": ["high"],
        "duration": "100 - 125 days",
        "temp": "15°C - 30°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://agritech.tnau.ac.in/horticulture/vegetables/onion/onion%20bulb1.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Onion",
        "overview": {
            "en": "Onion (Allium cepa) is India's most widely grown commercial bulb vegetable across Kharif, late Kharif, and Rabi seasons.",
            "kn": "ಈರುಳ್ಳಿ (Allium cepa) ಮುಂಗಾರು ಮತ್ತು ಹಿಂಗಾರು ಋತುಗಳಲ್ಲಿ ಭಾರತದಾದ್ಯಂತ ಬೆಳೆಯುವ ಪ್ರಮುಖ ವಾಣಿಜ್ಯ ತರಕಾರಿ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "प्याज (Allium cepa) खरीफ और रबी मौसम में भारत भर में उगाई जाने वाली प्रमुख व्यावसायिक कंद सब्जी है।",
            "ta": "வெங்காயம் (Allium cepa) கரீஃப் மற்றும் ரபி பருவங்களில் இந்தியா முழுவதும் பயிரிடப்படும் முக்கிய வணிகப் பயிராகும்.",
            "te": "ఉల్లి (Allium cepa) ఖరీఫ్ మరియు రబీ సీజన్లలో భారతదేశం అంతటా పండించే ప్రధాన వాణిజ్య కూరగాయ పంట.",
        },
        "fertilizer": {
            "en": "NPK 100:50:50 kg/ha plus 30 kg Sulphur/ha for pungency and bulb storage life.",
            "kn": "NPK 100:50:50 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಗಡ್ಡೆ ಬಾಳಿಕೆಗಾಗಿ ಗಂಧಕ (30 ಕೆಜಿ) ನೀಡಿ.",
            "hi": "NPK 100:50:50 किग्रा/हेक्टेयर के साथ कंद की गुणवत्ता और भंडारण के लिए 30 किग्रा सल्फर दें।",
            "ta": "NPK 100:50:50 கிலோ/எக்டர் உடன் 30 கிலோ கந்தகம் இடவும்.",
            "te": "NPK 100:50:50 కిలోలతో పాటు నిల్వ సామర్థ్యం కోసం 30 కిలోల సల్ఫర్ వేయండి.",
        },
        "tip": {
            "en": "Stop irrigation 15 days before harvest when 50% of tops fall over, then cure bulbs in shade.",
            "kn": "50% ಗಿಡದ ದಂಟು ಬಾಗಿದಾಗ ಕಟಾವಿಗೆ 15 ದಿನ ಮೊದಲು ನೀರು ನಿಲ್ಲಿಸಿ ನೆರಳಿನಲ್ಲಿ ಒಣಗಿಸಿ.",
            "hi": "50% पत्तियां झुकने पर कटाई से 15 दिन पहले सिंचाई बंद करें और छाया में सुखाएं।",
            "ta": "50% தண்டு சாயும்போது அறுவடைக்கு 15 நாட்கள் முன் நீரை நிறுத்தி நிழலில் உலர்த்தவும்.",
            "te": "50% ఆకులు వాలినప్పుడు కోతకు 15 రోజుల ముందు నీరు ఆపి నీడలో ఆరబెట్టండి.",
        },
        "guidelines": {
            "en": [
                "1. Nursery & Transplanting: Transplant 6-8 week old seedlings at 15x10 cm spacing.",
                "2. Raised Beds: Use raised beds in Kharif to prevent bulb rot.",
                "3. Irrigation: Give light, frequent irrigations; avoid moisture fluctuation during bulbing.",
                "4. Thrips & Purple Blotch: Use blue sticky traps and timely sprays.",
                "5. Curing: Harvest at 50% neck-fall and cure bulbs for 10-12 days before storage.",
            ],
            "kn": [
                "1. ನಾಟಿ: 6-8 ವಾರದ ಸಸಿಗಳನ್ನು 15x10 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ನಾಟಿ ಮಾಡಿ.",
                "2. ಏರುಮಡಿ: ಮುಂಗಾರಿನಲ್ಲಿ ಗಡ್ಡೆ ಕೊಳೆಯದಂತೆ ಏರುಮಡಿಗಳಲ್ಲಿ ಬೆಳೆಯಿರಿ.",
                "3. ನೀರಾವರಿ: ಗಡ್ಡೆ ಕಟ್ಟುವಾಗ ನಿಯಮಿತವಾಗಿ ಲಘು ನೀರು ಕೊಡಿ.",
                "4. ರೋಗ ನಿಗಾ: ಥ್ರಿಪ್ಸ್ ನುಸಿ ಮತ್ತು ನೇರಳೆ ಮಚ್ಚೆ ರೋಗವನ್ನು ನಿಯಂತ್ರಿಸಿ.",
                "5. ಕಟಾವು: ಶೇ. 50 ದಂಟು ಬಾಗಿದಾಗ ಕಿತ್ತು 10-12 ದಿನ ನೆರಳಿನಲ್ಲಿ ಒಣಗಿಸಿ.",
            ],
            "hi": [
                "1. रोपाई: 6-8 सप्ताह पुरानी पौध को 15x10 सेमी दूरी पर रोपें।",
                "2. उठी हुई क्यारियां: खरीफ में सड़न रोकने के लिए उठी क्यारियों पर खेती करें।",
                "3. सिंचाई: कंद बनते समय हल्की व नियमित सिंचाई करें।",
                "4. थ्रिप्स व झुलसा प्रबंधन: नीले चिपचिपे ट्रैप लगाएं।",
                "5. कटाई व सुखाना: 50% गर्दन झुकने पर निकालकर 10-12 दिन छाया में सुखाएं।",
            ],
            "ta": [
                "1. நடவு: 6-8 வார நாற்றுகளை 15x10 செ.மீ இடைவெளியில் நடவும்.",
                "2. மேட்டுப்பாத்தி: கரீஃப் பருவத்தில் அழுகலைத் தடுக்க மேட்டுப்பாத்திகளில் நடவும்.",
                "3. நீர்ப்பாசனம்: கிழங்கு உருவாகும் போது சீரான லேசான பாசனம் செய்யவும்.",
                "4. பூச்சி/நோய்: இலைப்பேன் மற்றும் ஊதாப் புள்ளி நோயைக் கண்காணிக்கவும்.",
                "5. அறுவடை: 50% தண்டு சாய்ந்ததும் பறித்து 10-12 நாட்கள் நிழலில் உலர்த்தவும்.",
            ],
            "te": [
                "1. నాటు: 6-8 వారాల నారును 15x10 సెం.మీ దూరంలో నాటండి.",
                "2. ఎత్తు మడులు: ఖరీఫ్‌లో కుళ్లు రాకుండా ఎత్తు మడులపై పెంచండి.",
                "3. నీటిపారుదల: గడ్డ ఊరే సమయంలో క్రమంగా తేలికపాటి తడులు ఇవ్వండి.",
                "4. పురుగు/తెగులు: తామరపురుగులు మరియు ఊదా మచ్చ తెగులును నివారించండి.",
                "5. కోత: 50% కాండాలు వాలినప్పుడు తీసి 10-12 రోజులు నీడలో ఆరబెట్టండి.",
            ],
        },
    },
    {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "primary_soil": ["loamy", "red", "black"],
        "secondary_soil": ["alluvial", "sandy"],
        "primary_season": ["rabi", "kharif"],
        "secondary_season": ["zaid"],
        "ideal_rain": 700,
        "min_rain": 500,
        "max_rain": 1200,
        "min_temp": 18,
        "max_temp": 31,
        "min_ph": 6.0,
        "max_ph": 7.0,
        "primary_water": ["medium", "high"],
        "secondary_water": ["low"],
        "duration": "90 - 120 days",
        "temp": "18°C - 31°C",
        "ph_range": "6.0 - 7.0",
        "image_url": "https://www.dripworks.com/content/tomato-growing-guide-banner.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Tomato",
        "overview": {
            "en": "Tomato (Solanum lycopersicum) is a high-value vegetable grown year-round in India with proper staking, drip irrigation, and pest management.",
            "kn": "ಟೊಮೆಟೊ (Solanum lycopersicum) ಹನಿ ನೀರಾವರಿ ಮತ್ತು ಆಸರೆ ನೀಡುವ ಮೂಲಕ ವರ್ಷಪೂರ್ತಿ ಬೆಳೆಯಬಹುದಾದ ಲಾಭದಾಯಕ ತರಕಾರಿ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "टमाटर (Solanum lycopersicum) ड्रिप सिंचाई और सहारा देकर साल भर उगाई जाने वाली उच्च मूल्य वाली सब्जी फसल है।",
            "ta": "தக்காளி (Solanum lycopersicum) சொட்டுநீர்ப் பாசனம் மற்றும் முட்டுக் கொடுத்து ஆண்டு முழுவதும் பயிரிடப்படும் பயிராகும்.",
            "te": "టమోటా (Solanum lycopersicum) డ్రిప్ సాగు మరియు ఊతమివ్వడం ద్వారా ఏడాది పొడవునా పండించే లాభదాయక కూరగాయ పంట.",
        },
        "fertilizer": {
            "en": "NPK 120:80:80 kg/ha plus Calcium Nitrate & Boron foliar spray to prevent blossom-end rot.",
            "kn": "NPK 120:80:80 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಕಾಯಿ ಕೊಳೆಯುವುದನ್ನು ತಡೆಯಲು ಕ್ಯಾಲ್ಸಿಯಂ ನೈಟ್ರೇಟ್ ಸಿಂಪಡಿಸಿ.",
            "hi": "NPK 120:80:80 किग्रा/हेक्टेयर के साथ फल सड़न रोकने हेतु कैल्शियम नाइट्रेट व बोरोन का छिड़काव करें।",
            "ta": "NPK 120:80:80 கிலோ/எக்டர் உடன் கால்சியம் நைட்ரேட் மற்றும் போரான் தெளிக்கவும்.",
            "te": "NPK 120:80:80 కిలోలతో పాటు క్యాల్షియం నైట్రేట్, బోరాన్ పిచికారీ చేయండి.",
        },
        "tip": {
            "en": "Stake indeterminate hybrids early and use silver-black plastic mulch to control weeds and thrips.",
            "kn": "ಗಿಡಗಳಿಗೆ ಬೇಗನೆ ಕೋಲು ಆಸರೆ ಕೊಡಿ ಮತ್ತು ಕಳೆ ನಿಯಂತ್ರಣಕ್ಕೆ ಪ್ಲಾಸ್ಟಿಕ್ ಮಲ್ಚಿಂಗ್ ಬಳಸಿ.",
            "hi": "पौधों को समय पर सहारा (स्टेकिंग) दें और खरपतवार व कीट रोकने के लिए मल्चिंग का उपयोग करें।",
            "ta": "செடிகளுக்கு ஆரம்பத்திலேயே குச்சி ஊன்றி, களை கட்டுப்பாட்டுக்கு மல்ச்சிங் பயன்படுத்தவும்.",
            "te": "మొక్కలకు ముందే కర్రలతో ఊతమిచ్చి, కలుపు నియంత్రణకు మల్చింగ్ వాడండి.",
        },
        "guidelines": {
            "en": [
                "1. Transplanting: Transplant 25-day old seedlings on mulched raised beds at 60x45 cm.",
                "2. Staking: Provide bamboo/wire staking at 25-30 DAT.",
                "3. Drip & Fertigation: Supply water evenly; erratic watering causes fruit cracking.",
                "4. Pest Watch: Monitor for whiteflies (leaf curl virus) and Tuta absoluta.",
                "5. Harvest: Pick at breaker/pink stage for distant markets or full red for local sale.",
            ],
            "kn": [
                "1. ನಾಟಿ: 25 ದಿನದ ಸಸಿಗಳನ್ನು ಮಲ್ಚಿಂಗ್ ಮಾಡಿದ ಏರುಮಡಿಗಳಲ್ಲಿ 60x45 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ನೆಡಿ.",
                "2. ಆಸರೆ ನೀಡುವುದು: 25-30 ದಿನಗಳಲ್ಲಿ ಬಿದಿರು/ತಂತಿ ಆಸರೆ ಕಟ್ಟಿ.",
                "3. ನೀರಾವರಿ: ಸಮಪ್ರಮಾಣದಲ್ಲಿ ನೀರು ಕೊಡಿ; ಏರುಪೇರಾದರೆ ಹಣ್ಣು ಒಡೆಯುತ್ತದೆ.",
                "4. ಕೀಟ ನಿಗಾ: ಬಿಳಿನೊಣ (ಎಲೆ ಮುರುಟು ರೋಗ) ಮತ್ತು ಹಣ್ಣು ಕೊರಕವನ್ನು ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ದೂರದ ಮಾರುಕಟ್ಟೆಗೆ ಅರ್ಧ ಕೆಂಪಾದಾಗ, ಸ್ಥಳೀಯ ಮಾರಾಟಕ್ಕೆ ಪೂರ್ಣ ಹಣ್ಣಾದಾಗ ಕೀಳಿ.",
            ],
            "hi": [
                "1. रोपाई: 25 दिन की पौध मल्च की गई मेड़ों पर 60x45 सेमी दूरी पर लगाएं।",
                "2. सहारा देना: 25-30 दिन पर बांस व तार से स्टेकिंग करें।",
                "3. सिंचाई: समान नमी रखें; अनियमित पानी से फल फट सकते हैं।",
                "4. कीट नियंत्रण: सफेद मक्खी (पत्ती मरोड़ वायरस) और फल छेदक से बचाएं।",
                "5. तुड़ाई: दूर के बाजार के लिए हल्के लाल और स्थानीय बिक्री के लिए पूरे लाल फल तोड़ें।",
            ],
            "ta": [
                "1. நடவு: 25 நாள் நாற்றுகளை 60x45 செ.மீ இடைவெளியில் மேட்டுப்பாத்திகளில் நடவும்.",
                "2. முட்டுக் கொடுத்தல்: 25-30 நாட்களில் மூங்கில்/கம்பி மூலம் முட்டுக் கொடுக்கவும்.",
                "3. சொட்டுநீர்: சீரான நீர் பாய்ச்சவும்; நீர் மாறுபாடு பழம் வெடிப்பை ஏற்படுத்தும்.",
                "4. பூச்சி கட்டுப்பாடு: வெள்ளை ஈ மற்றும் பழத் துளைப்பானைக் கண்காணிக்கவும்.",
                "5. அறுவடை: தொலைதூர சந்தைக்கு செங்காயாகவும், உள்ளூருக்குப் பழுத்ததாகவும் பறிக்கவும்.",
            ],
            "te": [
                "1. నాటు: 25 రోజుల నారును మల్చింగ్ చేసిన బోదెలపై 60x45 సెం.మీ దూరంలో నాటండి.",
                "2. ఊతమివ్వడం: 25-30 రోజుల్లో వెదురు కర్రలు/వైర్లతో ఊతమివ్వండి.",
                "3. డ్రిప్: సమానంగా నీరు ఇవ్వండి; తేమ హెచ్చుతగ్గుల వల్ల కాయలు పగులుతాయి.",
                "4. పురుగు/తెగులు: తెల్లదోమ (ఆకుముడత) మరియు కాయ తొలుచు పురుగును గమనించండి.",
                "5. కోత: దూరపు మార్కెట్‌కు దోరగా ఉన్నప్పుడు, స్థానికంగా పూర్తిగా పండినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Green Gram (Moong)",
        "scientific_name": "Vigna radiata",
        "primary_soil": ["loamy", "sandy", "alluvial"],
        "secondary_soil": ["red", "black"],
        "primary_season": ["kharif", "zaid"],
        "secondary_season": ["rabi"],
        "ideal_rain": 650,
        "min_rain": 500,
        "max_rain": 1000,
        "min_temp": 22,
        "max_temp": 35,
        "min_ph": 6.0,
        "max_ph": 7.2,
        "primary_water": ["low", "medium"],
        "secondary_water": ["high"],
        "duration": "60 - 75 days",
        "temp": "22°C - 35°C",
        "ph_range": "6.0 - 7.2",
        "image_url": "https://agritech.tnau.ac.in/agriculture/English%20Version/Agriculture/CropProduction/Pulses/pulses_greengram_clip_image008.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Mung_bean",
        "overview": {
            "en": "Green Gram (Moong) is a fast-maturing 60-75 day pulse ideal for Kharif, summer Zaid catch cropping, and rice fallows.",
            "kn": "ಹೆಸರುಕಾಳು (Vigna radiata) 60-75 ದಿನಗಳಲ್ಲಿ ಬೆಳೆಯುವ ಅಲ್ಪಾವಧಿಯ ದ್ವಿದಳ ಧಾನ್ಯವಾಗಿದ್ದು, ಮಿಶ್ರಬೆಳೆಗೆ ಅತ್ಯಂತ ಸೂಕ್ತವಾಗಿದೆ.",
            "hi": "मूंग (Vigna radiata) 60-75 दिनों में पकने वाली त्वरित दलहन फसल है, जो खरीफ और जायद के लिए उत्तम है।",
            "ta": "பாசிப்பயறு (Vigna radiata) 60-75 நாட்களில் விளையும் குறுகிய காலப் பயறு வகை பயிராகும்.",
            "te": "పెసర (Vigna radiata) 60-75 రోజుల్లో పండే స్వల్పకాలిక పప్పుధాన్య పంట; ఖరీఫ్, వేసవికి ఎంతో అనుకూలం.",
        },
        "fertilizer": {
            "en": "NPK 15:40:20 kg/ha plus Rhizobium seed treatment; spray 2% DAP at flowering.",
            "kn": "NPK 15:40:20 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ರೈಜೋಬಿಯಂ ಬೀಜೋಪಚಾರ; ಹೂ ಬಿಡುವಾಗ 2% DAP ಸಿಂಪಡಿಸಿ.",
            "hi": "NPK 15:40:20 किग्रा/हेक्टेयर व राइजोबियम उपचार दें; फूल आने पर 2% DAP का छिड़काव करें।",
            "ta": "NPK 15:40:20 கிலோ/எக்டர் உடன் ரைசோபியம் நேர்த்தி; பூக்கும்போது 2% DAP தெளிக்கவும்.",
            "te": "NPK 15:40:20 కిలోలతో పాటు రైజోబియం శుద్ధి; పూత దశలో 2% DAP పిచికారీ చేయండి.",
        },
        "tip": {
            "en": "Pick mature black pods in 2 pickings or harvest promptly to avoid shattering in hot weather.",
            "kn": "ಕಾಯಿಗಳು ಕಪ್ಪಾದಾಗ 2 ಹಂತಗಳಲ್ಲಿ ಕಟಾವು ಮಾಡಿ; ಬಿಸಿಲಿನಲ್ಲಿ ಕಾಯಿ ಸಿಡಿಯದಂತೆ ಎಚ್ಚರವಹಿಸಿ.",
            "hi": "फलियां काली पड़ने पर 2 बार में तुड़ाई करें ताकि गर्मी में दाने न झड़ें।",
            "ta": "காய்கள் கருத்ததும் 2 முறை பறிக்கவும்; வெயிலில் வெடிப்பதைத் தவிர்க்கவும்.",
            "te": "కాయలు నల్లబడినప్పుడు 2 విడతలుగా కోయండి; ఎండకు గింజలు రాలకుండా చూడండి.",
        },
        "guidelines": {
            "en": [
                "1. Sowing: Sow 15-20 kg/ha seed at 30x10 cm spacing.",
                "2. Weed Control: Give one hand weeding at 20-25 DAS.",
                "3. Irrigation: For summer Moong, irrigate at 25 DAS (flowering) and 40 DAS (pod filling).",
                "4. Disease Control: Use Yellow Mosaic Virus (YMV) resistant varieties.",
                "5. Harvest: Harvest when 80% of pods turn black.",
            ],
            "kn": [
                "1. ಬಿತ್ತನೆ: ಹೆಕ್ಟೇರ್‌ಗೆ 15-20 ಕೆಜಿ ಬೀಜವನ್ನು 30x10 ಸೆಂ.ಮೀ ಅಂತರದಲ್ಲಿ ಬಿತ್ತಿ.",
                "2. ಕಳೆ ತೆಗೆಯುವುದು: 20-25 ದಿನಗಳಲ್ಲಿ ಒಂದು ಬಾರಿ ಕಳೆ ತೆಗೆಯಿರಿ.",
                "3. ನೀರಾವರಿ: ಬೇಸಿಗೆ ಬೆಳೆಗೆ ಹೂವು (25 ದಿನ) ಮತ್ತು ಕಾಯಿ ಹಂತದಲ್ಲಿ (40 ದಿನ) ನೀರು ಕೊಡಿ.",
                "4. ರೋಗ ನಿಗಾ: ಹಳದಿ ನಂಜಾಣು ರೋಗ (YMV) ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ.",
                "5. ಕಟಾವು: ಶೇ. 80 ಕಾಯಿಗಳು ಕಪ್ಪಾದಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. बुवाई: 15-20 किग्रा/हेक्टेयर बीज 30x10 सेमी दूरी पर बोएं।",
                "2. निराई: 20-25 दिन पर एक बार निराई करें।",
                "3. सिंचाई: जायद मूंग में फूल (25 दिन) और फली अवस्था (40 दिन) पर पानी दें।",
                "4. रोग बचाव: पीला मोजेक वायरस (YMV) प्रतिरोधी किस्में लगाएं।",
                "5. कटाई: 80% फलियां काली पड़ने पर कटाई करें।",
            ],
            "ta": [
                "1. விதைப்பு: 15-20 கிலோ/எக்டர் விதையை 30x10 செ.மீ இடைவெளியில் விதைக்கவும்.",
                "2. களை எடுத்தல்: 20-25 நாட்களில் ஒருமுறை களை எடுக்கவும்.",
                "3. நீர்ப்பாசனம்: கோடைப் பயிருக்கு பூக்கும் (25 நாள்), காய் பிடிக்கும் (40 நாள்) பருவத்தில் நீர் பாய்ச்சவும்.",
                "4. நோய் தடுப்பு: மஞ்சள் தேமல் நோய் எதிர்ப்பு ரகங்களைப் பயன்படுத்தவும்.",
                "5. அறுவடை: 80% காய்கள் கருமையாகும் போது அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. విత్తడం: హెక్టారుకు 15-20 కిలోల విత్తనాన్ని 30x10 సెం.మీ దూరంలో విత్తండి.",
                "2. కలుపు: 20-25 రోజుల్లో ఒకసారి కలుపు తీయండి.",
                "3. నీటిపారుదల: వేసవి పెసరకు పూత (25 రోజులు), కాయ దశలో (40 రోజులు) తడి ఇవ్వండి.",
                "4. తెగులు నివారణ: పసుపు పచ్చ తెగులు (YMV) నిరోధక రకాలను ఎంచుకోండి.",
                "5. కోత: 80% కాయలు నల్లబడినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Banana",
        "scientific_name": "Musa acuminata",
        "primary_soil": ["alluvial", "loamy"],
        "secondary_soil": ["clay", "red"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif"],
        "ideal_rain": 1300,
        "min_rain": 650,
        "max_rain": 2200,
        "min_temp": 15,
        "max_temp": 35,
        "min_ph": 6.0,
        "max_ph": 7.5,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "300 - 365 days",
        "temp": "15°C - 35°C",
        "ph_range": "6.0 - 7.5",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/0/01/Bananal_REFON.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Banana",
        "overview": {
            "en": "Banana (Musa acuminata) is India's top tropical fruit crop, yielding heavily in fertile, well-drained alluvial and loamy soils with assured irrigation.",
            "kn": "ಬಾಳೆ (Musa acuminata) ಫಲವತ್ತಾದ ಮೆಕ್ಕಲು ಮತ್ತು ಗೋಡು ಮಣ್ಣಿನಲ್ಲಿ ಉತ್ತಮ ನೀರಾವರಿಯೊಂದಿಗೆ ಹೆಚ್ಚಿನ ಇಳುವರಿ ನೀಡುವ ಪ್ರಮುಖ ಹಣ್ಣಿನ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "केला (Musa acuminata) उपजाऊ जलोढ़ व दोमट मिट्टी और सिंचाई सुविधा वाले क्षेत्रों की प्रमुख उच्च उपज वाली फल फसल है।",
            "ta": "வாழை (Musa acuminata) வளமான வண்டல் மற்றும் களிமண் கலந்த மண்ணில் அதிக மகசூல் தரும் முக்கிய பழப் பயிராகும்.",
            "te": "అరటి (Musa acuminata) సారవంతమైన ఒండ్రు, లోమీ నేలల్లో మరియు నీటి వసతి ఉన్న ప్రాంతాల్లో అధిక దిగుబడినిచ్చే పండు పంట.",
        },
        "fertilizer": {
            "en": "200g N : 60g P2O5 : 300g K2O per plant/year via drip fertigation or 4 splits.",
            "kn": "ಪ್ರತಿ ಗಿಡಕ್ಕೆ ವಾರ್ಷಿಕ 200 ಗ್ರಾಂ N : 60 ಗ್ರಾಂ P : 300 ಗ್ರಾಂ K ಅನ್ನು 4 ಹಂತಗಳಲ್ಲಿ ಅಥವಾ ಡ್ರಿಪ್ ಮೂಲಕ ನೀಡಿ.",
            "hi": "प्रति पौधा वार्षिक 200 ग्राम N : 60 ग्राम P : 300 ग्राम K ड्रिप फर्टिगेशन या 4 भागों में दें।",
            "ta": "ஒரு செடிக்கு ஆண்டுக்கு 200 கிராம் N : 60 கிராம் P : 300 கிராம் K இடவும்.",
            "te": "మొక్కకు ఏడాదికి 200గ్రా N : 60గ్రా P : 300గ్రా K చొప్పున డ్రిప్ లేదా 4 దఫాలుగా వేయండి.",
        },
        "tip": {
            "en": "Remove unwanted suckers regularly (desuckering) and prop heavy bunches with bamboo poles.",
            "kn": "ಪಕ್ಕದ ಕಂದುಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ತೆಗೆಯಿರಿ ಮತ್ತು ಗೊನೆ ಭಾರವಾದಾಗ ಬಿದಿರು ಆಸರೆ ನೀಡಿ.",
            "hi": "अतिरिक्त कंद (सकर्स) नियमित हटाएं और भारी घार को बांस से सहारा दें।",
            "ta": "பக்கக் கன்றுகளைத் தொடர்ந்து நீக்கி, தார்களுக்கு மூங்கில் முட்டுக் கொடுக்கவும்.",
            "te": "పక్క పిలకలను ఎప్పటికప్పుడు తీసివేసి, గెలలకు వెదురు కర్రలతో ఊతమివ్వండి.",
        },
        "guidelines": {
            "en": [
                "1. Planting: Plant tissue-culture plants at 1.8x1.8 m spacing in pits enriched with FYM.",
                "2. Drip Irrigation: Maintain continuous soil moisture without water stagnation.",
                "3. Desuckering: Keep only the main mother plant until bunch emergence.",
                "4. Bunch Care: Remove male bud after last hand opens and cover bunch for clean skin.",
                "5. Harvest: Harvest when fruit ridges round out and 75-80% maturity is reached.",
            ],
            "kn": [
                "1. ನಾಟಿ: ಅಂಗಾಂಶ ಕೃಷಿ ಸಸಿಗಳನ್ನು 1.8x1.8 ಮೀ ಅಂತರದ ಗುಂಡಿಗಳಲ್ಲಿ ನೆಡಿ.",
                "2. ಹನಿ ನೀರಾವರಿ: ನೀರು ನಿಲ್ಲದಂತೆ ನಿರಂತರ ತೇವಾಂಶ ಕಾಪಾಡಿ.",
                "3. ಕಂದು ತೆಗೆಯುವಿಕೆ: ಗೊನೆ ಬರುವವರೆಗೆ ತಾಯಿ ಗಿಡವನ್ನು ಮಾತ್ರ ಉಳಿಸಿ.",
                "4. ಗೊನೆ ಆರೈಕೆ: ಕೊನೆಯ ಚಿಪ್ಪು ಬಿಟ್ಟ ನಂತರ ಮೂಗು ತೆಗೆದು ಗೊನೆಗೆ ಕವರ್ ಕಟ್ಟಿ.",
                "5. ಕಟಾವು: ಕಾಯಿಯ ಅಂಚುಗಳು ದುಂಡಾಗಿ ಶೇ. 75-80 ಬಲಿತಾಗ ಕಟಾವು ಮಾಡಿ.",
            ],
            "hi": [
                "1. रोपाई: टिश्यू-कल्चर पौधों को 1.8x1.8 मीटर दूरी पर खाद भरे गड्ढों में लगाएं।",
                "2. ड्रिप सिंचाई: जलभराव के बिना लगातार नमी बनाए रखें।",
                "3. सकर्स हटाना: घार निकलने तक केवल मुख्य पौधा रखें।",
                "4. घार देखभाल: आखिरी पंक्ति खुलने पर नर कली हटाएं और घार को ढकें।",
                "5. कटाई: फलों की धारियां गोल होने और 75-80% पकने पर कटाई करें।",
            ],
            "ta": [
                "1. நடவு: திசு வளர்ப்புக் கன்றுகளை 1.8x1.8 மீ இடைவெளியில் நடவும்.",
                "2. சொட்டுநீர்: நீர் தேங்காமல் தொடர்ந்து ஈரப்பதம் பராமரிக்கவும்.",
                "3. கன்று நீக்கம்: தார் வெளிவரும் வரை தாய்ச் செடியை மட்டும் வளர்க்கவும்.",
                "4. தார் பராமரிப்பு: கடைசி சீப்பு விரிந்ததும் பூவை ஒடித்து உறை இடவும்.",
                "5. அறுவடை: காய்களின் விளிம்புகள் வட்டமானதும் 75-80% முதிர்ச்சியில் அறுவடை செய்யவும்.",
            ],
            "te": [
                "1. నాటు: టిష్యూ కల్చర్ మొక్కలను 1.8x1.8 మీ దూరంలో గుంతల్లో నాటండి.",
                "2. డ్రిప్: నీరు నిలవకుండా నిరంతరం తేమ ఉండేలా చూడండి.",
                "3. పిలకల తొలగింపు: గెల వచ్చే వరకు తల్లి మొక్కను మాత్రమే ఉంచండి.",
                "4. గెల సంరక్షణ: చివరి హస్తం విచ్చుకున్నాక మొగ్గ తీసి గెలకు కవర్ కట్టండి.",
                "5. కోత: కాయల అంచులు గుండ్రంగా మారి 75-80% ముదిరినప్పుడు కోయండి.",
            ],
        },
    },
    {
        "name": "Coconut",
        "scientific_name": "Cocos nucifera",
        "primary_soil": ["sandy", "alluvial", "red"],
        "secondary_soil": ["loamy"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif"],
        "ideal_rain": 1800,
        "min_rain": 1300,
        "max_rain": 2800,
        "min_temp": 20,
        "max_temp": 34,
        "min_ph": 5.2,
        "max_ph": 8.0,
        "primary_water": ["medium", "high"],
        "secondary_water": ["low"],
        "duration": "Perennial (5-7 yrs to bear)",
        "temp": "20°C - 34°C",
        "ph_range": "5.2 - 8.0",
        "image_url": "https://www.mahindratractor.com/sites/default/files/2026-01/blog-2-detail-page-blog-thumbnails.webp",
        "source_url": "https://en.wikipedia.org/wiki/Coconut",
        "overview": {
            "en": "Coconut (Cocos nucifera) is a perennial coastal and southern Indian plantation palm valued for copra, tender coconut, oil, and coir.",
            "kn": "ತೆಂಗು (Cocos nucifera) ಕರಾವಳಿ ಮತ್ತು ದಕ್ಷಿಣ ಭಾರತದ ಪ್ರಮುಖ ಬಹುವಾರ್ಷಿಕ ತೋಟಗಾರಿಕೆ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "नारियल (Cocos nucifera) तटीय और दक्षिण भारत की प्रमुख बहुवर्षीय बागवानी फसल है।",
            "ta": "தென்னை (Cocos nucifera) கடலோர மற்றும் தென்னிந்தியாவின் முக்கிய பல்லாண்டுத் தோட்டப் பயிராகும்.",
            "te": "కొబ్బరి (Cocos nucifera) తీరప్రాంత మరియు దక్షిణ భారతదేశపు ప్రధాన బహువార్షిక తోట పంట.",
        },
        "fertilizer": {
            "en": "500g N : 320g P2O5 : 1200g K2O per adult palm/year in 2 splits plus 50 kg organic manure.",
            "kn": "ದೊಡ್ಡ ಮರಕ್ಕೆ ವಾರ್ಷಿಕ 500 ಗ್ರಾಂ N : 320 ಗ್ರಾಂ P : 1200 ಗ್ರಾಂ K ಜೊತೆಗೆ 50 ಕೆಜಿ ಸಾವಯವ ಗೊಬ್ಬರ ನೀಡಿ.",
            "hi": "प्रति वयस्क वृक्ष वार्षिक 500 ग्राम N : 320 ग्राम P : 1200 ग्राम K व 50 किग्रा जैविक खाद दें।",
            "ta": "வளர்ந்த மரத்திற்கு ஆண்டுக்கு 500 கிராம் N : 320 கிராம் P : 1200 கிராம் K மற்றும் 50 கிலோ தொழுவுரம் இடவும்.",
            "te": "పెద్ద చెట్టుకు ఏడాదికి 500గ్రా N : 320గ్రా P : 1200గ్రా K మరియు 50 కిలోల సేంద్రియ ఎరువు వేయండి.",
        },
        "tip": {
            "en": "Mulch palm basins with coconut husks to retain moisture and apply Boron if button shedding occurs.",
            "kn": "ತೇವಾಂಶ ಉಳಿಸಲು ಬುಡದಲ್ಲಿ ತೆಂಗಿನ ಸಿಪ್ಪೆ ಹರಡಿ ಮತ್ತು ಎಳೆ ಕಾಯಿ ಉದುರಿದರೆ ಬೋರಾನ್ ನೀಡಿ.",
            "hi": "नमी बचाने के लिए थाले में नारियल के छिलके बिछाएं और छोटे फल झड़ने पर बोरोन दें।",
            "ta": "ஈரப்பதம் காக்க வட்டப்பாத்தியில் தேங்காய் மட்டை பரப்பி, குரும்பை உதிர்ந்தால் போரான் இடவும்.",
            "te": "తేమ కోసం పాదుల్లో కొబ్బరి పీచు పరచండి; పిందెలు రాలితే బోరాన్ వేయండి.",
        },
        "guidelines": {
            "en": [
                "1. Pit Planting: Plant 1-year-old seedlings in 1x1x1 m pits at 7.5x7.5 m spacing.",
                "2. Basin Management: Open circular basins (1.8 m radius) and apply organics before monsoon.",
                "3. Moisture Conservation: Bury coconut husks around basins in rainfed gardens.",
                "4. Pest Control: Watch for Rhinoceros beetle and Red Palm Weevil in crown.",
                "5. Harvest: Harvest 11-12 month mature nuts every 45-60 days.",
            ],
            "kn": [
                "1. ನಾಟಿ: 1 ವರ್ಷದ ಸಸಿಗಳನ್ನು 7.5x7.5 ಮೀ ಅಂತರದಲ್ಲಿ 1x1x1 ಮೀ ಗುಂಡಿಗಳಲ್ಲಿ ನೆಡಿ.",
                "2. ಪಾತಿ ನಿರ್ವಹಣೆ: ಮರದ ಸುತ್ತ 1.8 ಮೀ ವೃತ್ತಾಕಾರದ ಪಾತಿ ಮಾಡಿ ಸಾವಯವ ಗೊಬ್ಬರ ಹಾಕಿ.",
                "3. ತೇವಾಂಶ ರಕ್ಷಣೆ: ಮಳೆಯಾಶ್ರಿತ ತೋಟಗಳಲ್ಲಿ ತೆಂಗಿನ ಸಿಪ್ಪೆಯನ್ನು ಪಾತಿಯಲ್ಲಿ ಹೂಳಿ.",
                "4. ಕೀಟ ನಿಗಾ: ಗೇಂಡಾಮೃಗ ಜೀರುಂಡೆ ಮತ್ತು ಕೆಂಪು ಮೂತಿ ಹುಳುವನ್ನು ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: 45-60 ದಿನಗಳಿಗೊಮ್ಮೆ 11-12 ತಿಂಗಳ ಬಲಿತ ಕಾಯಿಗಳನ್ನು ಕೀಳಿ.",
            ],
            "hi": [
                "1. रोपाई: 1 साल के पौधे 7.5x7.5 मीटर दूरी पर 1x1x1 मीटर गड्ढों में लगाएं।",
                "2. थाला प्रबंधन: तने के चारों ओर 1.8 मीटर का घेरा बनाकर जैविक खाद डालें।",
                "3. नमी संरक्षण: वर्षा आधारित बागों में थालों में नारियल के छिलके दबाएं।",
                "4. कीट नियंत्रण: गैंडा भृंग और लाल ताड़ घुन से मुकुट की रक्षा करें।",
                "5. तुड़ाई: हर 45-60 दिन में 11-12 महीने के पके नारियल तोड़ें।",
            ],
            "ta": [
                "1. நடவு: 1 வயது கன்றுகளை 7.5x7.5 மீ இடைவெளியில் 1x1x1 மீ குழிகளில் நடவும்.",
                "2. பாத்தி அமைப்பு: 1.8 மீ சுற்றளவில் வட்டப்பாத்தி அமைத்து இயற்கை உரம் இடவும்.",
                "3. ஈரப்பத பாதுகாப்பு: மானாவாரி தோப்புகளில் தேங்காய் மட்டைகளைப் புதைக்கவும்.",
                "4. பூச்சி கட்டுப்பாடு: காண்டாமிருக வண்டு மற்றும் சிவப்பு கூன்வண்டைக் கண்காணிக்கவும்.",
                "5. அறுவடை: 45-60 நாட்களுக்கு ஒருமுறை 11-12 மாத முற்றிய காய்களைப் பறிக்கவும்.",
            ],
            "te": [
                "1. నాటు: 1 ఏడాది మొక్కలను 7.5x7.5 మీ దూరంలో 1x1x1 మీ గుంతల్లో నాటండి.",
                "2. పాదుల యాజమాన్యం: చెట్టు చుట్టూ 1.8 మీ పాదులు చేసి సేంద్రియ ఎరువు వేయండి.",
                "3. తేమ సంరక్షణ: వర్షాధార తోటల్లో పాదుల్లో కొబ్బరి డొక్కలు పూడ్చండి.",
                "4. పురుగుల నివారణ: కొమ్ము పురుగు మరియు ఎర్ర ముక్కు పురుగును గమనించండి.",
                "5. కోత: ప్రతి 45-60 రోజులకు 11-12 నెలల ముదిరిన కాయలను దించండి.",
            ],
        },
    },
    {
        "name": "Tea",
        "scientific_name": "Camellia sinensis",
        "primary_soil": ["red", "loamy"],
        "secondary_soil": ["alluvial"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif"],
        "ideal_rain": 2100,
        "min_rain": 1500,
        "max_rain": 2800,
        "min_temp": 18,
        "max_temp": 30,
        "min_ph": 4.5,
        "max_ph": 5.5,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "Perennial (3-4 yrs to pluck)",
        "temp": "18°C - 30°C",
        "ph_range": "4.5 - 5.5",
        "image_url": "https://cdn.britannica.com/75/199175-050-5A07EB4B/farmer-spraying-pesticides-tea-farm.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Tea",
        "overview": {
            "en": "Tea (Camellia sinensis) is a perennial hillside beverage crop requiring acidic soil (pH 4.5-5.5), high humidity, and well-distributed rainfall.",
            "kn": "ಚಹಾ (Camellia sinensis) ಆಮ್ಲೀಯ ಮಣ್ಣು (pH 4.5-5.5) ಮತ್ತು ಹೆಚ್ಚಿನ ಮಳೆ ಇರುವ ಬೆಟ್ಟದ ಇಳಿಜಾರುಗಳಲ್ಲಿ ಬೆಳೆಯುವ ಬಹುವಾರ್ಷಿಕ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "चाय (Camellia sinensis) अम्लीय मिट्टी (pH 4.5-5.5), उच्च आर्द्रता और अच्छी वर्षा वाले पहाड़ी ढलानों की बहुवर्षीय फसल है।",
            "ta": "தேயிலை (Camellia sinensis) அமிலத்தன்மை கொண்ட மண் மற்றும் அதிக மழை பெய்யும் மலைச்சரிவுகளில் வளரும் பல்லாண்டுப் பயிராகும்.",
            "te": "తేయాకు (Camellia sinensis) ఆమ్ల స్వభావం గల నేల (pH 4.5-5.5) మరియు అధిక వర్షపాతం ఉన్న కొండ వాలుల్లో పెరిగే బహువార్షిక పంట.",
        },
        "fertilizer": {
            "en": "NPK based on yield target (e.g., 100:40:100 kg/ha/year) in 4 splits with Zinc & Boron.",
            "kn": "ಇಳುವರಿ ಗುರಿಗೆ ಅನುಗುಣವಾಗಿ NPK (100:40:100 ಕೆಜಿ/ಹೆಕ್ಟೇರ್/ವರ್ಷ) ಅನ್ನು 4 ಹಂತಗಳಲ್ಲಿ ಜಿಂಕ್, ಬೋರಾನ್ ಜೊತೆ ನೀಡಿ.",
            "hi": "उपज लक्ष्य के अनुसार NPK (100:40:100 किग्रा/हेक्टेयर/वर्ष) को जिंक व बोरोन के साथ 4 भागों में दें।",
            "ta": "மகசூலுக்கு ஏற்ப NPK (100:40:100 கிலோ/எக்டர்/ஆண்டு) 4 பிரிவுகளாக துத்தநாகம், போரானுடன் இடவும்.",
            "te": "దిగుబడి లక్ష్యాన్ని బట్టి NPK (100:40:100 కిలోలు/హెక్టార్/ఏడాది) జింక్, బోరాన్‌తో 4 దఫాలుగా వేయండి.",
        },
        "tip": {
            "en": "Maintain shade trees (Silver Oak / Albizia) and pluck only two leaves and a bud for premium quality.",
            "kn": "ನೆರಳು ಮರಗಳನ್ನು (ಸಿಲ್ವರ್ ಓಕ್) ಬೆಳೆಸಿ ಮತ್ತು ಉತ್ತಮ ಗುಣಮಟ್ಟಕ್ಕೆ ಎರಡು ಎಲೆ ಹಾಗೂ ಒಂದು ಮೊಗ್ಗನ್ನು ಮಾತ್ರ ಕೀಳಿ.",
            "hi": "छायादार पेड़ बनाए रखें और बेहतरीन गुणवत्ता के लिए केवल दो पत्तियां और एक कली तोड़ें।",
            "ta": "நிழல் மரங்களைப் பராமரித்து, சிறந்த தரத்திற்கு இரண்டு இலைகள் மற்றும் ஒரு மொட்டை மட்டும் பறிக்கவும்.",
            "te": "నీడనిచ్చే చెట్లను పెంచి, నాణ్యత కోసం రెండు ఆకులు మరియు ఒక మొగ్గను మాత్రమే కోయండి.",
        },
        "guidelines": {
            "en": [
                "1. Sloping Drainage: Plant on terraced or sloped acidic soil with contour drains.",
                "2. Shade Management: Establish partial shade trees to regulate leaf temperature.",
                "3. Training & Pruning: Prune bushes periodically to maintain a flat plucking table.",
                "4. Pest Watch: Monitor for tea mosquito bug and red spider mite.",
                "5. Plucking: Pluck tender 2 leaves + 1 bud at 7-10 day intervals.",
            ],
            "kn": [
                "1. ಇಳಿಜಾರು ಭೂಮಿ: ನೀರು ಬಸಿದುಹೋಗುವ ಆಮ್ಲೀಯ ಇಳಿಜಾರು ಮಣ್ಣಿನಲ್ಲಿ ನಾಟಿ ಮಾಡಿ.",
                "2. ನೆರಳು ನಿರ್ವಹಣೆ: ಎಲೆಯ ತಾಪಮಾನ ನಿಯಂತ್ರಿಸಲು ಭಾಗಶಃ ನೆರಳು ಮರಗಳನ್ನು ಬೆಳೆಸಿ.",
                "3. ಕತ್ತರಿಸುವುದು (Pruning): ಗಿಡಗಳನ್ನು ಸಮತಟ್ಟಾಗಿ ಇಡಲು ನಿಯಮಿತವಾಗಿ ಕತ್ತರಿಸಿ.",
                "4. ಕೀಟ ನಿಗಾ: ಸೊಳ್ಳೆ ತಿಗಣೆ ಮತ್ತು ಕೆಂಪು ಜೇಡ ನುಸಿಯನ್ನು ಗಮನಿಸಿ.",
                "5. ಎಲೆ ಕೀಳುವುದು: ಪ್ರತಿ 7-10 ದಿನಗಳಿಗೊಮ್ಮೆ 2 ಎಲೆ + 1 ಮೊಗ್ಗು ಕೀಳಿ.",
            ],
            "hi": [
                "1. ढलान व जल निकासी: अम्लीय ढलान वाली मिट्टी में कंटूर नालियों के साथ रोपण करें।",
                "2. छाया प्रबंधन: पत्तियों का तापमान नियंत्रित रखने के लिए आंशिक छायादार पेड़ लगाएं।",
                "3. छंटाई: पत्तियां तोड़ने की ऊंचाई बनाए रखने के लिए नियमित छंटाई करें।",
                "4. कीट निगरानी: टी मॉस्किटो बग और लाल मकड़ी पर नजर रखें।",
                "5. तुड़ाई: हर 7-10 दिन में कोमल 2 पत्तियां और 1 कली तोड़ें।",
            ],
            "ta": [
                "1. சரிவு வடிகால்: அமில மண்ணில் வடிகால் வசதியுடன் நடவு செய்யவும்.",
                "2. நிழல் மேலாண்மை: வெப்பநிலையைச் சீராக வைக்க நிழல் மரங்களை வளர்க்கவும்.",
                "3. கவாத்து: பறிக்கும் மட்டத்தைப் பராமரிக்கத் தொடர்ந்து கவாத்து செய்யவும்.",
                "4. பூச்சி கண்காணிப்பு: தேயிலை கொசுப் பூச்சி மற்றும் சிவப்பு சிலந்தியைக் கண்காணிக்கவும்.",
                "5. பறிப்பு: 7-10 நாட்களுக்கு ஒருமுறை 2 இலை + 1 மொட்டு பறிக்கவும்.",
            ],
            "te": [
                "1. వాలు డ్రైనేజీ: ఆమ్ల నేలల్లో నీరు పోయేలా కాలువలు తీసి నాటండి.",
                "2. నీడ యాజమాన్యం: ఆకుల ఉష్ణోగ్రత నియంత్రణకు నీడ చెట్లను పెంచండి.",
                "3. కత్తిరింపు: ఆకులు కోసే ఎత్తును సరిగ్గా ఉంచేందుకు క్రమంగా ప్రూనింగ్ చేయండి.",
                "4. పురుగుల పర్యవేక్షణ: టీ దోమ నల్లి మరియు ఎర్ర సాలీడును గమనించండి.",
                "5. కోత: ప్రతి 7-10 రోజులకు లేత 2 ఆకులు + 1 మొగ్గ కోయండి.",
            ],
        },
    },
    {
        "name": "Coffee",
        "scientific_name": "Coffea arabica / canephora",
        "primary_soil": ["red", "loamy"],
        "secondary_soil": ["alluvial"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif"],
        "ideal_rain": 1800,
        "min_rain": 1400,
        "max_rain": 2300,
        "min_temp": 18,
        "max_temp": 30,
        "min_ph": 5.5,
        "max_ph": 6.5,
        "primary_water": ["medium", "high"],
        "secondary_water": ["low"],
        "duration": "Perennial (3-4 yrs to bear)",
        "temp": "18°C - 30°C",
        "ph_range": "5.5 - 6.5",
        "image_url": "http://www.agritech.tnau.ac.in/horticulture/images/plantation/coffee/coffee14.jpg",
        "source_url": "https://en.wikipedia.org/wiki/Coffee_production_in_India",
        "overview": {
            "en": "Coffee (Arabica & Robusta) is a shade-grown Western Ghats plantation crop thriving in rich forest-loam soils with distinct blossom and backing showers.",
            "kn": "ಕಾಫಿ (ಅರೇಬಿಕಾ ಮತ್ತು ರೋಬಸ್ಟಾ) ಪಶ್ಚಿಮ ಘಟ್ಟಗಳ ನೆರಳಿನಲ್ಲಿ ಫಲವತ್ತಾದ ಗೋಡು ಮಣ್ಣಿನಲ್ಲಿ ಬೆಳೆಯುವ ಪ್ರಮುಖ ತೋಟಗಾರಿಕೆ ಬೆಳೆಯಾಗಿದೆ.",
            "hi": "कॉफी (अरेबिका और रोबस्टा) पश्चिमी घाट के छायादार वनों की उपजाऊ दोमट मिट्टी में उगने वाली प्रमुख बागवानी फसल है।",
            "ta": "காபி (அராபிகா & ரோபஸ்டா) மேற்குத் தொடர்ச்சி மலைகளின் நிழலிலும் வளமான மண்ணிலும் வளரும் முக்கிய தோட்டப் பயிராகும்.",
            "te": "కాఫీ (అరాబికా & రోబస్టా) పశ్చిమ కనుమల నీడలో, సారవంతమైన లోమీ నేలల్లో పండే ప్రధాన తోట పంట.",
        },
        "fertilizer": {
            "en": "NPK 120:90:120 kg/ha/year in 2-3 splits (pre-blossom, post-blossom, post-monsoon) plus lime if acidic.",
            "kn": "NPK 120:90:120 ಕೆಜಿ/ಹೆಕ್ಟೇರ್/ವರ್ಷವನ್ನು 2-3 ಹಂತಗಳಲ್ಲಿ ನೀಡಿ; ಮಣ್ಣು ಹುಳಿಯಾಗಿದ್ದರೆ ಸುಣ್ಣ ಬಳಸಿ.",
            "hi": "NPK 120:90:120 किग्रा/हेक्टेयर/वर्ष 2-3 बार में दें; मिट्टी अधिक अम्लीय होने पर चूना डालें।",
            "ta": "NPK 120:90:120 கிலோ/எக்டர்/ஆண்டு 2-3 பிரிவுகளாக இடவும்; அமில மண்ணுக்கு சுண்ணாம்பு இடவும்.",
            "te": "NPK 120:90:120 కిలోలు/హెక్టార్/ఏడాది 2-3 దఫాలుగా వేసి, ఆమ్లత్వం ఉంటే సున్నం వేయండి.",
        },
        "tip": {
            "en": "Ensure timely blossom showers in March-April and control White Stem Borer via shade regulation.",
            "kn": "ಮಾರ್ಚ್-ಏಪ್ರಿಲ್ ಹೂ ಮಳೆ ಬಹಳ ಮುಖ್ಯ; ಸರಿಯಾದ ನೆರಳು ನಿರ್ವಹಣೆಯಿಂದ ಬಿಳಿ ಕಾಂಡ ಕೊರಕ ತಡೆಯಿರಿ.",
            "hi": "मार्च-अप्रैल में फूल खिलने की वर्षा महत्वपूर्ण है; छाया प्रबंधन से सफेद तना छेदक को रोकें।",
            "ta": "மார்ச்-ஏப்ரல் பூ மழை அவசியம்; நிழல் மேலாண்மை மூலம் வெள்ளைத் தண்டு துளைப்பானைத் தடுக்கவும்.",
            "te": "మార్చి-ఏప్రిల్‌లో పూత వర్షం ముఖ్యం; నీడ నియంత్రణతో తెల్ల కాండం తొలుచు పురుగును అరికట్టండి.",
        },
        "guidelines": {
            "en": [
                "1. Shade & Planting: Plant under two-tier shade canopy at 2.1x2.1 m (Arabica) or 3x3 m (Robusta).",
                "2. Soil Liming: Apply agricultural lime once in 2-3 years to keep pH near 6.0.",
                "3. Blossom Irrigation: Use sprinkler irrigation if March blossom showers are delayed.",
                "4. Pest & Disease: Monitor for White Stem Borer, Berry Borer, and Coffee Leaf Rust.",
                "5. Harvest: Pick only ripe red cherries selectively for wet processing.",
            ],
            "kn": [
                "1. ನಾಟಿ ಮತ್ತು ನೆರಳು: ಅರೇಬಿಕಾ 2.1x2.1 ಮೀ ಅಥವಾ ರೋಬಸ್ಟಾ 3x3 ಮೀ ಅಂತರದಲ್ಲಿ ನೆರಳಿನಡಿ ನೆಡಿ.",
                "2. ಸುಣ್ಣ ಬಳಕೆ: pH 6.0 ರಷ್ಟು ಇರಿಸಲು 2-3 ವರ್ಷಕ್ಕೊಮ್ಮೆ ಕೃಷಿ ಸುಣ್ಣ ಹಾಕಿ.",
                "3. ಹೂ ಮಳೆ ನೀರಾವರಿ: ಮಾರ್ಚ್ ಮಳೆ ತಡವಾದರೆ ಸ್ಪ್ರಿಂಕ್ಲರ್ ನೀರು ಕೊಡಿ.",
                "4. ಕೀಟ ಮತ್ತು ರೋಗ: ಬಿಳಿ ಕಾಂಡ ಕೊರಕ, ಕಾಯಿ ಕೊರಕ ಮತ್ತು ಎಲೆ ತುಕ್ಕು ರೋಗ ಗಮನಿಸಿ.",
                "5. ಕಟಾವು: ಹಣ್ಣಾದ ಕೆಂಪು ಕಾಫಿ ಹಣ್ಣುಗಳನ್ನು ಮಾತ್ರ ಆಯ್ದು ಕೊಯ್ಲು ಮಾಡಿ.",
            ],
            "hi": [
                "1. छाया व रोपण: अरेबिका को 2.1x2.1 मीटर और रोबस्टा को 3x3 मीटर पर दोहरी छाया के नीचे लगाएं।",
                "2. चूना उपयोग: मिट्टी का pH 6.0 रखने के लिए हर 2-3 साल में कृषि चूना डालें।",
                "3. सिंचाई: मार्च में फूल खिलने की बारिश में देरी हो तो स्प्रिंकलर सिंचाई करें।",
                "4. कीट व रोग: सफेद तना छेदक, बेरी बोरर और लीफ रस्ट की निगरानी करें।",
                "5. तुड़ाई: केवल पके लाल फलों (चेरी) की ही चुनाई करें।",
            ],
            "ta": [
                "1. நிழல் & நடவு: அராபிகா 2.1x2.1 மீ அல்லது ரோபஸ்டா 3x3 மீ இடைவெளியில் நிழலில் நடவும்.",
                "2. சுண்ணாம்பு: pH 6.0 பராமரிக்க 2-3 ஆண்டுக்கு ஒருமுறை சுண்ணாம்பு இடவும்.",
                "3. நீர்ப்பாசனம்: மார்ச் பூ மழை தாமதமானால் தெளிப்பு நீர்ப்பாசனம் செய்யவும்.",
                "4. பூச்சி/நோய்: வெள்ளைத் தண்டு துளைப்பான் மற்றும் இலைத் துரு நோயைக் கண்காணிக்கவும்.",
                "5. அறுவடை: பழுத்த சிவப்புப் பழங்களை மட்டும் தேர்ந்தெடுத்துப் பறிக்கவும்.",
            ],
            "te": [
                "1. నీడ & నాటు: అరాబికా 2.1x2.1 మీ లేదా రోబస్టా 3x3 మీ దూరంలో నీడ కింద నాటండి.",
                "2. సున్నం: pH 6.0 వద్ద ఉంచేందుకు 2-3 ఏళ్లకోసారి వ్యవసాయ సున్నం వేయండి.",
                "3. పూత తడి: మార్చిలో పూత వర్షం ఆలస్యమైతే స్ప్రింక్లర్ ద్వారా నీరు ఇవ్వండి.",
                "4. పురుగు/తెగులు: తెల్ల కాండం తొలుచు పురుగు, ఆకు కుంకుమ తెగులును గమనించండి.",
                "5. కోత: బాగా పండిన ఎర్రటి కాయలను మాత్రమే ఏరి కోయండి.",
            ],
        },
    },
]


@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/crops", methods=["GET"])
def list_crops():
    lang = request.args.get("lang", "en").strip().lower()
    if lang not in UI_TEXT:
        lang = "en"

    items = []
    for crop in CROPS:
        items.append({
            "name": crop["name"],
            "scientific_name": crop["scientific_name"],
            "duration": crop["duration"],
            "ideal_temp": crop["temp"],
            "ph_range": crop["ph_range"],
            "rain_range": f"{crop['min_rain']} - {crop['max_rain']} mm",
            "image_url": crop["image_url"],
            "source_url": crop["source_url"],
            "overview": crop["overview"].get(lang, crop["overview"]["en"]),
            "fertilizer": crop["fertilizer"].get(lang, crop["fertilizer"]["en"]),
            "farming_tip": crop["tip"].get(lang, crop["tip"]["en"]),
            "guidelines": crop["guidelines"].get(lang, crop["guidelines"]["en"]),
            "resources": build_resources(crop["name"], lang),
        })
    return jsonify({"crops": items, "count": len(items)})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be a valid JSON object."}), 400

        soil_value = data.get("soil_type", "")
        season_value = data.get("season", "")
        water_value = data.get("water_availability", "")
        lang_value = data.get("lang", "en")

        if not isinstance(soil_value, str) or not isinstance(season_value, str) or not isinstance(water_value, str):
            return jsonify({"error": "Please select Soil Type, Season, and Water Availability."}), 400
        if not isinstance(lang_value, str):
            lang_value = "en"

        soil = soil_value.strip().lower()
        season = season_value.strip().lower()
        water = water_value.strip().lower()
        rainfall = float(data.get("rainfall", -1))
        if not math.isfinite(rainfall) or rainfall < 0 or rainfall > 5000:
            return jsonify({"error": "Please enter a realistic rainfall value between 0 mm and 5000 mm."}), 400

        raw_temp = data.get("temperature")
        temperature = None
        if raw_temp not in (None, ""):
            temperature = float(raw_temp)
            if not math.isfinite(temperature) or temperature < -5 or temperature > 55:
                return jsonify({"error": "Temperature must be between -5°C and 55°C."}), 400

        raw_ph = data.get("soil_ph")
        soil_ph = None
        if raw_ph not in (None, ""):
            soil_ph = float(raw_ph)
            if not math.isfinite(soil_ph) or soil_ph < 3.0 or soil_ph > 10.0:
                return jsonify({"error": "Soil pH must be between 3.0 and 10.0."}), 400

        if not soil or not season or not water:
            return jsonify({"error": "Please select Soil Type, Season, and Water Availability."}), 400

        lang = lang_value.strip().lower()
        if lang not in UI_TEXT:
            lang = "en"
        txt = UI_TEXT[lang]
        terms = TERM_NAMES.get(lang, TERM_NAMES["en"])

        soil_label = terms.get(soil, soil)
        season_label = terms.get(season, season)
        water_label = terms.get(water, water)

        scored_crops = []
        for crop in CROPS:
            score = 0.0
            reasons = []
            warnings = []

            if soil in crop["primary_soil"]:
                score += 30
                reasons.append(txt["soil_ok"].format(soil=soil_label))
            elif soil in crop["secondary_soil"]:
                score += 18
                reasons.append(txt["soil_sec"].format(soil=soil_label))
            else:
                score -= 10
                warnings.append(txt["soil_bad"].format(soil=soil_label))

            if season in crop["primary_season"]:
                score += 30
                reasons.append(txt["season_ok"].format(season=season_label))
            elif season in crop["secondary_season"]:
                score += 18
                reasons.append(txt["season_sec"].format(season=season_label))
            else:
                score -= 15
                warnings.append(txt["season_bad"].format(season=season_label))

            if water in crop["primary_water"]:
                score += 20
                reasons.append(txt["water_ok"].format(water=water_label))
            elif water in crop["secondary_water"]:
                score += 10
                reasons.append(txt["water_sec"].format(water=water_label))
            else:
                score -= 15
                warnings.append(txt["water_bad"].format(water=water_label))

            if crop["min_rain"] <= rainfall <= crop["max_rain"]:
                rain_diff = abs(rainfall - crop["ideal_rain"])
                max_span = max(crop["ideal_rain"] - crop["min_rain"], crop["max_rain"] - crop["ideal_rain"], 1)
                rain_score = 20.0 - (rain_diff / max_span) * 8.0
                score += max(12.0, rain_score)
                reasons.append(txt["rain_ok"].format(rain=rainfall, min_r=crop["min_rain"], max_r=crop["max_rain"]))
            else:
                distance = crop["min_rain"] - rainfall if rainfall < crop["min_rain"] else rainfall - crop["max_rain"]
                penalty = min(20.0, (distance / 250.0) * 10.0)
                score -= penalty
                warnings.append(txt["rain_bad"].format(rain=rainfall, min_r=crop["min_rain"], max_r=crop["max_rain"]))

            if temperature is not None:
                if crop["min_temp"] <= temperature <= crop["max_temp"]:
                    score += 8.0
                    reasons.append(txt["temp_ok"].format(temp=temperature, min_t=crop["min_temp"], max_t=crop["max_temp"]))
                else:
                    score -= 10.0
                    warnings.append(txt["temp_bad"].format(temp=temperature, min_t=crop["min_temp"], max_t=crop["max_temp"]))

            if soil_ph is not None:
                if crop["min_ph"] <= soil_ph <= crop["max_ph"]:
                    score += 7.0
                    reasons.append(txt["ph_ok"].format(ph=soil_ph, min_p=crop["min_ph"], max_p=crop["max_ph"]))
                else:
                    score -= 8.0
                    warnings.append(txt["ph_bad"].format(ph=soil_ph, min_p=crop["min_ph"], max_p=crop["max_ph"]))

            final_percentage = round(max(5.0, min(100.0, score)), 1)

            if final_percentage >= 80:
                suitability_level = txt["high"]
            elif final_percentage >= 55:
                suitability_level = txt["med"]
            else:
                suitability_level = txt["low"]

            summary_text = ""
            if reasons:
                summary_text += ", ".join(reasons) + ". "
            if warnings:
                summary_text += txt["note"] + ", ".join(warnings) + "."

            scored_crops.append({
                "score": final_percentage,
                "name": crop["name"],
                "scientific_name": crop["scientific_name"],
                "confidence": f"{final_percentage}%",
                "suitability_level": suitability_level,
                "why_it_fits": summary_text.strip(),
                "duration": crop["duration"],
                "ideal_temp": crop["temp"],
                "ph_range": crop["ph_range"],
                "rain_range": f"{crop['min_rain']} - {crop['max_rain']} mm",
                "image_url": crop["image_url"],
                "source_url": crop["source_url"],
                "overview": crop["overview"].get(lang, crop["overview"]["en"]),
                "fertilizer": crop["fertilizer"].get(lang, crop["fertilizer"]["en"]),
                "farming_tip": crop["tip"].get(lang, crop["tip"]["en"]),
                "guidelines": crop["guidelines"].get(lang, crop["guidelines"]["en"]),
                "resources": build_resources(crop["name"], lang),
            })

        scored_crops.sort(key=lambda x: x["score"], reverse=True)
        return jsonify({"recommendations": scored_crops[:3]})

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid numeric input for rainfall, temperature, or soil pH."}), 400
    except Exception:
        app.logger.exception("Unexpected error while generating crop recommendations")
        return jsonify({"error": "Unable to generate recommendations. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)