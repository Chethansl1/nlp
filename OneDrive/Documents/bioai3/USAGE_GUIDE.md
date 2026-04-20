# MedAI Usage Guide

## Quick Start

### 1. Setup and Installation
```bash
# Navigate to project directory
cd bioai3

# Install dependencies
pip install -r requirements.txt

# Generate training data
python data/generate_training_data.py

# Run the application
python app.py
```

### 2. Access the Application
Open your web browser and go to: `http://localhost:5000`

## Step-by-Step Usage

### Step 1: Home Page
- View system statistics and features
- Click "Start Diagnosis" to begin

### Step 2: Symptom Selection
1. **Browse Categories**: Symptoms are organized into 8 medical categories:
   - General (fever, fatigue, etc.)
   - Respiratory (cough, shortness of breath, etc.)
   - Gastrointestinal (nausea, vomiting, etc.)
   - Neurological (headache, dizziness, etc.)
   - Cardiovascular (chest pain, palpitations, etc.)
   - Musculoskeletal (joint pain, muscle pain, etc.)
   - Dermatological (rash, itching, etc.)
   - Genitourinary (frequent urination, etc.)

2. **Search Symptoms**: Use the search bar to quickly find specific symptoms

3. **Select Symptoms**: Check the boxes for symptoms you're experiencing

4. **Review Selection**: Selected symptoms appear in the right panel

### Step 3: Get Prediction
1. Click "Analyze Symptoms" button
2. Wait for AI analysis (usually 1-2 seconds)
3. Review the results:
   - **Primary Diagnosis**: Most likely condition
   - **Confidence Level**: How certain the AI is (0-100%)
   - **Severity**: Mild, Moderate, or Severe
   - **Recommendations**: Medical advice and next steps
   - **Alternative Diagnoses**: Other possible conditions

### Step 4: Provide Feedback
1. Click "Provide Feedback" button
2. Rate the accuracy (1-5 stars)
3. Optionally provide:
   - Actual diagnosis (if known)
   - Additional comments
4. Submit feedback to help improve the system

### Step 5: New Prediction
1. Click "New Prediction" button after providing feedback
2. Clear previous symptoms and start over
3. The system learns from your feedback for future predictions

## Understanding Results

### Confidence Levels
- **80-100%**: High confidence (green)
- **60-79%**: Medium confidence (yellow)
- **Below 60%**: Low confidence (red)

### Severity Levels
- **Mild**: Usually manageable at home, monitor symptoms
- **Moderate**: Consider seeing a healthcare provider
- **Severe**: Seek immediate medical attention

### Recommendations
The system provides specific recommendations based on:
- Predicted condition
- Severity level
- Current medical guidelines
- Best practices for symptom management

## Advanced Features

### API Usage
You can also use the system programmatically:

```python
import requests

# Make a prediction
response = requests.post('http://localhost:5000/api/predict', 
                        json={'symptoms': ['fever', 'cough', 'headache']})
result = response.json()
print(f"Predicted disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2%}")

# Submit feedback
feedback_response = requests.post('http://localhost:5000/api/feedback',
                                 json={
                                     'prediction_id': result['prediction_id'],
                                     'feedback_type': 'accuracy',
                                     'feedback_value': 4,
                                     'comments': 'Very accurate'
                                 })
```

### System Statistics
Access real-time statistics at: `http://localhost:5000/api/stats`

### System Health Check
Check system status at: `http://localhost:5000/api/test`

## Troubleshooting

### Common Issues

1. **"No prediction to provide feedback for"**
   - Make sure you've made a prediction first
   - Check browser console for errors
   - Refresh the page and try again

2. **Slow predictions**
   - First prediction may take longer (model loading)
   - Subsequent predictions should be faster
   - Check system resources (RAM/CPU)

3. **Database errors**
   - Ensure SQLite is installed
   - Check file permissions in project directory
   - Delete `medical_predictions.db` to reset database

