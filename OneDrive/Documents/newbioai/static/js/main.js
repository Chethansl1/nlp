document.addEventListener('DOMContentLoaded', function() {
    // Global variables
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const nextButtons = document.querySelectorAll('.next-btn');
    const prevButtons = document.querySelectorAll('.prev-btn');
    const analyzeButton = document.getElementById('analyze-btn');
    const restartButton = document.getElementById('restart-btn');
    const symptomSearch = document.getElementById('symptom-search');
    const symptomCheckboxes = document.getElementById('symptom-checkboxes');
    const selectedSymptomsList = document.getElementById('selected-symptoms-list');
    const printPrescriptionBtn = document.getElementById('print-prescription');
    
    // Navigation elements
    const navAssessment = document.getElementById('nav-assessment');
    const navHistory = document.getElementById('nav-history');
    const navAbout = document.getElementById('nav-about');
    const footerAssessment = document.getElementById('footer-assessment');
    const footerHistory = document.getElementById('footer-history');
    const footerAbout = document.getElementById('footer-about');
    
    // Section elements
    const assessmentSection = document.getElementById('assessment-section');
    const historySection = document.getElementById('history-section');
    const aboutSection = document.getElementById('about-section');
    
    // Charts
    let riskOverviewChart = null;
    let riskTrendChart = null;
    
    // Global data
    let symptoms = []; // Will store all available symptoms
    let selectedSymptoms = []; // Will store user selected symptoms
    let currentPredictionId = null; // Store the current prediction ID
    let currentPredictions = []; // Store the current predictions
    
    // Fetch all available symptoms from the backend
    fetchSymptoms();
    
    // Main navigation
    navAssessment.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('assessment');
    });
    
    navHistory.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('history');
        loadHistory();
    });
    
    navAbout.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('about');
    });
    
    // Footer navigation
    footerAssessment.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('assessment');
    });
    
    footerHistory.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('history');
        loadHistory();
    });
    
    footerAbout.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('about');
    });
    
    // Tab navigation
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            switchTab(tabId);
        });
    });
    
    // Next button navigation
    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            const nextTab = button.getAttribute('data-next');
            switchTab(nextTab);
        });
    });
    
    // Previous button navigation
    prevButtons.forEach(button => {
        button.addEventListener('click', () => {
            const prevTab = button.getAttribute('data-prev');
            switchTab(prevTab);
        });
    });
    
    // Analyze button click
    analyzeButton.addEventListener('click', () => {
        // Validate inputs
        if (!validateInputs()) {
            return;
        }
        
        // Show loading indicator with animated steps
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results-content').style.display = 'none';
        
        // Animate loading steps
        animateLoadingSteps();
        
        // Switch to results tab
        switchTab('results');
        
        // Collect all user input
        const userData = collectUserData();
        
        // Send data to backend for analysis
        analyzeRisk(userData);
    });
    
    // Print prescription button
    if (printPrescriptionBtn) {
        printPrescriptionBtn.addEventListener('click', () => {
            printPrescription();
        });
    }
    
    // Restart button click
    restartButton.addEventListener('click', () => {
        // Ask for confirmation
        Swal.fire({
            title: 'Start new assessment?',
            text: 'Your current assessment data will be lost.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#4a6fdc',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, start new'
        }).then((result) => {
            if (result.isConfirmed) {
                // Reset all form fields
                resetForms();
                
                // Reset selected symptoms
                selectedSymptoms = [];
                updateSelectedSymptomsList();
                
                // Switch to first tab
                switchTab('symptoms');
                
                // Success toast
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    icon: 'success',
                    title: 'Assessment reset',
                    showConfirmButton: false,
                    timer: 2000
                });
            }
        });
    });
    
    // Symptom search functionality
    symptomSearch.addEventListener('input', () => {
        const searchTerm = symptomSearch.value.toLowerCase();
        filterSymptoms(searchTerm);
    });
    
    // Function to show a specific section
    function showSection(section) {
        // Hide all sections
        assessmentSection.style.display = 'none';
        historySection.style.display = 'none';
        aboutSection.style.display = 'none';
        
        // Remove active class from all nav items
        navAssessment.classList.remove('active');
        navHistory.classList.remove('active');
        navAbout.classList.remove('active');
        
        // Show selected section and highlight nav item
        if (section === 'assessment') {
            assessmentSection.style.display = 'block';
            navAssessment.classList.add('active');
        } else if (section === 'history') {
            historySection.style.display = 'block';
            navHistory.classList.add('active');
        } else if (section === 'about') {
            aboutSection.style.display = 'block';
            navAbout.classList.add('active');
        }
    }
    
    // Function to validate inputs before submission
    function validateInputs() {
        if (selectedSymptoms.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: 'Missing Information',
                text: 'Please select at least one symptom to continue.',
                confirmButtonColor: '#4a6fdc'
            });
            switchTab('symptoms');
            return false;
        }
        
        const age = document.getElementById('age').value;
        if (!age) {
            Swal.fire({
                icon: 'warning',
                title: 'Missing Information',
                text: 'Please enter your age to continue.',
                confirmButtonColor: '#4a6fdc'
            });
            switchTab('demographics');
            return false;
        }
        
        return true;
    }
    
    // Function to animate loading steps
    function animateLoadingSteps() {
        const steps = document.querySelectorAll('.loading-steps .step');
        let currentStep = 0;
        
        // Reset all steps
        steps.forEach(step => step.classList.remove('active'));
        
        // Show first step
        if (steps.length > 0) {
            steps[0].classList.add('active');
        }
        
        // Animate through steps
        const stepInterval = setInterval(() => {
            currentStep++;
            
            if (currentStep < steps.length) {
                steps[currentStep].classList.add('active');
            } else {
                clearInterval(stepInterval);
            }
        }, 800);
    }
    
    // Function to switch tabs
    function switchTab(tabId) {
        // Update tab buttons
        tabButtons.forEach(btn => {
            if (btn.getAttribute('data-tab') === tabId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Update tab panes
        tabPanes.forEach(pane => {
            if (pane.id === `${tabId}-tab`) {
                pane.classList.add('active');
            } else {
                pane.classList.remove('active');
            }
        });
    }
    
    // Function to fetch symptoms from backend
    function fetchSymptoms() {
        fetch('/symptoms')
            .then(response => response.json())
            .then(data => {
                symptoms = data.symptoms;
                populateSymptomsList(symptoms);
            })
            .catch(error => {
                console.error('Error fetching symptoms:', error);
                // Fallback symptom list in case the backend is not available
                symptoms = [
                    "increased thirst", "frequent urination", "extreme hunger", 
                    "unexplained weight loss", "fatigue", "blurred vision",
                    "chest pain", "shortness of breath", "pain in arms",
                    "lightheadedness", "nausea", "chronic cough", "wheezing",
                    "chest tightness", "frequent respiratory infections",
                    "memory loss", "confusion", "difficulty with familiar tasks",
                    "language problems", "poor judgment", "mood changes",
                    "joint pain", "joint swelling", "joint stiffness",
                    "fever", "weight loss"
                ];
                populateSymptomsList(symptoms);
            });
    }
    
    // Function to populate the symptoms list
    function populateSymptomsList(symptomsList) {
        symptomCheckboxes.innerHTML = '';
        
        symptomsList.forEach(symptom => {
            const div = document.createElement('div');
            div.className = 'symptom-item';
            div.textContent = symptom;
            div.dataset.symptom = symptom;
            
            if (selectedSymptoms.includes(symptom)) {
                div.classList.add('selected');
            }
            
            div.addEventListener('click', () => toggleSymptom(symptom, div));
            
            symptomCheckboxes.appendChild(div);
        });
    }
    
    // Function to filter symptoms based on search
    function filterSymptoms(searchTerm) {
        const filteredSymptoms = symptoms.filter(symptom => 
            symptom.toLowerCase().includes(searchTerm)
        );
        populateSymptomsList(filteredSymptoms);
    }
    
    // Function to toggle symptom selection
    function toggleSymptom(symptom, element) {
        const index = selectedSymptoms.indexOf(symptom);
        
        if (index === -1) {
            // Add symptom
            selectedSymptoms.push(symptom);
            element.classList.add('selected');
        } else {
            // Remove symptom
            selectedSymptoms.splice(index, 1);
            element.classList.remove('selected');
        }
        
        updateSelectedSymptomsList();
    }
    
    // Function to update the selected symptoms list
    function updateSelectedSymptomsList() {
        selectedSymptomsList.innerHTML = '';
        
        if (selectedSymptoms.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'No symptoms selected';
            li.style.backgroundColor = 'transparent';
            li.style.color = 'var(--text-muted)';
            selectedSymptomsList.appendChild(li);
            return;
        }
        
        selectedSymptoms.forEach(symptom => {
            const li = document.createElement('li');
            li.textContent = symptom;
            
            const removeButton = document.createElement('span');
            removeButton.className = 'remove-symptom';
            removeButton.textContent = ' ×';
            removeButton.addEventListener('click', () => {
                const index = selectedSymptoms.indexOf(symptom);
                if (index !== -1) {
                    selectedSymptoms.splice(index, 1);
                    updateSelectedSymptomsList();
                    
                    // Also update the checkboxes display
                    const symptomElements = document.querySelectorAll('.symptom-item');
                    symptomElements.forEach(el => {
                        if (el.dataset.symptom === symptom) {
                            el.classList.remove('selected');
                        }
                    });
                }
            });
            
            li.appendChild(removeButton);
            selectedSymptomsList.appendChild(li);
        });
    }
    
    // Function to collect all user input data
    function collectUserData() {
        // Get demographics data
        const age = document.getElementById('age').value;
        const gender = document.getElementById('gender').value;
        const height = document.getElementById('height').value;
        const weight = document.getElementById('weight').value;
        const smoking = document.querySelector('input[name="smoking"]:checked').value;
        const physicalActivity = document.getElementById('physical-activity').value;
        
        // Get family history
        const familyHistory = [];
        document.querySelectorAll('#family-history input:checked').forEach(input => {
            familyHistory.push(input.value);
        });
        
        // We've removed medical data input
        
        return {
            symptoms: selectedSymptoms,
            demographics: {
                age: parseInt(age) || 0,
                gender: gender,
                height: parseFloat(height) || 0,
                weight: parseFloat(weight) || 0,
                smoking: smoking,
                physical_activity: physicalActivity,
                family_history: familyHistory
            }
        };
    }
    
    // Function to send data to backend and analyze risk
    function analyzeRisk(userData) {
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Store prediction ID for future feedback
                currentPredictionId = data.prediction_id;
                displayResults(data.predictions);
                
                // Show success notification
                Swal.fire({
                    toast: true,
                    position: 'top-end',
                    icon: 'success',
                    title: 'Analysis complete',
                    text: 'Your risk assessment has been generated',
                    showConfirmButton: false,
                    timer: 3000
                });
            } else {
                displayError(data.message);
            }
        })
        .catch(error => {
            console.error('Error analyzing risk:', error);
            displayError('Failed to analyze your health data. Please try again.');
            
            // For demonstration, show mock results when backend is not available
            const mockPredictions = generateMockPredictions();
            setTimeout(() => {
                // Add graph data to mock predictions
                mockPredictions.forEach(prediction => {
                    prediction.graph_data = {
                        risk_over_time: {
                            labels: ['6 months ago', '3 months ago', '1 month ago', 'Current'],
                            data: [
                                Math.max(0, prediction.risk_percentage - Math.random() * 20),
                                Math.max(0, prediction.risk_percentage - Math.random() * 15),
                                Math.max(0, prediction.risk_percentage - Math.random() * 10),
                                prediction.risk_percentage
                            ]
                        }
                    };
                    
                    // Add trend data
                    if (prediction.risk_percentage > 60) {
                        prediction.trend = {
                            direction: 'increasing',
                            analysis: 'Your risk appears to be increasing over time.'
                        };
                    } else if (prediction.risk_percentage > 30) {
                        prediction.trend = {
                            direction: 'stable',
                            analysis: 'Your risk appears to be stable over time.'
                        };
                    } else {
                        prediction.trend = {
                            direction: 'decreasing',
                            analysis: 'Your risk appears to be decreasing over time.'
                        };
                    }
                    
                    // Add progression stage
                    if (prediction.risk_percentage > 60) {
                        prediction.progression_stage = 'Advanced';
                    } else if (prediction.risk_percentage > 30) {
                        prediction.progression_stage = 'Moderate';
                    } else {
                        prediction.progression_stage = 'Early';
                    }
                    
                    // Add treatments
                    prediction.treatments = [
                        'Medication therapy',
                        'Lifestyle modifications',
                        'Regular monitoring',
                        'Dietary changes',
                        'Exercise regimen'
                    ];
                });
                
                displayResults(mockPredictions);
            }, 2000);
        })
        .finally(() => {
            // Hide loading indicator after delay for better UX
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('results-content').style.display = 'block';
            }, 1500);
        });
    }
    
    // Function to load user history
    function loadHistory() {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '<div class="loading-container"><div class="loading-spinner"></div><p>Loading your history...</p></div>';
        
        fetch('/history')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayHistory(data.history);
                } else {
                    historyList.innerHTML = '<div class="error-message"><i class="fas fa-exclamation-circle"></i><p>Failed to load your history.</p></div>';
                }
            })
            .catch(error => {
                console.error('Error fetching history:', error);
                historyList.innerHTML = '<div class="error-message"><i class="fas fa-exclamation-circle"></i><p>Failed to load your history.</p></div>';
                
                // Show mock history for demo purposes
                setTimeout(() => {
                    const mockHistory = [
                        {
                            id: 'mock-1',
                            timestamp: new Date().toISOString(),
                            summary: [
                                { disease: 'Diabetes Type 2', risk: 68.5, level: 'High' },
                                { disease: 'Coronary Heart Disease', risk: 42.3, level: 'Moderate' },
                                { disease: 'Hypertension', risk: 37.8, level: 'Moderate' }
                            ]
                        },
                        {
                            id: 'mock-2',
                            timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
                            summary: [
                                { disease: 'Diabetes Type 2', risk: 72.1, level: 'High' },
                                { disease: 'Coronary Heart Disease', risk: 45.6, level: 'Moderate' },
                                { disease: 'Hypertension', risk: 40.2, level: 'Moderate' }
                            ]
                        }
                    ];
                    displayHistory(mockHistory);
                }, 1000);
            });
    }
    
    // Function to display history
    function displayHistory(history) {
        const historyList = document.getElementById('history-list');
        
        if (history.length === 0) {
            historyList.innerHTML = '<div class="empty-history"><p>You have no previous assessments.</p><button id="start-assessment-btn" class="next-btn">Start New Assessment</button></div>';
            
            document.getElementById('start-assessment-btn').addEventListener('click', () => {
                showSection('assessment');
            });
            
            return;
        }
        
        historyList.innerHTML = '';
        
        const template = document.getElementById('history-item-template').innerHTML;
        
        history.forEach(item => {
            const date = new Date(item.timestamp);
            
            // Use template literals for simple templating
            let html = template.replace('${id}', item.id).replace('${date}', date.toLocaleString());
            
            // Create temp div to convert string to DOM elements
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            const historyItem = tempDiv.firstElementChild;
            
            // Add risk badges
            const riskBadgesContainer = historyItem.querySelector(`#risk-badges-${item.id}`);
            
            item.summary.forEach(risk => {
                const riskBadge = document.createElement('div');
                riskBadge.className = `risk-badge ${risk.level}`;
                riskBadge.textContent = `${risk.disease}: ${risk.risk}%`;
                riskBadgesContainer.appendChild(riskBadge);
            });
            
            // Add event listener to view details button
            historyItem.querySelector('.view-details-btn').addEventListener('click', () => {
                viewHistoryDetails(item.id);
            });
            
            historyList.appendChild(historyItem);
        });
    }
    
    // Function to view history details
    function viewHistoryDetails(id) {
        // In a real app, this would fetch the specific assessment
        // For demo, we'll show a modal with info
        Swal.fire({
            title: 'Assessment Details',
            html: `
                <div class="history-details">
                    <p>Assessment ID: ${id}</p>
                    <p>This feature would show the complete assessment details from your history.</p>
                </div>
            `,
            showCancelButton: true,
            confirmButtonText: 'Compare with Current',
            cancelButtonText: 'Close',
            confirmButtonColor: '#4a6fdc'
        }).then((result) => {
            if (result.isConfirmed) {
                showSection('assessment');
            }
        });
    }
    
    // Function to create and update charts
    function updateCharts(predictions) {
        // Destroy existing charts if they exist
        if (riskOverviewChart) {
            riskOverviewChart.destroy();
        }
        
        if (riskTrendChart) {
            riskTrendChart.destroy();
        }
        
        // Create risk overview chart
        const overviewCtx = document.getElementById('risk-overview-chart').getContext('2d');
        
        const diseases = predictions.map(p => p.disease);
        const riskValues = predictions.map(p => p.risk_percentage);
        const backgroundColors = predictions.map(p => {
            if (p.risk_level === 'High') return 'rgba(231, 76, 60, 0.7)';
            if (p.risk_level === 'Moderate') return 'rgba(243, 156, 18, 0.7)';
            if (p.risk_level === 'Low') return 'rgba(39, 174, 96, 0.7)';
            return 'rgba(52, 152, 219, 0.7)';
        });
        
        riskOverviewChart = new Chart(overviewCtx, {
            type: 'bar',
            data: {
                labels: diseases,
                datasets: [{
                    label: 'Risk Percentage',
                    data: riskValues,
                    backgroundColor: backgroundColors,
                    borderColor: backgroundColors.map(c => c.replace('0.7', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Risk (%)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Disease Risk Overview',
                        font: {
                            size: 16
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Create risk trend chart
        const trendCtx = document.getElementById('risk-trend-chart').getContext('2d');
        
        // Get trend data from highest risk disease
        const highestRisk = predictions[0];
        const trendData = highestRisk.graph_data.risk_over_time;
        
        riskTrendChart = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendData.labels,
                datasets: [{
                    label: highestRisk.disease,
                    data: trendData.data,
                    borderColor: getColorForRiskLevel(highestRisk.risk_level),
                    backgroundColor: getColorForRiskLevel(highestRisk.risk_level, 0.1),
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Risk (%)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Risk Trend Analysis',
                        font: {
                            size: 16
                        }
                    }
                }
            }
        });
    }
    
    // Function to get color for risk level
    function getColorForRiskLevel(level, alpha = 1) {
        switch(level) {
            case 'High':
                return `rgba(231, 76, 60, ${alpha})`;
            case 'Moderate':
                return `rgba(243, 156, 18, ${alpha})`;
            case 'Low':
                return `rgba(39, 174, 96, ${alpha})`;
            default:
                return `rgba(52, 152, 219, ${alpha})`;
        }
    }
    
    // Function to get icon for disease
    function getDiseaseIcon(disease) {
        const diseaseIcons = {
            'Diabetes Type 2': 'fa-syringe',
            'Coronary Heart Disease': 'fa-heart',
            'Chronic Obstructive Pulmonary Disease': 'fa-lungs',
            'Alzheimer\'s Disease': 'fa-brain',
            'Rheumatoid Arthritis': 'fa-bone',
            'Hypertension': 'fa-heartbeat',
            'Depression': 'fa-cloud-rain'
        };
        
        return diseaseIcons[disease] || 'fa-file-medical';
    }
    
    // Function to display results
    function displayResults(predictions) {
        // Store current predictions globally
        currentPredictions = predictions;
        
        // Update the charts
        updateCharts(predictions);
        
        // Display the detailed results
        const resultsContainer = document.getElementById('risk-results');
        resultsContainer.innerHTML = '';
        
        predictions.forEach(prediction => {
            const riskCard = document.createElement('div');
            riskCard.className = 'risk-card';
            
            // Add risk level class
            if (prediction.risk_level === 'High') {
                riskCard.classList.add('high-risk');
            } else if (prediction.risk_level === 'Moderate') {
                riskCard.classList.add('moderate-risk');
            } else if (prediction.risk_level === 'Low') {
                riskCard.classList.add('low-risk');
            } else {
                riskCard.classList.add('minimal-risk');
            }
            
            // Risk header
            const riskHeader = document.createElement('div');
            riskHeader.className = 'risk-header';
            
            const diseaseNameDiv = document.createElement('div');
            diseaseNameDiv.className = 'risk-disease';
            
            // Add icon to disease name
            const diseaseIcon = document.createElement('i');
            diseaseIcon.className = `fas ${getDiseaseIcon(prediction.disease)}`;
            diseaseNameDiv.appendChild(diseaseIcon);
            
            const diseaseName = document.createTextNode(prediction.disease);
            diseaseNameDiv.appendChild(diseaseName);
            
            // Add progression stage if available
            if (prediction.progression_stage) {
                const stageSpan = document.createElement('span');
                stageSpan.className = 'risk-stage';
                stageSpan.textContent = prediction.progression_stage + ' Stage';
                diseaseNameDiv.appendChild(stageSpan);
            }
            
            const riskPercentageDiv = document.createElement('div');
            riskPercentageDiv.className = 'risk-percentage';
            riskPercentageDiv.textContent = `${prediction.risk_percentage}%`;
            
            riskHeader.appendChild(diseaseNameDiv);
            riskHeader.appendChild(riskPercentageDiv);
            
            // Risk level indicator
            const riskLevelDiv = document.createElement('div');
            riskLevelDiv.className = 'risk-level ' + prediction.risk_level.toLowerCase();
            riskLevelDiv.textContent = prediction.risk_level + ' Risk';
            
            // Add trend indicator if available
            if (prediction.trend) {
                const trendDiv = document.createElement('div');
                trendDiv.className = 'risk-trend';
                
                const trendIcon = document.createElement('i');
                trendIcon.className = 'fas trend-icon';
                
                if (prediction.trend.direction === 'increasing') {
                    trendIcon.className += ' fa-arrow-trend-up trend-increasing';
                } else if (prediction.trend.direction === 'decreasing') {
                    trendIcon.className += ' fa-arrow-trend-down trend-decreasing';
                } else {
                    trendIcon.className += ' fa-arrow-right trend-stable';
                }
                
                trendDiv.appendChild(trendIcon);
                trendDiv.appendChild(document.createTextNode(prediction.trend.analysis));
                
                riskCard.appendChild(trendDiv);
            }
            
            // Risk bar
            const riskBarContainer = document.createElement('div');
            riskBarContainer.className = 'risk-bar-container';
            
            const riskBar = document.createElement('div');
            riskBar.className = 'risk-bar';
            if (prediction.risk_level === 'High') {
                riskBar.classList.add('high-risk');
            } else if (prediction.risk_level === 'Moderate') {
                riskBar.classList.add('moderate-risk');
            } else {
                riskBar.classList.add('low-risk');
            }
            
            // Animate the width
            riskBar.style.width = '0%';
            setTimeout(() => {
                riskBar.style.width = `${prediction.risk_percentage}%`;
            }, 100);
            
            riskBarContainer.appendChild(riskBar);
            
            // Contributing factors
            const factorsDiv = document.createElement('div');
            factorsDiv.className = 'risk-factors';
            
            const factorsTitle = document.createElement('h4');
            
            // Add icon to factors title
            const factorsIcon = document.createElement('i');
            factorsIcon.className = 'fas fa-list-check';
            factorsTitle.appendChild(factorsIcon);
            
            factorsTitle.appendChild(document.createTextNode('Contributing Factors'));
            
            const factorsList = document.createElement('ul');
            
            if (prediction.contributing_factors && prediction.contributing_factors.length > 0) {
                prediction.contributing_factors.forEach(factor => {
                    const factorItem = document.createElement('li');
                    factorItem.textContent = factor;
                    factorsList.appendChild(factorItem);
                });
            } else {
                const factorItem = document.createElement('li');
                factorItem.textContent = 'No significant factors identified';
                factorsList.appendChild(factorItem);
            }
            
            factorsDiv.appendChild(factorsTitle);
            factorsDiv.appendChild(factorsList);
            
            // Treatment recommendations
            if (prediction.treatments && prediction.treatments.length > 0) {
                const treatmentsDiv = document.createElement('div');
                treatmentsDiv.className = 'risk-treatments';
                
                const treatmentsTitle = document.createElement('h4');
                
                // Add icon to treatments title
                const treatmentsIcon = document.createElement('i');
                treatmentsIcon.className = 'fas fa-pills';
                treatmentsTitle.appendChild(treatmentsIcon);
                
                treatmentsTitle.appendChild(document.createTextNode('Recommended Treatments'));
                
                const treatmentChips = document.createElement('div');
                treatmentChips.className = 'treatment-chips';
                
                prediction.treatments.forEach(treatment => {
                    const chip = document.createElement('div');
                    chip.className = 'treatment-chip';
                    
                    const chipIcon = document.createElement('i');
                    
                    if (treatment.includes('medication') || treatment.includes('therapy')) {
                        chipIcon.className = 'fas fa-capsules';
                    } else if (treatment.includes('exercise') || treatment.includes('physical')) {
                        chipIcon.className = 'fas fa-dumbbell';
                    } else if (treatment.includes('diet') || treatment.includes('nutrition')) {
                        chipIcon.className = 'fas fa-apple-alt';
                    } else {
                        chipIcon.className = 'fas fa-check-circle';
                    }
                    
                    chip.appendChild(chipIcon);
                    chip.appendChild(document.createTextNode(treatment));
                    
                    treatmentChips.appendChild(chip);
                });
                
                treatmentsDiv.appendChild(treatmentsTitle);
                treatmentsDiv.appendChild(treatmentChips);
                
                // Add prescription button
                const prescriptionBtn = document.createElement('button');
                prescriptionBtn.className = 'prescription-btn';
                prescriptionBtn.innerHTML = '<i class="fas fa-file-prescription"></i> View Full Prescription';
                prescriptionBtn.addEventListener('click', () => {
                    generatePrescription(prediction.disease);
                });
                
                treatmentsDiv.appendChild(prescriptionBtn);
            }
            
            // Assemble the card
            riskCard.appendChild(riskHeader);
            riskCard.appendChild(riskLevelDiv);
            riskCard.appendChild(riskBarContainer);
            riskCard.appendChild(factorsDiv);
            
            if (prediction.treatments && prediction.treatments.length > 0) {
                riskCard.appendChild(treatmentsDiv);
            }
            
            resultsContainer.appendChild(riskCard);
        });
        
        // Generate prescription for the highest risk disease
        if (predictions.length > 0) {
            generatePrescription(predictions[0].disease);
        }
    }
    
    // Function to generate a prescription
    function generatePrescription(diseaseName) {
        // Show loading in prescription section
        const prescriptionContent = document.getElementById('prescription-content');
        prescriptionContent.innerHTML = '<div class="loading-container"><div class="loading-spinner"></div><p>Generating personalized prescription...</p></div>';
        
        // Fetch prescription from backend
        fetch(`/prescription/${encodeURIComponent(diseaseName)}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    displayPrescription(data.prescription);
                } else {
                    prescriptionContent.innerHTML = '<div class="error-message"><p>Failed to generate prescription. Please try again.</p></div>';
                }
            })
            .catch(error => {
                console.error('Error generating prescription:', error);
                
                // For demonstration, show a mock prescription
                setTimeout(() => {
                    const mockPrescription = {
                        disease: diseaseName,
                        treatments: currentPredictions.find(p => p.disease === diseaseName)?.treatments || [],
                        lifestyle_modifications: [
                            "Regular physical activity (30 minutes daily)",
                            "Balanced diet with reduced processed foods",
                            "Stress management techniques",
                            "Adequate sleep (7-9 hours)"
                        ],
                        follow_up_recommendations: [
                            "Schedule follow-up appointment in 3 months",
                            "Complete recommended laboratory tests",
                            "Monitor symptoms and report any changes"
                        ]
                    };
                    
                    displayPrescription(mockPrescription);
                }, 1000);
            });
    }
    
    // Function to display prescription
    function displayPrescription(prescription) {
        const prescriptionContent = document.getElementById('prescription-content');
        
        // Get the template
        let template = document.getElementById('prescription-template').innerHTML;
        
        // Determine the disease name - could be in different properties depending on data source
        const diseaseName = prescription.disease_name || prescription.disease || "Medical Condition";
        const riskLevel = prescription.risk_level || "High";
        
        // Replace placeholders
        template = template.replace('${disease}', diseaseName);
        template = template.replace('${date}', new Date().toLocaleDateString());
        
        // Set the HTML
        prescriptionContent.innerHTML = template;
        
        // Add warning banner if present
        if (prescription.warning) {
            const warningDiv = document.createElement('div');
            warningDiv.className = 'prescription-warning';
            warningDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${prescription.warning}`;
            prescriptionContent.querySelector('.prescription-header').appendChild(warningDiv);
        }
        
        // Add risk level indicator
        const headerDiv = prescriptionContent.querySelector('.prescription-header h4');
        headerDiv.innerHTML = `${diseaseName} Management Plan <span class="risk-badge ${riskLevel.toLowerCase()}">${riskLevel} Risk</span>`;
        
        // Now populate the lists using DOM manipulation
        const treatmentsList = prescriptionContent.querySelector('#treatment-list');
        const lifestyleList = prescriptionContent.querySelector('#lifestyle-list');
        const followupList = prescriptionContent.querySelector('#followup-list');
        
        // Add a medications section if available
        let medicationsList = null;
        if (prescription.medications && prescription.medications.length > 0) {
            // Create medications section
            const medSection = document.createElement('div');
            medSection.className = 'prescription-section';
            medSection.innerHTML = '<h5><i class="fas fa-capsules"></i> Medications & Treatments</h5>';
            
            medicationsList = document.createElement('ul');
            medicationsList.className = 'medications-list';
            medSection.appendChild(medicationsList);
            
            // Insert after lifestyle modifications section
            const lifestyleSection = lifestyleList.parentNode;
            lifestyleSection.parentNode.insertBefore(medSection, lifestyleSection.nextSibling);
        }
        
        // Add treatments (general recommendations)
        if (prescription.treatments && prescription.treatments.length > 0) {
            prescription.treatments.forEach((treatment, index) => {
                // Skip the first two items if they're the DIAGNOSIS and TREATMENT PLAN headers
                if (index > 1 || (!treatment.includes('DIAGNOSIS') && !treatment.includes('TREATMENT PLAN'))) {
                    const li = document.createElement('li');
                    li.textContent = treatment;
                    
                    // Apply styling for urgent items
                    if (treatment.includes('URGENT')) {
                        li.className = 'urgent-item';
                    }
                    
                    treatmentsList.appendChild(li);
                }
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No specific treatments recommended at this time';
            treatmentsList.appendChild(li);
        }
        
        // Add lifestyle modifications
        if (prescription.lifestyle_modifications && prescription.lifestyle_modifications.length > 0) {
            prescription.lifestyle_modifications.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                
                // Apply styling for urgent items
                if (item.includes('URGENT')) {
                    li.className = 'urgent-item';
                }
                
                lifestyleList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No specific lifestyle modifications recommended at this time';
            lifestyleList.appendChild(li);
        }
        
        // Add medications if available
        if (medicationsList && prescription.medications && prescription.medications.length > 0) {
            prescription.medications.forEach(med => {
                const li = document.createElement('li');
                li.textContent = med;
                medicationsList.appendChild(li);
            });
        }
        
        // Add follow-up recommendations
        if (prescription.follow_up_recommendations && prescription.follow_up_recommendations.length > 0) {
            prescription.follow_up_recommendations.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                followupList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Follow up with your healthcare provider as needed';
            followupList.appendChild(li);
        }
    }
    
    // Function to print prescription
    function printPrescription() {
        const prescriptionElement = document.getElementById('prescription-content');
        
        if (!prescriptionElement) {
            return;
        }
        
        // Create a more professional print view
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
            <head>
                <title>MediPredict AI - Medical Prescription</title>
                <style>
                    @page { size: 8.5in 11in; margin: 0.5in; }
                    body { 
                        font-family: Arial, sans-serif; 
                        padding: 20px;
                        color: #2c3e50;
                        line-height: 1.5;
                    }
                    .prescription { 
                        max-width: 800px; 
                        margin: 0 auto; 
                        padding: 30px; 
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                    .prescription-header { 
                        display: flex; 
                        justify-content: space-between; 
                        margin-bottom: 20px; 
                        padding-bottom: 15px; 
                        border-bottom: 2px solid #4a6fdc; 
                    }
                    .prescription-header h4 {
                        font-size: 1.5rem;
                        margin: 0;
                        color: #4a6fdc;
                    }
                    .prescription-date {
                        color: #7f8c8d;
                    }
                    .prescription-section { 
                        margin-bottom: 25px; 
                    }
                    .prescription-section h5 { 
                        margin-bottom: 15px; 
                        color: #3a5abb;
                        border-bottom: 1px solid #eee;
                        padding-bottom: 8px;
                    }
                    .prescription-section ul { 
                        padding-left: 20px; 
                        margin: 0;
                    }
                    .prescription-section li {
                        margin-bottom: 8px;
                    }
                    .prescription-footer { 
                        margin-top: 30px; 
                        padding-top: 15px; 
                        border-top: 1px solid #ccc; 
                        font-size: 0.9em; 
                        color: #7f8c8d; 
                    }
                    .footer-note {
                        text-align: center;
                        margin-top: 40px;
                        color: #95a5a6;
                        font-size: 0.9em;
                        border-top: 1px dashed #ddd;
                        padding-top: 15px;
                    }
                    .logo {
                        text-align: center;
                        margin-bottom: 20px;
                        font-size: 1.8rem;
                        color: #4a6fdc;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="logo">MediPredict AI</div>
                ${prescriptionElement.innerHTML}
                <div class="footer-note">
                    <p>Generated by MediPredict AI - ${new Date().toLocaleString()}</p>
                    <p>This prescription is computer-generated and for informational purposes only.<br>
                    Please consult with a healthcare professional before making any changes to your health regimen.</p>
                </div>
            </body>
            </html>
        `);
        
        // Wait for content to load
        setTimeout(() => {
            printWindow.print();
            setTimeout(() => {
                printWindow.close();
            }, 500);
        }, 500);
    }
    
    // Function to display error
    function displayError(message) {
        const resultsContainer = document.getElementById('risk-results');
        resultsContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                <p>${message}</p>
                <p>Please try again or contact support if the problem persists.</p>
            </div>
        `;
    }
    
    // Function to reset all form fields
    function resetForms() {
        // Reset demographics
        document.getElementById('age').value = '';
        document.getElementById('gender').value = '';
        document.getElementById('height').value = '';
        document.getElementById('weight').value = '';
        document.querySelector('input[name="smoking"][value="no"]').checked = true;
        document.getElementById('physical-activity').value = 'low';
        
        // Reset family history
        document.querySelectorAll('#family-history input').forEach(input => {
            input.checked = false;
        });
        
        // Reset medical data
        document.getElementById('blood-glucose').value = '';
        document.getElementById('cholesterol').value = '';
        document.getElementById('systolic').value = '';
        document.getElementById('diastolic').value = '';
        document.getElementById('triglycerides').value = '';
        document.getElementById('hba1c').value = '';
        document.getElementById('crp').value = '';
        document.getElementById('esr').value = '';
        
        // Reset symptom search
        document.getElementById('symptom-search').value = '';
        filterSymptoms('');
    }
    
    // Function to generate mock predictions for demonstration
    function generateMockPredictions() {
        // This is only used when the backend is not available
        const mockData = [
            {
                disease: "Diabetes Type 2",
                risk_percentage: 78.5,
                risk_level: "High",
                contributing_factors: [
                    "Reported symptoms: increased thirst, frequent urination, blurred vision",
                    "Risk factors: Age, Family History, Physical inactivity",
                    "Biomarkers: Elevated blood glucose, elevated HbA1c"
                ]
            },
            {
                disease: "Coronary Heart Disease",
                risk_percentage: 52.3,
                risk_level: "Moderate",
                contributing_factors: [
                    "Risk factors: Age, Physical inactivity, High cholesterol",
                    "Biomarkers: Elevated blood pressure, elevated triglycerides",
                    "Symptoms: Occasional chest discomfort"
                ]
            },
            {
                disease: "Hypertension",
                risk_percentage: 47.9,
                risk_level: "Moderate",
                contributing_factors: [
                    "Biomarkers: Elevated blood pressure readings",
                    "Risk factors: Family history, stress levels",
                    "Lifestyle: Dietary sodium intake"
                ]
            },
            {
                disease: "Chronic Obstructive Pulmonary Disease",
                risk_percentage: 25.7,
                risk_level: "Low",
                contributing_factors: [
                    "Reported symptoms: shortness of breath, occasional coughing",
                    "Environmental factors: Past exposure to pollutants"
                ]
            },
            {
                disease: "Alzheimer's Disease",
                risk_percentage: 18.3,
                risk_level: "Low",
                contributing_factors: [
                    "Risk factors: Age",
                    "Family history: No known genetic predisposition"
                ]
            },
            {
                disease: "Depression",
                risk_percentage: 12.5,
                risk_level: "Low",
                contributing_factors: [
                    "Reported symptoms: Occasional fatigue",
                    "Lifestyle: Work-related stress"
                ]
            },
            {
                disease: "Rheumatoid Arthritis",
                risk_percentage: 6.8,
                risk_level: "Minimal",
                contributing_factors: [
                    "No significant contributing factors identified"
                ]
            }
        ];
        
        return mockData;
    }
    
    // Function to provide feedback to the AI model
    function provideFeedback(actualDiagnoses) {
        if (!currentPredictionId) {
            console.error('No prediction ID available for feedback');
            return;
        }
        
        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prediction_id: currentPredictionId,
                actual_diagnoses: actualDiagnoses
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Feedback provided successfully');
            } else {
                console.error('Failed to provide feedback:', data.message);
            }
        })
        .catch(error => {
            console.error('Error providing feedback:', error);
        });
    }
});