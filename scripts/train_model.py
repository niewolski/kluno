import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib
import os

# 1. Wczytanie danych
data = pd.read_csv('prepared_data/dane_treningowe.csv')

# 2. Zamiana kolumny "Skille" na listę (MultiLabelBinarizer)
data['Skille_lista'] = data['Skille'].fillna('').apply(lambda x: x.split(', ') if x else [])
mlb = MultiLabelBinarizer()
X_skille_df = pd.DataFrame(mlb.fit_transform(data['Skille_lista']), columns=mlb.classes_)

# 3. Przygotowanie zmiennych X (cechy) i y (target)
X = pd.concat([
    data[['Roczna_liczba_godzin', 'Przypisane_sprawy']].reset_index(drop=True),
    X_skille_df.reset_index(drop=True)
], axis=1)

y = data['NPS']

# 4. Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Trenowanie modelu XGBoost
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# 6. Ewaluacja
y_pred = model.predict(X_test)
print("📊 R²:", round(r2_score(y_test, y_pred), 4))
print("📉 MAE:", round(mean_absolute_error(y_test, y_pred), 2))

# 7. Zapis modelu
if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/model_nps.pkl')
print("✅ Model zapisany w: models/model_nps.pkl")

# 8. Zapis encoderów do przyszłej predykcji
joblib.dump(mlb, 'models/skille_encoder.pkl')
print("✅ Zapisano encoder skillów: models/skille_encoder.pkl")
