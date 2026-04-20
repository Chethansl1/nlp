from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import numpy as np
import pandas as pd
from datetime import datetime
import os
from ml_models.disease_predictor import DiseasePredictor
from ml_models.reinforcement_learner import ReinforcementLearner
from data.symptom_database import SymptomDatabase

app = Flask(__name__)
CORS(app)

# Initialize components
symptom_db = SymptomDatabase()
disease_predictor = DiseasePredictor()
rl_learner = ReinforcementLearner()

# Initialize database
def init_db():
    conn = sqlite3.connect('medical_predictions.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            predicted_disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            feedback INTEGER DEFAULT NULL,
            actual_diagnosis TEXT DEFAULT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            feedback_type TEXT NOT NULL,
            feedback_value INTEGER NOT NULL,
            comments TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES predictions (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    symptoms = symptom_db.get_all_symptoms()
    return render_template('predict.html', symptoms=symptoms)

@app.route('/api/symptoms')
def get_symptoms():
    symptoms = symptom_db.get_all_symptoms()
    return jsonify(symptoms)

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    try:
        data = request.json
        selected_symptoms = data.get('symptoms', [])
        
        print(f"Received prediction request with {len(selected_symptoms)} symptoms: {selected_symptoms}")
        
        if not selected_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Validate symptoms
        valid_symptoms = []
        for symptom in selected_symptoms:
            if isinstance(symptom, str) and symptom.strip():
                valid_symptoms.append(symptom.strip())
        
        if not valid_symptoms:
            return jsonify({'error': 'No valid symptoms provided'}), 400
        
        print(f"Valid symptoms for prediction: {valid_symptoms}")
        
        # Get prediction from ML model
        prediction_result = disease_predictor.predict(valid_symptoms)
        
        # Store prediction in database
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (symptoms, predicted_disease, confidence)
            VALUES (?, ?, ?)
        ''', (json.dumps(selected_symptoms), 
              prediction_result['disease'], 
              prediction_result['confidence']))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Update reinforcement learning model
        rl_learner.update_prediction_data(selected_symptoms, prediction_result)
        
        # Convert numpy types to Python native types for JSON serialization
        response_data = {
            'prediction_id': int(prediction_id),
            'disease': str(prediction_result['disease']),
            'confidence': float(prediction_result['confidence']),
            'recommendations': [str(rec) for rec in prediction_result['recommendations']],
            'severity': str(prediction_result['severity']),
            'alternative_diagnoses': [
                {
                    'disease': str(alt['disease']),
                    'probability': float(alt['probability'])
                } for alt in prediction_result['alternatives']
            ]
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        prediction_id = data.get('prediction_id')
        feedback_type = data.get('feedback_type')  # 'accuracy', 'helpfulness', etc.
        feedback_value = data.get('feedback_value')  # 1-5 rating
        comments = data.get('comments', '')
        actual_diagnosis = data.get('actual_diagnosis', '')
        
        # Validate required fields
        if not prediction_id:
            return jsonify({'error': 'Prediction ID is required'}), 400
        if not feedback_value:
            return jsonify({'error': 'Feedback value is required'}), 400
        
        # Store feedback
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        
        # Check if prediction exists
        cursor.execute('SELECT id FROM predictions WHERE id = ?', (prediction_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Update prediction with feedback
        if actual_diagnosis:
            cursor.execute('''
                UPDATE predictions 
                SET feedback = ?, actual_diagnosis = ?
                WHERE id = ?
            ''', (feedback_value, actual_diagnosis, prediction_id))
        
        # Store detailed feedback
        cursor.execute('''
            INSERT INTO feedback (prediction_id, feedback_type, feedback_value, comments)
            VALUES (?, ?, ?, ?)
        ''', (prediction_id, feedback_type, feedback_value, comments))
        
        conn.commit()
        conn.close()
        
        # Update reinforcement learning model with feedback
        rl_learner.process_feedback(prediction_id, feedback_value, actual_diagnosis)
        
        return jsonify({'status': 'success', 'message': 'Feedback recorded successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    try:
        # Retrain the model with new feedback data
        disease_predictor.retrain_with_feedback()
        rl_learner.update_policy()
        
        return jsonify({'status': 'success', 'message': 'Model retrained successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_prediction_state():
    """Clear prediction state for new prediction"""
    try:
        return jsonify({'status': 'success', 'message': 'Prediction state cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def test_system():
    """Test endpoint to check system status"""
    try:
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        
        # Get recent predictions
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total_predictions = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM feedback')
        total_feedback = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'total_predictions': total_predictions,
            'total_feedback': total_feedback,
            'models_loaded': len(disease_predictor.models) if disease_predictor else 0,
            'rl_initialized': rl_learner.model is not None if rl_learner else False
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    try:
        conn = sqlite3.connect('medical_predictions.db')
        cursor = conn.cursor()
        
        # Get prediction statistics
        cursor.execute('SELECT COUNT(*) FROM predictions')
        total_predictions = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence) FROM predictions')
        avg_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(feedback) FROM predictions WHERE feedback IS NOT NULL')
        avg_feedback = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT predicted_disease, COUNT(*) as count 
            FROM predictions 
            GROUP BY predicted_disease 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        top_diseases = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'total_predictions': total_predictions,
            'average_confidence': round(avg_confidence, 2),
            'average_feedback': round(avg_feedback, 2),
            'top_diseases': [{'disease': d[0], 'count': d[1]} for d in top_diseases]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    
    # Load and train initial model if not exists
    if not os.path.exists('models/'):
        os.makedirs('models/')
        disease_predictor.train_initial_model()
        rl_learner.initialize_policy()
    
    app.run(debug=True, host='0.0.0.0', port=5000)