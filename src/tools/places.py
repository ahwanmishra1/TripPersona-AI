import requests
from src.config.settings import settings


def _demo_data() -> dict:
    return {
        "tokyo": {
            "popular_places": [
                "Shibuya Crossing",
                "Senso-ji Temple",
                "Tokyo Tower",
                "Meiji Shrine",
                "teamLab Planets",
            ],
            "local_places": [
                "Yanaka",
                "Shimokitazawa",
                "Kichijoji",
                "Koenji",
                "Daikanyama",
            ],
            "food_areas": [
                "Tsukiji Outer Market",
                "Ebisu dining district",
                "Asakusa food lanes",
                "Ginza cafes",
                "Shinjuku Omoide Yokocho",
            ],
            "stay_areas": [
                "Shinjuku",
                "Shibuya",
                "Asakusa",
                "Ginza",
            ],
            "signature_foods": [
                "sushi",
                "ramen",
                "yakitori",
                "katsu curry",
                "matcha desserts",
            ],
        },
        "kyoto": {
            "popular_places": [
                "Fushimi Inari Shrine",
                "Kinkaku-ji",
                "Arashiyama Bamboo Grove",
                "Kiyomizu-dera",
                "Gion",
            ],
            "local_places": [
                "Philosopher’s Path backstreets",
                "Nishijin neighborhood",
                "Demachiyanagi",
                "quiet tea-house lanes",
                "local temple side streets",
            ],
            "food_areas": [
                "Nishiki Market",
                "Pontocho",
                "Gion cafes",
                "Arashiyama sweets lanes",
                "Kawaramachi dining streets",
            ],
            "stay_areas": [
                "Gion",
                "Kawaramachi",
                "Higashiyama",
                "Central Kyoto",
            ],
            "signature_foods": [
                "kaiseki",
                "matcha sweets",
                "yudofu",
                "ramen",
                "wagashi",
            ],
        },
        "jaipur": {
            "popular_places": [
                "Amber Fort",
                "Hawa Mahal",
                "City Palace",
                "Jal Mahal",
                "Nahargarh Fort",
            ],
            "local_places": [
                "Panna Meena ka Kund",
                "Jawahar Kala Kendra",
                "Bapu Bazaar lanes",
                "old city courtyards",
                "quiet artisan neighborhoods",
            ],
            "food_areas": [
                "MI Road",
                "old city sweet shops",
                "Bapu Bazaar food stops",
                "C-Scheme cafes",
                "local thali spots",
            ],
            "stay_areas": [
                "C-Scheme",
                "Bani Park",
                "MI Road area",
                "old city edge",
            ],
            "signature_foods": [
                "dal baati churma",
                "laal maas",
                "ghewar",
                "kachori",
                "lassi",
            ],
        },
        "goa": {
            "popular_places": [
                "Baga Beach",
                "Anjuna Beach",
                "Fort Aguada",
                "Chapora Fort",
                "Calangute Beach",
            ],
            "local_places": [
                "Fontainhas",
                "Assagao",
                "Divar Island",
                "Reis Magos",
                "quiet South Goa stretches",
            ],
            "food_areas": [
                "Anjuna cafes",
                "Panaji Latin Quarter dining",
                "Assagao restaurants",
                "Mapusa market stops",
                "beach shack belts",
            ],
            "stay_areas": [
                "Panaji",
                "Assagao",
                "Anjuna",
                "Candolim",
            ],
            "signature_foods": [
                "prawn curry",
                "bebinca",
                "cafreal",
                "fish thali",
                "poi sandwiches",
            ],
        },
    }


def _fallback(destination: str) -> dict:
    data = _demo_data()
    key = destination.strip().lower()
    return data.get(
        key,
        {
            "popular_places": [
                "Main Landmark",
                "City Museum",
                "Historic Center",
                "Famous Market",
                "Scenic Walk",
            ],
            "local_places": [
                "Neighborhood lane",
                "Arts district",
                "Hidden cafe street",
                "Local park",
                "Old town corner",
            ],
            "food_areas": [
                "Central food street",
                "Local market",
                "Cafe district",
                "Evening stalls",
                "Dessert lane",
            ],
            "stay_areas": [
                "City center",
                "cultural quarter",
                "transit-friendly district",
                "lively neighborhood",
            ],
            "signature_foods": [
                "regional specialty",
                "street snack",
                "local dessert",
            ],
        },
    )


def _tavily_extract_list(results: list, limit: int = 5) -> list[str]:
    items = []
    for result in results:
        title = result.get("title", "").strip()
        content = result.get("content", "").strip()
        if title and title not in items:
            items.append(title)
        elif content:
            shortened = content.split(".")[0].strip()
            if shortened and shortened not in items:
                items.append(shortened)
        if len(items) >= limit:
            break
    return items


def get_places(destination: str) -> dict:
    fallback = _fallback(destination)

    if not settings.tavily_api_key:
        return {"status": "demo", **fallback}

    try:
        queries = {
            "popular_places": f"top tourist attractions in {destination}",
            "local_places": f"hidden gems and local neighborhoods in {destination}",
            "food_areas": f"best food streets cafes markets and dining areas in {destination}",
            "stay_areas": f"best areas to stay in {destination} for travellers",
            "signature_foods": f"must try local food and signature dishes in {destination}",
        }

        out = {}
        for key, query in queries.items():
            res = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": settings.tavily_api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5,
                },
                timeout=12,
            )
            res.raise_for_status()
            data = res.json()
            extracted = _tavily_extract_list(data.get("results", []), limit=5)
            out[key] = extracted if extracted else fallback[key]

        return {"status": "live", **out}
    except Exception:
        return {"status": "demo", **fallback}