from kafka import KafkaConsumer
import requests
import json
import time

# 🔧 Configuration HDFS
HDFS_HOST = "localhost"  # Accès depuis Windows, donc localhost
HDFS_PORT = "9870"
HDFS_USER = "root"
HDFS_FILE_PATH = "/data/from_kafka.json"

# 🔧 Configuration Kafka
consumer = KafkaConsumer(
    'pollution',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

buffer = []

def write_to_hdfs(buffer):
    content = "\n".join(json.dumps(m) for m in buffer)
    url = f"http://{HDFS_HOST}:{HDFS_PORT}/webhdfs/v1{HDFS_FILE_PATH}?user.name={HDFS_USER}&op=APPEND"

    try:
        print(f"📡 Tentative d’écriture de {len(buffer)} messages dans HDFS...")
        init = requests.post(url, allow_redirects=False)
        if 'Location' in init.headers:
            redirect_url = init.headers['Location']
            # ⚠️ Remplace tout nom de conteneur par localhost pour que Windows comprenne
            redirect_url = redirect_url.replace('hadoop-datanode1', 'localhost')
            redirect_url = redirect_url.replace('hadoop-datanode2', 'localhost')
            redirect_url = redirect_url.replace('d4792f88242b', 'localhost')
            redirect_url = redirect_url.replace('d62920cf44bc', 'localhost')

            res = requests.post(redirect_url, data=content)
            if res.status_code == 200:
                print(f"✅ {len(buffer)} messages écrits dans HDFS.")
            else:
                print(f"⚠️ Erreur d’écriture finale : {res.status_code}")
        else:
            print("❌ Pas d'URL de redirection obtenue depuis WebHDFS.")
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi à HDFS : {e}")

print("🚀 Consumer Kafka lancé, en attente de messages...")
print("👀 Test de réception : ", consumer.poll(timeout_ms=5000))
for message in consumer:
    buffer.append(message.value)

    if len(buffer) >= 10:
        write_to_hdfs(buffer)
        buffer = []

    time.sleep(0.2)
