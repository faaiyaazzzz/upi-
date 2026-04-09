import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

def generate_data(n_samples=10000):
    np.random.seed(42)
    
    # Feature columns
    transaction_types = ['P2P', 'P2M', 'BILL_PAYMENT', 'RECHARGE']
    merchants = ['Amazon', 'Flipkart', 'Swiggy', 'Zomato', 'Paytm', 'PhonePe', 'GooglePay', 'None']
    devices = ['Android', 'iOS', 'Web', 'Unknown']
    
    data = {
        'transaction_type': np.random.choice(transaction_types, n_samples),
        'merchant': np.random.choice(merchants, n_samples),
        'amount': np.random.uniform(10, 100000, n_samples),
        'device': np.random.choice(devices, n_samples),
        'hour_of_day': np.random.randint(0, 24, n_samples),
        'is_fraud': 0
    }
    
    df = pd.DataFrame(data)
    
    # Simple logic for synthetic fraud
    # Higher fraud probability for high amounts, specific hours, and specific types
    fraud_mask = (
        (df['amount'] > 80000) | 
        ((df['hour_of_day'] >= 0) & (df['hour_of_day'] <= 4) & (df['amount'] > 5000)) |
        ((df['transaction_type'] == 'P2M') & (df['merchant'] == 'None'))
    )
    
    # Add some randomness to fraud
    df.loc[fraud_mask, 'is_fraud'] = np.random.choice([0, 1], size=fraud_mask.sum(), p=[0.3, 0.7])
    
    # Save data
    df.to_csv('data/upi_transactions.csv', index=False)
    print("Data generated and saved to data/upi_transactions.csv")
    return df

def train():
    if not os.path.exists('data/upi_transactions.csv') or os.path.getsize('data/upi_transactions.csv') == 0:
        df = generate_data()
    else:
        df = pd.read_csv('data/upi_transactions.csv')
    
    # Label Encoding
    le_transaction = LabelEncoder()
    le_merchant = LabelEncoder()
    le_device = LabelEncoder()
    
    df['transaction_type'] = le_transaction.fit_transform(df['transaction_type'])
    df['merchant'] = le_merchant.fit_transform(df['merchant'])
    df['device'] = le_device.fit_transform(df['device'])
    
    # Scaling
    scaler = StandardScaler()
    df['amount'] = scaler.fit_transform(df[['amount']])
    
    # Prepare features and target
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # Handling imbalance with SMOTE
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print("Model trained.")
    print(classification_report(y_test, y_pred))
    
    # Save model and artifacts
    joblib.dump(model, 'models/upi_fraud_model.pkl')
    joblib.dump(le_transaction, 'models/le_transaction.pkl')
    joblib.dump(le_merchant, 'models/le_merchant.pkl')
    joblib.dump(le_device, 'models/le_device.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print("Model and artifacts saved to models/")

if __name__ == "__main__":
    train()
