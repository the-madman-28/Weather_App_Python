import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        place = request.form.get("place", "").strip()
        api_key = os.getenv("WEATHER_API_KEY")

        if not place:
            error = "Please enter a place name."

        elif not api_key:
            error = "Weather API key is not configured."

        else:
            try:
                url = "https://api.weatherapi.com/v1/current.json"

                params = {
                    "key": api_key,
                    "q": place
                }

                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                data = response.json()

                if response.ok:
                    weather = {
                        "place": data["location"]["name"],
                        "country": data["location"]["country"],
                        "temp": data["current"]["temp_c"],
                        "condition": data["current"]["condition"]["text"]
                    }
                else:
                    error = data.get(
                        "error", {}
                    ).get(
                        "message",
                        "Unable to fetch weather."
                    )

            except requests.RequestException:
                error = "Unable to connect to weather service."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )
