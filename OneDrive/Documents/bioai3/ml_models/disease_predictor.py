import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb
from imblearn.over_sampling import SMOTE
import joblib
import sqlite3
import json
import os
from datetime import datetime

class DiseasePredictor:
    def __init__(self):
        self.models = {}
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.symptom_encoder = {}
        self.disease_info = self.load_disease_info()
        self.load_models()
    
    def load_disease_info(self):
        """Load comprehensive disease information"""
        return {
            'Common Cold': {
                'severity': 'Mild',
                'recommendations': [
                    'Rest and stay hydrated',
                    'Use over-the-counter pain relievers',
                    'Gargle with salt water',
                    'Consider seeing a doctor if symptoms persist over 10 days'
                ],
                'typical_duration': '7-10 days'
            },
            'Influenza': {
                'severity': 'Moderate',
                'recommendations': [
                    'Rest and stay hydrated',
                    'Antiviral medications if prescribed',
                    'Monitor for complications',
                    'Seek immediate care if breathing difficulties occur'
                ],
                'typical_duration': '1-2 weeks'
            },
            'Pneumonia': {
                'severity': 'Severe',
                'recommendations': [
                    'Seek immediate medical attention',
                    'Complete prescribed antibiotic course',
                    'Rest and maintain fluid intake',
                    'Monitor oxygen levels if available'
                ],
                'typical_duration': '2-3 weeks'
            },
            'Diabetes Type 2': {
                'severity': 'Chronic',
                'recommendations': [
                    'Consult endocrinologist immediately',
                    'Monitor blood glucose regularly',
                    'Follow diabetic diet plan',
                    'Regular exercise as recommended'
                ],
                'typical_duration': 'Lifelong management'
            },
            'Hypertension': {
                'severity': 'Chronic',
                'recommendations': [
                    'Consult cardiologist',
                    'Monitor blood pressure daily',
                    'Reduce sodium intake',
                    'Regular cardiovascular exercise'
                ],
                'typical_duration': 'Lifelong management'
            },
            'Migraine': {
                'severity': 'Moderate',
                'recommendations': [
                    'Identify and avoid triggers',
                    'Use prescribed migraine medications',
                    'Rest in dark, quiet environment',
                    'Consider preventive medications'
                ],
                'typical_duration': '4-72 hours per episode'
            },
            'Gastroenteritis': {
                'severity': 'Mild to Moderate',
                'recommendations': [
                    'Stay hydrated with clear fluids',
                    'BRAT diet (Bananas, Rice, Applesauce, Toast)',
                    'Avoid dairy and fatty foods',
                    'Seek care if severe dehydration occurs'
                ],
                'typical_duration': '1-3 days'
            },
            'Asthma': {
                'severity': 'Moderate to Severe',
                'recommendations': [
                    'Use prescribed inhalers as directed',
                    'Avoid known triggers',
                    'Have emergency action plan',
                    'Regular pulmonologist follow-up'
                ],
                'typical_duration': 'Chronic condition'
            },
            'Depression': {
                'severity': 'Moderate to Severe',
                'recommendations': [
                    'Consult mental health professional',
                    'Consider therapy and/or medication',
                    'Maintain social connections',
                    'Regular exercise and healthy lifestyle'
                ],
                'typical_duration': 'Variable, requires ongoing management'
            },
            'Anxiety Disorder': {
                'severity': 'Mild to Severe',
                'recommendations': [
                    'Practice relaxation techniques',
                    'Consider cognitive behavioral therapy',
                    'Limit caffeine and alcohol',
                    'Consult mental health professional'
                ],
                'typical_duration': 'Variable, manageable with treatment'
            }
        }
    
    def load_training_data(self):
        """Load training data from CSV file or generate synthetic data"""
        try:
            # Try to load from CSV file
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'training_data.csv')
            if os.path.exists(data_path):
                df = pd.read_csv(data_path)
                print(f"Loaded training data: {len(df)} samples, {df['disease'].nunique()} diseases")
                return df
        except Exception as e:
            print(f"Error loading training data: {e}")
        
        # Generate synthetic data if file doesn't exist
        print("Training data file not found, using hardcoded data...")
        return self.load_hardcoded_training_data()
    
    def load_hardcoded_training_data(self):
        """Load comprehensive training dataset (fallback)"""
        # Comprehensive symptom-disease mapping
        training_data = [
            # Common Cold
            (['runny_nose', 'sneezing', 'sore_throat', 'mild_cough'], 'Common Cold'),
            (['nasal_congestion', 'sneezing', 'mild_headache', 'sore_throat'], 'Common Cold'),
            (['runny_nose', 'mild_cough', 'sneezing', 'low_grade_fever'], 'Common Cold'),
            
            # Influenza
            (['high_fever', 'body_aches', 'fatigue', 'headache', 'chills'], 'Influenza'),
            (['sudden_fever', 'muscle_pain', 'severe_fatigue', 'dry_cough'], 'Influenza'),
            (['fever', 'headache', 'body_aches', 'weakness', 'sore_throat'], 'Influenza'),
            
            # Pneumonia
            (['chest_pain', 'difficulty_breathing', 'productive_cough', 'fever', 'chills'], 'Pneumonia'),
            (['shortness_of_breath', 'chest_pain', 'cough_with_phlegm', 'high_fever'], 'Pneumonia'),
            (['breathing_difficulty', 'chest_tightness', 'fever', 'fatigue', 'cough'], 'Pneumonia'),
            
            # Diabetes Type 2
            (['excessive_thirst', 'frequent_urination', 'unexplained_weight_loss', 'fatigue'], 'Diabetes Type 2'),
            (['increased_hunger', 'blurred_vision', 'slow_healing_wounds', 'frequent_infections'], 'Diabetes Type 2'),
            (['excessive_thirst', 'frequent_urination', 'fatigue', 'blurred_vision'], 'Diabetes Type 2'),
            
            # Hypertension
            (['headache', 'dizziness', 'chest_pain', 'shortness_of_breath'], 'Hypertension'),
            (['severe_headache', 'fatigue', 'vision_problems', 'chest_pain'], 'Hypertension'),
            (['headache', 'dizziness', 'nausea', 'blurred_vision'], 'Hypertension'),
            
            # Migraine
            (['severe_headache', 'nausea', 'sensitivity_to_light', 'vomiting'], 'Migraine'),
            (['throbbing_headache', 'visual_disturbances', 'nausea', 'sensitivity_to_sound'], 'Migraine'),
            (['intense_headache', 'nausea', 'light_sensitivity', 'sound_sensitivity'], 'Migraine'),
            
            # Gastroenteritis
            (['nausea', 'vomiting', 'diarrhea', 'abdominal_cramps'], 'Gastroenteritis'),
            (['stomach_pain', 'diarrhea', 'nausea', 'low_grade_fever'], 'Gastroenteritis'),
            (['vomiting', 'diarrhea', 'abdominal_pain', 'dehydration'], 'Gastroenteritis'),
            
            # Asthma
            (['wheezing', 'shortness_of_breath', 'chest_tightness', 'cough'], 'Asthma'),
            (['difficulty_breathing', 'wheezing', 'chest_pain', 'cough_at_night'], 'Asthma'),
            (['breathing_difficulty', 'wheezing', 'chest_tightness', 'exercise_intolerance'], 'Asthma'),
            
            # Depression
            (['persistent_sadness', 'loss_of_interest', 'fatigue', 'sleep_disturbances'], 'Depression'),
            (['hopelessness', 'appetite_changes', 'concentration_problems', 'fatigue'], 'Depression'),
            (['mood_changes', 'loss_of_energy', 'sleep_problems', 'feelings_of_worthlessness'], 'Depression'),
            
            # Anxiety Disorder
            (['excessive_worry', 'restlessness', 'fatigue', 'difficulty_concentrating'], 'Anxiety Disorder'),
            (['panic_attacks', 'rapid_heartbeat', 'sweating', 'trembling'], 'Anxiety Disorder'),
            (['nervousness', 'restlessness', 'rapid_heartbeat', 'sleep_problems'], 'Anxiety Disorder'),
        ]
        
        # Create expanded dataset with variations
        expanded_data = []
        for symptoms, disease in training_data:
            expanded_data.append((symptoms, disease))
            
            # Add variations with subset of symptoms
            if len(symptoms) > 2:
                for i in range(len(symptoms)):
                    subset = symptoms[:i] + symptoms[i+1:]
                    if len(subset) >= 2:
                        expanded_data.append((subset, disease))
        
        return expanded_data
    
    def prepare_features(self, training_data):
        """Prepare feature matrix from training data"""
        if isinstance(training_data, pd.DataFrame):
            # Handle DataFrame input (from CSV)
            # Separate features and target
            feature_columns = [col for col in training_data.columns 
                             if col not in ['disease', 'severity', 'category']]
            
            X = training_data[feature_columns].values
            y = training_data['disease'].values
            
            # Create symptom encoder from column names
            self.symptom_encoder = {symptom: i for i, symptom in enumerate(feature_columns)}
            
            return X, y
        else:
            # Handle list input (hardcoded data)
            all_symptoms = set()
            for symptoms, _ in training_data:
                all_symptoms.update(symptoms)
            
            all_symptoms = sorted(list(all_symptoms))
            self.symptom_encoder = {symptom: i for i, symptom in enumerate(all_symptoms)}
            
            X = []
            y = []
            
            for symptoms, disease in training_data:
                feature_vector = [0] * len(all_symptoms)
                for symptom in symptoms:
                    if symptom in self.symptom_encoder:
                        feature_vector[self.symptom_encoder[symptom]] = 1
                X.append(feature_vector)
                y.append(disease)
            
            return np.array(X), np.array(y)
    
    def train_initial_model(self):
        """Train the initial disease prediction models"""
        print("Training initial disease prediction models...")
        
        # Load training data
        training_data = self.load_training_data()
        X, y = self.prepare_features(training_data)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Apply SMOTE for balanced dataset
        smote = SMOTE(random_state=42)
        X_balanced, y_balanced = smote.fit_resample(X, y_encoded)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_balanced)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced
        )
        
        # Train multiple models
        models_config = {
            'random_forest': RandomForestClassifier(
                n_estimators=200, 
                max_depth=10, 
                random_state=42,
                class_weight='balanced'
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=150, 
                learning_rate=0.1, 
                max_depth=6, 
                random_state=42
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=42,
                eval_metric='mlogloss'
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=42,
                verbose=-1
            ),
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42
            )
        }
        
        best_model = None
        best_score = 0
        
        for name, model in models_config.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            avg_score = cv_scores.mean()
            
            print(f"{name} CV Score: {avg_score:.4f}")
            
            self.models[name] = model
            
            if avg_score > best_score:
                best_score = avg_score
                best_model = name
        
        print(f"Best model: {best_model} with score: {best_score:.4f}")
        
        # Save models
        self.save_models()
        
        return best_model, best_score
    
    def predict(self, symptoms):
        """Predict disease based on symptoms"""
        if not self.models:
            raise Exception("Models not trained. Please train the model first.")
        
        # Prepare feature vector
        feature_vector = [0] * len(self.symptom_encoder)
        for symptom in symptoms:
            if symptom in self.symptom_encoder:
                feature_vector[self.symptom_encoder[symptom]] = 1
        
        feature_vector = np.array(feature_vector).reshape(1, -1)
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Get predictions from all models
        predictions = {}
        probabilities = {}
        
        for name, model in self.models.items():
            try:
                pred = model.predict(feature_vector_scaled)[0]
                pred_proba = model.predict_proba(feature_vector_scaled)[0]
                
                disease = self.label_encoder.inverse_transform([pred])[0]
                confidence = max(pred_proba)
                
                predictions[name] = disease
                probabilities[name] = confidence
            except Exception as e:
                print(f"Error with model {name}: {e}")
                continue
        
        # Ensemble prediction (majority voting with confidence weighting)
        disease_votes = {}
        confidence_sum = {}
        
        for name, disease in predictions.items():
            confidence = probabilities[name]
            if disease not in disease_votes:
                disease_votes[disease] = 0
                confidence_sum[disease] = 0
            disease_votes[disease] += confidence
            confidence_sum[disease] += confidence
        
        # Get final prediction
        if disease_votes:
            final_disease = max(disease_votes.items(), key=lambda x: x[1])[0]
            final_confidence = confidence_sum[final_disease] / len([d for d in predictions.values() if d == final_disease])
        else:
            final_disease = "Unknown"
            final_confidence = 0.0
        
        # Get alternative diagnoses
        sorted_diseases = sorted(disease_votes.items(), key=lambda x: x[1], reverse=True)
        alternatives = [
            {'disease': str(disease), 'probability': float(conf/len(predictions))} 
            for disease, conf in sorted_diseases[1:4]
        ]
        
        # Get disease information
        disease_info = self.disease_info.get(final_disease, {
            'severity': 'Unknown',
            'recommendations': ['Consult a healthcare professional for proper diagnosis'],
            'typical_duration': 'Variable'
        })
        
        return {
            'disease': str(final_disease),
            'confidence': float(round(final_confidence, 3)),
            'severity': str(disease_info['severity']),
            'recommendations': [str(rec) for rec in disease_info['recommendations']],
            'alternatives': alternatives,
            'model_predictions': {str(k): str(v) for k, v in predictions.items()},
            'individual_confidences': {str(k): float(v) for k, v in probabilities.items()}
        }
    
    def retrain_with_feedback(self):
        """Retrain models with feedback data"""
        print("Retraining models with feedback data...")
        
        # Load feedback data from database
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT symptoms, actual_diagnosis, feedback 
            FROM predictions 
            WHERE actual_diagnosis IS NOT NULL AND feedback >= 4
        ''')
        
        feedback_data = cursor.fetchall()
        conn.close()
        
        if not feedback_data:
            print("No feedback data available for retraining.")
            return
        
        # Prepare feedback training data
        feedback_training = []
        for symptoms_json, actual_diagnosis, feedback in feedback_data:
            symptoms = json.loads(symptoms_json)
            feedback_training.append((symptoms, actual_diagnosis))
        
        # Combine with original training data
        original_data = self.load_training_data()
        combined_data = original_data + feedback_training
        
        # Retrain models
        X, y = self.prepare_features(combined_data)
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Apply SMOTE
        smote = SMOTE(random_state=42)
        X_balanced, y_balanced = smote.fit_resample(X, y_encoded)
        X_scaled = self.scaler.fit_transform(X_balanced)
        
        # Retrain all models
        for name, model in self.models.items():
            print(f"Retraining {name}...")
            model.fit(X_scaled, y_balanced)
        
        # Save updated models
        self.save_models()
        print("Models retrained successfully!")
    
    def save_models(self):
        """Save trained models"""
        if not os.path.exists('models'):
            os.makedirs('models')
        
        # Save models
        for name, model in self.models.items():
            joblib.dump(model, f'models/{name}_model.pkl')
        
        # Save encoders and scalers
        joblib.dump(self.label_encoder, 'models/label_encoder.pkl')
        joblib.dump(self.scaler, 'models/scaler.pkl')
        joblib.dump(self.symptom_encoder, 'models/symptom_encoder.pkl')
        
        print("Models saved successfully!")
    
    def load_models(self):
        """Load trained models"""
        try:
            if os.path.exists('models/label_encoder.pkl'):
                self.label_encoder = joblib.load('models/label_encoder.pkl')
                self.scaler = joblib.load('models/scaler.pkl')
                self.symptom_encoder = joblib.load('models/symptom_encoder.pkl')
                
                # Load all models
                model_files = [
                    'random_forest_model.pkl',
                    'gradient_boosting_model.pkl',
                    'xgboost_model.pkl',
                    'lightgbm_model.pkl',
                    'neural_network_model.pkl'
                ]
                
                for model_file in model_files:
                    model_path = f'models/{model_file}'
                    if os.path.exists(model_path):
                        model_name = model_file.replace('_model.pkl', '')
                        self.models[model_name] = joblib.load(model_path)
                
                print(f"Loaded {len(self.models)} models successfully!")
            else:
                print("No saved models found. Training initial models...")
                self.train_initial_model()
                
        except Exception as e:
            print(f"Error loading models: {e}")
            print("Training new models...")
            self.train_initial_model()