4. **Model loading errors**
   - Check if `models/` directory exists
   - Ensure sufficient RAM (4GB+ recommended)
   - Try restarting the application

### Getting Help

1. **Check Console Output**: Look for error messages in terminal
2. **Browser Console**: Check for JavaScript errors (F12)
3. **Log Files**: Check application logs for detailed errors
4. **System Test**: Use `/api/test` endpoint to check system status

## Best Practices

### For Accurate Predictions
1. **Be Specific**: Select all relevant symptoms
2. **Be Honest**: Don't omit symptoms you're experiencing
3. **Consider Timing**: Include symptoms from the current episode
4. **Provide Context**: Use the comments field for additional information

### For System Improvement
1. **Provide Feedback**: Always rate predictions when possible
2. **Include Actual Diagnosis**: If you know the real diagnosis, include it
3. **Be Detailed**: Use comments to explain accuracy or inaccuracy
4. **Regular Use**: The system improves with more data

## Data Privacy

- **No Personal Information**: System doesn't store personal details
- **Anonymous Predictions**: All data is anonymized
- **Local Storage**: Data stored locally in SQLite database
- **No External Sharing**: Your data stays on your system

## Limitations

### Important Disclaimers
- **Not a Medical Professional**: This system is for educational purposes only
- **Seek Professional Care**: Always consult healthcare providers for medical concerns
- **Emergency Situations**: Call emergency services for urgent medical needs
- **Accuracy Varies**: System accuracy depends on symptom selection and training data

### Technical Limitations
- **Symptom-Based Only**: Cannot analyze images, lab results, or physical exams
- **Training Data**: Limited to synthetic and literature-based data
- **Language**: Currently supports English only
- **Internet**: Requires local installation, not cloud-based

## System Architecture

### Machine Learning Models
1. **Random Forest**: Ensemble method for robust predictions
2. **Gradient Boosting**: Sequential learning for complex patterns
3. **XGBoost**: Advanced gradient boosting with high performance
4. **LightGBM**: Efficient gradient boosting for large datasets
5. **Neural Network**: Deep learning for non-linear relationships

### Reinforcement Learning
- **PPO Agent**: Learns from user feedback
- **Custom Environment**: Medical diagnosis simulation
- **Continuous Learning**: Improves with each feedback session

### Data Flow
1. **Symptom Input** → Feature Vector (88 dimensions)
2. **Ensemble Prediction** → 5 models vote on diagnosis
3. **Confidence Calculation** → Based on model agreement
4. **Result Generation** → Recommendations and alternatives
5. **Feedback Collection** → User rates accuracy
6. **Model Update** → RL agent learns from feedback

## File Structure Reference

```
bioai3/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                # Comprehensive documentation
├── USAGE_GUIDE.md           # This usage guide
├── 
├── ml_models/               # Machine learning components
│   ├── disease_predictor.py # Ensemble ML models
│   └── reinforcement_learner.py # RL system
├── 
├── data/                    # Training data and definitions
│   ├── symptoms.json        # 88 symptom definitions
│   ├── diseases.json        # 42 disease definitions
│   ├── training_data.csv    # 5000+ training samples
│   └── generate_training_data.py # Data generation script
├── 
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Home page with features
│   └── predict.html        # Prediction interface
├── 
├── static/                  # Static assets
│   ├── css/style.css       # Custom styling
│   └── js/main.js          # JavaScript functionality
├── 
├── models/                  # Saved ML models
│   ├── disease_models.pkl  # Trained ensemble models
│   └── rl_model.zip        # Reinforcement learning model
└── 
└── medical_predictions.db   # SQLite database
```

## Support and Contribution

### Getting Support
- Review this guide and README.md
- Check troubleshooting section
- Use system test endpoint for diagnostics
- Review console output for error messages

### Contributing
- Fork the repository
- Create feature branches
- Follow code standards (PEP 8)
- Add tests for new features
- Submit pull requests

---

**Remember**: This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, or treatment.