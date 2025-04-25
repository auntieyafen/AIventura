#weather agent

import os, requests, datetime as dt, json, openai
from typing import Dict, List
from dotenv import load_dotenv

# Load .env file
load_dotenv()
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
if not OPENWEATHER_KEY:
    raise RuntimeError("OPENWEATHER_KEY not set")

def get_city_weather(city: str, date: dt.date) -> dict:
    """Returns weather summary for the specified date (±5 days)"""
    url = ("https://api.openweathermap.org/data/2.5/forecast"
           f"?q={city}&units=metric&appid={OPENWEATHER_KEY}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        # Check for API errors
        if "cod" in data and data["cod"] != "200":
            raise RuntimeError(f"OpenWeatherMap API error: {data.get('message', 'Unknown error')}")
            
        # Check data format
        if "list" not in data:
            raise RuntimeError("API returned invalid data format")
            
        # Get the forecast closest to noon on the specified date
        target_ts = int(dt.datetime.combine(date, dt.time(12, 0)).timestamp())
        closest = min(data["list"], key=lambda x: abs(x["dt"] - target_ts))
        
        return {
            "temp": closest["main"]["temp"],
            "weather": closest["weather"][0]["main"],
            "description": closest["weather"][0]["description"],
            "humidity": closest["main"]["humidity"],
            "wind_speed": closest["wind"]["speed"],
            "clouds": closest["clouds"]["all"]
        }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Data parsing error: {str(e)}")

def get_weather_advice(weather_data: Dict, activities: List[str] = None) -> Dict:
    """Generate weather-related advice using LLM"""
    prompt = f"""Please provide travel advice based on the following weather data:
    Weather data: {json.dumps(weather_data, ensure_ascii=False, indent=2)}
    Planned activities: {json.dumps(activities, ensure_ascii=False) if activities else "Not specified"}
    
    Please consider:
    1. Whether temperature is suitable for outdoor activities
    2. Whether rain gear is needed
    3. Whether wind will affect activities
    4. Suggested clothing
    5. Suggested activity times
    
    Return format:
    {{
        "suitability": "Suitable/Not very suitable/Not suitable",
        "clothing_advice": "Clothing advice",
        "activity_advice": "Activity advice",
        "preparation": ["Preparation item 1", "Preparation item 2"],
        "best_time": "Suggested activity time",
        "alternative_activities": ["Alternative activity 1", "Alternative activity 2"]
    }}"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error generating weather advice: {str(e)}")
        return {
            "suitability": "Unknown",
            "clothing_advice": "Please prepare appropriate clothing based on weather forecast",
            "activity_advice": "Please adjust activity plans based on weather conditions",
            "preparation": ["Check weather forecast", "Prepare rain gear"],
            "best_time": "Decide based on weather conditions",
            "alternative_activities": ["Indoor activities", "Shopping"]
        }

def get_weather_with_advice(city: str, date: dt.date, activities: List[str] = None) -> Dict:
    """获取天气数据和建议"""
    weather_data = get_city_weather(city, date)
    advice = get_weather_advice(weather_data, activities)
    
    return {
        "weather": weather_data,
        "advice": advice
    }

if __name__ == "__main__":
    try:
        # Example usage
        city = "Munich"
        date = dt.date(2024, 5, 1)
        activities = ["Hiking", "Museum visit", "Coffee shop"]
        
        result = get_weather_with_advice(city, date, activities)
        
        print("\nWeather data:")
        print(f"Temperature: {result['weather']['temp']}°C")
        print(f"Weather: {result['weather']['weather']}")
        print(f"Description: {result['weather']['description']}")
        
        print("\nAdvice:")
        print(f"Suitability: {result['advice']['suitability']}")
        print(f"Clothing advice: {result['advice']['clothing_advice']}")
        print(f"Activity advice: {result['advice']['activity_advice']}")
        print("\nPreparation items:")
        for item in result['advice']['preparation']:
            print(f"- {item}")
        print(f"\nBest time: {result['advice']['best_time']}")
        print("\nAlternative activities:")
        for activity in result['advice']['alternative_activities']:
            print(f"- {activity}")
            
    except Exception as e:
        print(f"Error: {e}")
