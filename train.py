import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# ১. ডেটাসেট লোড করা (Kaggle থেকে ডাউনলোড করা weather.csv)
try:
    df = pd.read_csv('weather.csv')
    print("Successfully loaded weather.csv")
except FileNotFoundError:
    # যদি ফাইল না থাকে, তবে টেস্টিংয়ের জন্য ডামি ডেটা তৈরি হবে
    print("weather.csv ফাইলটি পাওয়া যায়নি। টেস্টিংয়ের জন্য ডামি ডেটা তৈরি হচ্ছে...")
    data = {
        'Humidity': np.random.uniform(0.3, 0.9, 1000),
        'Wind Speed (km/h)': np.random.uniform(5, 25, 1000),
        'Pressure (millibars)': np.random.uniform(1000, 1020, 1000),
        'Temperature (C)': np.random.uniform(15, 40, 1000)
    }
    df = pd.DataFrame(data)

# ২. ফিচার (X) এবং টার্গেট (y) আলাদা করা
X = df[['Humidity', 'Wind Speed (km/h)', 'Pressure (millibars)']]
y = df['Temperature (C)']

# ৩. ট্রেইন এবং টেস্ট স্প্লিট (Train-Test Split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ৪. মডেল ট্রেইনিং (Random Forest Regressor)
print("আবহাওয়ার পূর্বাভাস মডেলটির ট্রেইনিং শুরু হচ্ছে...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ৫. মডেল মূল্যায়ন (Evaluation)
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"মডেল ট্রেইনিং সফল হয়েছে! Root Mean Squared Error (RMSE): {rmse:.2f}°C")

# ৬. ভবিষ্যতের ব্যবহারের জন্য মডেলটি সেভ করা
joblib.dump(model, 'weather_model.pkl')
print("মডেলটি 'weather_model.pkl' নামে সফলভাবে সেভ হয়েছে।")