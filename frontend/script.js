const API_URL = 'http://localhost:5000';

const form = document.getElementById('carForm');
const resultCard = document.getElementById('resultCard');
const resultContent = document.getElementById('resultContent');
const errorCard = document.getElementById('errorCard');
const errorMessage = document.getElementById('errorMessage');
const apiStatus = document.getElementById('apiStatus');

const labelTranslations = {
    buying: 'Preço de Compra',
    maint: 'Manutenção',
    doors: 'Portas',
    persons: 'Pessoas',
    lug_boot: 'Porta-Malas',
    safety: 'Segurança',
    vhigh: 'Muito Alto',
    high: 'Alto',
    med: 'Médio',
    low: 'Baixo',
    small: 'Pequeno',
    big: 'Grande',
    '2': '2',
    '3': '3',
    '4': '4',
    '5more': '5+',
    more: 'Mais de 4'
};

async function checkApiStatus() {
    try {
        const response = await fetch(`${API_URL}/`);
        if (response.ok) {
            const data = await response.json();
            apiStatus.textContent = data.model_loaded ? 'Online ✓' : 'Online (Modelo não carregado)';
            apiStatus.className = data.model_loaded ? 'online' : 'offline';
        } else {
            apiStatus.textContent = 'Offline ✗';
            apiStatus.className = 'offline';
        }
    } catch (error) {
        apiStatus.textContent = 'Offline ✗';
        apiStatus.className = 'offline';
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    resultCard.style.display = 'none';
    
    setTimeout(() => {
        errorCard.style.display = 'none';
    }, 5000);
}

function getClassInfo(prediction) {
    const classMap = {
        'unacc': {
            label: 'Inaceitável',
            emoji: '❌',
            className: 'unacceptable'
        },
        'acc': {
            label: 'Aceitável',
            emoji: '👍',
            className: 'acceptable'
        },
        'good': {
            label: 'Bom',
            emoji: '⭐',
            className: 'good'
        },
        'vgood': {
            label: 'Muito Bom',
            emoji: '🌟',
            className: 'excellent'
        }
    };
    
    return classMap[prediction] || {
        label: prediction,
        emoji: '❓',
        className: 'acceptable'
    };
}

function displayResult(data) {
    const classInfo = getClassInfo(data.prediction);
    
    let html = `
        <div class="prediction-result ${classInfo.className}">
            <div class="prediction-label">${classInfo.emoji} ${classInfo.label}</div>
            <div class="prediction-class">Classificação: ${data.prediction}</div>
        </div>
    `;
    
    if (data.probabilities) {
        html += `
            <div class="probabilities">
                <h3>Probabilidades por Classe:</h3>
        `;
        
        const sortedProbs = Object.entries(data.probabilities)
            .sort(([, a], [, b]) => b - a);
        
        sortedProbs.forEach(([className, prob]) => {
            const percentage = (prob * 100).toFixed(1);
            const info = getClassInfo(className);
            html += `
                <div class="probability-item">
                    <span class="probability-label">${info.emoji} ${info.label}</span>
                    <div class="probability-bar">
                        <div class="probability-fill" style="width: ${percentage}%">
                            ${percentage}%
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
    }
    
    html += `
        <div class="input-summary">
            <h3>Dados Informados:</h3>
            <div class="input-summary-grid">
                ${Object.entries(data.input).map(([key, value]) => `
                    <div class="input-item">
                        <strong>${labelTranslations[key] || key}:</strong>
                        <span>${labelTranslations[value] || value}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    resultContent.innerHTML = html;
    resultCard.style.display = 'block';
    errorCard.style.display = 'none';
    
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    const submitBtn = document.querySelector('.btn-submit');
    
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult(result);
        } else {
            showError(result.error || 'Erro ao processar a predição');
        }
    } catch (error) {
        showError('Erro de conexão com a API. Verifique se o backend está rodando.');
    } finally {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
});

checkApiStatus();
setInterval(checkApiStatus, 30000);
