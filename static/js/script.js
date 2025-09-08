// MediPredict main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const predictForm = document.getElementById('predict-form');
    const resultSection = document.getElementById('result-section');
    const diseaseName = document.getElementById('disease-name');
    const confidenceValue = document.getElementById('confidence-value');
    const relatedSymptomsList = document.getElementById('related-symptoms-list');
    const searchInput = document.getElementById('symptom-search');
    const clearBtn = document.getElementById('clear-btn');

    console.log("MediPredict JS loaded");
    
    // Load available symptoms
    loadSymptoms();
    
    // Form submission
    if (predictForm) {
        predictForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get selected symptoms
            const selectedSymptoms = getSelectedSymptoms();
            
            if (Object.keys(selectedSymptoms).length === 0) {
                alert('Please select at least one symptom');
                return;
            }
            
            // Make prediction
            makePrediction(selectedSymptoms);
        });
    }
    
    // Clear all symptoms
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            clearAllSymptoms();
        });
    }
    
    // Filter symptoms on search
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterSymptoms(this.value);
        });
    }
    
    // Load all available symptoms from API
    function loadSymptoms() {
        fetch('/symptoms')
            .then(response => response.json())
            .then(data => {
                const symptomsContainer = document.getElementById('symptoms-container');
                
                if (symptomsContainer && data.symptoms) {
                    symptomsContainer.innerHTML = '';
                    
                    data.symptoms.forEach(symptom => {
                        const div = document.createElement('div');
                        div.className = 'symptom-item';
                        
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = `symptom-${symptom}`;
                        checkbox.name = `symptom-${symptom}`;
                        checkbox.value = symptom;
                        
                        const label = document.createElement('label');
                        label.htmlFor = `symptom-${symptom}`;
                        label.textContent = symptom.replace(/_/g, ' ');
                        
                        div.appendChild(checkbox);
                        div.appendChild(label);
                        symptomsContainer.appendChild(div);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading symptoms:', error);
            });
    }
    
    // Filter symptoms based on search input
    function filterSymptoms(searchText) {
        const symptoms = document.querySelectorAll('.symptom-item');
        const searchLower = searchText.toLowerCase();
        
        symptoms.forEach(symptomItem => {
            const label = symptomItem.querySelector('label');
            const text = label.textContent.toLowerCase();
            
            if (text.includes(searchLower)) {
                symptomItem.style.display = 'flex';
            } else {
                symptomItem.style.display = 'none';
            }
        });
    }
    
    // Get all selected symptoms
    function getSelectedSymptoms() {
        const checkboxes = document.querySelectorAll('#symptoms-container input[type="checkbox"]:checked');
        const symptoms = {};
        
        checkboxes.forEach(checkbox => {
            symptoms[checkbox.value] = 1;  // Set to 1 for selected symptoms
        });
        
        return symptoms;
    }
    
    // Clear all symptom selections
    function clearAllSymptoms() {
        const checkboxes = document.querySelectorAll('#symptoms-container input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Hide results section if visible
        resultSection.classList.add('hidden');
    }
    
    // Make prediction with selected symptoms
    function makePrediction(symptoms) {
        console.log("Making prediction with symptoms:", symptoms);
        
        // Check if any symptoms were selected
        if (Object.keys(symptoms).length === 0) {
            alert("Please select at least one symptom before predicting.");
            return;
        }
        
        // Show loading state
        resultSection.innerHTML = '<div class="card result-card"><h3>Analyzing symptoms...</h3><p>Please wait...</p><div class="loader"></div></div>';
        resultSection.classList.remove('hidden');
        
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms: symptoms })
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Prediction result:", data);
            
            if (data.error) {
                resultSection.innerHTML = `<div class="card result-card"><h3>Error</h3><p>${data.error}</p></div>`;
                return;
            }
            
            // Recreate the result section with the new data
            resultSection.innerHTML = `
                <div class="card result-card">
                    <h3>Prediction Result</h3>
                    <p>Based on your symptoms, you may have:</p>
                    <h2 id="disease-name">${data.prediction}</h2>
                    <p>Confidence: <span id="confidence-value" class="confidence">${(data.confidence * 100).toFixed(2)}%</span></p>
                    
                    <div class="related-symptoms">
                        <h4>Related Symptoms:</h4>
                        <ul id="related-symptoms-list">
                            ${data.related_symptoms && data.related_symptoms.length > 0 ? 
                              data.related_symptoms.map(item => 
                                `<li>${item.symptom.replace(/_/g, ' ')} (${item.count})</li>`
                              ).join('') : 
                              '<li>No related symptoms found</li>'}
                        </ul>
                    </div>
                    
                    <p><em>Note: This is not a medical diagnosis. Please consult with a healthcare professional.</em></p>
                </div>
            `;
            
            resultSection.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error making prediction:', error);
            resultSection.innerHTML = `<div class="card result-card"><h3>Error</h3><p>Could not complete the prediction. Please try again.</p></div>`;
        });
    }
});
