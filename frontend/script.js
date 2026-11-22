const API_BASE_URL = (() => {
    const { hostname, port, protocol, origin } = window.location;
    if (protocol === 'file:' || (['', 'localhost', '127.0.0.1'].includes(hostname) && port !== '5000')) {
        return 'http://127.0.0.1:5000';
    }
    return origin;
})();

const FALLBACK_CROP_IMG = "data:image/svg+xml;utf8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 160"><rect width="240" height="160" fill="#e9f2e6"/><path d="M120 125V65M120 85c-18-16-42-12-46 6 18 12 36 8 46-6zm0-12c18-16 42-12 46 6-18 12-36 8-46-6z" stroke="#2d5a3c" stroke-width="5" fill="#c4e173" stroke-linecap="round" stroke-linejoin="round"/></svg>'
);

const T = {
    en: {
        title: "Crop Recommendation System",
        soil: ["Select Soil Type", "Alluvial Soil", "Black Soil", "Red / Laterite Soil", "Loamy Soil", "Clay Soil", "Sandy Soil"],
        season: ["Select Season", "Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)", "Annual (All Year)"],
        rain: "Annual Rainfall (mm, e.g. 850)",
        water: ["Water Availability", "High (Abundant Irrigation / Rain)", "Medium (Moderate Irrigation)", "Low (Rainfed / Dry)"],
        btn: "Recommend Crop", wait: "Calculating real-world accuracy scores...", head: "Top 3 Real-World Crop Predictions",
        guide: "<strong>Suitability Guide:</strong> 80–100% = Optimal | 55–79% = Viable | Below 55% = High Risk",
        best: "Best Match (#1)", opt: "Option", match: "Match", durationLbl: "Duration", tempLbl: "Ideal Temp", phLbl: "Soil pH", rainLbl: "Rainfall",
        printBtn: "Print Report", guideBtn: "View Stage-by-Stage Cultivation Guidelines", emptyHistory: "No saved recommendations yet.",
        lbl: ["Condition Analysis", "Growth Duration", "Ideal Temperature", "Fertilizer Advice", "Farming Tip"],
        stages: ["Land Preparation", "Sowing & Spacing", "Irrigation Schedule", "Pest & Weed Control", "Harvesting"],
        wikiSectionTitle: "Complete Crop Cultivation Profiles",
        wikiSectionSub: "Explore real-world climate, soil pH, NPK nutrition, research guides, and stage-by-stage cultivation practices for all 20 crops.",
        crops: {}
    },
    kn: {
        title: "ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ",
        soil: ["ಮಣ್ಣಿನ ಪ್ರಕಾರ ಆಯ್ಕೆಮಾಡಿ", "ಮೆಕ್ಕಲು ಮಣ್ಣು", "ಕಪ್ಪು ಮಣ್ಣು", "ಕೆಂಪು ಮಣ್ಣು", "ಗೋಡು ಮಣ್ಣು", "ಜೇಡಿಮಣ್ಣು", "ಮರಳು ಮಣ್ಣು"],
        season: ["ಋತುವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "ಮುಂಗಾರು (Kharif)", "ಹಿಂಗಾರು (Rabi)", "ಬೇಸಿಗೆ (Zaid)", "ವಾರ್ಷಿಕ (Annual)"],
        rain: "ವಾರ್ಷಿಕ ಮಳೆ (ಮಿಮೀ, ಉದಾ: 850)",
        water: ["ನೀರಿನ ಲಭ್ಯತೆ", "ಹೆಚ್ಚು (ಸಾಕಷ್ಟು ನೀರಾವರಿ)", "ಮಧ್ಯಮ", "ಕಡಿಮೆ (ಮಳೆಯಾಶ್ರಿತ)"],
        btn: "ಬೆಳೆ ಶಿಫಾರಸು ಮಾಡಿ", wait: "ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...", head: "ಅತ್ಯುತ್ತಮ 3 ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
        guide: "<strong>ಮಾರ್ಗದರ್ಶಿ:</strong> 80–100% = ಅತ್ಯುತ್ತಮ | 55–79% = ಸಾಧಾರಣ | 55% ಕಡಿಮೆ = ಅಪಾಯ",
        best: "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ (#1)", opt: "ಆಯ್ಕೆ", match: "ಹೊಂದಾಣಿಕೆ", durationLbl: "ಬೆಳೆ ಅವಧಿ", tempLbl: "ಸೂಕ್ತ ತಾಪಮಾನ", phLbl: "ಮಣ್ಣಿನ pH", rainLbl: "ಮಳೆ",
        printBtn: "ವರದಿ ಮುದ್ರಿಸಿ", guideBtn: "ಸಂಪೂರ್ಣ ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ ನೋಡಿ", emptyHistory: "ಇನ್ನೂ ಯಾವುದೇ ಉಳಿಸಿದ ಶಿಫಾರಸುಗಳಿಲ್ಲ.",
        lbl: ["ವಿಶ್ಲೇಷಣೆ", "ಬೆಳೆ ಅವಧಿ", "ಸೂಕ್ತ ತಾಪಮಾನ", "ಗೊಬ್ಬರ ಸಲಹೆ", "ಕೃಷಿ ಸಲಹೆ"],
        stages: ["ಭೂಮಿ ಸಿದ್ಧತೆ", "ಬಿತ್ತನೆ", "ನೀರಾವರಿ", "ಕೀಟ ನಿಯಂತ್ರಣ", "ಕಟಾವು"],
        wikiSectionTitle: "ಸಂಪೂರ್ಣ ಬೆಳೆ ಕೃಷಿ ಮಾಹಿತಿ",
        wikiSectionSub: "ಎಲ್ಲಾ 20 ಬೆಳೆಗಳ ಹವಾಮಾನ, ಮಣ್ಣಿನ pH, ಗೊಬ್ಬರ, ಸಂಶೋಧನಾ ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಹಂತ-ಹಂತದ ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿಯನ್ನು ನೋಡಿ.",
        crops: { "Rice (Paddy)": "ಭತ್ತ (Rice)", "Wheat": "ಗೋಧಿ (Wheat)", "Maize (Corn)": "ಮೆಕ್ಕೆಜೋಳ (Maize)", "Cotton": "ಹತ್ತಿ (Cotton)", "Sugarcane": "ಕಬ್ಬು (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "ಸಿರಿಧಾನ್ಯಗಳು (Millets)", "Groundnut (Peanut)": "ಶೇಂಗಾ (Groundnut)", "Soybean": "ಸೋಯಾಬೀನ್ (Soybean)", "Chickpea (Bengal Gram)": "ಕಡಲೆ (Chickpea)", "Potato": "ಆಲೂಗಡ್ಡೆ (Potato)", "Mustard (Sarson)": "ಸಾಸಿವೆ (Mustard)", "Pigeon Pea (Tur / Arhar)": "ತೊಗರಿ (Pigeon Pea)", "Sunflower": "ಸೂರ್ಯಕಾಂತಿ (Sunflower)", "Onion": "ಈರುಳ್ಳಿ (Onion)", "Tomato": "ಟೊಮೆಟೊ (Tomato)", "Green Gram (Moong)": "ಹೆಸರುಕಾಳು (Moong)", "Banana": "ಬಾಳೆ (Banana)", "Coconut": "ತೆಂಗು (Coconut)", "Tea": "ಚಹಾ (Tea)", "Coffee": "ಕಾಫಿ (Coffee)" }
    },
    hi: {
        title: "फसल अनुशंसा प्रणाली",
        soil: ["मिट्टी का प्रकार चुनें", "जलोढ़ मिट्टी", "काली मिट्टी", "लाल मिट्टी", "दोमट मिट्टी", "चिकनी मिट्टी", "बलुई मिट्टी"],
        season: ["मौसम चुनें", "खरीफ (मानसून)", "रबी (सर्दी)", "जायद (गर्मी)", "वार्षिक (पूरे साल)"],
        rain: "वार्षिक वर्षा (मिमी, जैसे 850)",
        water: ["पानी की उपलब्धता", "अधिक (पर्याप्त सिंचाई)", "मध्यम", "कम (वर्षा आधारित)"],
        btn: "फसल का सुझाव दें", wait: "जांच की जा रही है...", head: "शीर्ष 3 उपयुक्त फसलें",
        guide: "<strong>गाइड:</strong> 80–100% = सर्वोत्तम | 55–79% = मध्यम | 55% से कम = जोखिम",
        best: "सर्वोत्तम विकल्प (#1)", opt: "विकल्प", match: "मिलान", durationLbl: "फसल अवधि", tempLbl: "आदर्श तापमान", phLbl: "मिट्टी pH", rainLbl: "वर्षा",
        printBtn: "रिपोर्ट प्रिंट करें", guideBtn: "चरण-दर-चरण खेती दिशानिर्देश देखें", emptyHistory: "अभी तक कोई सहेजा गया सुझाव नहीं है।",
        lbl: ["स्थिति विश्लेषण", "फसल अवधि", "आदर्श तापमान", "उर्वरक सलाह", "खेती की टिप"],
        stages: ["खेत की तैयारी", "बुवाई", "सिंचाई", "कीट नियंत्रण", "कटाई"],
        wikiSectionTitle: "संपूर्ण फसल खेती प्रोफ़ाइल",
        wikiSectionSub: "सभी 20 फसलों के लिए जलवायु, मिट्टी का pH, खाद और चरणबद्ध खेती के दिशानिर्देश देखें।",
        crops: { "Rice (Paddy)": "धान / चावल (Rice)", "Wheat": "गेहूं (Wheat)", "Maize (Corn)": "मक्का (Maize)", "Cotton": "कपास (Cotton)", "Sugarcane": "गन्ना (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "बाजरा / रागी (Millets)", "Groundnut (Peanut)": "मूंगफली (Groundnut)", "Soybean": "सोयाबीन (Soybean)", "Chickpea (Bengal Gram)": "चना (Chickpea)", "Potato": "आलू (Potato)", "Mustard (Sarson)": "सरसों (Mustard)", "Pigeon Pea (Tur / Arhar)": "अरहर / तूर (Pigeon Pea)", "Sunflower": "सूरजमुखी (Sunflower)", "Onion": "प्याज (Onion)", "Tomato": "टमाटर (Tomato)", "Green Gram (Moong)": "मूंग (Moong)", "Banana": "केला (Banana)", "Coconut": "नारियल (Coconut)", "Tea": "चाय (Tea)", "Coffee": "कॉफी (Coffee)" }
    },
    ta: {
        title: "பயிர் பரிந்துரை அமைப்பு",
        soil: ["மண் வகையைத் தேர்ந்தெடுக்கவும்", "வண்டல் மண்", "கரிசல் மண்", "செம்மண்", "களிமண் கலந்த மண்", "களிமண்", "மணல் மண்"],
        season: ["பருவத்தைத் தேர்ந்தெடுக்கவும்", "கரீஃப் (மழைக்காலம்)", "ரபி (குளிர்காலம்)", "சையத் (கோடைகாலம்)", "ஆண்டு முழுவதும்"],
        rain: "ஆண்டு மழையளவு (மிமீ, எ.கா. 850)",
        water: ["நீர் இருப்பு", "அதிகம்", "நடுத்தரம்", "குறைவு"],
        btn: "பயிரைப் பரிந்துரைக்கவும்", wait: "கணக்கிடப்படுகிறது...", head: "சிறந்த 3 பயிர் பரிந்துரைகள்",
        guide: "<strong>வழிகாட்டி:</strong> 80–100% = சிறந்தது | 55–79% = நடுத்தரம் | 55% கீழ் = ஆபத்து",
        best: "சிறந்த தேர்வு (#1)", opt: "விருப்பம்", match: "பொருத்தம்", durationLbl: "வளர்ச்சி காலம்", tempLbl: "சிறந்த வெப்பநிலை", phLbl: "மண் pH", rainLbl: "மழை",
        printBtn: "அறிக்கை அச்சிடு", guideBtn: "முழு சாகுபடி வழிகாட்டுதல்களைப் பார்க்கவும்", emptyHistory: "சேமிக்கப்பட்ட பரிந்துரைகள் இன்னும் இல்லை.",
        lbl: ["நிலை ஆய்வு", "வளர்ச்சி காலம்", "சிறந்த வெப்பநிலை", "உர ஆலோசனை", "விவசாய குறிப்பு"],
        stages: ["நிலம் தயாரித்தல்", "விதைப்பு", "நீர்ப்பாசனம்", "பூச்சி கட்டுப்பாடு", "அறுவடை"],
        wikiSectionTitle: "முழுமையான பயிர் சாகுபடி வழிகாட்டி",
        wikiSectionSub: "அனைத்து 20 பயிர்களின் காலநிலை, மண் pH, உர அளவு மற்றும் சாகுபடி முறைகளைப் பார்க்கவும்.",
        crops: { "Rice (Paddy)": "நெல் (Rice)", "Wheat": "கோதுமை (Wheat)", "Maize (Corn)": "மக்காச்சோளம் (Maize)", "Cotton": "பருத்தி (Cotton)", "Sugarcane": "கரும்பு (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "சிறுதானியங்கள் (Millets)", "Groundnut (Peanut)": "நிலக்கடலை (Groundnut)", "Soybean": "சோயாபீன்ஸ் (Soybean)", "Chickpea (Bengal Gram)": "கொண்டைக்கடலை (Chickpea)", "Potato": "உருளைக்கிழங்கு (Potato)", "Mustard (Sarson)": "கடுகு (Mustard)", "Pigeon Pea (Tur / Arhar)": "துவரை (Pigeon Pea)", "Sunflower": "சூரியகாந்தி (Sunflower)", "Onion": "வெங்காயம் (Onion)", "Tomato": "தக்காளி (Tomato)", "Green Gram (Moong)": "பாசிப்பயறு (Moong)", "Banana": "வாழை (Banana)", "Coconut": "தென்னை (Coconut)", "Tea": "தேயிலை (Tea)", "Coffee": "காபி (Coffee)" }
    },
    te: {
        title: "పంట సిఫార్సు వ్యవస్థ",
        soil: ["నేల రకాన్ని ఎంచుకోండి", "ఒండ్రు నేల", "నల్ల రేగడి నేల", "ఎర్ర నేల", "లోమీ నేల", "బంకమట్టి నేల", "ఇసుక నేల"],
        season: ["సీజన్ ఎంచుకోండి", "ఖరీఫ్ (వర్షాకాలం)", "రబీ (చలికాలం)", "జైద్ (వేసవి)", "వార్షిక (సంవత్సరం)"],
        rain: "వార్షిక వర్షపాతం (మిమీ, ఉదా: 850)",
        water: ["నీటి లభ్యత", "ఎక్కువ", "మధ్యస్థం", "తక్కువ"],
        btn: "పంటను సిఫార్సు చేయండి", wait: "లెక్కిస్తోంది...", head: "అత్యుత్తమ 3 పంట సిఫార్సులు",
        guide: "<strong>గైడ్:</strong> 80–100% = ఉత్తమం | 55–79% = మధ్యస్థం | 55% తక్కువ = ప్రమాదం",
        best: "ఉత్తమ ఎంపిక (#1)", opt: "ఎంపిక", match: "సరిపోలిక", durationLbl: "పంట కాలం", tempLbl: "ఉష్ణోగ్రత", phLbl: "నేల pH", rainLbl: "వర్షపాతం",
        printBtn: "నివేదిక ముద్రించు", guideBtn: "పూర్తి సాగు మార్గదర్శకాలను చూడండి", emptyHistory: "ఇంకా సేవ్ చేసిన సిఫార్సులు లేవు.",
        lbl: ["విశ్లేషణ", "పంట కాలం", "ఉష్ణోగ్రత", "ఎరువుల సలహా", "వ్యవసాయ చిట్కా"],
        stages: ["నేల తయారీ", "విత్తడం", "నీటిపారుదల", "పురుగు నియంత్రణ", "కోత"],
        wikiSectionTitle: "పూర్తి పంట సాగు వివరాలు",
        wikiSectionSub: "మొత్తం 20 పంటల వాతావరణం, నేల pH, ఎరువులు మరియు దశలవారీ సాగు మార్గదర్శకాలను చూడండి.",
        crops: { "Rice (Paddy)": "వరి (Rice)", "Wheat": "గోధుమ (Wheat)", "Maize (Corn)": "మొక్కజొన్న (Maize)", "Cotton": "పత్తి (Cotton)", "Sugarcane": "చెరకు (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "చిరుధాన్యాలు (Millets)", "Groundnut (Peanut)": "వేరుశనగ (Groundnut)", "Soybean": "సోయాబీన్ (Soybean)", "Chickpea (Bengal Gram)": "శనగలు (Chickpea)", "Potato": "బంగాళాదుంప (Potato)", "Mustard (Sarson)": "ఆవాలు (Mustard)", "Pigeon Pea (Tur / Arhar)": "కందులు (Pigeon Pea)", "Sunflower": "పొద్దుతిరుగుడు (Sunflower)", "Onion": "ఉల్లిపాయ (Onion)", "Tomato": "టమాటా (Tomato)", "Green Gram (Moong)": "పెసలు (Moong)", "Banana": "అరటి (Banana)", "Coconut": "కొబ్బరి (Coconut)", "Tea": "తేయాకు (Tea)", "Coffee": "కాఫీ (Coffee)" }
    }
};

const UI_LABELS = {
    en: ["Language", "SMART FARMING ASSISTANT", "Share your farm conditions and get the crops most likely to thrive.", "Top 3 matches", "Real-world agronomy", "Stage-wise guidelines", "Tell us about your farm", "Ready", "Soil type", "Growing season", "Annual rainfall", "Water availability", "Reset", "Recommend Crop", "AgriChoice • Smart crop planning", "History", "SAVED RESULTS", "Recommendation History", "Clear all history", "Crop Guide", "Avg temperature (°C)", "Soil pH", "Quick test:", "Monsoon Paddy", "Black Cotton", "Dryland Millets", "Major crops", "Regional languages", "Precision scoring", "Agronomic ranges grounded in FAO, ICAR, TNAU, and Wikipedia references; verify with local soil testing."],
    kn: ["ಭಾಷೆ", "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ", "ನಿಮ್ಮ ಹೊಲದ ಪರಿಸ್ಥಿತಿ ನೀಡಿ ಮತ್ತು ಸೂಕ್ತ ಬೆಳೆಗಳನ್ನು ತಿಳಿದುಕೊಳ್ಳಿ.", "ಮೇಲಿನ 3 ಬೆಳೆಗಳು", "ನೈಜ ಕೃಷಿ ಮಾಹಿತಿ", "ಹಂತ-ಹಂತದ ಮಾರ್ಗದರ್ಶನ", "ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳು", "ಸಿದ್ಧ", "ಮಣ್ಣಿನ ಪ್ರಕಾರ", "ಬೆಳೆ ಋತು", "ವಾರ್ಷಿಕ ಮಳೆ", "ನೀರಿನ ಲಭ್ಯತೆ", "ಮರುಹೊಂದಿಸಿ", "ಬೆಳೆ ಶಿಫಾರಸು ಮಾಡಿ", "AgriChoice • ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಯೋಜನೆ", "ಇತಿಹಾಸ", "ಉಳಿಸಿದ ಫಲಿತಾಂಶಗಳು", "ಶಿಫಾರಸು ಇತಿಹಾಸ", "ಎಲ್ಲಾ ಇತಿಹಾಸ ಅಳಿಸಿ", "ಬೆಳೆ ಮಾರ್ಗದರ್ಶಿ", "ಸರಾಸರಿ ತಾಪಮಾನ (°C)", "ಮಣ್ಣಿನ pH", "ತ್ವರಿತ ಪರೀಕ್ಷೆ:", "ಮುಂಗಾರು ಭತ್ತ", "ಕಪ್ಪು ಹತ್ತಿ", "ಒಣಭೂಮಿ ರಾಗಿ", "ಪ್ರಮುಖ ಬೆಳೆಗಳು", "ಪ್ರಾದೇಶಿಕ ಭಾಷೆಗಳು", "ನಿಖರ ಮೌಲ್ಯಮಾಪನ", "FAO, ICAR, TNAU ಮತ್ತು ವಿಕಿಪೀಡಿಯಾ ಆಧಾರಿತ ಮಾಹಿತಿ; ಸ್ಥಳೀಯ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯೊಂದಿಗೆ ದೃಢೀಕರಿಸಿ."],
    hi: ["भाषा", "स्मार्ट खेती सहायक", "अपनी खेत की स्थिति दें और सबसे उपयुक्त फसलें जानें।", "शीर्ष 3 विकल्प", "वास्तविक कृषि डेटा", "चरणबद्ध दिशानिर्देश", "अपने खेत के बारे में बताएं", "तैयार", "मिट्टी का प्रकार", "बुआई का मौसम", "वार्षिक वर्षा", "पानी की उपलब्धता", "रीसेट", "फसल का सुझाव दें", "AgriChoice • स्मार्ट फसल योजना", "इतिहास", "सहेजे गए परिणाम", "अनुशंसा इतिहास", "सभी इतिहास मिटाएं", "फसल गाइड", "औसत तापमान (°C)", "मिट्टी का pH", "त्वरित परीक्षण:", "खरीफ धान", "काली कपास", "सूखा बाजरा", "प्रमुख फसलें", "क्षेत्रीय भाषाएं", "सटीक स्कोरिंग", "FAO, ICAR, TNAU और विकिपीडिया पर आधारित; स्थानीय मिट्टी परीक्षण से पुष्टि करें।"],
    ta: ["மொழி", "ஸ்மார்ட் விவசாய உதவியாளர்", "பண்ணையின் நிலையைச் சொல்லி சிறந்த பயிர்களைக் கண்டறியுங்கள்.", "சிறந்த 3 தேர்வுகள்", "உண்மையான வேளாண் தகவல்", "படிப்படியான வழிகாட்டல்", "பண்ணை விவரங்களைச் சொல்லுங்கள்", "தயார்", "மண் வகை", "பயிர் பருவம்", "வருடாந்திர மழை", "நீர் இருப்பு", "மீட்டமை", "பயிரைப் பரிந்துரைக்கவும்", "AgriChoice • திறன்வாய்ந்த பயிர் திட்டம்", "வரலாறு", "சேமித்த முடிவுகள்", "பரிந்துரை வரலாறு", "அனைத்து வரலாற்றையும் அழி", "பயிர் வழிகாட்டி", "சராசரி வெப்பநிலை (°C)", "மண் pH", "விரைவு சோதனை:", "பருவ நெல்", "கரிசல் பருத்தி", "மானாவாரி ராகி", "முக்கிய பயிர்கள்", "பிராந்திய மொழிகள்", "துல்லிய மதிப்பீடு", "FAO, ICAR, TNAU மற்றும் விக்கிப்பீடியா தகவல்கள்; உள்ளூர் மண் பரிசோதனையுடன் உறுதிப்படுத்தவும்."],
    te: ["భాష", "స్మార్ట్ వ్యవసాయ సహాయకుడు", "పొల పరిస్థితులు తెలుపుతూ అత్యనుకూల పంటలను తెలుసుకోండి.", "అగ్ర 3 ఎంపికలు", "వాస్తవ వ్యవసాయ సమాచారం", "దశలవారీ మార్గదర్శకాలు", "మీ పొలం వివరాలు చెప్పండి", "సిద్ధం", "నేల రకం", "పంట సీజన్", "వార్షిక వర్షపాతం", "నీటి లభ్యత", "రీసెట్", "పంటను సిఫార్సు చేయండి", "AgriChoice • స్మార్ట్ పంట ప్రణాళిక", "చరిత్ర", "సేవ్ చేసిన ఫలితాలు", "సిఫార్సు చరిత్ర", "చరిత్రను క్లియర్ చేయండి", "పంట గైడ్", "సగటు ఉష్ణోగ్రత (°C)", "నేల pH", "త్వరిత పరీక్ష:", "ఖరీఫ్ వరి", "నల్ల పత్తి", "మెట్ట రాగులు", "ప్రధాన పంటలు", "ప్రాంతీయ భాషలు", "ఖచ్చితమైన స్కోరింగ్", "FAO, ICAR, TNAU మరియు వికీపీడియా ఆధారితం; స్థానిక నేల పరీక్షతో నిర్ధారించండి."]
};

const staticIds = [
    'languageLabel', 'eyebrow', 'introText', 'featureOne', 'featureTwo', 'featureThree',
    'formTitle', 'statusText', 'soilLabel', 'seasonLabel', 'rainLabel', 'waterLabel',
    'resetBtn', 'submitText', 'footerText', 'historyLabel', 'historyEyebrow', 'historyTitle',
    'clearHistoryBtn', 'encyclopediaLabel', 'tempInputLabel', 'phInputLabel',
    'presetsLabel', 'presetPaddy', 'presetCotton', 'presetMillet',
    'statCropsLabel', 'statLangsLabel', 'statGuidanceLabel', 'footerMeta'
];

const PRESETS = {
    paddy: { soil_type: 'alluvial', season: 'kharif', rainfall: 1750, water_availability: 'high', temperature: 28, soil_ph: 6.0 },
    cotton: { soil_type: 'black', season: 'kharif', rainfall: 850, water_availability: 'medium', temperature: 27, soil_ph: 6.5 },
    millet: { soil_type: 'red', season: 'zaid', rainfall: 450, water_availability: 'low', temperature: 29, soil_ph: 6.2 }
};

let lang = 'en';
const rainfallInput = document.getElementById('rainfall');
const rainfallSlider = document.getElementById('rainfallSlider');
const rainTierBadge = document.getElementById('rainTierBadge');

function updateRainBadge(val) {
    const n = parseFloat(val);
    if (Number.isNaN(n)) { rainTierBadge.textContent = '0–5000 mm'; return; }
    if (n < 500) rainTierBadge.textContent = `${n} mm • Low`;
    else if (n <= 1150) rainTierBadge.textContent = `${n} mm • Moderate`;
    else rainTierBadge.textContent = `${n} mm • High`;
}

rainfallSlider.addEventListener('input', function () { rainfallInput.value = this.value; updateRainBadge(this.value); });
rainfallInput.addEventListener('input', function () {
    const val = parseFloat(this.value);
    if (!Number.isNaN(val)) rainfallSlider.value = Math.min(3000, Math.max(0, val));
    updateRainBadge(this.value);
});

document.getElementById('encyclopediaBtn').addEventListener('click', () => {
    document.getElementById('encyclopediaSection').scrollIntoView({ behavior: 'smooth' });
});

document.querySelectorAll('[data-preset]').forEach(btn => {
    btn.addEventListener('click', () => {
        const preset = PRESETS[btn.dataset.preset];
        if (!preset) return;
        document.getElementById('soil_type').value = preset.soil_type;
        document.getElementById('season').value = preset.season;
        rainfallInput.value = preset.rainfall;
        rainfallSlider.value = Math.min(3000, preset.rainfall);
        updateRainBadge(preset.rainfall);
        document.getElementById('water_availability').value = preset.water_availability;
        document.getElementById('temperature').value = preset.temperature;
        document.getElementById('soil_ph').value = preset.soil_ph;
        document.getElementById('cropForm').requestSubmit();
    });
});

document.getElementById('langSelect').addEventListener('change', function (e) {
    lang = e.target.value;
    const t = T[lang] || T.en;
    const labels = UI_LABELS[lang] || UI_LABELS.en;
    staticIds.forEach((id, i) => {
        const el = document.getElementById(id);
        if (el && labels[i]) el.textContent = labels[i];
    });
    document.getElementById('appTitle').textContent = t.title;
    rainfallInput.placeholder = t.rain;
    document.getElementById('submitText').textContent = t.btn;

    const encTitle = document.getElementById('encyclopediaHeading');
    const encSub = document.querySelector('#encyclopediaSection .encyclopedia-header p');
    if (encTitle) encTitle.textContent = t.wikiSectionTitle;
    if (encSub) encSub.textContent = t.wikiSectionSub;

    ['optSoilDefault', 'optSoilAlluvial', 'optSoilBlack', 'optSoilRed', 'optSoilLoamy', 'optSoilClay', 'optSoilSandy'].forEach((id, i) => {
        document.getElementById(id).textContent = t.soil[i];
    });
    ['optSeasonDefault', 'optSeasonKharif', 'optSeasonRabi', 'optSeasonZaid', 'optSeasonAnnual'].forEach((id, i) => {
        document.getElementById(id).textContent = t.season[i];
    });
    ['optWaterDefault', 'optWaterHigh', 'optWaterMedium', 'optWaterLow'].forEach((id, i) => {
        document.getElementById(id).textContent = t.water[i];
    });

    loadEncyclopedia();
    const resDiv = document.getElementById('result');
    if (resDiv && !resDiv.classList.contains('hidden') && resDiv.innerHTML.trim() !== '') {
        document.getElementById('cropForm').requestSubmit();
    }
});

function getTierClass(score) {
    if (score >= 80) return 'tier-optimal';
    if (score >= 55) return 'tier-viable';
    return 'tier-risk';
}

function renderGuidelinesHtml(c, t) {
    const resources = Array.isArray(c.resources) ? c.resources : [];
    const resourcePills = resources.length ? `
        <div class="resource-links">
            ${resources.map(r => `<a class="resource-pill type-${escapeHtml(r.type)}" href="${escapeHtml(r.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(r.label)} ↗</a>`).join('')}
        </div>` : '';
    if (!Array.isArray(c.guidelines) || !c.guidelines.length) return resourcePills;
    return `
        ${resourcePills}
        <details class="guidelines-toggle">
            <summary>${t.guideBtn} <span>▾</span></summary>
            <ol class="guidelines-list">
                ${c.guidelines.map((stepText, idx) => `<li><strong>${t.stages[idx] || ''}:</strong> ${escapeHtml(stepText)}</li>`).join('')}
            </ol>
        </details>`;
}

document.getElementById('cropForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const t = T[lang] || T.en;
    const resDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    document.getElementById('statusText').textContent = t.wait;
    resDiv.classList.remove('hidden');
    resDiv.style.display = 'block';
    resDiv.innerHTML = `<p style="text-align:center; color: var(--muted); font-weight: 600;">${t.wait}</p>`;

    const tempVal = document.getElementById('temperature').value;
    const phVal = document.getElementById('soil_ph').value;
    const payload = {
        soil_type: document.getElementById('soil_type').value,
        season: document.getElementById('season').value,
        rainfall: parseFloat(rainfallInput.value),
        water_availability: document.getElementById('water_availability').value,
        temperature: tempVal !== '' ? parseFloat(tempVal) : null,
        soil_ph: phVal !== '' ? parseFloat(phVal) : null,
        lang: lang
    };

    try {
        const res = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok && data.recommendations) {
            let html = `
                <div class="results-topbar">
                    <div><h3 class="section-title">${t.head}</h3><p class="score-guide">${t.guide}</p></div>
                    <button type="button" class="print-btn" id="printResultsBtn">${t.printBtn}</button>
                </div>`;
            saveHistory(payload, data.recommendations);
            data.recommendations.forEach((c, idx) => {
                const badge = idx === 0 ? t.best : `${t.opt} #${idx + 1}`;
                const cls = idx === 0 ? 'crop-card top-pick' : 'crop-card';
                const name = t.crops[c.name] || c.name;
                const numericScore = typeof c.score === 'number' ? c.score : parseFloat(c.confidence) || 0;
                const tierCls = getTierClass(numericScore);
                html += `
                    <article class="${cls}">
                        <div class="crop-hero-row">
                            <img class="crop-thumb" src="${escapeHtml(c.image_url)}" alt="${escapeHtml(name)}" loading="lazy" onerror="this.src='${FALLBACK_CROP_IMG}'">
                            <div class="result-header">
                                <div>
                                    <span class="badge ${tierCls}">${badge}</span>
                                    <h4>${escapeHtml(name)}</h4>
                                    <p class="sci-name">${escapeHtml(c.scientific_name)}</p>
                                    <p class="tier-label">${escapeHtml(c.suitability_level)}</p>
                                </div>
                                <div class="score-pill"><strong>${escapeHtml(c.confidence)}</strong><span>${t.match}</span></div>
                            </div>
                        </div>
                        <div class="score-bar-track" aria-hidden="true"><div class="score-bar-fill ${tierCls}" style="width: ${Math.min(100, Math.max(5, numericScore))}%"></div></div>
                        <p class="crop-overview">${escapeHtml(c.overview)}</p>
                        <div class="metrics-row">
                            <span class="metric-chip"><strong>${t.durationLbl}:</strong> ${escapeHtml(c.duration)}</span>
                            <span class="metric-chip"><strong>${t.tempLbl}:</strong> ${escapeHtml(c.ideal_temp)}</span>
                            <span class="metric-chip"><strong>${t.phLbl}:</strong> ${escapeHtml(c.ph_range)}</span>
                            <span class="metric-chip"><strong>${t.rainLbl}:</strong> ${escapeHtml(c.rainfall_range)}</span>
                        </div>
                        <div class="result-details">
                            <div class="detail-box"><strong>${t.lbl[0]}:</strong> ${escapeHtml(c.why_it_fits)}</div>
                            <div class="detail-box"><strong>${t.lbl[3]}:</strong> ${escapeHtml(c.fertilizer)}</div>
                            <div class="detail-box"><strong>${t.lbl[4]}:</strong> ${escapeHtml(c.farming_tip)}</div>
                        </div>
                        ${renderGuidelinesHtml(c, t)}
                    </article>`;
            });
            resDiv.innerHTML = html;
            const printBtn = document.getElementById('printResultsBtn');
            if (printBtn) printBtn.addEventListener('click', () => window.print());
            resDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            resDiv.innerHTML = `<div class="error-box">Warning: ${escapeHtml(data.error || 'Unable to generate recommendations.')}</div>`;
        }
    } catch (err) {
        resDiv.innerHTML = '<div class="error-box">Could not connect to the backend. Start it with <code>python backend/app.py</code>.</div>';
    } finally {
        submitBtn.disabled = false;
        document.getElementById('statusText').textContent = UI_LABELS[lang][7];
    }
});

