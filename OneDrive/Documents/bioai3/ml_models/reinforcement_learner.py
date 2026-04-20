import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces
import sqlite3
import json
import joblib
import os
from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class MedicalDiagnosisEnv(gym.Env):
    """Custom Gym environment for medical diagnosis reinforcement learning"""
    
    def __init__(self, symptom_space_size=100, disease_space_size=20):
        super(MedicalDiagnosisEnv, self).__init__()
        
        # Define action and observation space
        self.action_space = spaces.Discrete(disease_space_size)  # Predict one of N diseases
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(symptom_space_size,), dtype=np.float32
        )
        
        self.symptom_space_size = symptom_space_size
        self.disease_space_size = disease_space_size
        self.current_symptoms = None
        self.true_disease = None
        self.prediction_history = deque(maxlen=1000)
        
    def reset(self, seed=None, options=None):
        """Reset the environment"""
        super().reset(seed=seed)
        # Generate random symptom pattern or load from database
        self.current_symptoms = self._generate_symptom_pattern()
        return self.current_symptoms, {}
    
    def step(self, action):
        """Execute one step in the environment"""
        predicted_disease = action
        
        # Calculate reward based on prediction accuracy
        reward = self._calculate_reward(predicted_disease)
        
        # Episode is done after one prediction
        done = True
        
        # Store prediction for learning
        self.prediction_history.append({
            'symptoms': self.current_symptoms.copy(),
            'predicted_disease': predicted_disease,
            'true_disease': self.true_disease,
            'reward': reward
        })
        
        info = {
            'predicted_disease': predicted_disease,
            'true_disease': self.true_disease,
            'accuracy': 1.0 if predicted_disease == self.true_disease else 0.0
        }
        
        return self.current_symptoms, reward, done, False, info
    
    def _generate_symptom_pattern(self):
        """Generate a symptom pattern with corresponding true disease"""
        # Load real data from database or use synthetic data
        symptom_pattern = np.zeros(self.symptom_space_size, dtype=np.float32)
        
        # Generate realistic symptom combinations
        disease_patterns = {
            0: [0, 1, 2, 5],      # Common Cold
            1: [3, 4, 6, 7, 8],   # Influenza
            2: [9, 10, 11, 12],   # Pneumonia
            3: [13, 14, 15, 16],  # Diabetes
            4: [17, 18, 19, 20],  # Hypertension
            # Add more patterns...
        }
        
        # Randomly select a disease
        self.true_disease = random.randint(0, min(len(disease_patterns)-1, self.disease_space_size-1))
        
        # Set corresponding symptoms
        if self.true_disease in disease_patterns:
            for symptom_idx in disease_patterns[self.true_disease]:
                if symptom_idx < self.symptom_space_size:
                    symptom_pattern[symptom_idx] = 1.0
        
        # Add some noise/variation
        noise_indices = random.sample(range(self.symptom_space_size), 
                                    random.randint(1, 3))
        for idx in noise_indices:
            symptom_pattern[idx] = random.uniform(0.1, 0.9)
        
        return symptom_pattern
    
    def _calculate_reward(self, predicted_disease):
        """Calculate reward based on prediction accuracy and confidence"""
        if predicted_disease == self.true_disease:
            # High reward for correct prediction
            return 10.0
        else:
            # Negative reward for incorrect prediction
            # Could be modified based on severity of misdiagnosis
            return -5.0
    
    def load_real_data(self):
        """Load real symptom-disease data from database"""
        try:
            conn = sqlite3.connect('medical_predictions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symptoms, actual_diagnosis, feedback 
                FROM predictions 
                WHERE actual_diagnosis IS NOT NULL
            ''')
            
            real_data = cursor.fetchall()
            conn.close()
            
            return real_data
        except:
            return []

class ReinforcementLearner:
    """Reinforcement Learning component for improving disease predictions"""
    
    def __init__(self):
        self.env = MedicalDiagnosisEnv()
        self.model = None
        self.training_data = deque(maxlen=10000)
        self.performance_history = []
        self.load_or_initialize_model()
    
    def load_or_initialize_model(self):
        """Load existing RL model or initialize new one"""
        model_path = 'models/rl_model.zip'
        
        if os.path.exists(model_path):
            try:
                self.model = PPO.load(model_path, env=self.env)
                print("Loaded existing RL model")
            except Exception as e:
                print(f"Error loading RL model: {e}")
                self.initialize_policy()
        else:
            self.initialize_policy()
    
    def initialize_policy(self):
        """Initialize the reinforcement learning policy"""
        print("Initializing new RL policy...")
        
        # Use PPO (Proximal Policy Optimization) algorithm
        self.model = PPO(
            "MlpPolicy",
            self.env,
            verbose=1,
            learning_rate=0.0003,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
            tensorboard_log="./tensorboard_logs/"
        )
        
        # Initial training
        print("Starting initial RL training...")
        self.model.learn(total_timesteps=10000)
        
        # Save the model
        self.save_model()
        print("RL model initialized and saved!")
    
    def update_prediction_data(self, symptoms, prediction_result):
        """Update training data with new prediction"""
        self.training_data.append({
            'symptoms': symptoms,
            'prediction': prediction_result,
            'timestamp': pd.Timestamp.now()
        })
    
    def process_feedback(self, prediction_id, feedback_value, actual_diagnosis):
        """Process user feedback to improve the model"""
        try:
            # Load prediction data
            conn = sqlite3.connect('medical_predictions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symptoms, predicted_disease 
                FROM predictions 
                WHERE id = ?
            ''', (prediction_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                symptoms_json, predicted_disease = result
                symptoms = json.loads(symptoms_json)
                
                # Create training example for RL
                reward = self._calculate_feedback_reward(
                    feedback_value, predicted_disease, actual_diagnosis
                )
                
                # Store for batch training
                self.training_data.append({
                    'symptoms': symptoms,
                    'predicted_disease': predicted_disease,
                    'actual_diagnosis': actual_diagnosis,
                    'feedback_value': feedback_value,
                    'reward': reward,
                    'timestamp': pd.Timestamp.now()
                })
                
                # Trigger retraining if enough feedback accumulated
                if len(self.training_data) >= 100:
                    self.update_policy()
                    
        except Exception as e:
            print(f"Error processing feedback: {e}")
    
    def _calculate_feedback_reward(self, feedback_value, predicted_disease, actual_diagnosis):
        """Calculate reward based on user feedback"""
        # Base reward from feedback (1-5 scale)
        base_reward = (feedback_value - 3) * 2  # Convert to -4 to +4 scale
        
        # Bonus for correct diagnosis
        if actual_diagnosis and predicted_disease.lower() == actual_diagnosis.lower():
            base_reward += 5
        elif actual_diagnosis and predicted_disease.lower() != actual_diagnosis.lower():
            base_reward -= 3
        
        return base_reward
    
    def update_policy(self):
        """Update the RL policy based on accumulated feedback"""
        if len(self.training_data) < 50:
            print("Not enough training data for policy update")
            return
        
        print("Updating RL policy with feedback data...")
        
        try:
            # Create custom training environment with real data
            self._create_feedback_environment()
            
            # Continue training with new data
            self.model.learn(total_timesteps=5000)
            
            # Evaluate performance
            self._evaluate_performance()
            
            # Save updated model
            self.save_model()
            
            print("RL policy updated successfully!")
            
        except Exception as e:
            print(f"Error updating policy: {e}")
    
    def _create_feedback_environment(self):
        """Create training environment with real feedback data"""
        # Convert training data to environment format
        feedback_data = list(self.training_data)[-1000:]  # Use recent data
        
        # Update environment with real data
        self.env.real_data = feedback_data
    
    def _evaluate_performance(self):
        """Evaluate the current model performance"""
        try:
            # Run evaluation episodes
            obs = self.env.reset()
            total_reward = 0
            correct_predictions = 0
            total_predictions = 0
            
            for _ in range(100):  # 100 evaluation episodes
                action, _ = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.env.step(action)
                
                total_reward += reward
                total_predictions += 1
                if info.get('accuracy', 0) == 1.0:
                    correct_predictions += 1
                
                if done:
                    obs = self.env.reset()
            
            accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
            avg_reward = total_reward / total_predictions if total_predictions > 0 else 0
            
            self.performance_history.append({
                'timestamp': pd.Timestamp.now(),
                'accuracy': accuracy,
                'avg_reward': avg_reward,
                'total_predictions': total_predictions
            })
            
            print(f"RL Model Performance - Accuracy: {accuracy:.3f}, Avg Reward: {avg_reward:.3f}")
            
        except Exception as e:
            print(f"Error evaluating performance: {e}")
    
    def get_prediction_adjustment(self, symptoms, base_prediction):
        """Get RL-based adjustment to base prediction"""
        try:
            # Convert symptoms to environment format
            symptom_vector = self._symptoms_to_vector(symptoms)
            
            # Get RL model prediction
            action, _ = self.model.predict(symptom_vector, deterministic=True)
            
            # Convert action to disease adjustment
            adjustment = {
                'confidence_adjustment': 0.0,
                'alternative_suggestion': None,
                'risk_assessment': 'standard'
            }
            
            # Apply RL insights to adjust prediction
            if hasattr(self.model, 'predict_proba'):
                action_probs = self.model.predict_proba(symptom_vector)
                confidence_boost = max(action_probs) - 0.5
                adjustment['confidence_adjustment'] = confidence_boost * 0.1
            
            return adjustment
            
        except Exception as e:
            print(f"Error getting RL adjustment: {e}")
            return {'confidence_adjustment': 0.0}
    
    def _symptoms_to_vector(self, symptoms):
        """Convert symptom list to vector format for RL model"""
        vector = np.zeros(self.env.symptom_space_size, dtype=np.float32)
        
        # Simple mapping - in production, use proper encoding
        symptom_mapping = {
            'fever': 0, 'cough': 1, 'headache': 2, 'fatigue': 3,
            'nausea': 4, 'vomiting': 5, 'diarrhea': 6, 'chest_pain': 7,
            # Add more mappings...
        }
        
        for symptom in symptoms:
            if symptom in symptom_mapping:
                idx = symptom_mapping[symptom]
                if idx < len(vector):
                    vector[idx] = 1.0
        
        return vector
    
    def save_model(self):
        """Save the RL model"""
        try:
            if not os.path.exists('models'):
                os.makedirs('models')
            
            self.model.save('models/rl_model.zip')
            
            # Save performance history
            if self.performance_history:
                performance_df = pd.DataFrame(self.performance_history)
                performance_df.to_csv('models/rl_performance_history.csv', index=False)
            
            print("RL model saved successfully!")
            
        except Exception as e:
            print(f"Error saving RL model: {e}")
    
    def get_performance_stats(self):
        """Get current performance statistics"""
        if not self.performance_history:
            return {
                'accuracy': 0.0,
                'avg_reward': 0.0,
                'total_episodes': 0,
                'improvement_trend': 'No data'
            }
        
        recent_performance = self.performance_history[-10:]  # Last 10 evaluations
        
        avg_accuracy = np.mean([p['accuracy'] for p in recent_performance])
        avg_reward = np.mean([p['avg_reward'] for p in recent_performance])
        total_episodes = sum([p['total_predictions'] for p in recent_performance])
        
        # Calculate improvement trend
        if len(self.performance_history) >= 2:
            recent_acc = np.mean([p['accuracy'] for p in self.performance_history[-5:]])
            older_acc = np.mean([p['accuracy'] for p in self.performance_history[-10:-5]])
            
            if recent_acc > older_acc + 0.01:
                trend = 'Improving'
            elif recent_acc < older_acc - 0.01:
                trend = 'Declining'
            else:
                trend = 'Stable'
        else:
            trend = 'Insufficient data'
        
        return {
            'accuracy': round(avg_accuracy, 3),
            'avg_reward': round(avg_reward, 3),
            'total_episodes': total_episodes,
            'improvement_trend': trend
        }