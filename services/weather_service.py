import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

API_KEY = "d3e50f733c3431b45fb3f30d379f0f44"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = "Colombo"

def fetch_weather(city_name: str) -> dict:
	query = urlencode({"q": city_name, "appid": API_KEY, "units": "metric"})
	url = f"{BASE_URL}?{query}"

	try:
		with urlopen(url) as response:
			return json.load(response)
	except HTTPError as error:
		return {"error": f"HTTP {error.code}", "details": error.read().decode("utf-8", errors="replace")}
	except URLError as error:
		return {"error": "network_error", "details": str(error)}


if __name__ == "__main__":
	print(fetch_weather(city))