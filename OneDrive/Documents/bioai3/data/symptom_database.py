import json
import sqlite3
from typing import List, Dict, Any

class SymptomDatabase:
    """Comprehensive symptom database for medical diagnosis"""
    
    def __init__(self):
        self.symptoms_data = self.load_comprehensive_symptoms()
        self.init_symptom_db()
    
    def load_comprehensive_symptoms(self):
        """Load comprehensive symptom database"""
        return {
            # General Symptoms
            "fever": {
                "category": "General",
                "description": "Elevated body temperature above normal (>100.4°F/38°C)",
                "severity_levels": ["Low-grade (100.4-102°F)", "Moderate (102-104°F)", "High (>104°F)"],
                "related_systems": ["Immune", "Circulatory"]
            },
            "fatigue": {
                "category": "General",
                "description": "Extreme tiredness or lack of energy",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous", "Muscular"]
            },
            "headache": {
                "category": "Neurological",
                "description": "Pain in the head or neck region",
                "severity_levels": ["Mild", "Moderate", "Severe", "Migraine-level"],
                "related_systems": ["Nervous", "Circulatory"]
            },
            "dizziness": {
                "category": "Neurological",
                "description": "Feeling of unsteadiness or lightheadedness",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous", "Circulatory"]
            },
            
            # Respiratory Symptoms
            "cough": {
                "category": "Respiratory",
                "description": "Forceful expulsion of air from lungs",
                "severity_levels": ["Dry cough", "Productive cough", "Persistent cough"],
                "related_systems": ["Respiratory"]
            },
            "shortness_of_breath": {
                "category": "Respiratory",
                "description": "Difficulty breathing or feeling breathless",
                "severity_levels": ["Mild exertion", "Moderate exertion", "At rest"],
                "related_systems": ["Respiratory", "Circulatory"]
            },
            "chest_pain": {
                "category": "Respiratory",
                "description": "Pain or discomfort in the chest area",
                "severity_levels": ["Mild", "Moderate", "Severe", "Sharp/Stabbing"],
                "related_systems": ["Respiratory", "Circulatory"]
            },
            "wheezing": {
                "category": "Respiratory",
                "description": "High-pitched whistling sound when breathing",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Respiratory"]
            },
            "sore_throat": {
                "category": "Respiratory",
                "description": "Pain or irritation in the throat",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Respiratory", "Immune"]
            },
            "runny_nose": {
                "category": "Respiratory",
                "description": "Nasal discharge or congestion",
                "severity_levels": ["Clear discharge", "Thick discharge", "Bloody discharge"],
                "related_systems": ["Respiratory"]
            },
            "sneezing": {
                "category": "Respiratory",
                "description": "Sudden, forceful expulsion of air through nose",
                "severity_levels": ["Occasional", "Frequent", "Persistent"],
                "related_systems": ["Respiratory", "Immune"]
            },
            
            # Gastrointestinal Symptoms
            "nausea": {
                "category": "Gastrointestinal",
                "description": "Feeling of sickness with urge to vomit",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Digestive", "Nervous"]
            },
            "vomiting": {
                "category": "Gastrointestinal",
                "description": "Forceful expulsion of stomach contents",
                "severity_levels": ["Occasional", "Frequent", "Persistent"],
                "related_systems": ["Digestive", "Nervous"]
            },
            "diarrhea": {
                "category": "Gastrointestinal",
                "description": "Loose or watery bowel movements",
                "severity_levels": ["Mild", "Moderate", "Severe/Watery"],
                "related_systems": ["Digestive"]
            },
            "abdominal_pain": {
                "category": "Gastrointestinal",
                "description": "Pain in the stomach or abdominal area",
                "severity_levels": ["Mild", "Moderate", "Severe", "Cramping"],
                "related_systems": ["Digestive"]
            },
            "loss_of_appetite": {
                "category": "Gastrointestinal",
                "description": "Reduced desire to eat",
                "severity_levels": ["Mild", "Moderate", "Complete loss"],
                "related_systems": ["Digestive", "Nervous"]
            },
            
            # Cardiovascular Symptoms
            "chest_tightness": {
                "category": "Cardiovascular",
                "description": "Feeling of pressure or constriction in chest",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Circulatory", "Respiratory"]
            },
            "rapid_heartbeat": {
                "category": "Cardiovascular",
                "description": "Heart rate faster than normal (>100 bpm)",
                "severity_levels": ["Mild (100-120 bpm)", "Moderate (120-150 bpm)", "Severe (>150 bpm)"],
                "related_systems": ["Circulatory"]
            },
            "irregular_heartbeat": {
                "category": "Cardiovascular",
                "description": "Abnormal heart rhythm",
                "severity_levels": ["Occasional", "Frequent", "Persistent"],
                "related_systems": ["Circulatory"]
            },
            
            # Musculoskeletal Symptoms
            "muscle_pain": {
                "category": "Musculoskeletal",
                "description": "Pain in muscles throughout the body",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Muscular"]
            },
            "joint_pain": {
                "category": "Musculoskeletal",
                "description": "Pain in joints",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Skeletal", "Muscular"]
            },
            "back_pain": {
                "category": "Musculoskeletal",
                "description": "Pain in the back region",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Skeletal", "Muscular"]
            },
            
            # Neurological Symptoms
            "confusion": {
                "category": "Neurological",
                "description": "Difficulty thinking clearly or concentrating",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            "memory_problems": {
                "category": "Neurological",
                "description": "Difficulty remembering things",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            "seizures": {
                "category": "Neurological",
                "description": "Sudden, uncontrolled electrical activity in brain",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            
            # Skin Symptoms
            "rash": {
                "category": "Dermatological",
                "description": "Skin irritation or eruption",
                "severity_levels": ["Mild", "Moderate", "Severe/Widespread"],
                "related_systems": ["Integumentary", "Immune"]
            },
            "itching": {
                "category": "Dermatological",
                "description": "Uncomfortable sensation causing urge to scratch",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Integumentary", "Nervous"]
            },
            "skin_discoloration": {
                "category": "Dermatological",
                "description": "Changes in skin color",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Integumentary"]
            },
            
            # Endocrine/Metabolic Symptoms
            "excessive_thirst": {
                "category": "Endocrine",
                "description": "Abnormally increased thirst",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Endocrine", "Urinary"]
            },
            "frequent_urination": {
                "category": "Endocrine",
                "description": "Urinating more often than normal",
                "severity_levels": ["Mild increase", "Moderate increase", "Severe increase"],
                "related_systems": ["Urinary", "Endocrine"]
            },
            "unexplained_weight_loss": {
                "category": "Endocrine",
                "description": "Losing weight without trying",
                "severity_levels": ["5-10 lbs", "10-20 lbs", ">20 lbs"],
                "related_systems": ["Endocrine", "Digestive"]
            },
            "unexplained_weight_gain": {
                "category": "Endocrine",
                "description": "Gaining weight without dietary changes",
                "severity_levels": ["5-10 lbs", "10-20 lbs", ">20 lbs"],
                "related_systems": ["Endocrine"]
            },
            
            # Mental Health Symptoms
            "anxiety": {
                "category": "Mental Health",
                "description": "Feelings of worry, nervousness, or unease",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            "depression": {
                "category": "Mental Health",
                "description": "Persistent feelings of sadness or hopelessness",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            "mood_swings": {
                "category": "Mental Health",
                "description": "Rapid changes in emotional state",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous", "Endocrine"]
            },
            "sleep_disturbances": {
                "category": "Mental Health",
                "description": "Problems with sleeping patterns",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            
            # Eye/Vision Symptoms
            "blurred_vision": {
                "category": "Ophthalmological",
                "description": "Loss of sharpness in vision",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous", "Circulatory"]
            },
            "eye_pain": {
                "category": "Ophthalmological",
                "description": "Pain in or around the eyes",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            "sensitivity_to_light": {
                "category": "Ophthalmological",
                "description": "Discomfort or pain from light exposure",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Nervous"]
            },
            
            # Additional Specific Symptoms
            "chills": {
                "category": "General",
                "description": "Feeling cold with shivering",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Immune", "Circulatory"]
            },
            "sweating": {
                "category": "General",
                "description": "Excessive perspiration",
                "severity_levels": ["Mild", "Moderate", "Profuse"],
                "related_systems": ["Integumentary", "Nervous"]
            },
            "swollen_lymph_nodes": {
                "category": "Immune",
                "description": "Enlarged lymph glands",
                "severity_levels": ["Mild", "Moderate", "Severe"],
                "related_systems": ["Immune"]
            }
        }
    
    def init_symptom_db(self):
        """Initialize symptom database"""
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                severity_levels TEXT NOT NULL,
                related_systems TEXT NOT NULL
            )
        ''')
        
        # Insert symptoms if not exists
        for symptom_name, symptom_data in self.symptoms_data.items():
            cursor.execute('''
                INSERT OR IGNORE INTO symptoms 
                (name, category, description, severity_levels, related_systems)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                symptom_name,
                symptom_data['category'],
                symptom_data['description'],
                json.dumps(symptom_data['severity_levels']),
                json.dumps(symptom_data['related_systems'])
            ))
        
        conn.commit()
        conn.close()
    
    def get_all_symptoms(self):
        """Get all symptoms organized by category"""
        symptoms_by_category = {}
        
        for symptom_name, symptom_data in self.symptoms_data.items():
            category = symptom_data['category']
            if category not in symptoms_by_category:
                symptoms_by_category[category] = []
            
            symptoms_by_category[category].append({
                'name': symptom_name,
                'display_name': symptom_name.replace('_', ' ').title(),
                'description': symptom_data['description'],
                'severity_levels': symptom_data['severity_levels']
            })
        
        return symptoms_by_category
    
    def get_symptoms_by_category(self, category):
        """Get symptoms for a specific category"""
        return [
            {
                'name': name,
                'display_name': name.replace('_', ' ').title(),
                'description': data['description'],
                'severity_levels': data['severity_levels']
            }
            for name, data in self.symptoms_data.items()
            if data['category'] == category
        ]
    
    def get_symptom_details(self, symptom_name):
        """Get detailed information about a specific symptom"""
        return self.symptoms_data.get(symptom_name, None)
    
    def search_symptoms(self, query):
        """Search symptoms by name or description"""
        query = query.lower()
        results = []
        
        for symptom_name, symptom_data in self.symptoms_data.items():
            if (query in symptom_name.lower() or 
                query in symptom_data['description'].lower()):
                results.append({
                    'name': symptom_name,
                    'display_name': symptom_name.replace('_', ' ').title(),
                    'description': symptom_data['description'],
                    'category': symptom_data['category']
                })
        
        return results
    
    def get_related_symptoms(self, symptom_name):
        """Get symptoms related to the given symptom"""
        if symptom_name not in self.symptoms_data:
            return []
        
        symptom_systems = set(self.symptoms_data[symptom_name]['related_systems'])
        related = []
        
        for name, data in self.symptoms_data.items():
            if name != symptom_name:
                if set(data['related_systems']) & symptom_systems:
                    related.append({
                        'name': name,
                        'display_name': name.replace('_', ' ').title(),
                        'description': data['description'],
                        'category': data['category']
                    })
        
        return related[:10]  # Return top 10 related symptoms
    
    def validate_symptoms(self, symptom_list):
        """Validate that all symptoms in the list exist"""
        valid_symptoms = []
        invalid_symptoms = []
        
        for symptom in symptom_list:
            if symptom in self.symptoms_data:
                valid_symptoms.append(symptom)
            else:
                invalid_symptoms.append(symptom)
        
        return valid_symptoms, invalid_symptoms
    
    def get_symptom_categories(self):
        """Get all available symptom categories"""
        categories = set()
        for symptom_data in self.symptoms_data.values():
            categories.add(symptom_data['category'])
        
        return sorted(list(categories))