import requests

API_KEY = "e65a07b36673c2fe08d37e2839592bbf"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city_name):
    complete_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code == 200:
            main = data.get("main")
            weather = data.get("weather")[0] if data.get("weather") else None

            if main and weather:
                temp = main.get("temp")
                humidity = main.get("humidity")
                description = weather.get("description")
                return f"Temperature: {temp}°C\nHumidity: {humidity}%\nCondition: {description.capitalize()}"
            else:
                return "Unexpected response structure. Please try again."
        elif data.get("message"):
            return f"API error: {data['message'].capitalize()}"
        else:
            return f"City '{city_name}' not found or request failed."

    except Exception as e:
        return f"Error fetching weather: {str(e)}"
