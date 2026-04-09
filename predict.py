import requests
import json

def test_prediction():
    url = 'http://localhost:5001/predict'
    
    # Example legitimate transaction
    legitimate_data = {
        'transaction_type': 'P2P',
        'merchant': 'None',
        'amount': 500,
        'device': 'Android',
        'hour_of_day': 14
    }
    
    # Example fraud transaction
    fraudulent_data = {
        'transaction_type': 'P2M',
        'merchant': 'None',
        'amount': 95000,
        'device': 'Web',
        'hour_of_day': 2
    }
    
    print("Testing legitimate transaction...")
    response = requests.post(url, json=legitimate_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\nTesting fraudulent transaction...")
    response = requests.post(url, json=fraudulent_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_prediction()
