import requests
import base64
from datetime import datetime
import os

# ---- Personal Info for Nutritionix ----
GENDER = 'Male'
WEIGHT_KG = '90'
HEIGHT_CM = '182'
AGE = '20'

username = os.getenv("SHEETY_USER")
password = os.getenv("SHEETY_PASS")

# Encode in base64
auth_string = f"{username}:{password}"
base64_bytes = base64.b64encode(auth_string.encode("utf-8"))
auth_header = f"Basic {base64_bytes.decode('utf-8')}"

# ---- Nutritionix API Credentials ----
APP_ID = os.getenv("YOUR_APP_ID")
API_KEY = os.getenv("YOUR_API_KEY")

# ---- Nutritionix API Endpoint ----
exercise_endpoint = os.getenv("YOUR_Nutritionix_API_Endpoints")

# ---- Sheety API Endpoint ----
sheety_endpoint = os.getenv("YOUR_Sheety_API_Endpoint")

# ---- Sheety Authorization Header ----
sheety_headers = {
    "Authorization": auth_header
}
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# ---- Send to Nutritionix API ----
response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# ---- Get Current Date and Time ----
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

# ---- Send Each Exercise to Google Sheet via Sheety ----
for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(sheety_endpoint, json=sheet_inputs, headers=sheety_headers)
    print(sheet_response.text)
