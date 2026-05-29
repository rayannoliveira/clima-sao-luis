import requests


def extract_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-2.5297"
        "&longitude=-44.3028"
        "&hourly=temperature_2m,weather_code"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()