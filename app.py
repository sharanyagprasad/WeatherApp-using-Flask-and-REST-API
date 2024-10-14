from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_current_weather(city="Kansas City"):
    api_key = os.getenv("API_KEY")
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=imperial'
    
    response = requests.get(request_url)
    return response.json()



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check if city is None or empty
    if not city or not city.strip():
        return render_template('error.html')

    # Fetch weather data for the provided city
    weather_data = get_current_weather(city)

    # Check if the API response code indicates success
    if weather_data['cod'] != 200:
        return render_template('error.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


if __name__ == "__main__":
    app.run()
