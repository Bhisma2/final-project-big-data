from confluent_kafka import Producer
import pandas as pd
import json
import random

conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'samsung-stock-producer',
}

producer = Producer(**conf)
print("Spinning up Kafka Producer...")

data = pd.read_csv("dataset/samsung_stock.csv")
data.columns = data.columns.str.strip()

data.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

print("Kolom yang ditemukan:", data.columns)
print("Beberapa data pertama:")
print(data.head())

data['date'] = pd.to_datetime(data['date'], errors='coerce')

topic = "samsung-stock-data"

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

for index, row in data.iterrows():
    if pd.notna(row['date']) and pd.notna(row['Adj Close']) and pd.notna(row['Close']):
        message = {
            "date": row["date"].strftime('%Y-%m-%d'),
            "adj_close": row["Adj Close"],
            "close": row["Close"],
            "high": row["High"],
            "low": row["Low"],
            "open": row["Open"],
            "volume": row["Volume"],
        }

        key = str(row["date"].strftime('%Y%m%d'))

        try:
            producer.produce(topic, key=key, value=json.dumps(message), callback=delivery_report)
            print(f"Message {index} sent to Kafka")
        except Exception as e:
            print(f"Failed to send message {index}: {e}")
    else:
        print(f"Data pada indeks {index} tidak lengkap, melewati...")

producer.flush()
print("All messages sent.")
