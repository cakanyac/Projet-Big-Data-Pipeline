from kafka import KafkaProducer
import requests
import json
import time

# Configuration
KAFKA_BROKER = "localhost:9092"  # À adapter selon ton Docker
KAFKA_TOPIC = "openaq_data"
API_URL = "https://api.openaq.org/v3/sensors/5239/measurements"
API_KEY = "197470ed002e95e1b92194c57b3aba03b02b86001d745dedc3854593719597ac"  # Remplace par ta vraie clé



# Initialiser le producteur Kafka
#producer = KafkaProducer(
 #   bootstrap_servers=KAFKA_BROKER,
#    value_serializer=lambda v: json.dumps(v).encode("utf-8")
#)

# Fonction pour récupérer les données OpenAQ
def fetch_data():
    headers = {"X-API-Key": API_KEY, "Accept": "application/json"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        print("ok")
        return response.json()
    else:
        print(f"Erreur API: {response.status_code} - {response.text}")
        return []

# Envoi des données à Kafka en boucle
#while True:
 #   data = fetch_data()
  #  for record in data:
   #     producer.send(KAFKA_TOPIC, record)
    #    print(f"Envoyé à Kafka : {record}")
    #time.sleep(10)  # Pause entre les requêtes

def save_data_to_file(data, filename="measurements.json"):
    formatted = []

    for item in data["results"]:
        formatted.append({
            "datetime": item["period"]["datetimeFrom"]["utc"],
            "parameter": item["parameter"]["name"],
            "unit": item["parameter"]["units"],
            "value": item["value"]
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(formatted, f, ensure_ascii=False, indent=2)
    print(f"✅ Données sauvegardées dans {filename}")
    
print(fetch_data())

if __name__ == "__main__":
    data = fetch_data()
    save_data_to_file(data)