"""
Training Data Generator for MedAI Disease Prediction System

This script generates a comprehensive synthetic medical dataset for training
the disease prediction models. The data is based on real medical knowledge
and symptom-disease relationships.
"""

import pandas as pd
import numpy as np
import json
import random
from collections import defaultdict
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class MedicalDataGenerator:
    def __init__(self):
        self.symptoms = self.load_symptoms()
        self.diseases = self.load_diseases()
        self.symptom_disease_patterns = self.create_symptom_disease_patterns()
        
    def load_symptoms(self):
        """Load symptom definitions"""
        symptoms_file = os.path.join(os.path.dirname(__file__), 'symptoms.json')
        if os.path.exists(symptoms_file):
            with open(symptoms_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_symptoms()
    
    def load_diseases(self):
        """Load disease definitions"""
        diseases_file = os.path.join(os.path.dirname(__file__), 'diseases.json')
        if os.path.exists(diseases_file):
            with open(diseases_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_diseases()
    
    def create_default_symptoms(self):
        """Create comprehensive symptom database"""
        symptoms = {
            "General": [
                {"name": "fever", "display_name": "Fever", "description": "Body temperature above normal"},
                {"name": "fatigue", "display_name": "Fatigue", "description": "Extreme tiredness or exhaustion"},
                {"name": "weight_loss", "display_name": "Weight Loss", "description": "Unintentional loss of body weight"},
                {"name": "weight_gain", "display_name": "Weight Gain", "description": "Unintentional increase in body weight"},
                {"name": "chills", "display_name": "Chills", "description": "Feeling cold with shivering"},
                {"name": "night_sweats", "display_name": "Night Sweats", "description": "Excessive sweating during sleep"},
                {"name": "loss_of_appetite", "display_name": "Loss of Appetite", "description": "Reduced desire to eat"},
                {"name": "malaise", "display_name": "Malaise", "description": "General feeling of discomfort or illness"},
                {"name": "weakness", "display_name": "Weakness", "description": "Lack of physical strength"},
                {"name": "dehydration", "display_name": "Dehydration", "description": "Excessive loss of body water"},
                {"name": "swollen_lymph_nodes", "display_name": "Swollen Lymph Nodes", "description": "Enlarged lymph glands"},
                {"name": "pale_skin", "display_name": "Pale Skin", "description": "Unusually light skin color"},
            ],
            "Respiratory": [
                {"name": "cough", "display_name": "Cough", "description": "Sudden expulsion of air from lungs"},
                {"name": "shortness_of_breath", "display_name": "Shortness of Breath", "description": "Difficulty breathing"},
                {"name": "chest_pain", "display_name": "Chest Pain", "description": "Pain in the chest area"},
                {"name": "wheezing", "display_name": "Wheezing", "description": "High-pitched breathing sound"},
                {"name": "sore_throat", "display_name": "Sore Throat", "description": "Pain or irritation in throat"},
                {"name": "runny_nose", "display_name": "Runny Nose", "description": "Nasal discharge"},
                {"name": "nasal_congestion", "display_name": "Nasal Congestion", "description": "Blocked nasal passages"},
                {"name": "sneezing", "display_name": "Sneezing", "description": "Sudden expulsion of air through nose"},
                {"name": "hoarse_voice", "display_name": "Hoarse Voice", "description": "Rough or harsh voice"},
                {"name": "coughing_blood", "display_name": "Coughing Blood", "description": "Blood in cough or sputum"},
                {"name": "rapid_breathing", "display_name": "Rapid Breathing", "description": "Faster than normal breathing rate"},
                {"name": "shallow_breathing", "display_name": "Shallow Breathing", "description": "Reduced depth of breathing"},
            ],
            "Gastrointestinal": [
                {"name": "nausea", "display_name": "Nausea", "description": "Feeling of sickness with urge to vomit"},
                {"name": "vomiting", "display_name": "Vomiting", "description": "Forceful expulsion of stomach contents"},
                {"name": "diarrhea", "display_name": "Diarrhea", "description": "Loose or watery bowel movements"},
                {"name": "constipation", "display_name": "Constipation", "description": "Difficulty passing stool"},
                {"name": "abdominal_pain", "display_name": "Abdominal Pain", "description": "Pain in the stomach area"},
                {"name": "bloating", "display_name": "Bloating", "description": "Feeling of fullness in abdomen"},
                {"name": "heartburn", "display_name": "Heartburn", "description": "Burning sensation in chest"},
                {"name": "loss_of_taste", "display_name": "Loss of Taste", "description": "Inability to taste food"},
                {"name": "loss_of_smell", "display_name": "Loss of Smell", "description": "Inability to smell odors"},
                {"name": "bloody_stool", "display_name": "Bloody Stool", "description": "Blood in bowel movements"},
                {"name": "black_stool", "display_name": "Black Stool", "description": "Dark, tarry bowel movements"},
                {"name": "excessive_gas", "display_name": "Excessive Gas", "description": "Increased intestinal gas"},
            ],
            "Neurological": [
                {"name": "headache", "display_name": "Headache", "description": "Pain in the head or neck"},
                {"name": "dizziness", "display_name": "Dizziness", "description": "Feeling of unsteadiness"},
                {"name": "confusion", "display_name": "Confusion", "description": "Difficulty thinking clearly"},
                {"name": "memory_loss", "display_name": "Memory Loss", "description": "Inability to remember information"},
                {"name": "seizures", "display_name": "Seizures", "description": "Sudden electrical activity in brain"},
                {"name": "numbness", "display_name": "Numbness", "description": "Loss of sensation"},
                {"name": "tingling", "display_name": "Tingling", "description": "Pins and needles sensation"},
                {"name": "vision_problems", "display_name": "Vision Problems", "description": "Difficulty seeing clearly"},
                {"name": "hearing_loss", "display_name": "Hearing Loss", "description": "Reduced ability to hear"},
                {"name": "balance_problems", "display_name": "Balance Problems", "description": "Difficulty maintaining balance"},
                {"name": "tremors", "display_name": "Tremors", "description": "Involuntary shaking"},
                {"name": "speech_problems", "display_name": "Speech Problems", "description": "Difficulty speaking clearly"},
            ],
            "Cardiovascular": [
                {"name": "palpitations", "display_name": "Palpitations", "description": "Awareness of heartbeat"},
                {"name": "irregular_heartbeat", "display_name": "Irregular Heartbeat", "description": "Abnormal heart rhythm"},
                {"name": "high_blood_pressure", "display_name": "High Blood Pressure", "description": "Elevated blood pressure"},
                {"name": "low_blood_pressure", "display_name": "Low Blood Pressure", "description": "Reduced blood pressure"},
                {"name": "swelling_legs", "display_name": "Swelling in Legs", "description": "Fluid retention in lower extremities"},
                {"name": "swelling_ankles", "display_name": "Swelling in Ankles", "description": "Fluid retention in ankles"},
                {"name": "cold_hands_feet", "display_name": "Cold Hands/Feet", "description": "Poor circulation to extremities"},
                {"name": "blue_lips", "display_name": "Blue Lips", "description": "Cyanosis of lips"},
                {"name": "fainting", "display_name": "Fainting", "description": "Brief loss of consciousness"},
                {"name": "lightheadedness", "display_name": "Lightheadedness", "description": "Feeling faint or dizzy"},
            ],
            "Musculoskeletal": [
                {"name": "joint_pain", "display_name": "Joint Pain", "description": "Pain in joints"},
                {"name": "muscle_pain", "display_name": "Muscle Pain", "description": "Pain in muscles"},
                {"name": "back_pain", "display_name": "Back Pain", "description": "Pain in the back"},
                {"name": "neck_pain", "display_name": "Neck Pain", "description": "Pain in the neck"},
                {"name": "stiffness", "display_name": "Stiffness", "description": "Reduced flexibility"},
                {"name": "swelling_joints", "display_name": "Swelling in Joints", "description": "Joint inflammation"},
                {"name": "muscle_weakness", "display_name": "Muscle Weakness", "description": "Reduced muscle strength"},
                {"name": "muscle_cramps", "display_name": "Muscle Cramps", "description": "Involuntary muscle contractions"},
                {"name": "bone_pain", "display_name": "Bone Pain", "description": "Deep aching in bones"},
                {"name": "limited_mobility", "display_name": "Limited Mobility", "description": "Reduced range of motion"},
            ],
            "Dermatological": [
                {"name": "rash", "display_name": "Rash", "description": "Skin irritation or eruption"},
                {"name": "itching", "display_name": "Itching", "description": "Desire to scratch skin"},
                {"name": "dry_skin", "display_name": "Dry Skin", "description": "Lack of moisture in skin"},
                {"name": "skin_discoloration", "display_name": "Skin Discoloration", "description": "Changes in skin color"},
                {"name": "bruising", "display_name": "Bruising", "description": "Discoloration from bleeding under skin"},
                {"name": "hair_loss", "display_name": "Hair Loss", "description": "Loss of hair from scalp or body"},
                {"name": "nail_changes", "display_name": "Nail Changes", "description": "Changes in nail appearance"},
                {"name": "skin_lesions", "display_name": "Skin Lesions", "description": "Abnormal skin growths or marks"},
                {"name": "excessive_sweating", "display_name": "Excessive Sweating", "description": "Abnormally increased sweating"},
                {"name": "skin_sensitivity", "display_name": "Skin Sensitivity", "description": "Increased skin reactivity"},
            ],
            "Genitourinary": [
                {"name": "frequent_urination", "display_name": "Frequent Urination", "description": "Increased frequency of urination"},
                {"name": "painful_urination", "display_name": "Painful Urination", "description": "Pain during urination"},
                {"name": "blood_in_urine", "display_name": "Blood in Urine", "description": "Hematuria"},
                {"name": "difficulty_urinating", "display_name": "Difficulty Urinating", "description": "Problems with urination"},
                {"name": "incontinence", "display_name": "Incontinence", "description": "Loss of bladder control"},
                {"name": "pelvic_pain", "display_name": "Pelvic Pain", "description": "Pain in pelvic region"},
                {"name": "genital_discharge", "display_name": "Genital Discharge", "description": "Abnormal genital secretions"},
                {"name": "genital_itching", "display_name": "Genital Itching", "description": "Itching in genital area"},
                {"name": "erectile_dysfunction", "display_name": "Erectile Dysfunction", "description": "Difficulty achieving erection"},
                {"name": "menstrual_irregularities", "display_name": "Menstrual Irregularities", "description": "Abnormal menstrual cycles"},
            ]
        }
        
        # Save symptoms to file
        symptoms_file = os.path.join(os.path.dirname(__file__), 'symptoms.json')
        with open(symptoms_file, 'w') as f:
            json.dump(symptoms, f, indent=2)
        
        return symptoms
    
    def create_default_diseases(self):
        """Create comprehensive disease database"""
        diseases = [
            # Infectious Diseases
            {"name": "Common Cold", "category": "Infectious", "severity": "Mild", "prevalence": 0.15},
            {"name": "Influenza", "category": "Infectious", "severity": "Moderate", "prevalence": 0.08},
            {"name": "Pneumonia", "category": "Infectious", "severity": "Severe", "prevalence": 0.03},
            {"name": "Bronchitis", "category": "Infectious", "severity": "Moderate", "prevalence": 0.05},
            {"name": "Sinusitis", "category": "Infectious", "severity": "Mild", "prevalence": 0.06},
            {"name": "Strep Throat", "category": "Infectious", "severity": "Moderate", "prevalence": 0.04},
            {"name": "Urinary Tract Infection", "category": "Infectious", "severity": "Moderate", "prevalence": 0.07},
            {"name": "Gastroenteritis", "category": "Infectious", "severity": "Moderate", "prevalence": 0.05},
            
            # Chronic Conditions
            {"name": "Diabetes Type 2", "category": "Chronic", "severity": "Moderate", "prevalence": 0.09},
            {"name": "Hypertension", "category": "Chronic", "severity": "Moderate", "prevalence": 0.12},
            {"name": "Asthma", "category": "Chronic", "severity": "Moderate", "prevalence": 0.08},
            {"name": "Arthritis", "category": "Chronic", "severity": "Moderate", "prevalence": 0.06},
            {"name": "COPD", "category": "Chronic", "severity": "Severe", "prevalence": 0.04},
            {"name": "Heart Disease", "category": "Chronic", "severity": "Severe", "prevalence": 0.05},
            {"name": "Chronic Kidney Disease", "category": "Chronic", "severity": "Severe", "prevalence": 0.03},
            
            # Acute Conditions
            {"name": "Appendicitis", "category": "Acute", "severity": "Severe", "prevalence": 0.01},
            {"name": "Heart Attack", "category": "Acute", "severity": "Severe", "prevalence": 0.01},
            {"name": "Stroke", "category": "Acute", "severity": "Severe", "prevalence": 0.01},
            {"name": "Kidney Stones", "category": "Acute", "severity": "Severe", "prevalence": 0.02},
            {"name": "Gallstones", "category": "Acute", "severity": "Moderate", "prevalence": 0.02},
            
            # Mental Health
            {"name": "Depression", "category": "Mental Health", "severity": "Moderate", "prevalence": 0.08},
            {"name": "Anxiety Disorder", "category": "Mental Health", "severity": "Moderate", "prevalence": 0.07},
            {"name": "Panic Disorder", "category": "Mental Health", "severity": "Moderate", "prevalence": 0.03},
            
            # Gastrointestinal
            {"name": "GERD", "category": "Gastrointestinal", "severity": "Mild", "prevalence": 0.06},
            {"name": "IBS", "category": "Gastrointestinal", "severity": "Mild", "prevalence": 0.05},
            {"name": "Peptic Ulcer", "category": "Gastrointestinal", "severity": "Moderate", "prevalence": 0.03},
            {"name": "Crohn's Disease", "category": "Gastrointestinal", "severity": "Severe", "prevalence": 0.01},
            
            # Neurological
            {"name": "Migraine", "category": "Neurological", "severity": "Moderate", "prevalence": 0.07},
            {"name": "Tension Headache", "category": "Neurological", "severity": "Mild", "prevalence": 0.10},
            {"name": "Epilepsy", "category": "Neurological", "severity": "Severe", "prevalence": 0.01},
            {"name": "Multiple Sclerosis", "category": "Neurological", "severity": "Severe", "prevalence": 0.001},
            
            # Dermatological
            {"name": "Eczema", "category": "Dermatological", "severity": "Mild", "prevalence": 0.04},
            {"name": "Psoriasis", "category": "Dermatological", "severity": "Moderate", "prevalence": 0.02},
            {"name": "Acne", "category": "Dermatological", "severity": "Mild", "prevalence": 0.08},
            
            # Endocrine
            {"name": "Hypothyroidism", "category": "Endocrine", "severity": "Moderate", "prevalence": 0.05},
            {"name": "Hyperthyroidism", "category": "Endocrine", "severity": "Moderate", "prevalence": 0.01},
            
            # Musculoskeletal
            {"name": "Fibromyalgia", "category": "Musculoskeletal", "severity": "Moderate", "prevalence": 0.02},
            {"name": "Osteoporosis", "category": "Musculoskeletal", "severity": "Moderate", "prevalence": 0.03},
            
            # Allergic/Immune
            {"name": "Allergic Rhinitis", "category": "Allergic", "severity": "Mild", "prevalence": 0.09},
            {"name": "Food Allergy", "category": "Allergic", "severity": "Moderate", "prevalence": 0.04},
            
            # Other
            {"name": "Anemia", "category": "Hematological", "severity": "Moderate", "prevalence": 0.05},
            {"name": "Sleep Apnea", "category": "Sleep Disorder", "severity": "Moderate", "prevalence": 0.04},
        ]
        
        # Save diseases to file
        diseases_file = os.path.join(os.path.dirname(__file__), 'diseases.json')
        with open(diseases_file, 'w') as f:
            json.dump(diseases, f, indent=2)
        
        return diseases
    
    def create_symptom_disease_patterns(self):
        """Create realistic symptom-disease relationships"""
        patterns = {
            # Common Cold
            "Common Cold": {
                "primary": ["runny_nose", "nasal_congestion", "sneezing", "sore_throat", "cough"],
                "secondary": ["fatigue", "headache", "low_grade_fever", "loss_of_taste", "loss_of_smell"],
                "probability": {"primary": 0.8, "secondary": 0.4}
            },
            
            # Influenza
            "Influenza": {
                "primary": ["fever", "fatigue", "muscle_pain", "headache", "cough"],
                "secondary": ["chills", "sore_throat", "runny_nose", "nausea", "vomiting"],
                "probability": {"primary": 0.9, "secondary": 0.5}
            },
            
            # Pneumonia
            "Pneumonia": {
                "primary": ["fever", "cough", "shortness_of_breath", "chest_pain", "fatigue"],
                "secondary": ["chills", "rapid_breathing", "confusion", "nausea", "vomiting"],
                "probability": {"primary": 0.85, "secondary": 0.6}
            },
            
            # Diabetes Type 2
            "Diabetes Type 2": {
                "primary": ["frequent_urination", "excessive_thirst", "fatigue", "weight_loss"],
                "secondary": ["blurred_vision", "slow_healing", "numbness", "tingling"],
                "probability": {"primary": 0.7, "secondary": 0.4}
            },
            
            # Hypertension
            "Hypertension": {
                "primary": ["headache", "dizziness", "shortness_of_breath"],
                "secondary": ["chest_pain", "palpitations", "nosebleeds", "fatigue"],
                "probability": {"primary": 0.6, "secondary": 0.3}
            },
            
            # Asthma
            "Asthma": {
                "primary": ["wheezing", "shortness_of_breath", "chest_tightness", "cough"],
                "secondary": ["fatigue", "rapid_breathing", "anxiety"],
                "probability": {"primary": 0.9, "secondary": 0.5}
            },
            
            # Depression
            "Depression": {
                "primary": ["persistent_sadness", "loss_of_interest", "fatigue", "sleep_problems"],
                "secondary": ["appetite_changes", "concentration_problems", "hopelessness"],
                "probability": {"primary": 0.8, "secondary": 0.6}
            },
            
            # Migraine
            "Migraine": {
                "primary": ["severe_headache", "nausea", "light_sensitivity", "sound_sensitivity"],
                "secondary": ["vomiting", "visual_disturbances", "dizziness"],
                "probability": {"primary": 0.9, "secondary": 0.5}
            },
            
            # GERD
            "GERD": {
                "primary": ["heartburn", "acid_reflux", "chest_pain", "difficulty_swallowing"],
                "secondary": ["chronic_cough", "hoarse_voice", "sore_throat"],
                "probability": {"primary": 0.8, "secondary": 0.4}
            },
            
            # UTI
            "Urinary Tract Infection": {
                "primary": ["painful_urination", "frequent_urination", "urgency", "cloudy_urine"],
                "secondary": ["pelvic_pain", "fever", "fatigue", "blood_in_urine"],
                "probability": {"primary": 0.85, "secondary": 0.5}
            }
        }
        
        # Add more patterns for remaining diseases
        for disease in self.diseases:
            disease_name = disease["name"]
            if disease_name not in patterns:
                patterns[disease_name] = self.generate_generic_pattern(disease)
        
        return patterns
    
    def generate_generic_pattern(self, disease):
        """Generate generic symptom pattern for diseases without specific patterns"""
        all_symptoms = []
        for category in self.symptoms.values():
            all_symptoms.extend([s["name"] for s in category])
        
        # Select random symptoms based on disease category and severity
        num_primary = random.randint(3, 6)
        num_secondary = random.randint(2, 5)
        
        primary = random.sample(all_symptoms, min(num_primary, len(all_symptoms)))
        remaining = [s for s in all_symptoms if s not in primary]
        secondary = random.sample(remaining, min(num_secondary, len(remaining)))
        
        return {
            "primary": primary,
            "secondary": secondary,
            "probability": {"primary": 0.7, "secondary": 0.3}
        }
    
    def generate_patient_record(self, disease):
        """Generate a single patient record for a given disease"""
        pattern = self.symptom_disease_patterns.get(disease["name"], 
                                                   self.generate_generic_pattern(disease))
        
        # Get all possible symptoms
        all_symptoms = []
        for category in self.symptoms.values():
            all_symptoms.extend([s["name"] for s in category])
        
        # Initialize symptom vector
        symptom_vector = {symptom: 0 for symptom in all_symptoms}
        
        # Add primary symptoms
        for symptom in pattern["primary"]:
            if symptom in symptom_vector and random.random() < pattern["probability"]["primary"]:
                symptom_vector[symptom] = 1
        
        # Add secondary symptoms
        for symptom in pattern["secondary"]:
            if symptom in symptom_vector and random.random() < pattern["probability"]["secondary"]:
                symptom_vector[symptom] = 1
        
        # Add some noise (random symptoms with low probability)
        for symptom in all_symptoms:
            if symptom_vector[symptom] == 0 and random.random() < 0.05:
                symptom_vector[symptom] = 1
        
        # Create record
        record = symptom_vector.copy()
        record["disease"] = disease["name"]
        record["severity"] = disease["severity"]
        record["category"] = disease["category"]
        
        return record
    
    def generate_training_data(self, num_samples=5000):
        """Generate complete training dataset"""
        print(f"Generating {num_samples} training samples...")
        
        records = []
        
        # Calculate number of samples per disease based on prevalence
        total_prevalence = sum(d["prevalence"] for d in self.diseases)
        
        for disease in self.diseases:
            # Calculate samples for this disease
            disease_samples = int((disease["prevalence"] / total_prevalence) * num_samples)
            disease_samples = max(disease_samples, 10)  # Minimum 10 samples per disease
            
            print(f"Generating {disease_samples} samples for {disease['name']}")
            
            for _ in range(disease_samples):
                record = self.generate_patient_record(disease)
                records.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(records)
        
        # Shuffle the data
        df = df.sample(frac=1).reset_index(drop=True)
        
        print(f"Generated {len(df)} total samples")
        print(f"Diseases: {df['disease'].nunique()}")
        print(f"Average symptoms per patient: {df.drop(['disease', 'severity', 'category'], axis=1).sum(axis=1).mean():.2f}")
        
        return df
    
    def save_training_data(self, df, filename="training_data.csv"):
        """Save training data to CSV file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        df.to_csv(filepath, index=False)
        print(f"Training data saved to {filepath}")
        
        # Print statistics
        print("\nDataset Statistics:")
        print(f"Total samples: {len(df)}")
        print(f"Total features: {len(df.columns) - 3}")  # Excluding disease, severity, category
        print(f"Unique diseases: {df['disease'].nunique()}")
        
        print("\nDisease distribution:")
        disease_counts = df['disease'].value_counts()
        for disease, count in disease_counts.head(10).items():
            print(f"  {disease}: {count} samples")
        
        print("\nSeverity distribution:")
        severity_counts = df['severity'].value_counts()
        for severity, count in severity_counts.items():
            print(f"  {severity}: {count} samples")
        
        print("\nCategory distribution:")
        category_counts = df['category'].value_counts()
        for category, count in category_counts.items():
            print(f"  {category}: {count} samples")

def main():
    """Main function to generate training data"""
    print("MedAI Training Data Generator")
    print("=" * 40)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.dirname(__file__)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Initialize generator
    generator = MedicalDataGenerator()
    
    # Generate training data
    df = generator.generate_training_data(num_samples=5000)
    
    # Save to file
    generator.save_training_data(df)
    
    print("\nTraining data generation completed successfully!")
    print("Files created:")
    print("  - symptoms.json: Symptom definitions")
    print("  - diseases.json: Disease definitions")
    print("  - training_data.csv: Training dataset")

if __name__ == "__main__":
    main()