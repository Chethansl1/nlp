#!/usr/bin/env python3
"""
Test script to verify the prediction API works correctly
"""

import requests
import json
import time

def test_prediction_api():
    """Test the prediction API with sample symptoms"""
    
    base_url = "http://localhost:5000"
    
    # Test data
    test_cases = [
        {
            "name": "Common Cold Symptoms",
            "symptoms": ["runny_nose", "sneezing", "sore_throat", "cough"]
        },
        {
            "name": "Flu Symptoms", 
            "symptoms": ["fever", "fatigue", "muscle_pain", "headache"]
        },
        {
            "name": "Single Symptom",
            "symptoms": ["headache"]
        }
    ]
    
    print("Testing MedAI Prediction API")
    print("=" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Symptoms: {test_case['symptoms']}")
        
        try:
            # Make prediction request
            response = requests.post(
                f"{base_url}/api/predict",
                json={"symptoms": test_case["symptoms"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Success!")
                print(f"   Predicted Disease: {result['disease']}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Severity: {result['severity']}")
                print(f"   Prediction ID: {result['prediction_id']}")
                
                if result.get('alternative_diagnoses'):
                    print(f"   Alternatives: {len(result['alternative_diagnoses'])} found")
                
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    test_prediction_api()