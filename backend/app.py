from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import math

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'

CROPS = [
    {
        "name": "Rice (Paddy)",
        "primary_soil": ["clay", "alluvial"],
        "secondary_soil": ["loamy"],
        "primary_season": ["kharif"],
        "secondary_season": ["monsoon"],
        "ideal_rain": 200,
        "min_rain": 120,
        "max_rain": 350,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "120 - 150 days",
        "temp": "20°C - 35°C",
        "fertilizer": {
            "en": "NPK 120:60:60 kg/ha; apply Nitrogen in 3 split doses.",
            "kn": "NPK 120:60:60 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಸಾರಜನಕವನ್ನು 3 ಹಂತಗಳಲ್ಲಿ ನೀಡಿ.",
            "hi": "NPK 120:60:60 किग्रा/हेक्टेयर; नाइट्रोजन को 3 भागों में दें।",
            "ta": "NPK 120:60:60 கிலோ/எக்டர்; தழைச்சத்தை 3 பிரிவுகளாக இடவும்.",
            "te": "NPK 120:60:60 కిలోలు/హెక్టారుకు; నత్రజనిని 3 దఫాలుగా వేయండి."
        },
        "tip": {
            "en": "Maintain 2-5 cm of standing water during vegetative stage and drain 10 days before harvest.",
            "kn": "ಬೆಳವಣಿಗೆಯ ಹಂತದಲ್ಲಿ 2-5 ಸೆಂ.ಮೀ ನೀರು ನಿಲ್ಲಿಸಿ ಮತ್ತು ಕಟಾವಿಗೆ 10 ದಿನಗಳ ಮೊದಲು ನೀರು ಬಸಿದುಹೋಗುವಂತೆ ಮಾಡಿ.",
            "hi": "बढ़वार के समय 2-5 सेमी पानी बनाए रखें और कटाई से 10 दिन पहले पानी निकाल दें।",
            "ta": "வளர்ச்சிப் பருவத்தில் 2-5 செ.மீ நீர் நிறுத்தி, அறுவடைக்கு 10 நாட்களுக்கு முன் நீரை வடிக்கவும்.",
            "te": "పెరుగుదల దశలో 2-5 సెం.మీ నీరు నిల్వ ఉంచి, కోతకు 10 రోజుల ముందు నీటిని తీసివేయండి."
        }
    },
    {
        "name": "Wheat",
        "primary_soil": ["loamy", "alluvial"],
        "secondary_soil": ["clay"],
        "primary_season": ["rabi"],
        "secondary_season": ["winter"],
        "ideal_rain": 75,
        "min_rain": 30,
        "max_rain": 130,
        "primary_water": ["medium"],
        "secondary_water": ["high"],
        "duration": "110 - 130 days",
        "temp": "10°C - 25°C",
        "fertilizer": {
            "en": "NPK 120:60:40 kg/ha; apply Phosphorus and Potash at sowing.",
            "kn": "NPK 120:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಬಿತ್ತನೆಯ ಸಮಯದಲ್ಲಿ ರಂಜಕ ಮತ್ತು ಪೊಟ್ಯಾಶ್ ನೀಡಿ.",
            "hi": "NPK 120:60:40 किग्रा/हेक्टेयर; बुवाई के समय फास्फोरस और पोटाश डालें।",
            "ta": "NPK 120:60:40 கிலோ/எக்டர்; விதைக்கும்போது மணிச்சத்து மற்றும் சாம்பல் சத்து இடவும்.",
            "te": "NPK 120:60:40 కిలోలు/హెక్టారుకు; విత్తే సమయంలో భాస్వరం మరియు పొటాష్ వేయండి."
        },
        "tip": {
            "en": "Ensure critical irrigation at Crown Root Initiation (CRI) stage, around 21 days after sowing.",
            "kn": "ಬಿತ್ತನೆ ಮಾಡಿದ 21 ದಿನಗಳ ನಂತರ ಬೇರು ಬಿಡುವ ಹಂತದಲ್ಲಿ (CRI) ತಪ್ಪದೇ ನೀರು ಹಾಯಿಸಿ.",
            "hi": "बुवाई के लगभग 21 दिन बाद जड़ जमने की अवस्था (CRI) में सिंचाई जरूर करें।",
            "ta": "விதைத்த 21 நாட்களில் வேர் பிடிக்கும் பருவத்தில் (CRI) தவறாமல் நீர் பாய்ச்சவும்.",
            "te": "విత్తిన 21 రోజుల తర్వాత వేర్లు వచ్చే దశలో (CRI) తప్పనిసరిగా నీరు పెట్టండి."
        }
    },
    {
        "name": "Maize (Corn)",
        "primary_soil": ["loamy", "alluvial"],
        "secondary_soil": ["sandy", "red"],
        "primary_season": ["kharif"],
        "secondary_season": ["rabi"],
        "ideal_rain": 90,
        "min_rain": 50,
        "max_rain": 160,
        "primary_water": ["medium"],
        "secondary_water": ["high", "low"],
        "duration": "90 - 110 days",
        "temp": "18°C - 32°C",
        "fertilizer": {
            "en": "NPK 120:60:40 kg/ha plus Zinc Sulphate (25 kg/ha) for higher yield.",
            "kn": "ಹೆಚ್ಚಿನ ಇಳುವರಿಗಾಗಿ NPK 120:60:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ಜೊತೆಗೆ ಸತುವಿನ ಸಲ್ಫೇಟ್ (25 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) ನೀಡಿ.",
            "hi": "अधिक उपज के लिए NPK 120:60:40 किग्रा/हेक्टेयर के साथ जिंक सल्फेट (25 किग्रा) डालें।",
            "ta": "அதிக மகசூலுக்கு NPK 120:60:40 கிலோ/எக்டர் உடன் துத்தநாக சல்பேட் (25 கிலோ) இடவும்.",
            "te": "అధిక దిగుబడి కోసం NPK 120:60:40 కిలోలతో పాటు జింక్ సల్ఫేట్ (25 కిలోలు) వేయండి."
        },
        "tip": {
            "en": "Avoid waterlogging in early stages; ensure proper drainage and timely weeding within 30 days.",
            "kn": "ಆರಂಭಿಕ ಹಂತದಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು 30 ದಿನಗಳಲ್ಲಿ ಕಳೆ ತೆಗೆಯಿರಿ.",
            "hi": "शुरुआती अवस्था में जलभराव से बचें और 30 दिनों के भीतर निराई-गुड़ाई करें।",
            "ta": "ஆரம்ப நிலையில் நீர் தேங்குவதைத் தவிர்த்து, 30 நாட்களுக்குள் களையெடுக்கவும்.",
            "te": "ప్రారంభ దశలో నీరు నిల్వకుండా చూసి, 30 రోజులలోపు కలుపు తీయండి."
        }
    },
    {
        "name": "Cotton",
        "primary_soil": ["black"],
        "secondary_soil": ["alluvial", "loamy"],
        "primary_season": ["kharif"],
        "secondary_season": ["annual"],
        "ideal_rain": 85,
        "min_rain": 50,
        "max_rain": 140,
        "primary_water": ["medium"],
        "secondary_water": ["low"],
        "duration": "150 - 180 days",
        "temp": "21°C - 30°C",
        "fertilizer": {
            "en": "NPK 100:50:50 kg/ha; foliar spray of 2% DAP during boll formation.",
            "kn": "NPK 100:50:50 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಕಾಯಿ ಕಟ್ಟುವ ಹಂತದಲ್ಲಿ 2% DAP ಸಿಂಪಡಿಸಿ.",
            "hi": "NPK 100:50:50 किग्रा/हेक्टेयर; टिंडे बनते समय 2% DAP का छिड़काव करें।",
            "ta": "NPK 100:50:50 கிலோ/எக்டர்; காய்கள் பிடிக்கும்போது 2% DAP தெளிக்கவும்.",
            "te": "NPK 100:50:50 కిలోలు/హెక్టారుకు; కాయలు పట్టే దశలో 2% DAP పిచికారీ చేయండి."
        },
        "tip": {
            "en": "Black cotton soil retains moisture well; monitor regularly for bollworms and whiteflies.",
            "kn": "ಕಪ್ಪು ಮಣ್ಣು ತೇವಾಂಶವನ್ನು ಚೆನ್ನಾಗಿ ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುತ್ತದೆ; ಕಾಯಿಕೊರಕ ಹುಳುಗಳ ಬಗ್ಗೆ ನಿಗಾ ಇರಿಸಿ.",
            "hi": "काली मिट्टी नमी बनाए रखती है; सुंडी और सफेद मक्खी की नियमित निगरानी करें।",
            "ta": "கரிசல் மண் ஈரப்பதத்தைத் தக்கவைக்கும்; காய்ப்புழுக்களைத் தொடர்ந்து கண்காணிக்கவும்.",
            "te": "నల్ల రేగడి నేల తేమను బాగా నిలుపుకుంటుంది; కాయతొలుచు పురుగులను గమనిస్తూ ఉండండి."
        }
    },
    {
        "name": "Sugarcane",
        "primary_soil": ["loamy", "black"],
        "secondary_soil": ["alluvial", "clay"],
        "primary_season": ["annual"],
        "secondary_season": ["kharif"],
        "ideal_rain": 150,
        "min_rain": 100,
        "max_rain": 280,
        "primary_water": ["high"],
        "secondary_water": ["medium"],
        "duration": "10 - 12 months",
        "temp": "20°C - 35°C",
        "fertilizer": {
            "en": "NPK 250:100:120 kg/ha applied in multiple stages with organic compost.",
            "kn": "ಸಾವಯವ ಗೊಬ್ಬರದೊಂದಿಗೆ ಹಲವು ಹಂತಗಳಲ್ಲಿ NPK 250:100:120 ಕೆಜಿ/ಹೆಕ್ಟೇರ್ ನೀಡಿ.",
            "hi": "जैविक खाद के साथ कई चरणों में NPK 250:100:120 किग्रा/हेक्टेयर डालें।",
            "ta": "இயற்கை உரத்துடன் பல கட்டங்களாக NPK 250:100:120 கிலோ/எக்டர் இடவும்.",
            "te": "సేంద్రీయ ఎరువులతో పాటు పలు దశల్లో NPK 250:100:120 కిలోలు/హెక్టారుకు వేయండి."
        },
        "tip": {
            "en": "Use earthing-up practices at 90-120 days to prevent lodging and improve root aeration.",
            "kn": "ಬೆಳೆ ಬೀಳುವುದನ್ನು ತಡೆಯಲು 90-120 ದಿನಗಳಲ್ಲಿ ಬುಡಕ್ಕೆ ಮಣ್ಣು ಏರಿಸಿ.",
            "hi": "फसल को गिरने से बचाने के लिए 90-120 दिनों में मिट्टी चढ़ाएं।",
            "ta": "பயிர் சாய்வதைத் தடுக்க 90-120 நாட்களில் மண் அணைக்கவும்.",
            "te": "పంట పడిపోకుండా ఉండటానికి 90-120 రోజులలో మొక్కల మొదళ్ల వద్ద మట్టి ఎగదోయండి."
        }
    },
    {
        "name": "Millets (Ragi / Bajra / Jowar)",
        "primary_soil": ["sandy", "red"],
        "secondary_soil": ["black", "loamy"],
        "primary_season": ["kharif", "zaid"],
        "secondary_season": ["summer"],
        "ideal_rain": 45,
        "min_rain": 15,
        "max_rain": 90,
        "primary_water": ["low"],
        "secondary_water": ["medium"],
        "duration": "75 - 100 days",
        "temp": "25°C - 35°C",
        "fertilizer": {
            "en": "NPK 40:20:20 kg/ha; responds well to Farmyard Manure (FYM).",
            "kn": "NPK 40:20:20 ಕೆಜಿ/ಹೆಕ್ಟೇರ್; ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರಕ್ಕೆ (FYM) ಉತ್ತಮವಾಗಿ ಸ್ಪಂದಿಸುತ್ತದೆ.",
            "hi": "NPK 40:20:20 किग्रा/हेक्टेयर; गोबर की खाद (FYM) से अच्छी उपज मिलती है।",
            "ta": "NPK 40:20:20 கிலோ/எக்டர்; தொழுஉரத்திற்கு (FYM) நன்கு பலன் தரும்.",
            "te": "NPK 40:20:20 కిలోలు/హెక్టారుకు; పశువుల ఎరువుకు (FYM) బాగా స్పందిస్తుంది."
        },
        "tip": {
            "en": "Highly drought-tolerant; ideal for dryland farming with minimal irrigation.",
            "kn": "ಬರ ನಿರೋಧಕ ಬೆಳೆ; ಕಡಿಮೆ ನೀರಿನಲ್ಲಿ ಒಣಭೂಮಿ ಕೃಷಿಗೆ ಅತ್ಯಂತ ಸೂಕ್ತ.",
            "hi": "अत्यधिक सूखा-सहिष्णु; कम सिंचाई वाले क्षेत्रों के लिए सर्वोत्तम।",
            "ta": "வறட்சியைத் தாங்கும் பயிர்; குறைந்த நீர்ப்பாசனத்திற்கு மிகவும் ஏற்றது.",
            "te": "కరువును తట్టుకునే పంట; తక్కువ నీటితో మెట్ట వ్యవసాయానికి అనుకూలం."
        }
    }
]
UI_TEXT = {
    "en": {
        "high": "Highly Suitable (Optimal Yield Expected)",
        "med": "Moderately Suitable (Requires Management)",
        "low": "Low Suitability (High Risk)",
        "soil_ok": "Ideal {soil} soil",
        "soil_sec": "Compatible {soil} soil",
        "soil_bad": "{soil} soil is not preferred",
        "season_ok": "Prime {season} season",
        "season_sec": "Secondary {season} season",
        "season_bad": "Off-season for {season}",
        "water_ok": "Optimal {water} water supply",
        "water_sec": "Manageable {water} water supply",
        "water_bad": "Water mismatch ({water} provided)",
        "rain_ok": "Rainfall ({rain} mm) is within optimal range ({min_r}-{max_r} mm)",
        "rain_bad": "Rainfall ({rain} mm) is outside ideal {min_r}-{max_r} mm range",
        "note": "Note: "
    },
    "kn": {
        "high": "ಅತ್ಯಂತ ಸೂಕ್ತವಾಗಿದೆ (ಉತ್ತಮ ಇಳುವರಿ ನಿರೀಕ್ಷಿತ)",
        "med": "ಸಾಧಾರಣ ಸೂಕ್ತವಾಗಿದೆ (ಸರಿಯಾದ ನಿರ್ವಹಣೆ ಅಗತ್ಯ)",
        "low": "ಕಡಿಮೆ ಸೂಕ್ತತೆ (ಹೆಚ್ಚಿನ ಅಪಾಯ)",
        "soil_ok": "ಸೂಕ್ತವಾದ {soil} ಮಣ್ಣು",
        "soil_sec": "ಹೊಂದಿಕೊಳ್ಳುವ {soil} ಮಣ್ಣು",
        "soil_bad": "{soil} ಮಣ್ಣು ಅಷ್ಟಾಗಿ ಸೂಕ್ತವಲ್ಲ",
        "season_ok": "ಪ್ರಮುಖ {season} ಋತು",
        "season_sec": "ಪರ್ಯಾಯ {season} ಋತು",
        "season_bad": "{season} ಋತುವಿಗೆ ಸೂಕ್ತವಲ್ಲ",
        "water_ok": "ಉತ್ತಮ {water} ನೀರಿನ ಲಭ್ಯತೆ",
        "water_sec": "ನಿರ್ವಹಿಸಬಹುದಾದ {water} ನೀರಿನ ಲಭ್ಯತೆ",
        "water_bad": "ನೀರಿನ ಹೊಂದಾಣಿಕೆಯಿಲ್ಲ ({water})",
        "rain_ok": "ಮಳೆಯ ಪ್ರಮಾಣ ({rain} mm) ಸೂಕ್ತ ಮಿತಿಯಲ್ಲಿದೆ ({min_r}-{max_r} mm)",
        "rain_bad": "ಮಳೆಯ ಪ್ರಮಾಣ ({rain} mm) ಸೂಕ್ತ ಮಿತಿಗಿಂತ ({min_r}-{max_r} mm) ಹೊರಗಿದೆ",
        "note": "ಸೂಚನೆ: "
    },
    "hi": {
        "high": "अत्यधिक उपयुक्त (सर्वोत्तम उपज की उम्मीद)",
        "med": "मध्यम रूप से उपयुक्त (देखभाल आवश्यक)",
        "low": "कम उपयुक्तता (अधिक जोखिम)",
        "soil_ok": "आदर्श {soil} मिट्टी",
        "soil_sec": "अनुकूल {soil} मिट्टी",
        "soil_bad": "{soil} मिट्टी उपयुक्त नहीं है",
        "season_ok": "मुख्य {season} मौसम",
        "season_sec": "वैकल्पिक {season} मौसम",
        "season_bad": "{season} के लिए बेमौसम",
        "water_ok": "उत्तम {water} पानी की उपलब्धता",
        "water_sec": "प्रबंधनीय {water} पानी की उपलब्धता",
        "water_bad": "पानी का असंतुलन ({water})",
        "rain_ok": "वर्षा ({rain} mm) आदर्श सीमा ({min_r}-{max_r} mm) के भीतर है",
        "rain_bad": "वर्षा ({rain} mm) आदर्श सीमा ({min_r}-{max_r} mm) से बाहर है",
        "note": "नोट: "
    },
    "ta": {
        "high": "மிகவும் பொருத்தமானது (சிறந்த மகசூல் எதிர்பார்க்கப்படுகிறது)",
        "med": "மிதமான பொருத்தம் (பராமரிப்பு தேவை)",
        "low": "குறைந்த பொருத்தம் (அதிக ஆபத்து)",
        "soil_ok": "சிறந்த {soil} மண்",
        "soil_sec": "பொருந்தக்கூடிய {soil} மண்",
        "soil_bad": "{soil} மண் உகந்ததல்ல",
        "season_ok": "முதன்மை {season} பருவம்",
        "season_sec": "இரண்டாம் நிலை {season} பருவம்",
        "season_bad": "{season} பருவத்திற்கு ஏற்றதல்ல",
        "water_ok": "சிறந்த {water} நீர் இருப்பு",
        "water_sec": "சமாளிக்கக்கூடிய {water} நீர் இருப்பு",
        "water_bad": "நீர் பொருந்தவில்லை ({water})",
        "rain_ok": "மழையளவு ({rain} mm) உகந்த வரம்பிற்குள் ({min_r}-{max_r} mm) உள்ளது",
        "rain_bad": "மழையளவு ({rain} mm) உகந்த வரம்பிற்கு ({min_r}-{max_r} mm) வெளியே உள்ளது",
        "note": "குறிப்பு: "
    },
    "te": {
        "high": "అత్యంత అనుకూలమైనది (ఉత్తమ దిగుబడి ఆశించవచ్చు)",
        "med": "మధ్యస్థంగా అనుకూలమైనది (నిర్వహణ అవసరం)",
        "low": "తక్కువ అనుకూలత (అధిక ప్రమాదం)",
        "soil_ok": "అనువైన {soil} నేల",
        "soil_sec": "సరిపోయే {soil} నేల",
        "soil_bad": "{soil} నేల అనుకూలం కాదు",
        "season_ok": "ప్రధాన {season} సీజన్",
        "season_sec": "ప్రత్యామ్నాయ {season} సీజన్",
        "season_bad": "{season} సీజన్‌కు అనుకూలం కాదు",
        "water_ok": "ఉత్తమ {water} నీటి లభ్యత",
        "water_sec": "నిర్వహించదగిన {water} నీటి లభ్యత",
        "water_bad": "నీటి అసమతుల్యత ({water})",
        "rain_ok": "వర్షపాతం ({rain} mm) అనుకూల పరిధిలో ({min_r}-{max_r} mm) ఉంది",
        "rain_bad": "వర్షపాతం ({rain} mm) అనుకూల పరిధికి ({min_r}-{max_r} mm) వెలుపల ఉంది",
        "note": "గమనిక: "
    }
}


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Request body must be a valid JSON object.'}), 400

        soil_value = data.get('soil_type', '')
        season_value = data.get('season', '')
        water_value = data.get('water_availability', '')
        lang_value = data.get('lang', 'en')

        if not isinstance(soil_value, str) or not isinstance(season_value, str) or not isinstance(water_value, str):
            return jsonify({'error': 'Please select Soil Type, Season, and Water Availability.'}), 400
        if not isinstance(lang_value, str):
            lang_value = 'en'

        soil = soil_value.strip().lower()
        season = season_value.strip().lower()
        water = water_value.strip().lower()
        rainfall = float(data.get('rainfall', -1))
        if not math.isfinite(rainfall):
            return jsonify({'error': 'Please enter a realistic rainfall value between 0 mm and 5000 mm.'}), 400
        lang = lang_value.strip().lower()
        txt = UI_TEXT.get(lang, UI_TEXT['en'])

        if not soil or not season or not water:
            return jsonify({'error': 'Please select Soil Type, Season, and Water Availability.'}), 400
        if rainfall < 0 or rainfall > 5000:
            return jsonify({'error': 'Please enter a realistic rainfall value between 0 mm and 5000 mm.'}), 400

        scored_crops = []
        for crop in CROPS:
            score = 0.0
            reasons = []
            warnings = []

            if soil in crop['primary_soil']:
                score += 30
                reasons.append(txt['soil_ok'].format(soil=soil))
            elif soil in crop['secondary_soil']:
                score += 18
                reasons.append(txt['soil_sec'].format(soil=soil))
            else:
                score -= 10
                warnings.append(txt['soil_bad'].format(soil=soil))

            if season in crop['primary_season']:
                score += 30
                reasons.append(txt['season_ok'].format(season=season))
            elif season in crop['secondary_season']:
                score += 18
                reasons.append(txt['season_sec'].format(season=season))
            else:
                score -= 15
                warnings.append(txt['season_bad'].format(season=season))

            if water in crop['primary_water']:
                score += 20
                reasons.append(txt['water_ok'].format(water=water))
            elif water in crop['secondary_water']:
                score += 10
                reasons.append(txt['water_sec'].format(water=water))
            else:
                score -= 15
                warnings.append(txt['water_bad'].format(water=water))

            if crop['min_rain'] <= rainfall <= crop['max_rain']:
                rain_diff = abs(rainfall - crop['ideal_rain'])
                max_span = max(crop['ideal_rain'] - crop['min_rain'], crop['max_rain'] - crop['ideal_rain'], 1)
                rain_score = 20.0 - (rain_diff / max_span) * 8.0
                score += max(12.0, rain_score)
                reasons.append(txt['rain_ok'].format(rain=rainfall, min_r=crop['min_rain'], max_r=crop['max_rain']))
            else:
                distance = crop['min_rain'] - rainfall if rainfall < crop['min_rain'] else rainfall - crop['max_rain']
                penalty = min(20.0, (distance / 50.0) * 10.0)
                score -= penalty
                warnings.append(txt['rain_bad'].format(rain=rainfall, min_r=crop['min_rain'], max_r=crop['max_rain']))

            final_percentage = round(max(5.0, min(100.0, score)), 1)

            if final_percentage >= 80:
                suitability_level = txt['high']
            elif final_percentage >= 55:
                suitability_level = txt['med']
            else:
                suitability_level = txt['low']

            summary_text = ""
            if reasons:
                summary_text += ", ".join(reasons) + ". "
            if warnings:
                summary_text += txt['note'] + ", ".join(warnings) + "."

            fert_text = crop['fertilizer'].get(lang, crop['fertilizer']['en'])
            tip_text = crop['tip'].get(lang, crop['tip']['en'])

            scored_crops.append({
                'score': final_percentage,
                'name': crop['name'],
                'confidence': f"{final_percentage}%",
                'suitability_level': suitability_level,
                'why_it_fits': summary_text.strip(),
                'duration': crop['duration'],
                'ideal_temp': crop['temp'],
                'fertilizer': fert_text,
                'farming_tip': tip_text
            })

        scored_crops.sort(key=lambda x: x['score'], reverse=True)
        return jsonify({'recommendations': scored_crops[:3]})

    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid numeric input for rainfall.'}), 400
    except Exception:
        app.logger.exception('Unexpected error while generating crop recommendations')
        return jsonify({'error': 'Unable to generate recommendations. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
