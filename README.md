# UPI Fraud Detection System

A real-time UPI transaction fraud detection system powered by Machine Learning (Random Forest) and a Flask web backend. This system analyzes transaction patterns and predicts the likelihood of fraud in real-time, storing all results in a persistent database.

## 🚀 Features

- **Real-time Prediction**: Uses a Random Forest classifier to analyze transaction parameters (amount, type, merchant, device, time) and determine fraud probability.
- **Dynamic Frontend**: A modern, responsive web interface for entering transaction details and viewing results.
- **Real-time Database**: Integrated SQLite database to store transaction history and prediction results for live monitoring.
- **History Tracking**: A live-updating history table on the frontend that polls the backend for the latest transaction logs.
- **Scalable Backend**: Flask-based REST API with CORS support, ready for integration with other services.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLite
- **Machine Learning**: Scikit-learn, Pandas, Joblib, Imbalanced-learn (SMOTE)
- **Frontend**: HTML5, CSS3 (Inter font), Vanilla JavaScript
- **Tools**: Git, GitHub CLI

## 📂 Project Structure

- `app.py`: Main Flask application with API endpoints and database logic.
- `train_model.py`: Script to generate synthetic data, train the model, and save artifacts.
- `models/`: Directory containing serialized model and preprocessing objects (`.pkl`).
- `static/`: Frontend assets (HTML, CSS, JS).
- `data/`: Directory for the training dataset (CSV).
- `requirements.txt`: List of Python dependencies.

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/faaiyaazzzz/upi-.git
   cd upi-
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model** (if models are missing):
   ```bash
   python3 train_model.py
   ```

4. **Run the application**:
   ```bash
   python3 app.py
   ```

5. **Access the Web UI**:
   Open your browser and navigate to `http://localhost:5001/`.

## 📊 API Endpoints

- `POST /predict`: Submit transaction data for fraud analysis.
- `GET /history`: Fetch the latest transaction history from the database.
- `GET /health`: Check the server status.

## 🛡️ Security Note

This project uses a synthetic dataset for demonstration purposes. In a production environment, ensure you use real, anonymized transaction data and secure your API endpoints.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Built with ❤️ for secure digital payments.
