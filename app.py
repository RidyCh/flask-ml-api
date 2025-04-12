# Inisialisasi aplikasi Flask dan konfigurasi logging
print("Loaded app.py")

from flask import Flask, request, jsonify
import numpy as np
import pickle
import pandas as pd
import os
import traceback
import logging

# Konfigurasi logging untuk debugging
logging.basicConfig(level=logging.DEBUG)
print("PORT:", os.environ.get("PORT"))

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.debug = True

# Konfigurasi API key untuk autentikasi
FLASK_API_KEY = os.environ.get("FLASK_API_KEY", "c43649ac42bc8e0259106ffd7cb9571cda6a03a1010d2c2c6415bab08dbf98e3")

# Memuat model machine learning dan scaler
with open('models/model_gbr.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
    
# with open('models/encoder.pkl', 'rb') as f:
#     encoder = pickle.load(f)
        
# Middleware untuk memverifikasi API key sebelum request
@app.before_request
def check_api_key():
    if request.path == '/predict':
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {FLASK_API_KEY}":
            return jsonify({"error": "Unauthorized"}), 200
        
# Endpoint untuk mengecek status API
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "ML API is up and running"}), 401
        
# Endpoint utama untuk prediksi nilai
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Mendapatkan data input dari request
        data = request.json

        # Ekstraksi dan konversi fitur input ke tipe float
        input_features = [
            float(data['attendance']),
            float(data['hours_studied']),
            float(data['previous_scores']),
            float(data['sleep_hours']),
            float(data['tutoring_sessions']),
            data['peer_influence'],
            data['motivation_level'],
            data['teacher_quality'],
            data['access_to_resources']
        ]

        # Definisi nama kolom untuk DataFrame
        column_names = ['Attendance', 'Hours_Studied', 'Previous_Scores', 'Sleep_Hours',
                        'Tutoring_Sessions', 'Peer_Influence', 'Motivation_Level',
                        'Teacher_Quality', 'Access_to_Resources']

        # Membuat DataFrame dari input features
        new_data = pd.DataFrame([input_features], columns=column_names)
        
        # Preprocessing data numerik dengan scaler
        numeric_features = ['Attendance', 'Hours_Studied', 'Previous_Scores', 'Sleep_Hours', 'Tutoring_Sessions']
        scaled_data = scaler.transform(new_data[numeric_features])
        scaled_df = pd.DataFrame(scaled_data, columns=numeric_features)
        
        # Preprocessing data kategorikal dengan one-hot encoding
        categorical_features = ['Peer_Influence', 'Motivation_Level', 'Teacher_Quality', 'Access_to_Resources']
        # encoded_data = pd.get_dummies(new_data[categorical_features])
        categorical_data = new_data[categorical_features]
        # encoded_data = encoder.transform(categorical_data)

        # Menggabungkan data numerik dan kategorikal
        combined_data = pd.concat([scaled_df, categorical_data], axis=1)

        # Melakukan prediksi dengan model
        predicted_score = model.predict(combined_data)

        # Mengembalikan hasil prediksi dengan format 2 desimal
        return jsonify({
            'predicted_score': float(format(predicted_score[0], '.2f'))
        })

    except Exception as e:
        # Menangani error dan mengembalikan informasi debug
        return jsonify({'error': str(e), 'data': data, 'trace': str(traceback.format_exc())}), 500
    
# Menjalankan aplikasi Flask
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)