import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import os

# Training data aligned with your 4 required parameters
data = [
    # Soil Type, Season, Rainfall (mm), Water Availability, Crop
    ['Alluvial', 'Kharif', 1200, 'High', 'Rice'],
    ['Clay', 'Kharif', 1300, 'High', 'Rice'],
    ['Alluvial', 'Rabi', 400, 'Medium', 'Wheat'],
    ['Loamy', 'Rabi', 450, 'Medium', 'Wheat'],
    ['Black', 'Kharif', 700, 'Medium', 'Cotton'],
    ['Black', 'Kharif', 650, 'Low', 'Cotton'],
    ['Loamy', 'Kharif', 800, 'Medium', 'Maize'],
    ['Red', 'Kharif', 750, 'Medium', 'Maize'],
    ['Alluvial', 'Annual', 1500, 'High', 'Sugarcane'],
    ['Black', 'Annual', 1400, 'High', 'Sugarcane'],
    ['Sandy', 'Kharif', 500, 'Low', 'Groundnut'],
    ['Red', 'Kharif', 550, 'Low', 'Groundnut'],
    ['Sandy', 'Zaid', 250, 'Low', 'Watermelon'],
    ['Loamy', 'Zaid', 300, 'Medium', 'Watermelon'],
    ['Red', 'Rabi', 350, 'Low', 'Millets (Ragi / Jowar)'],
    ['Sandy', 'Kharif', 300, 'Low', 'Millets (Ragi / Jowar)'],
    ['Loamy', 'Rabi', 500, 'Medium', 'Potato'],
    ['Alluvial', 'Rabi', 550, 'Medium', 'Potato'],
    ['Black', 'Rabi', 400, 'Low', 'Chickpea (Chana)'],
    ['Loamy', 'Rabi', 380, 'Low', 'Chickpea (Chana)'],
]

df = pd.DataFrame(data, columns=['soil_type', 'season', 'rainfall', 'water_availability', 'crop'])

X = df[['soil_type', 'season', 'rainfall', 'water_availability']]
y = df['crop']

# Encode categorical columns (soil_type, season, water_availability)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['soil_type', 'season', 'water_availability'])
    ],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

model.fit(X, y)

# Save model using an absolute path relative to this script
base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, 'model')
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'crop_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"Model trained and saved successfully at: {model_path}")
