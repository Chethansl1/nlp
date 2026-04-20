from flask import Flask, render_template, request, jsonify, session
import os
import json
import pickle
import numpy as np
import uuid
from datetime import datetime
from models.disease_predictor import DiseasePredictor

app = Flask(__name__)
app.secret_key = 'advanced_disease_prediction_secret_key'

# Initialize the disease predictor
predictor = DiseasePredictor()

# In-memory storage for predictions (in a real app, this would be a database)
prediction_history = {}

@app.route('/')
def index():
    # Generate a unique session ID if not present
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Extract features
        symptoms = data.get('symptoms', [])
        demographics = data.get('demographics', {})
        
        # We've removed medical data input, so just pass None
        # Combine all features
        features = predictor.process_input(symptoms, demographics)
        
        # Get enhanced prediction with graphs and treatment recommendations
        prediction_id, predictions = predictor.predict(features)
        
        # Store prediction for this user
        user_id = session.get('user_id', 'anonymous')
        
        prediction_history[prediction_id] = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'predictions': predictions
        }
        
        return jsonify({
            'status': 'success',
            'prediction_id': prediction_id,
            'predictions': predictions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def provide_feedback():
    """Endpoint to provide feedback for reinforcement learning"""
    try:
        data = request.get_json()
        prediction_id = data.get('prediction_id')
        actual_diagnoses = data.get('actual_diagnoses', [])
        
        # Find prediction in history
        if prediction_id not in prediction_history:
            return jsonify({
                'status': 'error',
                'message': 'Prediction not found'
            }), 404
        
        # Update model with feedback
        success = predictor.provide_feedback(prediction_id, actual_diagnoses)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Feedback recorded successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to record feedback'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/diseases', methods=['GET'])
def get_diseases():
    # Return the list of diseases for the frontend
    return jsonify({
        'diseases': predictor.get_disease_list()
    })

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    # Return the list of symptoms for the frontend
    return jsonify({
        'symptoms': predictor.get_symptom_list()
    })

@app.route('/prescription/<disease>', methods=['GET'])
def get_prescription(disease):
    """Get comprehensive prescription template for a specific disease"""
    try:
        if disease not in predictor.disease_symptoms:
            return jsonify({
                'status': 'error',
                'message': 'Disease not found'
            }), 404
            
        # Generate enhanced treatment recommendations for this disease
        treatment_data = predictor._generate_treatment_recommendations(disease, "High", {})
        
        # Create a comprehensive prescription template
        prescription = {
            'disease': disease,
            'disease_name': disease,  # Added for clarity
            'risk_level': 'High',
            'treatments': treatment_data['treatments'],
            'lifestyle_modifications': treatment_data['lifestyle_modifications'],
            'medications': treatment_data['medications'],
            'follow_up_recommendations': treatment_data['follow_up_recommendations'],
            'warning_signs': [
                "Seek immediate medical attention if symptoms worsen",
                "Contact healthcare provider if new symptoms develop",
                "Follow medication schedule strictly"
            ],
            'warning': f"This is a detailed treatment plan for {disease}. Please consult with a healthcare professional before making any changes to your health regimen."
        }
        
        return jsonify({
            'status': 'success',
            'prescription': prescription
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get prediction history for the current user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 401
        
    # Get predictions for this user
    user_predictions = []
    for pred_id, prediction in prediction_history.items():
        if prediction['user_id'] == user_id:
            user_predictions.append({
                'id': pred_id,
                'timestamp': prediction['timestamp'],
                'summary': [{'disease': p['disease'], 'risk': p['risk_percentage']} 
                           for p in prediction['predictions'][:3]]  # Just include top 3 for summary
            })
    
    return jsonify({
        'status': 'success',
        'history': sorted(user_predictions, key=lambda x: x['timestamp'], reverse=True)
    })

if __name__ == '__main__':
    app.run(debug=True)