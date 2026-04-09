from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import sqlite3


app = Flask(__name__, static_folder='static')
CORS(app)


# Database setup
DB_PATH = 'transactions.db'


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT,
                merchant TEXT,
                amount REAL,
                device TEXT,
                hour_of_day INTEGER,
                is_fraud INTEGER,
                fraud_probability REAL,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


init_db()


# Load models and artifacts
try:
    model = joblib.load('models/upi_fraud_model.pkl')
    le_transaction = joblib.load('models/le_transaction.pkl')
    le_merchant = joblib.load('models/le_merchant.pkl')
    le_device = joblib.load('models/le_device.pkl')
    scaler = joblib.load('models/scaler.pkl')
    print("Models and artifacts loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")


@app.route('/')
def index():
    if app.static_folder:
        return send_from_directory(app.static_folder, 'index.html')
    return "Static folder not found", 404


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Check for required fields
        required_fields = [
            'transaction_type', 'merchant', 'amount', 'device', 'hour_of_day'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Preprocessing
        input_data = pd.DataFrame([data])

        # Use LabelEncoders
        try:
            input_data['transaction_type'] = le_transaction.transform(
                input_data['transaction_type']
            )
            input_data['merchant'] = le_merchant.transform(
                input_data['merchant']
            )
            input_data['device'] = le_device.transform(
                input_data['device']
            )
        except ValueError as e:
            return jsonify({'error': f'Invalid value in input: {str(e)}'}), 400

        # Scaling
        input_data['amount'] = scaler.transform(input_data[['amount']])

        # Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        result = {
            'is_fraud': int(prediction),
            'fraud_probability': float(probability),
            'status': 'Fraudulent' if prediction == 1 else 'Legitimate'
        }

        # Save to real-time database
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions
                    (transaction_type, merchant, amount, device,
                     hour_of_day, is_fraud, fraud_probability, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['transaction_type'],
                    data['merchant'],
                    float(data['amount']),
                    data['device'],
                    int(data['hour_of_day']),
                    int(prediction),
                    float(probability),
                    result['status']
                ))
                conn.commit()
        except Exception as db_err:
            print(f"Database error: {db_err}")

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/history', methods=['GET'])
def history():
    try:
        limit = request.args.get('limit', default=10, type=int)
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM transactions
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()

            history_data = [dict(row) for row in rows]
            return jsonify(history_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
