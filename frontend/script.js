const API_BASE_URL = (() => {
    const { hostname, port, protocol, origin } = window.location;
    if (protocol === 'file:' || (['', 'localhost', '127.0.0.1'].includes(hostname) && port !== '5000')) {
        return 'http://127.0.0.1:5000';
    }
    return origin;
})();

const T = {
    en: {
        title: "Crop Recommendation System",
        soil: ["Select Soil Type", "Alluvial Soil", "Black Soil", "Red / Laterite Soil", "Loamy Soil", "Clay Soil", "Sandy Soil"],
        season: ["Select Season", "Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)", "Annual (All Year)"],
        rain: "Rainfall (in mm, e.g., 120)",
        water: ["Water Availability", "High (Abundant Irrigation / Rain)", "Medium (Moderate Irrigation)", "Low (Rainfed / Dry)"],
        btn: "Recommend Crop",
        wait: "Calculating accuracy scores...",
        head: "Top 3 Accurate Crop Predictions",
        guide: "<strong>Suitability Guide:</strong> 80–100% = Optimal | 55–79% = Viable | Below 55% = High Risk",
        best: "Best Match (#1)",
        opt: "Option",
        match: "Accuracy Match",
        lbl: ["Condition Analysis", "Growth Duration", "Ideal Temperature", "Fertilizer Advice", "Farming Tip"],
        crops: {}
    },
    kn: {
        title: "ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ",
        soil: ["ಮಣ್ಣಿನ ಪ್ರಕಾರ ಆಯ್ಕೆಮಾಡಿ", "ಮೆಕ್ಕಲು ಮಣ್ಣು", "ಕಪ್ಪು ಮಣ್ಣು", "ಕೆಂಪು ಮಣ್ಣು", "ಗೋಡು ಮಣ್ಣು", "ಜೇಡಿಮಣ್ಣು", "ಮರಳು ಮಣ್ಣು"],
        season: ["ಋತುವನ್ನು ಆಯ್ಕೆಮಾಡಿ", "ಮುಂಗಾರು (Kharif)", "ಹಿಂಗಾರು (Rabi)", "ಬೇಸಿಗೆ (Zaid)", "ವಾರ್ಷಿಕ (Annual)"],
        rain: "ಮಳೆಯ ಪ್ರಮಾಣ (ಮಿಮೀ ನಲ್ಲಿ, ಉದಾ: 120)",
        water: ["ನೀರಿನ ಲಭ್ಯತೆ", "ಹೆಚ್ಚು (ಸಾಕಷ್ಟು ನೀರಾವರಿ)", "ಮಧ್ಯಮ", "ಕಡಿಮೆ (ಮಳೆಯಾಶ್ರಿತ)"],
        btn: "ಬೆಳೆ ಶಿಫಾರಸು ಮಾಡಿ",
        wait: "ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        head: "ಅತ್ಯುತ್ತಮ 3 ಬೆಳೆ ಶಿಫಾರಸುಗಳು",
        guide: "<strong>ಮಾರ್ಗದರ್ಶಿ:</strong> 80–100% = ಅತ್ಯುತ್ತಮ | 55–79% = ಸಾಧಾರಣ | 55% ಕಡಿಮೆ = ಅಪಾಯ",
        best: "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ (#1)",
        opt: "ಆಯ್ಕೆ",
        match: "ಹೊಂದಾಣಿಕೆ",
        lbl: ["ವಿಶ್ಲೇಷಣೆ", "ಬೆಳೆ ಅವಧಿ", "ಸೂಕ್ತ ತಾಪಮಾನ", "ಗೊಬ್ಬರ ಸಲಹೆ", "ಕೃಷಿ ಸಲಹೆ"],
        crops: { "Rice (Paddy)": "ಭತ್ತ (Rice)", "Wheat": "ಗೋಧಿ (Wheat)", "Maize (Corn)": "ಮೆಕ್ಕೆಜೋಳ (Maize)", "Cotton": "ಹತ್ತಿ (Cotton)", "Sugarcane": "ಕಬ್ಬು (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "ಸಿರಿಧಾನ್ಯಗಳು (Millets)" }
    },
    hi: {
        title: "फसल अनुशंसा प्रणाली",
        soil: ["मिट्टी का प्रकार चुनें", "जलोढ़ मिट्टी", "काली मिट्टी", "लाल मिट्टी", "दोमट मिट्टी", "चिकनी मिट्टी", "बलुई मिट्टी"],
        season: ["मौसम चुनें", "खरीफ (मानसून)", "रबी (सर्दी)", "जायद (गर्मी)", "वार्षिक (पूरे साल)"],
        rain: "वर्षा (मिमी में, जैसे 120)",
        water: ["पानी की उपलब्धता", "अधिक (पर्याप्त सिंचाई)", "मध्यम", "कम (वर्षा आधारित)"],
        btn: "फसल का सुझाव दें",
        wait: "जांच की जा रही है...",
        head: "शीर्ष 3 उपयुक्त फसलें",
        guide: "<strong>गाइड:</strong> 80–100% = सर्वोत्तम | 55–79% = मध्यम | 55% से कम = जोखिम",
        best: "सर्वोत्तम विकल्प (#1)",
        opt: "विकल्प",
        match: "सटीकता मिलान",
        lbl: ["स्थिति विश्लेषण", "फसल अवधि", "आदर्श तापमान", "उर्वरक सलाह", "खेती की टिप"],
        crops: { "Rice (Paddy)": "धान / चावल (Rice)", "Wheat": "गेहूं (Wheat)", "Maize (Corn)": "मक्का (Maize)", "Cotton": "कपास (Cotton)", "Sugarcane": "गन्ना (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "बाजरा / रागी (Millets)" }
    },
    ta: {
        title: "பயிர் பரிந்துரை அமைப்பு",
        soil: ["மண் வகையைத் தேர்ந்தெடுக்கவும்", "வண்டல் மண்", "கரிசல் மண்", "செம்மண்", "களிமண் கலந்த மண்", "களிமண்", "மணல் மண்"],
        season: ["பருவத்தைத் தேர்ந்தெடுக்கவும்", "கரீஃப் (மழைக்காலம்)", "ரபி (குளிர்காலம்)", "சையத் (கோடைகாலம்)", "ஆண்டு முழுவதும்"],
        rain: "மழையளவு (மிமீ, எ.கா. 120)",
        water: ["நீர் இருப்பு", "அதிகம்", "நடுத்தரம்", "குறைவு"],
        btn: "பயிரைப் பரிந்துரைக்கவும்",
        wait: "கணக்கிடப்படுகிறது...",
        head: "சிறந்த 3 பயிர் பரிந்துரைகள்",
        guide: "<strong>வழிகாட்டி:</strong> 80–100% = சிறந்தது | 55–79% = நடுத்தரம் | 55% கீழ் = ஆபத்து",
        best: "சிறந்த தேர்வு (#1)",
        opt: "விருப்பம்",
        match: "பொருத்தம்",
        lbl: ["நிலை ஆய்வு", "வளர்ச்சி காலம்", "சிறந்த வெப்பநிலை", "உர ஆலோசனை", "விவசாய குறிப்பு"],
        crops: { "Rice (Paddy)": "நெல் (Rice)", "Wheat": "கோதுமை (Wheat)", "Maize (Corn)": "மக்காச்சோளம் (Maize)", "Cotton": "பருத்தி (Cotton)", "Sugarcane": "கரும்பு (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "சிறுதானியங்கள் (Millets)" }
    },
    te: {
        title: "పంట సిఫార్సు వ్యవస్థ",
        soil: ["నేల రకాన్ని ఎంచుకోండి", "ఒండ్రు నేల", "నల్ల రేగడి నేల", "ఎర్ర నేల", "లోమీ నేల", "బంకమట్టి నేల", "ఇసుక నేల"],
        season: ["సీజన్ ఎంచుకోండి", "ఖరీఫ్ (వర్షాకాలం)", "రబీ (చలికాలం)", "జైద్ (వేసవి)", "వార్షిక (సంవత్సరం)"],
        rain: "వర్షపాతం (మిమీ లో, ఉదా: 120)",
        water: ["నీటి లభ్యత", "ఎక్కువ", "మధ్యస్థం", "తక్కువ"],
        btn: "పంటను సిఫార్సు చేయండి",
        wait: "లెక్కిస్తోంది...",
        head: "అత్యుత్తమ 3 పంట సిఫార్సులు",
        guide: "<strong>గైడ్:</strong> 80–100% = ఉత్తమం | 55–79% = మధ్యస్థం | 55% తక్కువ = ప్రమాదం",
        best: "ఉత్తమ ఎంపిక (#1)",
        opt: "ఎంపిక",
        match: "సరిపోలిక",
        lbl: ["విశ్లేషణ", "పంట కాలం", "ఉష్ణోగ్రత", "ఎరువుల సలహా", "వ్యవసాయ చిట్కా"],
        crops: { "Rice (Paddy)": "వరి (Rice)", "Wheat": "గోధుమ (Wheat)", "Maize (Corn)": "మొక్కజొన్న (Maize)", "Cotton": "పత్తి (Cotton)", "Sugarcane": "చెరకు (Sugarcane)", "Millets (Ragi / Bajra / Jowar)": "చిరుధాన్యాలు (Millets)" }
    }
};

const UI_LABELS = {
    en: ["Language", "SMART FARMING ASSISTANT", "Share your farm conditions and get the crops most likely to thrive.", "Top 3 matches", "Local recommendations", "Farming guidance", "Tell us about your farm", "Ready", "Soil type", "Growing season", "Annual rainfall", "Water availability", "Reset", "Recommend Crop", "AgriChoice • Smart crop planning"],
    kn: ["ಭಾಷೆ", "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ", "ನಿಮ್ಮ ಹೊಲದ ಪರಿಸ್ಥಿತಿ ನೀಡಿ ಮತ್ತು ಸೂಕ್ತ ಬೆಳೆಗಳನ್ನು ತಿಳಿದುಕೊಳ್ಳಿ.", "ಮೇಲಿನ 3 ಬೆಳೆಗಳು", "ಸ್ಥಳೀಯ ಶಿಫಾರಸು", "ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ", "ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳು", "ಸಿದ್ಧ", "ಮಣ್ಣಿನ ಪ್ರಕಾರ", "ಬೆಳೆ ಋತು", "ವಾರ್ಷಿಕ ಮಳೆ", "ನೀರಿನ ಲಭ್ಯತೆ", "ಮರುಹೊಂದಿಸಿ", "ಬೆಳೆ ಶಿಫಾರಸು ಮಾಡಿ", "AgriChoice • ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಯೋಜನೆ"],
    hi: ["भाषा", "स्मार्ट खेती सहायक", "अपनी खेत की स्थिति दें और सबसे उपयुक्त फसलें जानें।", "शीर्ष 3 विकल्प", "स्थानीय सुझाव", "खेती मार्गदर्शन", "अपने खेत के बारे में बताएं", "तैयार", "मिट्टी का प्रकार", "बुआई का मौसम", "वार्षिक वर्षा", "पानी की उपलब्धता", "रीसेट", "फसल का सुझाव दें", "AgriChoice • स्मार्ट फसल योजना"],
    ta: ["மொழி", "ஸ்மார்ட் விவசாய உதவியாளர்", "பண்ணையின் நிலையைச் சொல்லி சிறந்த பயிர்களைக் கண்டறியுங்கள்.", "சிறந்த 3 தேர்வுகள்", "உள்ளூர் பரிந்துரை", "விவசாய வழிகாட்டுதல்", "பண்ணை விவரங்களைச் சொல்லுங்கள்", "தயார்", "மண் வகை", "பயிர் பருவம்", "வருடாந்திர மழை", "நீர் இருப்பு", "மீட்டமை", "பயிரைப் பரிந்துரைக்கவும்", "AgriChoice • திறன்வாய்ந்த பயிர் திட்டம்"],
    te: ["భాష", "స్మార్ట్ వ్యవసాయ సహాయకుడు", "పొల పరిస్థితులు తెలుపుతూ అత్యనుకూల పంటలను తెలుసుకోండి.", "అగ్ర 3 ఎంపికలు", "స్థానిక సిఫార్సు", "వ్యవసాయ మార్గదర్శకం", "మీ పొలం వివరాలు చెప్పండి", "సిద్ధం", "నేల రకం", "పంట సీజన్", "వార్షిక వర్షపాతం", "నీటి లభ్యత", "రీసెట్", "పంటను సిఫార్సు చేయండి", "AgriChoice • స్మార్ట్ పంట ప్రణాళిక"]
};

const staticIds = [
    'languageLabel', 'eyebrow', 'introText', 'featureOne', 'featureTwo', 'featureThree',
    'formTitle', 'statusText', 'soilLabel', 'seasonLabel', 'rainLabel', 'waterLabel',
    'resetBtn', 'submitText', 'footerText'
];

let lang = 'en';

document.getElementById('langSelect').addEventListener('change', function (e) {
    lang = e.target.value;
    const t = T[lang] || T.en;
    const labels = UI_LABELS[lang] || UI_LABELS.en;
    staticIds.forEach((id, i) => {
        document.getElementById(id).textContent = labels[i];
    });
    document.getElementById('appTitle').textContent = t.title;
    document.getElementById('rainfall').placeholder = t.rain;
    document.getElementById('submitText').textContent = t.btn;

    ['optSoilDefault', 'optSoilAlluvial', 'optSoilBlack', 'optSoilRed', 'optSoilLoamy', 'optSoilClay', 'optSoilSandy'].forEach((id, i) => {
        document.getElementById(id).textContent = t.soil[i];
    });
    ['optSeasonDefault', 'optSeasonKharif', 'optSeasonRabi', 'optSeasonZaid', 'optSeasonAnnual'].forEach((id, i) => {
        document.getElementById(id).textContent = t.season[i];
    });
    ['optWaterDefault', 'optWaterHigh', 'optWaterMedium', 'optWaterLow'].forEach((id, i) => {
        document.getElementById(id).textContent = t.water[i];
    });
});

document.getElementById('cropForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const t = T[lang] || T.en;
    const resDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    document.getElementById('statusText').textContent = t.wait;
    resDiv.classList.remove('hidden');
    resDiv.style.display = 'block';
    resDiv.innerHTML = `<p style="text-align:center;">${t.wait}</p>`;

    const payload = {
        soil_type: document.getElementById('soil_type').value,
        season: document.getElementById('season').value,
        rainfall: parseFloat(document.getElementById('rainfall').value),
        water_availability: document.getElementById('water_availability').value,
        lang: lang
    };

    try {
        const res = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok && data.recommendations) {
            let html = `<h3 class="section-title">${t.head}</h3><p class="score-guide">${t.guide}</p>`;
            saveHistory(payload, data.recommendations);
            data.recommendations.forEach((c, idx) => {
                const badge = idx === 0 ? t.best : `${t.opt} #${idx + 1}`;
                const cls = idx === 0 ? 'crop-card top-pick' : 'crop-card';
                const name = t.crops[c.name] || c.name;
                html += `
                    <div class="${cls}">
                        <div class="result-header">
                            <span class="badge">${badge} • ${t.match}: ${c.confidence}</span>
                            <h4>${name}</h4>
                            <p class="tier-label">${c.suitability_level}</p>
                        </div>
                        <div class="result-details">
                            <p><strong>${t.lbl[0]}:</strong> ${c.why_it_fits}</p>
                            <p><strong>${t.lbl[1]}:</strong> ${c.duration}</p>
                            <p><strong>${t.lbl[2]}:</strong> ${c.ideal_temp}</p>
                            <p><strong>${t.lbl[3]}:</strong> ${c.fertilizer}</p>
                            <p><strong>${t.lbl[4]}:</strong> ${c.farming_tip}</p>
                        </div>
                    </div>`;
            });
            resDiv.innerHTML = html;
            resDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            resDiv.innerHTML = `<p style="color:#c62828; text-align:center; font-weight:bold;">Warning: ${data.error}</p>`;
        }
    } catch (err) {
        console.error('Crop recommendation request failed:', err);
        resDiv.innerHTML = '<p style="color:#c62828; text-align:center;">Could not connect to the backend. Start it from the project folder with <code>.venv\\Scripts\\python.exe backend\\app.py</code>.</p>';
    } finally {
        submitBtn.disabled = false;
        document.getElementById('statusText').textContent = UI_LABELS[lang][7];
    }
});

document.getElementById('resetBtn').addEventListener('click', function () {
    document.getElementById('cropForm').reset();
    const result = document.getElementById('result');
    result.innerHTML = '';
    result.classList.add('hidden');
    result.style.display = 'none';
    document.getElementById('statusText').textContent = UI_LABELS[lang][7];
});

const HISTORY_KEY = 'agrichoice_recommendation_history';

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    })[char]);
}

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    } catch (error) {
        return [];
    }
}

