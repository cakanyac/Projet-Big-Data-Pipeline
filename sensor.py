import requests

API_URL = "https://api.openaq.org/v3/sensors"
API_KEY = "collect.py"  # à remplacer par ta vraie clé

headers = {
    "X-API-Key": API_KEY,
    "Accept": "application/json"
}

# Étape 1 : récupérer la liste des capteurs
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    sensors = response.json().get("results", [])
    if sensors:
        first_sensor = sensors[0]
        sensor_id = first_sensor["id"]
        print(f"Capteur trouvé : ID = {sensor_id}, nom = {first_sensor.get('name')}")

        # Étape 2 : détail du capteur via GET /v3/sensors/{id}
        sensor_detail_url = f"{API_URL}/{sensor_id}"
        detail_response = requests.get(sensor_detail_url, headers=headers)

        if detail_response.status_code == 200:
            sensor_detail = detail_response.json()
            print("Détails du capteur :", sensor_detail)
        else:
            print(f"Erreur récupération détails capteur {sensor_id} :", detail_response.status_code)
    else:
        print("Aucun capteur trouvé.")
else:
    print("Erreur récupération capteurs :", response.status_code)
    
'''
import requests

headers = {
    "X-API-Key": "TA_CLE_API"
}

response = requests.get("https://api.openaq.org/v3/sensors", headers=headers)
print(response.json())
'''