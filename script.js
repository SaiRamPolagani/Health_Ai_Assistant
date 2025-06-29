// Symptom Analysis
function analyzeSymptoms() {
    const symptoms = document.getElementById('symptoms-input').value.trim();
    
    if (symptoms) {
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symptoms: symptoms })
        })
        .then(response => response.json())
        .then(data => {
            displayFullAnalysis(data.prediction.predicted_disease);
            updateCharts(symptoms);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('analysis-result').innerHTML = `
                <div class="alert alert-danger">Error processing request</div>
            `;
        });
    }
}

// Display full Gemini response directly
function displayFullAnalysis(text) {
    const resultDiv = document.getElementById('analysis-result');

    resultDiv.innerHTML = `
        <div class="alert alert-info mt-4">
            <h4 class="alert-heading">Analysis Results</h4>
            <p>${text.replace(/\n/g, "<br>")}</p>
        </div>
    `;
}

// Dashboard Charts
function initializeCharts() {
    // Symptoms Chart
    const symptomsCtx = document.getElementById('symptomsChart').getContext('2d');
    new Chart(symptomsCtx, {
        type: 'bar',
        data: {
            labels: ['Headache', 'Fever', 'Cough', 'Fatigue', 'Body Pain'],
            datasets: [{
                label: 'Symptom Frequency',
                data: [12, 19, 8, 15, 10],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Health Trends Chart
    const trendsCtx = document.getElementById('trendsChart').getContext('2d');
    new Chart(trendsCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Overall Health Score',
                data: [75, 78, 80, 79, 85, 83],
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Update charts with new data (placeholder)
function updateCharts(symptoms) {
    // You can update charts dynamically here based on symptoms
}

// Initialize charts on page load
document.addEventListener('DOMContentLoaded', initializeCharts);
