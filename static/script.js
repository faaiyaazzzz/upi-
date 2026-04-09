document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = {
        transaction_type: formData.get('transaction_type'),
        merchant: formData.get('merchant'),
        amount: parseFloat(formData.get('amount')),
        device: formData.get('device'),
        hour_of_day: parseInt(formData.get('hour_of_day'))
    };

    const predictBtn = document.getElementById('predictBtn');
    const resultContainer = document.getElementById('result');
    const statusText = document.getElementById('statusText');
    const probabilityText = document.getElementById('probabilityText');
    const probabilityFill = document.getElementById('probabilityFill');

    // UI State Management
    predictBtn.disabled = true;
    predictBtn.innerText = 'Analyzing...';
    resultContainer.classList.add('hidden');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            // Display Result
            resultContainer.classList.remove('hidden');
            statusText.innerText = result.status;
            
            if (result.is_fraud === 1) {
                statusText.className = 'status-fraudulent';
                probabilityFill.style.backgroundColor = '#dc3545';
            } else {
                statusText.className = 'status-legitimate';
                probabilityFill.style.backgroundColor = '#28a745';
            }

            const probPercent = (result.fraud_probability * 100).toFixed(2);
            probabilityText.innerText = `Fraud Probability: ${probPercent}%`;
            probabilityFill.style.width = `${probPercent}%`;
            
            // Update History Table
            updateHistory();
            
            // Scroll to result
            resultContainer.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while making the prediction.');
    } finally {
        predictBtn.disabled = false;
        predictBtn.innerText = 'Predict Fraud Status';
    }
});

async function updateHistory() {
    try {
        const response = await fetch('/history?limit=10');
        const history = await response.json();
        
        const historyBody = document.getElementById('historyBody');
        historyBody.innerHTML = '';
        
        history.forEach(item => {
            const row = document.createElement('tr');
            
            // Format time
            const date = new Date(item.timestamp + 'Z'); // Assume UTC from SQLite
            const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const statusClass = item.is_fraud === 1 ? 'badge-fraudulent' : 'badge-legitimate';
            
            row.innerHTML = `
                <td>${timeStr}</td>
                <td>${item.merchant}</td>
                <td>₹${item.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</td>
                <td><span class="status-badge ${statusClass}">${item.status}</span></td>
            `;
            
            historyBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}

// Initial load
updateHistory();
// Optional: Poll for updates every 10 seconds if multiple users/sessions
setInterval(updateHistory, 10000);
