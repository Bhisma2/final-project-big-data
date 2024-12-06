# Kelompok 4

run docker
```bash
docker-compose up -d
```

download dataset
```bash
bash dataset/download.sh
```

kafka
```bash
docker exec -it <kafka id> kafka-topics.sh --create --topic samsung-stock-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec -it <kafka id> kafka-console-consumer.sh --topic samsung-stock-data --bootstrap-server localhost:9092  --from-beginning
```

stream dataset
```bash
cd kafka
python3 producer.py
```

## Uji coba web dan model
```sh
# buka 2 terminal berbeda
cd web
python3 -m http.server 8000 
python3 app.py 
```
target berikutnya depploy model ke docker

### login minio
```txt
minio/minio123
```