# Gunakan image dasar berbasis Python
FROM python:3.9-slim

# Set environment variable untuk TensorFlow (opsional untuk CPU-only)
ENV TF_FORCE_GPU_ALLOW_GROWTH="true"
ENV CUDA_VISIBLE_DEVICES="-1"

# Set working directory
WORKDIR /app

# Salin seluruh isi direktori ke dalam image
COPY . /app

# Instal semua dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port Flask
EXPOSE 5000

# Jalankan aplikasi
CMD ["python", "app.py"]
