#map_agent
import os, requests, logging, json, openai
from typing import List, Dict, Optional, Set
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()
GMAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GMAPS_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY not set")

def get_place_coordinates(place: str, city: str) -> Optional[Dict]:
    """Get coordinates for a place using Google Places API"""
    try:
        # First try to get coordinates using Places API
        places_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": f"{place}, {city}",
            "inputtype": "textquery",
            "fields": "geometry,name,formatted_address,types,opening_hours,rating",
            "key": GMAPS_KEY
        }
        
        response = requests.get(places_url, params=params, timeout=10)
        data = response.json()
        
        if data["status"] == "OK" and data["candidates"]:
            location = data["candidates"][0]["geometry"]["location"]
            return {
                "name": place,
                "address": data["candidates"][0]["formatted_address"],
                "lat": location["lat"],
                "lng": location["lng"],
                "types": data["candidates"][0].get("types", []),
                "opening_hours": data["candidates"][0].get("opening_hours", {}),
                "rating": data["candidates"][0].get("rating", 0)
            }
            
        return None
    except Exception as e:
        logger.warning(f"Failed to get coordinates for {place}: {str(e)}")
        return None

def validate_route(original_places: Set[str], optimized_places: List[str]) -> bool:
    """Validate that the optimized route includes all original places"""
    return set(optimized_places) == original_places

def optimize_route_with_llm(places: List[str], city: str, preferences: Dict) -> Dict:
    """Optimize route planning using LLM"""
    # Get detailed information for places
    place_info = []
    for place in places:
        info = get_place_coordinates(place, city)
        if info:
            place_info.append(info)
    
    # Build LLM prompt
    prompt = f"""Please plan the optimal route for the following attractions in {city}:
    Attractions list: {json.dumps(place_info, ensure_ascii=False, indent=2)}
    User preferences: {json.dumps(preferences, ensure_ascii=False, indent=2)}
    
    Please consider:
    1. Opening hours of attractions
    2. User's preferred transportation mode
    3. Ratings and types of attractions
    4. Reasonable time allocation for visits
    
    Return format:
    {{
        "ordered_places": ["attraction1", "attraction2", ...],
        "suggested_times": ["09:00", "11:00", ...],
        "transport_modes": ["walking", "transit", ...],
        "visit_duration": [120, 90, ...],  // minutes
        "notes": ["suggestion1", "suggestion2", ...]
    }}"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        llm_suggestion = json.loads(response.choices[0].message.content)
        
        # Use Google Maps API to validate and optimize LLM suggestions
        return optimize_route_with_maps(llm_suggestion["ordered_places"], city, llm_suggestion["transport_modes"])
    except Exception as e:
        logger.error(f"LLM route optimization failed: {str(e)}")
        return optimize_route(places, city)

def optimize_route_with_maps(places: List[str], city: str, transport_modes: List[str]) -> Dict:
    """使用Google Maps API优化路线"""
    if len(places) < 2:
        return {"ordered": places}
    
    # Remove duplicates while preserving order
    unique_places = []
    seen = set()
    for place in places:
        if place not in seen:
            seen.add(place)
            unique_places.append(place)
    
    if len(unique_places) != len(places):
        logger.warning(f"Removed {len(places) - len(unique_places)} duplicate places")
        places = unique_places
    
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    # Get place information
    place_info = []
    for place in places:
        info = get_place_coordinates(place, city)
        if info:
            place_info.append(info)
        else:
            place_info.append({
                "name": place,
                "address": f"{place}, {city}, Germany",
                "lat": None,
                "lng": None
            })
    
    formatted_places = [info["address"] for info in place_info]
    original_places_set = set(places)
    
    # Try different transportation modes
    best_result = None
    last_error = None
    
    for mode in transport_modes:
        try:
            waypoints = "|".join(formatted_places[1:-1])
            
            params = {
                "origin": formatted_places[0],
                "destination": formatted_places[-1],
                "waypoints": f"optimize:true|{waypoints}" if waypoints else None,
                "key": GMAPS_KEY,
                "mode": mode,
                "alternatives": "false",
                "language": "en"
            }
            
            logger.info(f"Trying {mode} mode for places: {formatted_places}")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK" and data["routes"]:
                route = data["routes"][0]
                
                total_distance = sum(leg["distance"]["value"] for leg in route["legs"]) / 1000
                total_duration = sum(leg["duration"]["value"] for leg in route["legs"]) / 60
                
                waypoint_order = [places[i] for i in route["waypoint_order"]]
                ordered_places = [places[0]] + waypoint_order + [places[-1]]
                
                if not validate_route(original_places_set, ordered_places):
                    logger.warning(f"Route validation failed for {mode} mode: missing places")
                    continue
                
                result = {
                    "ordered": ordered_places,
                    "polyline": route["overview_polyline"]["points"],
                    "dist_km": total_distance,
                    "duration_min": total_duration,
                    "mode": mode,
                    "places": formatted_places,
                    "coordinates": [(info["lat"], info["lng"]) for info in place_info]
                }
                
                if mode == "driving":
                    result["duration_min"] *= 1.2
                elif mode == "transit":
                    result["duration_min"] *= 1.3
                
                logger.info(f"Route calculated successfully using {mode} mode")
                return result
                
            last_error = data.get("error_message", f"No route found using {mode} mode")
            logger.warning(f"No route found using {mode} mode: {data.get('status')}")
            
        except Exception as e:
            last_error = str(e)
            logger.error(f"Request failed with {mode} mode: {str(e)}")
    
    return {
        "ordered": places,
        "dist_km": None,
        "duration_min": None,
        "mode": None,
        "places": formatted_places,
        "coordinates": [(info["lat"], info["lng"]) for info in place_info],
        "warning": "Could not calculate optimized route, using original order"
    }

def optimize_route(places: List[str], city: str, preferences: Dict = None) -> Dict:
    """主优化函数，根据是否有用户偏好选择不同的优化策略"""
    if preferences:
        return optimize_route_with_llm(places, city, preferences)
    return optimize_route_with_maps(places, city, ["driving", "walking", "transit"])

if __name__ == "__main__":
    try:
        # Example usage
        places = [
            "Café Frischhut",
            "English Garden",
            "Marienplatz",
            "Hofbräuhaus"
        ]
        
        preferences = {
            "transport_preference": "walking",
            "budget": "medium",
            "interests": ["coffee", "outdoor"]
        }
        
        result = optimize_route(places, "Munich", preferences)
        
        print("\nRoute:")
        for i, place in enumerate(result["ordered"], 1):
            print(f"{i}. {place}")
            
        if result.get("dist_km") is not None:
            print(f"\nTotal distance: {result['dist_km']:.1f} km")
            print(f"Total duration: {result['duration_min']:.0f} minutes")
            print(f"Transportation mode: {result['mode']}")
            
        if "warning" in result:
            print(f"\nWarning: {result['warning']}")
            
    except Exception as e:
        print(f"Error: {e}")