from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)
CORS(app)

# Serve index.html
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_values = request.json.get("last_values", [])
        if len(input_values) != 5:
            return jsonify({"error": "Please provide exactly 5 input values."}), 400

        input_values = np.array(input_values).reshape(-1, 1)
        input_values = scaler.transform(input_values)
        input_sequence = np.array(input_values).reshape(1, -1, 1)

        predicted_prices = []
        current_sequence = input_sequence[0]

        for _ in range(5):
            prediction = model.predict(current_sequence[np.newaxis, :, :])
            predicted_prices.append(prediction[0, 0])
            current_sequence = np.append(current_sequence[1:], prediction, axis=0)

        predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1)).flatten().tolist()
        return jsonify({"predicted_prices": predicted_prices})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Load model and scaler
    model = load_model("lstm_model.h5")
    scaler = pickle.load(open("scaler.pkl", "rb"))
    app.run(debug=True)