async function loadEncyclopedia() {
    const grid = document.getElementById('encyclopediaGrid');
    const t = T[lang] || T.en;
    try {
        const res = await fetch(`${API_BASE_URL}/crops?lang=${encodeURIComponent(lang)}`);
        const data = await res.json();
        if (!res.ok || !data.crops) return;
        grid.innerHTML = data.crops.map(c => {
            const name = t.crops[c.name] || c.name;
            return `
                <article class="wiki-card">
                    <img class="wiki-card-img" src="${escapeHtml(c.image_url)}" alt="${escapeHtml(name)}" loading="lazy" onerror="this.src='${FALLBACK_CROP_IMG}'">
                    <div class="wiki-card-body">
                        <h3>${escapeHtml(name)}</h3>
                        <p class="sci-name">${escapeHtml(c.scientific_name)}</p>
                        <p class="crop-overview">${escapeHtml(c.overview)}</p>
                        <div class="wiki-specs">
                            <div><strong>${t.rainLbl}:</strong> ${escapeHtml(c.rainfall_range)}</div>
                            <div><strong>${t.tempLbl}:</strong> ${escapeHtml(c.ideal_temp)}</div>
                            <div><strong>${t.phLbl}:</strong> ${escapeHtml(c.ph_range)}</div>
                            <div><strong>${t.durationLbl}:</strong> ${escapeHtml(c.duration)}</div>
                        </div>
                        ${renderGuidelinesHtml(c, t)}
                    </div>
                </article>`;
        }).join('');
    } catch (err) {
        grid.innerHTML = '<p style="color: var(--muted); font-size: 13px;">Start the backend (<code>python backend/app.py</code>) to load the full crop encyclopedia.</p>';
    }
}

