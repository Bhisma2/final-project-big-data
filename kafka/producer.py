from confluent_kafka import Producer
import pandas as pd
import json

# Konfigurasi Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'samsung-stock-producer',
}

producer = Producer(**conf)
print("Kafka Producer siap...")

# Load dataset
DATASET_PATH = "../dataset/samsung_stock.csv"

try:
    data = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    print(f"File {DATASET_PATH} tidak ditemukan. Pastikan dataset sudah tersedia.")
    exit(1)

# Preprocessing dataset
data.columns = data.columns.str.strip()
data.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
data['date'] = pd.to_datetime(data['date'], errors='coerce')

topic = "samsung-stock-data"

def delivery_report(err, msg):
    if err:
        print(f"Pengiriman pesan gagal: {err}")
    else:
        print(f"Pesan terkirim ke {msg.topic()} [partisi {msg.partition()}]")

for index, row in data.iterrows():
    if pd.notna(row['date']):
        message = {
            "date": row["date"].strftime('%Y-%m-%d'),
            "adj_close": row["Adj Close"],
            "close": row["Close"],
            "high": row["High"],
            "low": row["Low"],
            "open": row["Open"],
            "volume": row["Volume"],
        }
        key = row["date"].strftime('%Y%m%d')
        try:
            producer.produce(topic, key=key, value=json.dumps(message), callback=delivery_report)
        except Exception as e:
            print(f"Gagal mengirim pesan: {e}")
    else:
        print(f"Data pada indeks {index} tidak valid, melewati...")

producer.flush()
print("Semua pesan telah dikirim.")
