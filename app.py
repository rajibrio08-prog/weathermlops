from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import uvicorn
import numpy as np


# FastAPI অ্যাপ ইনিশিয়ালাইজ করা
app = FastAPI(title="Weather Forecasting ML API", version="1.0")

# ট্রেইনড মডেলটি লোড করা
try:
    model = joblib.load('weather_model.pkl')
    print("মডেল সফলভাবে লোড হয়েছে।")
except FileNotFoundError:
    print("ত্রুটি: 'weather_model.pkl' ফাইলটি পাওয়া যায়নি। প্রথমে train.py রান করুন।")
    model = None

# ইউজারের কাছ থেকে আসা ডেটার ফরম্যাট নির্ধারণ (Pydantic ব্যবহার করে)
# এখানে alias ব্যবহার করে স্পেস ও ব্র্যাকেটের ঝামেলার সমাধান করা হয়েছে
from pydantic import BaseModel, Field, ConfigDict

class WeatherInput(BaseModel):
    Humidity: float
    Wind_Speed: float = Field(..., alias="Wind Speed (km/h)")
    Pressure: float = Field(..., alias="Pressure (millibars)")

    class Config:
        populate_by_name = True  # এটি দিলে আপনি স্পেসসহ বা স্পেস ছাড়া দুভাবেই ডেটা পাঠাতে পারবেন


@app.get("/")
def home():
    return {"message": "স্বাগতম! এটি অবহাওয়া পূর্বাভাসের ML API। প্রেডিকশনের জন্য /predict এন্ডপয়েন্ট ব্যবহার করুন।"}


@app.post("/predict")
def predict_temperature(data: WeatherInput):
    if model is None:
        return {"error": "মডেলটি লোড বা ট্রেইন করা নেই।"}
    
    # ইনপুট ডেটাকে মডেলের উপযোগী অ্যারে-তে রূপান্তর করা (স্পেস ছাড়া পাইথন ভ্যারিয়েবল নাম)
    input_data = np.array([[data.Humidity, data.Wind_Speed, data.Pressure]])
    
    # মডেলের মাধ্যমে প্রেডিকশন বা পূর্বাভাস দেওয়া
    predicted_temp = model.predict(input_data)[0]
    
    return {
        "input_received": {
            "Humidity": data.Humidity,
            "Wind Speed (km/h)": data.Wind_Speed,
            "Pressure (millibars)": data.Pressure
        },
        "predicted_temperature_celsius": round(float(predicted_temp), 2)
    }

if __name__ == "__main__":
    # স্থানীয় সার্ভারে অ্যাপ্লিকেশনটি রান করা (Port: 8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)