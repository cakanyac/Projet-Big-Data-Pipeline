from kafka import KafkaProducer
import json
import time

# Charger les données depuis le fichier JSON
with open('measurements.json', 'r') as f:
    data = json.load(f)

# Configurer le producteur Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Envoyer chaque mesure dans le topic "pollution"
for record in data:
    producer.send('pollution', record)
    time.sleep(0.1)  # petite pause pour simuler un flux
    print(f"Message envoyé : {record}")

producer.flush()
