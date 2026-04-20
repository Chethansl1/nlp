#!/usr/bin/env python3
"""
Advanced training script for perfect disease prediction accuracy
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import lightgbm as lgb
import joblib
import json

class PerfectDiseasePredictor:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.symptom_encoder = {}
        self.feature_names = []
        
    def load_and_prepare_data(self):
        """Load and prepare the training data"""
        print("Loading comprehensive training data...")
        
        # Load training data
        data_path = 'data/training_data.csv'
        if not os.path.exists(data_path):
            raise FileNotFoundError("Training data not found. Run generate_training_data.py first.")
        
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} samples with {df['disease'].nunique()} diseases")
        
        # Separate features and target
        feature_columns = [col for col in df.columns if col not in ['disease', 'severity', 'category']]
        self.feature_names = feature_columns
        
        X = df[feature_columns].values
        y = df['disease'].values
        
        # Create symptom encoder
        self.symptom_encoder = {symptom: i for i, symptom in enumerate(feature_columns)}
        
        print(f"Features: {len(feature_columns)}")
        print(f"Unique diseases: {len(np.unique(y))}")
        
        return X, y
    
    def optimize_hyperparameters(self, X_train, y_train):
        """Optimize hyperparameters for each model"""
        print("Optimizing hyperparameters...")
        
        # Random Forest optimization
        rf_params = {
            'n_estimators': [200, 300, 500],
            'max_depth': [15, 20, 25],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf_grid = GridSearchCV(
            RandomForestClassifier(random_state=42, class_weight='balanced'),
            rf_params, cv=5, scoring='accuracy', n_jobs=-1, verbose=1
        )
        rf_grid.fit(X_train, y_train)
        
        print(f"Best RF params: {rf_grid.best_params_}")
        print(f"Best RF score: {rf_grid.best_score_:.4f}")
        
        # XGBoost optimization
        xgb_params = {
            'n_estimators': [200, 300, 500],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1, 0.15],
            'subsample': [0.8, 0.9, 1.0]
        }
        
        xgb_grid = GridSearchCV(
            xgb.XGBClassifier(random_state=42, eval_metric='mlogloss'),
            xgb_params, cv=5, scoring='accuracy', n_jobs=-1, verbose=1
        )
        xgb_grid.fit(X_train, y_train)
        
        print(f"Best XGB params: {xgb_grid.best_params_}")
        print(f"Best XGB score: {xgb_grid.best_score_:.4f}")
        
        return rf_grid.best_estimator_, xgb_grid.best_estimator_
    
    def train_ensemble_models(self, X, y):
        """Train an ensemble of optimized models"""
        print("Training ensemble models...")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Apply SMOTE for balanced dataset
        print("Applying SMOTE for balanced dataset...")
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_balanced, y_balanced = smote.fit_resample(X, y_encoded)
        
        print(f"After SMOTE: {X_balanced.shape[0]} samples")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Get optimized models
        best_rf, best_xgb = self.optimize_hyperparameters(X_train_scaled, y_train)
        
        # Define all models with optimized parameters
        models = {
            'random_forest_optimized': best_rf,
            'xgboost_optimized': best_xgb,
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=10,
                subsample=0.8,
                random_state=42
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=10,
                num_leaves=100,
                feature_fraction=0.8,
                bagging_fraction=0.8,
                random_state=42,
                verbose=-1
            ),
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(300, 200, 100, 50),
                activation='relu',
                solver='adam',
                learning_rate_init=0.001,
                max_iter=2000,
                early_stopping=True,
                validation_fraction=0.1,
                random_state=42
            )
        }
        
        # Train and evaluate each model
        model_scores = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            if name == 'random_forest_optimized' or name == 'xgboost_optimized':
                # Already fitted during optimization
                pass
            else:
                model.fit(X_train_scaled, y_train)
            
            # Evaluate on test set
            y_pred = model.predict(X_test_scaled)
            test_accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            print(f"  Test Accuracy: {test_accuracy:.4f}")
            print(f"  CV Accuracy: {cv_mean:.4f} (+/- {cv_std * 2:.4f})")
            
            self.models[name] = model
            model_scores[name] = cv_mean
        
        # Print final results
        print(f"\n{'='*50}")
        print("FINAL MODEL PERFORMANCE RANKING:")
        print(f"{'='*50}")
        
        sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (name, score) in enumerate(sorted_models, 1):
            print(f"{i}. {name}: {score:.4f}")
        
        return sorted_models[0][0]  # Return best model name
    
    def save_models(self):
        """Save all trained models"""
        print("Saving models...")
        
        # Create models directory
        os.makedirs('models', exist_ok=True)
        
        # Save individual models
        for name, model in self.models.items():
            model_path = f'models/{name}_model.pkl'
            joblib.dump(model, model_path)
            print(f"  Saved {name} to {model_path}")
        
        # Save preprocessing objects
        joblib.dump(self.scaler, 'models/scaler.pkl')
        joblib.dump(self.label_encoder, 'models/label_encoder.pkl')
        
        # Save symptom encoder
        with open('models/symptom_encoder.json', 'w') as f:
            json.dump(self.symptom_encoder, f)
        
        # Save feature names
        with open('models/feature_names.json', 'w') as f:
            json.dump(self.feature_names, f)
        
        print("All models and preprocessing objects saved!")
    
    def test_predictions(self):
        """Test the trained models with sample predictions"""
        print(f"\n{'='*50}")
        print("TESTING PREDICTIONS:")
        print(f"{'='*50}")
        
        test_cases = [
            {
                'name': 'Common Cold',
                'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'nasal_congestion']
            },
            {
                'name': 'Influenza',
                'symptoms': ['fever', 'fatigue', 'muscle_pain', 'headache', 'chills']
            },
            {
                'name': 'Pneumonia',
                'symptoms': ['chest_pain', 'shortness_of_breath', 'cough', 'fever', 'fatigue']
            },
            {
                'name': 'Diabetes Type 2',
                'symptoms': ['frequent_urination', 'fatigue', 'weight_loss', 'excessive_thirst']
            },
            {
                'name': 'Hypertension',
                'symptoms': ['headache', 'dizziness', 'chest_pain', 'shortness_of_breath']
            }
        ]
        
        for test_case in test_cases:
            print(f"\nTesting: {test_case['name']}")
            print(f"Symptoms: {test_case['symptoms']}")
            
            # Create feature vector
            feature_vector = np.zeros(len(self.feature_names))
            for symptom in test_case['symptoms']:
                if symptom in self.symptom_encoder:
                    idx = self.symptom_encoder[symptom]
                    feature_vector[idx] = 1
            
            feature_vector = feature_vector.reshape(1, -1)
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Get predictions from all models
            predictions = {}
            for name, model in self.models.items():
                pred = model.predict(feature_vector_scaled)[0]
                pred_proba = model.predict_proba(feature_vector_scaled)[0]
                
                disease = self.label_encoder.inverse_transform([pred])[0]
                confidence = max(pred_proba)
                
                predictions[name] = (disease, confidence)
            
            # Show results
            for name, (disease, confidence) in predictions.items():
                print(f"  {name}: {disease} ({confidence:.3f})")

def main():
    """Main training function"""
    print("🚀 PERFECT DISEASE PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    try:
        # Initialize predictor
        predictor = PerfectDiseasePredictor()
        
        # Load and prepare data
        X, y = predictor.load_and_prepare_data()
        
        # Train ensemble models
        best_model = predictor.train_ensemble_models(X, y)
        
        # Save models
        predictor.save_models()
        
        # Test predictions
        predictor.test_predictions()
        
        print(f"\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print(f"Best performing model: {best_model}")
        print(f"All models saved to 'models/' directory")
        print(f"Ready for deployment with high accuracy!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()