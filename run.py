import os
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/weather", methods=["POST"])
def get_weather():

    place = request.form.get("place", "").strip()

    if not place:
        return jsonify({
            "success": False,
            "error": "Please enter a place name."
        })

    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return jsonify({
            "success": False,
            "error": "Weather API key is not configured."
        })

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

        if not response.ok:
            error_message = data.get(
                "error", {}
            ).get(
                "message",
                "Unable to fetch weather."
            )

            return jsonify({
                "success": False,
                "error": error_message
            })

        weather = {
            "place": data["location"]["name"],
            "country": data["location"]["country"],
            "temp": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"]
        }

        return jsonify({
            "success": True,
            "weather": weather
        })

    except requests.RequestException:
        return jsonify({
            "success": False,
            "error": "Unable to connect to weather service."
        })

    except (KeyError, ValueError):
        return jsonify({
            "success": False,
            "error": "Invalid response received from weather service."
        })


if __name__ == "__main__":
    app.run(debug=False)