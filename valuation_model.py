# valuation_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

class ValuationModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=200, random_state=42)
        self.scaler = StandardScaler()

    def train(self, data_path: str):
        df = pd.read_csv(data_path)
        X = df.drop(['valuation'], axis=1)
        y = df['valuation']

        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        print(f"Model trained. R² Score: {score}")
        joblib.dump(self.model, "valuation_model.pkl")
        joblib.dump(self.scaler, "scaler.pkl")

    def predict(self, features: np.array):
        model = joblib.load("valuation_model.pkl")
        scaler = joblib.load("scaler.pkl")
        features_scaled = scaler.transform([features])
        return model.predict(features_scaled)[0]

# Example Usage:
# model = ValuationModel()
# model.train("patent_dataset.csv")
# print(model.predict([feature_vector]))