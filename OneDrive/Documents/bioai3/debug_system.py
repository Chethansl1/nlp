#!/usr/bin/env python3
"""
Debug script to identify and fix system issues
"""

import requests
import json
import time
import os

def test_system_health():
    """Test basic system health"""
    print("SYSTEM HEALTH CHECK")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test system status
        response = requests.get(f"{base_url}/api/test", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ System Status: HEALTHY")
            print(f"   Total Predictions: {status.get('total_predictions', 'N/A')}")
            print(f"   Total Feedback: {status.get('total_feedback', 'N/A')}")
            print(f"   Models Loaded: {status.get('models_loaded', 'N/A')}")
            print(f"   RL Initialized: {status.get('rl_initialized', 'N/A')}")
            return True
        else:
            print(f"❌ System Status: UNHEALTHY ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ System Status: UNREACHABLE ({e})")
        return False

def test_single_prediction():
    """Test a single prediction"""
    print(f"\nSINGLE PREDICTION TEST")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    test_symptoms = ["fever", "cough", "headache"]
    
    try:
        print(f"Testing with symptoms: {test_symptoms}")
        
        response = requests.post(
            f"{base_url}/api/predict",
            json={"symptoms": test_symptoms},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Prediction successful!")
                print(f"   Disease: {result.get('disease', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 'N/A')}")
                print(f"   Prediction ID: {result.get('prediction_id', 'N/A')}")
                return result.get('prediction_id')
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Raw response: {response.text[:500]}")
                return None
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"Error response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_continuous_predictions():
    """Test multiple consecutive predictions"""
    print(f"\nCONTINUOUS PREDICTION TEST")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    test_cases = [
        ["fever", "cough"],
        ["headache", "nausea"],
        ["fatigue", "muscle_pain"],
        ["runny_nose", "sneezing"]
    ]
    
    prediction_ids = []
    
    for i, symptoms in enumerate(test_cases, 1):
        print(f"\nPrediction {i}: {symptoms}")
        
        try:
            response = requests.post(
                f"{base_url}/api/predict",
                json={"symptoms": symptoms},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction_id = result.get('prediction_id')
                prediction_ids.append(prediction_id)
                print(f"  ✅ Success - ID: {prediction_id}, Disease: {result.get('disease')}")
            else:
                print(f"  ❌ Failed - Status: {response.status_code}")
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
        
        # Small delay between predictions
        time.sleep(1)
    
    print(f"\nContinuous prediction results:")
    print(f"  Successful predictions: {len([p for p in prediction_ids if p])}")
    print(f"  Failed predictions: {len([p for p in prediction_ids if not p])}")
    
    return prediction_ids

def test_feedback_system(prediction_ids):
    """Test feedback system"""
    print(f"\nFEEDBACK SYSTEM TEST")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    for i, prediction_id in enumerate(prediction_ids, 1):
        if not prediction_id:
            continue
            
        print(f"Testing feedback for prediction {prediction_id}")
        
        try:
            response = requests.post(
                f"{base_url}/api/feedback",
                json={
                    "prediction_id": prediction_id,
                    "feedback_type": "accuracy",
                    "feedback_value": 4,
                    "comments": f"Test feedback {i}"
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"  ✅ Feedback submitted successfully")
            else:
                print(f"  ❌ Feedback failed: {response.status_code}")
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"  ❌ Feedback exception: {e}")

def check_data_files():
    """Check if required data files exist"""
    print(f"\nDATA FILES CHECK")
    print("=" * 40)
    
    required_files = [
        'data/training_data.csv',
        'data/symptoms.json',
        'data/diseases.json',
        'models/disease_models.pkl'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} (missing)")

def main():
    """Main debug function"""
    print("MEDAI SYSTEM DEBUG TOOL")
    print("=" * 50)
    
    # Check data files
    check_data_files()
    
    # Test system health
    if not test_system_health():
        print("\n❌ System is not running or unhealthy!")
        print("Please start the application with: python app.py")
        return
    
    # Test single prediction
    prediction_id = test_single_prediction()
    
    # Test continuous predictions
    prediction_ids = test_continuous_predictions()
    
    # Test feedback system
    if prediction_ids:
        test_feedback_system(prediction_ids)
    
    print(f"\n{'='*50}")
    print("DEBUG COMPLETED")
    print("=" * 50)
    
    # Summary
    working_predictions = len([p for p in prediction_ids if p])
    total_predictions = len(prediction_ids)
    
    if working_predictions == total_predictions and working_predictions > 0:
        print("✅ All systems working correctly!")
    elif working_predictions > 0:
        print(f"⚠️  Partial functionality: {working_predictions}/{total_predictions} predictions working")
    else:
        print("❌ System has major issues - no predictions working")

if __name__ == "__main__":
    main()