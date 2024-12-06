from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)
CORS(app)

# Serve API status
@app.route("/")
def home():
    return jsonify({"message": "API is running. Use /predict to make predictions."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_values = request.json.get("last_values", [])
        if len(input_values) != 5:
            return jsonify({"error": "Please provide exactly 5 input values."}), 400

        # Preprocess inputs
        input_values = np.array(input_values).reshape(-1, 1)
        input_values = scaler.transform(input_values)
        input_sequence = np.array(input_values).reshape(1, -1, 1)

        # Generate predictions
        predicted_prices = []
        current_sequence = input_sequence[0]

        for _ in range(5):
            prediction = model.predict(current_sequence[np.newaxis, :, :])
            predicted_prices.append(prediction[0, 0])
            current_sequence = np.append(current_sequence[1:], prediction, axis=0)

        # Post-process predictions
        predicted_prices = scaler.inverse_transform(
            np.array(predicted_prices).reshape(-1, 1)
        ).flatten().tolist()
        return jsonify({"predicted_prices": predicted_prices})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Load model and scaler
    try:
        model = load_model("lstm_model.h5")
        scaler = pickle.load(open("scaler.pkl", "rb"))
        print("Model and scaler loaded successfully.")
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        exit(1)

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
