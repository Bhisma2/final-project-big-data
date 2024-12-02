#!/bin/bash

FILE="./samsung-stock-data-2024.zip"
CSV_FILE="./samsung-stock-data-2024.csv"
DEST_DIR="./dataset"

if [ ! -d "$DEST_DIR" ]; then
  mkdir -p "$DEST_DIR"
  echo "Direktori $DEST_DIR telah dibuat."
fi

if [ ! -f "$FILE" ]; then
  echo "Mengunduh file..."
  curl -L -o $FILE https://www.kaggle.com/api/v1/datasets/download/umerhaddii/samsung-stock-data-2024

  if [ $? -ne 0 ]; then
    echo "Unduhan gagal!"
    exit 1
  fi
else
  echo "File sudah ada, melanjutkan ke ekstraksi."
fi

if [ ! -f "$DEST_DIR/samsung-stock-data-2024.csv" ]; then
  unzip $FILE -d "$DEST_DIR" || { echo "Ekstraksi gagal"; exit 1; }
fi

mv "$DEST_DIR/samsung-stock-data-2024.csv" "$DEST_DIR/samsung_stock.csv"

rm $FILE

echo "Selesai! File telah disalin menjadi $DEST_DIR/samsung_stock.csv"