function saveHistory(payload, recommendations) {
    const history = getHistory();
    history.unshift({
        payload,
        recommendations,
        date: new Date().toISOString()
    });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 12)));
    updateHistoryCount();
}

function updateHistoryCount() {
    document.getElementById('historyCount').textContent = getHistory().length;
}

function renderHistory() {
    const history = getHistory();
    const list = document.getElementById('historyList');

    if (!history.length) {
        list.innerHTML = '<p class="empty-history">No saved recommendations yet.</p>';
        return;
    }

    list.innerHTML = history.map((item, index) => {
        const topCrop = item.recommendations[0];
        const date = new Date(item.date);
        const dateText = Number.isNaN(date.getTime()) ? '' : date.toLocaleString();
        return `
            <button type="button" class="history-item" data-history-index="${index}">
                <strong>${escapeHtml(topCrop.name)} • ${escapeHtml(topCrop.confidence)}</strong>
                <span>${escapeHtml(item.payload.soil_type)} soil • ${escapeHtml(item.payload.season)} • ${escapeHtml(item.payload.rainfall)} mm • ${escapeHtml(dateText)}</span>
            </button>`;
    }).join('');

    list.querySelectorAll('[data-history-index]').forEach(button => {
        button.addEventListener('click', () => {
            const item = history[Number(button.dataset.historyIndex)];
            const payload = item.payload;
            document.getElementById('soil_type').value = payload.soil_type;
            document.getElementById('season').value = payload.season;
            document.getElementById('rainfall').value = payload.rainfall;
            document.getElementById('water_availability').value = payload.water_availability;
            document.getElementById('historyOverlay').hidden = true;
            document.getElementById('cropForm').requestSubmit();
        });
    });
}

document.getElementById('historyBtn').addEventListener('click', function () {
    renderHistory();
    document.getElementById('historyOverlay').hidden = false;
});

document.getElementById('closeHistoryBtn').addEventListener('click', function () {
    document.getElementById('historyOverlay').hidden = true;
});

document.getElementById('historyOverlay').addEventListener('click', function (event) {
    if (event.target === this) {
        this.hidden = true;
    }
});

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        document.getElementById('historyOverlay').hidden = true;
    }
});

document.getElementById('clearHistoryBtn').addEventListener('click', function () {
    localStorage.removeItem(HISTORY_KEY);
    updateHistoryCount();
    renderHistory();
});

updateHistoryCount();
