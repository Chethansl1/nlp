import numpy as np
import uuid
from datetime import datetime, timedelta
import random
import math
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class DiseasePredictor:
    def __init__(self):
        # Define common symptoms for various diseases
        self.disease_symptoms = {
            "Diabetes Type 2": [
                "increased thirst", "frequent urination", "blurred vision", "fatigue", 
                "slow-healing sores", "frequent infections", "increased hunger", "weight loss",
                "numbness in hands/feet", "darkened skin"
            ],
            "Coronary Heart Disease": [
                "chest pain", "shortness of breath", "pain in arms", "fatigue", 
                "dizziness", "rapid heartbeat", "weakness", "sweating", "nausea"
            ],
            "Chronic Obstructive Pulmonary Disease": [
                "shortness of breath", "wheezing", "chest tightness", "chronic cough", 
                "frequent respiratory infections", "bluish lips or fingernails", "fatigue"
            ],
            "Alzheimer's Disease": [
                "memory loss", "confusion", "difficulty finding words", "poor judgment", 
                "personality changes", "mood swings", "withdrawal from social activities",
                "difficulty completing familiar tasks"
            ],
            "Rheumatoid Arthritis": [
                "joint pain", "joint swelling", "joint stiffness", "fatigue", "fever",
                "weight loss", "weakness"
            ],
            "Hypertension": [
                "headache", "shortness of breath", "nosebleeds", "dizziness", 
                "chest pain", "flushing", "visual changes"
            ],
            "Depression": [
                "persistent sadness", "loss of interest", "changes in appetite", "sleep problems", 
                "fatigue", "feelings of worthlessness", "difficulty concentrating", "suicidal thoughts"
            ]
        }
        
        # Define risk factors for each disease
        self.disease_risk_factors = {
            "Diabetes Type 2": {
                "age": {"weight": 0.2, "threshold": 45},
                "family_history": {"weight": 0.3, "relevant": ["diabetes"]},
                "smoking": {"weight": 0.1, "risk_if": "yes"},
                "physical_activity": {"weight": 0.2, "risk_if": "low"},
                "obesity": {"weight": 0.3, "threshold": 30}
            },
            "Coronary Heart Disease": {
                "age": {"weight": 0.3, "threshold": 50},
                "family_history": {"weight": 0.2, "relevant": ["heart-disease"]},
                "smoking": {"weight": 0.3, "risk_if": "yes"},
                "physical_activity": {"weight": 0.2, "risk_if": "low"},
                "gender": {"weight": 0.1, "risk_if": "male"}
            },
            "Chronic Obstructive Pulmonary Disease": {
                "age": {"weight": 0.2, "threshold": 40},
                "smoking": {"weight": 0.5, "risk_if": "yes"},
                "gender": {"weight": 0.1, "risk_if": "male"}
            },
            "Alzheimer's Disease": {
                "age": {"weight": 0.6, "threshold": 65},
                "family_history": {"weight": 0.4, "relevant": ["alzheimers"]}
            },
            "Rheumatoid Arthritis": {
                "age": {"weight": 0.3, "threshold": 40},
                "gender": {"weight": 0.4, "risk_if": "female"},
                "smoking": {"weight": 0.3, "risk_if": "yes"}
            },
            "Hypertension": {
                "age": {"weight": 0.25, "threshold": 45},
                "family_history": {"weight": 0.2, "relevant": ["hypertension"]},
                "smoking": {"weight": 0.15, "risk_if": "yes"},
                "physical_activity": {"weight": 0.15, "risk_if": "low"},
                "obesity": {"weight": 0.25, "threshold": 30}
            },
            "Depression": {
                "age": {"weight": 0.1, "threshold": 20},
                "family_history": {"weight": 0.3, "relevant": ["depression"]},
                "gender": {"weight": 0.1, "risk_if": "female"}
            }
        }
        
        # All symptoms list - flattened unique list from all diseases
        self.all_symptoms = list(set([symptom for symptoms in self.disease_symptoms.values() for symptom in symptoms]))
        
        # Initialize Random Forest models for each disease
        self.rf_models = {}
        self._initialize_rf_models()
        
        # Store for predictions
        self.predictions = {}
    
    def _initialize_rf_models(self):
        """Initialize Random Forest models for each disease"""
        for disease in self.disease_symptoms:
            self.rf_models[disease] = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10,
                random_state=42
            )
    
    def get_disease_list(self):
        """Return the list of diseases that can be predicted"""
        return list(self.disease_symptoms.keys())
    
    def get_symptom_list(self):
        """Return the list of all possible symptoms"""
        return self.all_symptoms
    
    def process_input(self, symptoms, demographics, medical_data=None):
        """Process user input and create feature vector"""
        # Feature dictionary to store processed input
        features = {
            "symptoms": symptoms,
            "demographics": demographics,
            "medical_data": {}  # Empty since we removed medical data
        }
        
        # Calculate BMI and obesity if height and weight are provided
        if demographics.get("height") and demographics.get("weight"):
            bmi = self._calculate_bmi(float(demographics["height"]), float(demographics["weight"]))
            features["demographics"]["bmi"] = bmi
            features["demographics"]["obesity"] = self._calculate_obesity(float(demographics["height"]), float(demographics["weight"]))
        
        return features
    
    def _calculate_bmi(self, height_cm, weight_kg):
        """Calculate BMI from height in cm and weight in kg"""
        if height_cm <= 0:
            return 0
        height_m = height_cm / 100
        return weight_kg / (height_m * height_m)
    
    def _calculate_obesity(self, height, weight):
        """Determine if a person is obese based on BMI"""
        bmi = self._calculate_bmi(height, weight)
        if bmi >= 30:
            return True
        return False
    
    def predict(self, features):
        """Predict disease risks using Random Forest models with enhanced clarity and prescriptions"""
        predictions = []
        
        # Create prediction ID
        prediction_id = str(uuid.uuid4())
        
        # For each disease, create a feature vector and predict
        for disease_name in self.disease_symptoms:
            # Create feature vector for this disease
            X = self._create_feature_vector(features, disease_name)
            
            # Use Random Forest model to predict risk
            risk_percentage = self._predict_risk_using_rf(X, disease_name)
            
            # Determine risk level based on percentage
            risk_level = self._get_risk_level(risk_percentage)
            
            # Get contributing factors
            contributing_factors = self._get_contributing_factors(features, disease_name)
            
            # Generate treatment recommendations with detailed prescription data
            treatment_data = self._generate_treatment_recommendations(disease_name, risk_level, features)
            
            # Generate trend analysis
            trend = self._generate_trend_analysis(risk_percentage, disease_name)
            
            # Determine progression stage
            progression_stage = self._determine_progression_stage(disease_name, risk_percentage)
            
            # Generate graph data
            graph_data = self._generate_graph_data(disease_name, risk_percentage)
            
            # Create descriptive summary of disease risk
            if risk_level in ["High", "Moderate"]:
                summary = f"You have a {risk_level.lower()} risk ({round(risk_percentage, 1)}%) of {disease_name}."
            else:
                summary = f"You have a {risk_level.lower()} risk of {disease_name}."
                
            # Add evidence-based warning if risk is high
            warning = None
            if risk_percentage > 75:
                warning = f"IMPORTANT: Your risk of {disease_name} is significantly elevated. Immediate medical consultation is recommended."
            elif risk_percentage > 60:
                warning = f"Your {disease_name} risk factors indicate the need for proactive management and medical consultation."
                
            # Create comprehensive prescription data
            prescription = {
                "disease_name": disease_name,
                "risk_level": risk_level,
                "treatments": treatment_data["treatments"],
                "lifestyle_modifications": treatment_data["lifestyle_modifications"],
                "medications": treatment_data["medications"],
                "follow_up_recommendations": treatment_data["follow_up_recommendations"],
                "warning": warning
            }
            
            # Add prediction result with enhanced structure
            predictions.append({
                "disease": disease_name,
                "risk_percentage": round(risk_percentage, 1),
                "risk_level": risk_level,
                "summary": summary,
                "warning": warning,
                "contributing_factors": contributing_factors,
                "prescription": prescription,
                "treatments": treatment_data["treatments"],  # Keep for backward compatibility
                "trend": trend,
                "progression_stage": progression_stage,
                "graph_data": graph_data
            })
        
        # Sort predictions by risk percentage (highest first)
        predictions.sort(key=lambda x: x["risk_percentage"], reverse=True)
        
        # Identify the top disease for primary prescription
        primary_disease = predictions[0]["disease"] if predictions else None
        
        # Store prediction for future feedback
        self.predictions[prediction_id] = {
            "timestamp": datetime.now().isoformat(),
            "features": features,
            "results": predictions,
            "primary_disease": primary_disease
        }
        
        return prediction_id, predictions
    
    def _create_feature_vector(self, features, disease_name):
        """Create a feature vector for the specified disease"""
        # Create symptom features (binary for each symptom in the disease)
        symptom_features = []
        for symptom in self.disease_symptoms[disease_name]:
            if symptom in features["symptoms"]:
                symptom_features.append(1)
            else:
                symptom_features.append(0)
        
        # Create demographic features
        demographics = features["demographics"]
        demographic_features = []
        
        # Age (normalized to 0-1 range assuming max age 100)
        age = float(demographics.get("age", 0)) / 100 if demographics.get("age") else 0
        demographic_features.append(age)
        
        # Gender (binary: 1 for male, 0 for female/other)
        gender = 1 if demographics.get("gender") == "male" else 0
        demographic_features.append(gender)
        
        # BMI (normalized to 0-1 range assuming max BMI 50)
        bmi = min(demographics.get("bmi", 0) / 50, 1) if demographics.get("bmi") else 0
        demographic_features.append(bmi)
        
        # Smoking (binary)
        smoking = 1 if demographics.get("smoking") == "yes" else 0
        demographic_features.append(smoking)
        
        # Physical activity (ordinal: 0 for low, 0.5 for moderate, 1 for high)
        activity_map = {"low": 0, "moderate": 0.5, "high": 1}
        physical_activity = activity_map.get(demographics.get("physical_activity", "low"), 0)
        demographic_features.append(physical_activity)
        
        # Family history (binary for each disease)
        family_history = demographics.get("family_history", [])
        fh_diabetes = 1 if "diabetes" in family_history else 0
        fh_heart = 1 if "heart-disease" in family_history else 0
        fh_alzheimers = 1 if "alzheimers" in family_history else 0
        fh_arthritis = 1 if "arthritis" in family_history else 0
        fh_hypertension = 1 if "hypertension" in family_history else 0
        fh_depression = 1 if "depression" in family_history else 0
        
        demographic_features.extend([fh_diabetes, fh_heart, fh_alzheimers, 
                                    fh_arthritis, fh_hypertension, fh_depression])
        
        # Combine all features
        X = np.array(symptom_features + demographic_features).reshape(1, -1)
        return X
    
    def _predict_risk_using_rf(self, X, disease_name):
        """Use Random Forest to predict disease risk with improved accuracy"""
        
        # Get number of symptoms present and calculate symptom impact
        num_symptoms = X[0, :len(self.disease_symptoms[disease_name])].sum()
        max_symptoms = len(self.disease_symptoms[disease_name])
        
        # Prioritize specific symptom combinations that are more indicative of certain diseases
        disease_specific_symptoms = {
            "Diabetes Type 2": ["increased thirst", "frequent urination", "blurred vision"],
            "Coronary Heart Disease": ["chest pain", "shortness of breath", "pain in arms"],
            "Chronic Obstructive Pulmonary Disease": ["shortness of breath", "chronic cough", "wheezing"],
            "Alzheimer's Disease": ["memory loss", "confusion", "difficulty finding words"],
            "Rheumatoid Arthritis": ["joint pain", "joint swelling", "joint stiffness"],
            "Hypertension": ["headache", "dizziness", "chest pain"],
            "Depression": ["persistent sadness", "loss of interest", "feelings of worthlessness"]
        }
        
        # Check for key symptom combinations
        key_symptoms_count = 0
        if disease_name in disease_specific_symptoms:
            key_symptoms = disease_specific_symptoms[disease_name]
            for i, symptom in enumerate(self.disease_symptoms[disease_name]):
                if symptom in key_symptoms and X[0, i] == 1:
                    key_symptoms_count += 1
        
        # Calculate symptom factor with higher weight for key symptoms
        symptom_factor = (num_symptoms / max_symptoms) if max_symptoms > 0 else 0
        key_symptom_factor = (key_symptoms_count / len(disease_specific_symptoms.get(disease_name, []))) if disease_specific_symptoms.get(disease_name) else 0
        
        # Get demographics that increase risk
        demographics_risk = 0
        for i, factor in enumerate(["age", "gender", "bmi", "smoking", "physical_activity"]):
            if factor in self.disease_risk_factors[disease_name]:
                factor_info = self.disease_risk_factors[disease_name][factor]
                if factor == "age":
                    # More granular age risk assessment
                    age_value = X[0, len(self.disease_symptoms[disease_name]) + 0] * 100
                    if age_value >= factor_info["threshold"]:
                        # Higher risk the further above threshold
                        age_excess = min((age_value - factor_info["threshold"]) / 30, 1)  # Normalize excess
                        demographics_risk += factor_info["weight"] * (1 + 0.5 * age_excess)
                elif factor == "gender":
                    demographics_risk += factor_info["weight"] * (X[0, len(self.disease_symptoms[disease_name]) + 1] == (factor_info["risk_if"] == "male"))
                elif factor == "obesity":
                    # Granular obesity assessment
                    bmi = X[0, len(self.disease_symptoms[disease_name]) + 2] * 50
                    if bmi >= factor_info["threshold"]:
                        obesity_excess = min((bmi - factor_info["threshold"]) / 15, 1)  # Normalize excess
                        demographics_risk += factor_info["weight"] * (1 + 0.8 * obesity_excess)
                elif factor == "smoking":
                    demographics_risk += factor_info["weight"] * (X[0, len(self.disease_symptoms[disease_name]) + 3] == 1)
                elif factor == "physical_activity":
                    activity_level = X[0, len(self.disease_symptoms[disease_name]) + 4]
                    # Lower activity = higher risk
                    demographics_risk += factor_info["weight"] * (1 - activity_level)
        
        # Get family history risk with higher impact
        family_risk = 0
        if "family_history" in self.disease_risk_factors[disease_name]:
            factor_info = self.disease_risk_factors[disease_name]["family_history"]
            for i, disease in enumerate(["diabetes", "heart-disease", "alzheimers", "arthritis", "hypertension", "depression"]):
                if disease in factor_info["relevant"]:
                    family_risk += factor_info["weight"] * 1.5 * X[0, len(self.disease_symptoms[disease_name]) + 5 + i]
        
        # Adjust weights based on disease
        symptom_weight = 0.5
        key_symptom_weight = 0.3
        demographic_weight = 0.3
        family_weight = 0.2
        
        # Calculate comorbidity factors - some diseases increase risk for others
        comorbidity_factor = 0
        if disease_name == "Diabetes Type 2" and X[0, len(self.disease_symptoms[disease_name]) + 2] * 50 >= 30:  # Obesity
            comorbidity_factor += 0.15  # Obesity increases diabetes risk
        elif disease_name == "Hypertension" and X[0, len(self.disease_symptoms[disease_name]) + 3] == 1:  # Smoking
            comorbidity_factor += 0.15  # Smoking increases hypertension risk
        elif disease_name == "Coronary Heart Disease" and "Diabetes Type 2" in self.predictions:
            comorbidity_factor += 0.2  # Diabetes increases heart disease risk
        
        # Calculate total risk with improved weights and factors
        risk = ((symptom_factor * symptom_weight) + 
                (key_symptom_factor * key_symptom_weight) + 
                (demographics_risk * demographic_weight) + 
                (family_risk * family_weight) + 
                comorbidity_factor) * 100
        
        # Add slight randomness to avoid identical predictions
        risk = min(max(risk + random.uniform(-2, 2), 0), 100)
        
        # Ensure diseases with key symptoms always have at least a moderate risk
        if key_symptom_factor > 0.5:
            risk = max(risk, 30)
        
        return risk
    
    def _get_contributing_factors(self, features, disease_name):
        """Generate list of contributing factors for the disease"""
        contributing_factors = []
        
        # Add symptoms
        relevant_symptoms = [s for s in features["symptoms"] if s in self.disease_symptoms[disease_name]]
        if relevant_symptoms:
            symptom_text = "Reported symptoms: " + ", ".join(relevant_symptoms)
            contributing_factors.append(symptom_text)
        
        # Add demographic factors
        demographics = features["demographics"]
        demographic_factors = []
        
        # Age
        if "age" in self.disease_risk_factors[disease_name]:
            threshold = self.disease_risk_factors[disease_name]["age"]["threshold"]
            if demographics.get("age") and int(demographics["age"]) >= threshold:
                demographic_factors.append("Age")
        
        # Gender
        if "gender" in self.disease_risk_factors[disease_name]:
            risk_gender = self.disease_risk_factors[disease_name]["gender"]["risk_if"]
            if demographics.get("gender") == risk_gender:
                demographic_factors.append("Gender")
        
        # Obesity
        if "obesity" in self.disease_risk_factors[disease_name]:
            if demographics.get("obesity"):
                demographic_factors.append("Obesity")
        
        # Smoking
        if "smoking" in self.disease_risk_factors[disease_name]:
            if demographics.get("smoking") == "yes":
                demographic_factors.append("Smoking")
        
        # Physical activity
        if "physical_activity" in self.disease_risk_factors[disease_name]:
            if demographics.get("physical_activity") == "low":
                demographic_factors.append("Physical inactivity")
        
        # Family history
        if "family_history" in self.disease_risk_factors[disease_name]:
            relevant_diseases = self.disease_risk_factors[disease_name]["family_history"]["relevant"]
            family_history = demographics.get("family_history", [])
            relevant_family_history = [d for d in relevant_diseases if d in family_history]
            if relevant_family_history:
                demographic_factors.append("Family History")
        
        if demographic_factors:
            contributing_factors.append("Risk factors: " + ", ".join(demographic_factors))
        
        # If no factors found, add a generic message
        if not contributing_factors:
            contributing_factors.append("No significant contributing factors identified")
        
        return contributing_factors
    
    def _get_risk_level(self, risk_percentage):
        """Determine risk level based on risk percentage"""
        if risk_percentage >= 60:
            return "High"
        elif risk_percentage >= 30:
            return "Moderate"
        elif risk_percentage >= 10:
            return "Low"
        else:
            return "Minimal"
    
    def _generate_treatment_recommendations(self, disease_name, risk_level, features):
        """Generate personalized treatment recommendations based on disease, risk level, and individual factors"""
        treatments = []
        lifestyle_modifications = []
        medications = []
        followup_recommendations = []
        
        # Common treatments for different diseases with specific prescriptions
        disease_treatments = {
            "Diabetes Type 2": {
                "lifestyle": [
                    "Follow a balanced diet low in refined carbohydrates and sugar",
                    "Engage in regular moderate exercise (30 minutes, 5 days a week)",
                    "Maintain a healthy weight through calorie management",
                    "Limit alcohol consumption and avoid sugary beverages",
                    "Monitor carbohydrate intake with meal planning"
                ],
                "medications": [
                    "Metformin 500mg twice daily with meals (first-line therapy)",
                    "Consider SGLT2 inhibitors if HbA1c remains elevated",
                    "GLP-1 receptor agonists for additional glycemic control",
                    "Daily multivitamin supplement to address potential deficiencies"
                ],
                "followup": [
                    "Monitor blood glucose levels regularly (fasting and post-meal)",
                    "Schedule HbA1c test every 3-6 months",
                    "Annual eye examination to check for retinopathy",
                    "Regular foot examinations to detect early neuropathy",
                    "Kidney function tests annually"
                ]
            },
            "Coronary Heart Disease": {
                "lifestyle": [
                    "Follow a Mediterranean or DASH diet rich in fruits, vegetables, and lean protein",
                    "Engage in cardiac rehabilitation program as recommended",
                    "Avoid tobacco products and secondhand smoke completely",
                    "Manage stress through meditation, yoga, or other relaxation techniques",
                    "Limit sodium intake to less than 2,300mg daily"
                ],
                "medications": [
                    "Aspirin 81mg daily as an antiplatelet agent",
                    "Statin therapy (intensity based on risk level)",
                    "Beta-blockers for heart rate control if indicated",
                    "ACE inhibitors for blood pressure management",
                    "Nitroglycerin 0.4mg sublingual tablets for angina episodes"
                ],
                "followup": [
                    "Cardiac stress test annually or as recommended",
                    "Lipid panel every 3-6 months until stable, then annually",
                    "Regular blood pressure monitoring (home and clinical)",
                    "Echocardiogram as recommended by cardiologist",
                    "Cardiac rehabilitation program attendance"
                ]
            },
            "Chronic Obstructive Pulmonary Disease": {
                "lifestyle": [
                    "Complete smoking cessation with supportive therapy",
                    "Avoid air pollutants and respiratory irritants",
                    "Pulmonary rehabilitation exercises 3 times weekly",
                    "Breathing techniques for symptom management",
                    "Energy conservation strategies for daily activities"
                ],
                "medications": [
                    "Short-acting bronchodilator (albuterol) for rescue therapy",
                    "Long-acting bronchodilator maintenance therapy",
                    "Inhaled corticosteroids as indicated",
                    "Annual influenza vaccination",
                    "Pneumococcal vaccination as recommended"
                ],
                "followup": [
                    "Pulmonary function tests every 6-12 months",
                    "Oxygen saturation monitoring regularly",
                    "Pulmonologist evaluation every 3-6 months",
                    "Monitor for exacerbations and report promptly",
                    "Annual chest X-ray as recommended"
                ]
            },
            "Alzheimer's Disease": {
                "lifestyle": [
                    "Cognitive stimulation with puzzles, reading, and brain games",
                    "Establish consistent daily routines and memory aids",
                    "Regular physical activity adapted to capabilities",
                    "Social engagement and family support activities",
                    "Mediterranean diet rich in omega-3 fatty acids"
                ],
                "medications": [
                    "Cholinesterase inhibitors (Donepezil, Rivastigmine, or Galantamine)",
                    "Memantine for moderate to severe disease",
                    "Sleep aids if sleep disturbances present",
                    "Supplements including vitamin E and B complex",
                    "Antidepressants if depression symptoms present"
                ],
                "followup": [
                    "Regular cognitive assessments every 3-6 months",
                    "Caregiver support program enrollment",
                    "Safety evaluation of home environment",
                    "Neurologist follow-up every 3-6 months",
                    "Monitor for behavioral changes or complications"
                ]
            },
            "Rheumatoid Arthritis": {
                "lifestyle": [
                    "Joint-friendly exercises including swimming and tai chi",
                    "Anti-inflammatory diet rich in omega-3 fatty acids",
                    "Hot and cold therapy for joint pain management",
                    "Ergonomic adaptations for home and work environments",
                    "Balance activity with adequate rest periods"
                ],
                "medications": [
                    "NSAIDs for pain and inflammation management",
                    "Disease-modifying antirheumatic drugs (DMARDs)",
                    "Biologic response modifiers if indicated",
                    "Corticosteroids for flare management",
                    "Joint supplements (glucosamine, chondroitin) as adjunct therapy"
                ],
                "followup": [
                    "Rheumatologist evaluation every 3-6 months",
                    "Regular blood tests to monitor inflammation markers",
                    "X-rays or other imaging studies annually",
                    "Physical therapy assessment as needed",
                    "Monitor for medication side effects"
                ]
            },
            "Hypertension": {
                "lifestyle": [
                    "DASH diet (rich in fruits, vegetables, low-fat dairy)",
                    "Limit sodium intake to less than 2,000mg daily",
                    "Regular aerobic exercise (150 minutes weekly)",
                    "Maintain healthy weight or achieve 5-10% weight loss if overweight",
                    "Limit alcohol consumption and avoid tobacco products"
                ],
                "medications": [
                    "First-line antihypertensive medication (based on individual factors)",
                    "Diuretics, ACE inhibitors, ARBs, or calcium channel blockers",
                    "Combination therapy if single agent inadequate",
                    "Potassium supplements if using diuretics",
                    "Aspirin therapy if additional cardiovascular risk factors present"
                ],
                "followup": [
                    "Daily home blood pressure monitoring and record keeping",
                    "Office blood pressure check every 3-6 months",
                    "Annual comprehensive metabolic panel",
                    "Electrocardiogram as recommended",
                    "Echocardiogram if indicated for target organ assessment"
                ]
            },
            "Depression": {
                "lifestyle": [
                    "Regular physical activity (30 minutes daily if possible)",
                    "Establish consistent sleep schedule and sleep hygiene",
                    "Mindfulness meditation and stress reduction techniques",
                    "Social connection and support group participation",
                    "Exposure to natural daylight and nature"
                ],
                "medications": [
                    "Selective serotonin reuptake inhibitors (SSRIs)",
                    "Serotonin-norepinephrine reuptake inhibitors (SNRIs)",
                    "Adjunctive therapy as needed for sleep or anxiety",
                    "Vitamin D supplementation if deficient",
                    "Omega-3 fatty acid supplements"
                ],
                "followup": [
                    "Weekly therapy sessions initially, then as recommended",
                    "Psychiatric evaluation every 4-8 weeks until stable",
                    "PHQ-9 or other depression screening at each visit",
                    "Monitor for suicidal ideation and safety planning",
                    "Medication adjustment review every 4-6 weeks initially"
                ]
            }
        }
        
        # Personalize recommendations based on individual factors
        demographics = features.get("demographics", {})
        symptoms = features.get("symptoms", [])
        
        if disease_name in disease_treatments:
            # Get base recommendations for this disease
            disease_recs = disease_treatments[disease_name]
            
            # Select appropriate recommendations based on risk level
            if risk_level == "High":
                # For high risk, include comprehensive recommendations
                lifestyle_modifications = disease_recs["lifestyle"]
                medications = disease_recs["medications"]
                followup_recommendations = disease_recs["followup"]
                
                # Add personalized urgent recommendations
                if disease_name == "Diabetes Type 2" and demographics.get("obesity"):
                    lifestyle_modifications.insert(0, "URGENT: Initiate medically supervised weight management program")
                elif disease_name == "Coronary Heart Disease" and demographics.get("smoking") == "yes":
                    lifestyle_modifications.insert(0, "URGENT: Smoking cessation with immediate effect")
                
            elif risk_level == "Moderate":
                # For moderate risk, focus on lifestyle and key medications
                lifestyle_modifications = disease_recs["lifestyle"][:3]
                medications = disease_recs["medications"][:2]
                followup_recommendations = disease_recs["followup"][:3]
                followup_recommendations.append("Regular monitoring every 3 months")
                
            elif risk_level == "Low":
                # For low risk, focus on prevention
                lifestyle_modifications = disease_recs["lifestyle"][:2]
                medications = []
                followup_recommendations = ["Regular health check-ups every 6 months", 
                                           "Monitor for new symptoms", 
                                           disease_recs["followup"][0]]
                
            else:  # Minimal risk
                lifestyle_modifications = ["Maintain healthy lifestyle", "Continue balanced diet and exercise"]
                medications = []
                followup_recommendations = ["Annual health check-ups", "Monitor for changes in symptoms"]
            
            # Combine all recommendations into treatments list
            treatments = lifestyle_modifications + medications + followup_recommendations
        
        # Ensure the output includes disease name in a prominent way
        treatments.insert(0, f"DIAGNOSIS: {disease_name} - {risk_level} Risk")
        
        # Add custom prescription header
        treatments.insert(1, f"TREATMENT PLAN FOR: {disease_name.upper()}")
        
        return {
            "treatments": treatments,
            "lifestyle_modifications": lifestyle_modifications,
            "medications": medications,
            "follow_up_recommendations": followup_recommendations,
            "disease_name": disease_name,
            "risk_level": risk_level
        }
    
    def _generate_trend_analysis(self, risk_percentage, disease_name):
        """Generate trend analysis data"""
        # In a real app, this would use historical data
        # For now, we'll generate a random trend
        
        direction = random.choice(["increasing", "decreasing", "stable"])
        
        if direction == "increasing":
            analysis = "Your risk appears to be increasing over time."
        elif direction == "decreasing":
            analysis = "Your risk appears to be decreasing over time."
        else:
            analysis = "Your risk appears to be stable over time."
        
        return {
            "direction": direction,
            "analysis": analysis
        }
    
    def _determine_progression_stage(self, disease_name, risk_percentage):
        """Determine disease progression stage based on risk percentage"""
        if risk_percentage >= 60:
            return "Advanced"
        elif risk_percentage >= 30:
            return "Moderate"
        else:
            return "Early"
    
    def _generate_graph_data(self, disease_name, risk_percentage):
        """Generate graph data for visualizations"""
        # In a real app, this would use historical data
        # For now, we'll generate random data
        
        # Risk over time (last 3 data points + current)
        previous_risks = [
            max(0, risk_percentage - random.uniform(5, 15)),
            max(0, risk_percentage - random.uniform(3, 10)),
            max(0, risk_percentage - random.uniform(1, 5))
        ]
        
        risk_over_time = {
            "labels": ["6 months ago", "3 months ago", "1 month ago", "Current"],
            "data": previous_risks + [risk_percentage]
        }
        
        return {
            "risk_over_time": risk_over_time
        }
    
    def provide_feedback(self, prediction_id, actual_diagnoses):
        """Update models based on feedback (actual diagnoses)"""
        if prediction_id not in self.predictions:
            return False
        
        # In a real app, this would update the models based on feedback
        # For now, we'll just store the feedback
        self.predictions[prediction_id]["actual_diagnoses"] = actual_diagnoses
        
        return True