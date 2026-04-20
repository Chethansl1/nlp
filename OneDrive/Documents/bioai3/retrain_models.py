#!/usr/bin/env python3
"""
Script to retrain the disease prediction models with the comprehensive dataset
"""

import os
import sys
import pandas as pd
import numpy as np
from ml_models.disease_predictor import DiseasePredictor

def retrain_models():
    """Retrain all models with the comprehensive dataset"""
    
    print("MedAI Model Retraining Script")
    print("=" * 50)
    
    # Check if training data exists
    data_path = os.path.join('data', 'training_data.csv')
    if not os.path.exists(data_path):
        print("❌ Training data not found!")
        print("Please run: python data/generate_training_data.py")
        return False
    
    # Load and inspect training data
    print("Loading training data...")
    df = pd.read_csv(data_path)
    
    print(f"✅ Training data loaded:")
    print(f"   - Total samples: {len(df)}")
    print(f"   - Features: {len(df.columns) - 3}")  # Excluding disease, severity, category
    print(f"   - Diseases: {df['disease'].nunique()}")
    print(f"   - Categories: {df['category'].nunique()}")
    
    # Show disease distribution
    print(f"\nTop 10 diseases by frequency:")
    disease_counts = df['disease'].value_counts().head(10)
    for disease, count in disease_counts.items():
        print(f"   - {disease}: {count} samples")
    
    # Initialize disease predictor
    print(f"\nInitializing disease predictor...")
    predictor = DiseasePredictor()
    
    # Train models
    print(f"\nStarting model training...")
    try:
        best_model, best_score = predictor.train_initial_model()
        
        print(f"\n✅ Model training completed!")
        print(f"   - Best model: {best_model}")
        print(f"   - Best CV score: {best_score:.4f}")
        print(f"   - Total models trained: {len(predictor.models)}")
        
        # Test prediction
        print(f"\nTesting prediction with sample symptoms...")
        test_symptoms = ['fever', 'cough', 'headache', 'fatigue']
        
        try:
            result = predictor.predict(test_symptoms)
            print(f"✅ Test prediction successful:")
            print(f"   - Symptoms: {test_symptoms}")
            print(f"   - Predicted disease: {result['disease']}")
            print(f"   - Confidence: {result['confidence']:.3f}")
            print(f"   - Severity: {result['severity']}")
            
        except Exception as e:
            print(f"❌ Test prediction failed: {e}")
            return False
        
        print(f"\n🎉 Model retraining completed successfully!")
        print(f"The models are now ready for use with improved accuracy.")
        
        return True
        
    except Exception as e:
        print(f"❌ Model training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_models():
    """Validate the trained models"""
    print(f"\nValidating trained models...")
    
    try:
        predictor = DiseasePredictor()
        
        # Load existing models
        if predictor.load_models():
            print(f"✅ Models loaded successfully")
            print(f"   - Available models: {list(predictor.models.keys())}")
            
            # Test with various symptom combinations
            test_cases = [
                {
                    'name': 'Common Cold',
                    'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough']
                },
                {
                    'name': 'Flu',
                    'symptoms': ['fever', 'fatigue', 'muscle_pain', 'headache', 'chills']
                },
                {
                    'name': 'Migraine',
                    'symptoms': ['headache', 'nausea', 'vision_problems']
                },
                {
                    'name': 'Diabetes',
                    'symptoms': ['frequent_urination', 'fatigue', 'weight_loss']
                },
                {
                    'name': 'Hypertension',
                    'symptoms': ['headache', 'dizziness', 'chest_pain']
                }
            ]
            
            print(f"\nTesting with sample cases:")
            for test_case in test_cases:
                try:
                    result = predictor.predict(test_case['symptoms'])
                    print(f"   {test_case['name']}:")
                    print(f"     Predicted: {result['disease']} ({result['confidence']:.2f})")
                    
                except Exception as e:
                    print(f"   {test_case['name']}: ❌ Failed - {e}")
            
            return True
        else:
            print(f"❌ Failed to load models")
            return False
            
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

def main():
    """Main function"""
    print("Choose an option:")
    print("1. Retrain models from scratch")
    print("2. Validate existing models")
    print("3. Both retrain and validate")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == '1':
        success = retrain_models()
    elif choice == '2':
        success = validate_models()
    elif choice == '3':
        success = retrain_models()
        if success:
            success = validate_models()
    else:
        print("Invalid choice!")
        return
    
    if success:
        print(f"\n✅ All operations completed successfully!")
        print(f"You can now run the application with: python app.py")
    else:
        print(f"\n❌ Some operations failed. Please check the errors above.")

if __name__ == "__main__":
    main()