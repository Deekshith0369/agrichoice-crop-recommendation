# 🌱 AgriChoice — Crop Recommendation System

A machine learning web application that recommends the most suitable crops based on **Soil Type, Season, Rainfall, and Water Availability**.

## Features
- **4-Parameter ML Prediction:** Uses a Random Forest classifier trained on Soil Type, Season, Rainfall (mm), and Water Availability.
- **Top 3 Crop Recommendations:** Displays match percentages, crop duration, ideal temperature, and NPK fertilizer guidance.
- **Multilingual Support:** Supports English and Kannada interfaces.
- **Prediction History:** Tracks recent field checks in the browser.

## How to Run Locally
1. **Start the Backend:**
   ```bash
   cd backend
   pip install flask flask-cors scikit-learn pandas numpy
   python app.py
   ```
2. **Start the Frontend:**
   ```bash
   cd frontend
   python -m http.server 5500
   ```
3. Open `http://localhost:5500` in your browser.
