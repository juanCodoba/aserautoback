import requests

class FetchExternalData:
    def execute(self, query):
        # Ejemplo: Obtener el clima de una ciudad
        api_key = "tu_api_key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None