document.getElementById('resetBtn').addEventListener('click', function () {
    document.getElementById('cropForm').reset();
    rainfallSlider.value = 850;
    updateRainBadge('');
    const result = document.getElementById('result');
    result.innerHTML = ''; result.classList.add('hidden'); result.style.display = 'none';
    document.getElementById('statusText').textContent = UI_LABELS[lang][7];
});

const HISTORY_KEY = 'agrichoice_recommendation_history';
function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[char]);
}
function getHistory() { try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); } catch (e) { return []; } }
function saveHistory(payload, recommendations) {
    const history = getHistory();
    history.unshift({ payload, recommendations, date: new Date().toISOString() });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 12)));
    updateHistoryCount();
}
function updateHistoryCount() { document.getElementById('historyCount').textContent = getHistory().length; }

function renderHistory() {
    const history = getHistory();
    const list = document.getElementById('historyList');
    const clearBtn = document.getElementById('clearHistoryBtn');
    const t = T[lang] || T.en;
    if (!history.length) { list.innerHTML = `<p class="empty-history">${t.emptyHistory}</p>`; clearBtn.style.display = 'none'; return; }
    clearBtn.style.display = 'block';
    list.innerHTML = history.map((item, index) => {
        const topCrop = item.recommendations[0];
        const cropName = t.crops[topCrop.name] || topCrop.name;
        const date = new Date(item.date);
        const dateText = Number.isNaN(date.getTime()) ? '' : date.toLocaleString();
        return `<button type="button" class="history-item" data-history-index="${index}"><strong>${escapeHtml(cropName)} • ${escapeHtml(topCrop.confidence)}</strong><span>${escapeHtml(item.payload.soil_type)} • ${escapeHtml(item.payload.season)} • ${escapeHtml(item.payload.rainfall)} mm • ${escapeHtml(dateText)}</span></button>`;
    }).join('');
    list.querySelectorAll('[data-history-index]').forEach(button => {
        button.addEventListener('click', () => {
            const payload = history[Number(button.dataset.historyIndex)].payload;
            document.getElementById('soil_type').value = payload.soil_type;
            document.getElementById('season').value = payload.season;
            rainfallInput.value = payload.rainfall;
            rainfallSlider.value = Math.min(3000, Math.max(0, payload.rainfall));
            updateRainBadge(payload.rainfall);
            document.getElementById('water_availability').value = payload.water_availability;
            document.getElementById('temperature').value = payload.temperature ?? '';
            document.getElementById('soil_ph').value = payload.soil_ph ?? '';
            document.getElementById('historyOverlay').hidden = true;
            document.getElementById('cropForm').requestSubmit();
        });
    });
}

document.getElementById('historyBtn').addEventListener('click', function () { renderHistory(); document.getElementById('historyOverlay').hidden = false; });
document.getElementById('closeHistoryBtn').addEventListener('click', function () { document.getElementById('historyOverlay').hidden = true; });
document.getElementById('historyOverlay').addEventListener('click', function (e) { if (e.target === this) this.hidden = true; });
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') document.getElementById('historyOverlay').hidden = true; });
document.getElementById('clearHistoryBtn').addEventListener('click', function () { localStorage.removeItem(HISTORY_KEY); updateHistoryCount(); renderHistory(); });

updateHistoryCount();
loadEncyclopedia();