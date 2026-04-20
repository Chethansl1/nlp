// Main JavaScript file for MedAI Disease Prediction System

// Global variables
let currentStats = null;
let chartInstances = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize animations
    initializeAnimations();
    
    // Load initial data
    loadInitialData();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeAnimations() {
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .step-card, .stat-item').forEach(el => {
        observer.observe(el);
    });
}

function loadInitialData() {
    // Load any initial data needed
    if (typeof loadHomeStats === 'function') {
        loadHomeStats();
    }
}

// Statistics functionality
async function showStats() {
    const modal = new bootstrap.Modal(document.getElementById('statsModal'));
    modal.show();
    
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (response.ok) {
            displayStats(data);
            currentStats = data;
        } else {
            throw new Error(data.error || 'Failed to load statistics');
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('statsContent').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error loading statistics: ${error.message}
            </div>
        `;
    }
}

function displayStats(data) {
    const statsContent = document.getElementById('statsContent');
    
    const html = `
        <div class="row g-4">
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-icon bg-primary">
                        <i class="fas fa-chart-bar"></i>
                    </div>
                    <div class="stat-info">
                        <h3>${data.total_predictions || 0}</h3>
                        <p>Total Predictions</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-icon bg-success">
                        <i class="fas fa-percentage"></i>
                    </div>
                    <div class="stat-info">
                        <h3>${Math.round((data.average_confidence || 0) * 100)}%</h3>
                        <p>Average Confidence</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-icon bg-info">
                        <i class="fas fa-star"></i>
                    </div>
                    <div class="stat-info">
                        <h3>${(data.average_feedback || 0).toFixed(1)}/5</h3>
                        <p>Average Rating</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="stat-card">
                    <div class="stat-icon bg-warning">
                        <i class="fas fa-clock"></i>
                    </div>
                    <div class="stat-info">
                        <h3>24/7</h3>
                        <p>Available</p>
                    </div>
                </div>
            </div>
        </div>
        
        ${data.top_diseases && data.top_diseases.length > 0 ? `
            <div class="mt-4">
                <h5>Most Common Predictions</h5>
                <div class="chart-container">
                    <canvas id="diseaseChart" width="400" height="200"></canvas>
                </div>
            </div>
        ` : ''}
        
        <div class="mt-4">
            <div class="row">
                <div class="col-md-6">
                    <div class="info-box">
                        <h6><i class="fas fa-robot me-2"></i>AI Models</h6>
                        <p>Using ensemble of 5 advanced ML models including Random Forest, XGBoost, and Neural Networks</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-box">
                        <h6><i class="fas fa-brain me-2"></i>Reinforcement Learning</h6>
                        <p>Continuously improving through user feedback and real-world validation</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    statsContent.innerHTML = html;
    
    // Create chart if data available
    if (data.top_diseases && data.top_diseases.length > 0) {
        createDiseaseChart(data.top_diseases);
    }
}

function createDiseaseChart(diseaseData) {
    const ctx = document.getElementById('diseaseChart');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (chartInstances.diseaseChart) {
        chartInstances.diseaseChart.destroy();
    }
    
    const labels = diseaseData.map(d => d.disease);
    const counts = diseaseData.map(d => d.count);
    
    chartInstances.diseaseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#FF6384',
                    '#C9CBCF',
                    '#4BC0C0',
                    '#FF6384'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Utility functions
function showLoading(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) {
        element.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading...</p>
            </div>
        `;
    }
}

function showError(element, message) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) {
        element.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// API helper functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Form validation
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Local storage helpers
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Performance monitoring
function measurePerformance(name, fn) {
    return async function(...args) {
        const start = performance.now();
        try {
            const result = await fn.apply(this, args);
            const end = performance.now();
            console.log(`${name} took ${(end - start).toFixed(2)} milliseconds`);
            return result;
        } catch (error) {
            const end = performance.now();
            console.error(`${name} failed after ${(end - start).toFixed(2)} milliseconds:`, error);
            throw error;
        }
    };
}

// Export functions for use in other scripts
window.MedAI = {
    showStats,
    showLoading,
    showError,
    showNotification,
    apiRequest,
    validateForm,
    saveToLocalStorage,
    loadFromLocalStorage,
    formatDate,
    debounce,
    measurePerformance
};

// Add CSS for stat cards
const style = document.createElement('style');
style.textContent = `
    .stat-card {
        display: flex;
        align-items: center;
        padding: 1.5rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
    }
    
    .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        color: white;
        font-size: 1.5rem;
    }
    
    .stat-info h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
        color: #333;
    }
    
    .stat-info p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    .info-box {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    
    .info-box h6 {
        color: #007bff;
        margin-bottom: 0.5rem;
    }
    
    .info-box p {
        margin: 0;
        font-size: 0.9rem;
        color: #666;
    }
    
    .chart-container {
        position: relative;
        height: 300px;
        margin-top: 1rem;
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;

document.head.appendChild(style);