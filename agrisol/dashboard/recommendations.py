import os

import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "recommender_model.joblib")
model = joblib.load(MODEL_PATH)

def get_ai_recommendation(humidite, temperature, ph, lumiere, co2, niveau_eau):
    X = np.array([[humidite, temperature, ph, lumiere, co2, niveau_eau]])
    prediction = model.predict(X)
    return prediction[0]