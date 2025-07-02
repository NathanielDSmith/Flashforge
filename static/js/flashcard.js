class FlashcardStudyMode {
    constructor() {
        this.studyMode = false;
        this.currentCardIndex = 0;
        this.cardData = [];
        this.init();
    }

    init() {
        if (typeof window.cardData !== 'undefined') {
            this.cardData = window.cardData;
        }
    }

    flipCardBack(button) {
        const flipCard = button.closest('.flip-card');
        flipCard.classList.remove('flipped');
    }

    flipStudyCard() {
        const studyCard = document.getElementById('studyCard');
        studyCard.classList.add('flipped');
    }

    flipStudyCardBack() {
        const studyCard = document.getElementById('studyCard');
        studyCard.classList.remove('flipped');
    }

    toggleStudyMode() {
        if (!this.studyMode) {
            this.enterStudyMode();
        } else {
            this.exitStudyMode();
        }
    }

    enterStudyMode() {
        if (this.cardData.length === 0) return;
        
        this.studyMode = true;
        this.currentCardIndex = 0;
        
        document.getElementById('normalMode').classList.add('hidden');
        document.getElementById('studyMode').classList.remove('hidden');
        
        this.loadStudyCard();
        this.updateStudyButton();
        this.showStudyControls();
    }

    exitStudyMode() {
        this.studyMode = false;
        
        document.getElementById('normalMode').classList.remove('hidden');
        document.getElementById('studyMode').classList.add('hidden');
        
        this.updateStudyButton();
        this.hideStudyControls();
    }

    loadStudyCard() {
        const card = this.cardData[this.currentCardIndex];
        document.getElementById('studyQuestion').textContent = card.question;
        document.getElementById('studyAnswer').textContent = card.answer;
        
        const studyCard = document.getElementById('studyCard');
        studyCard.classList.remove('flipped');
    }

    showStudyControls() {
        let controls = document.getElementById('studyControls');
        if (!controls) {
            controls = document.createElement('div');
            controls.id = 'studyControls';
            controls.className = 'fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg p-4 flex space-x-4 z-50';
            controls.innerHTML = `
                <button onclick="flashcardStudy.previousCard()" class="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
                    Previous
                </button>
                <button onclick="flashcardStudy.nextCard()" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
                    Next
                </button>
            `;
            document.body.appendChild(controls);
        }
        controls.style.display = 'flex';
    }

    hideStudyControls() {
        const controls = document.getElementById('studyControls');
        if (controls) {
            controls.style.display = 'none';
        }
    }

    nextCard() {
        if (this.currentCardIndex < this.cardData.length - 1) {
            this.currentCardIndex++;
            this.loadStudyCard();
            this.updateStudyButton();
        }
    }

    previousCard() {
        if (this.currentCardIndex > 0) {
            this.currentCardIndex--;
            this.loadStudyCard();
            this.updateStudyButton();
        }
    }

    updateStudyButton() {
        const button = document.getElementById('studyModeBtn');
        if (!button) return;

        if (this.studyMode) {
            button.innerHTML = `
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                Exit Study Mode (${this.currentCardIndex + 1}/${this.cardData.length})
            `;
        } else {
            button.innerHTML = `
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                Enter Study Mode
            `;
        }
    }
}

function flipCard(cardElement) {
    cardElement.classList.toggle('flipped');
}

function flipCardBack(button) {
    if (window.flashcardStudy) {
        window.flashcardStudy.flipCardBack(button);
    }
}

function flipStudyCard() {
    if (window.flashcardStudy) {
        window.flashcardStudy.flipStudyCard();
    }
}

function flipStudyCardBack() {
    if (window.flashcardStudy) {
        window.flashcardStudy.flipStudyCardBack();
    }
}

function toggleStudyMode() {
    if (window.flashcardStudy) {
        window.flashcardStudy.toggleStudyMode();
    }
}

function nextCard() {
    if (window.flashcardStudy) {
        window.flashcardStudy.nextCard();
    }
}

function previousCard() {
    if (window.flashcardStudy) {
        window.flashcardStudy.previousCard();
    }
}

function deleteCard(setId, cardId, button) {
    event.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this card?')) {
        return;
    }
    
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/set/${setId}/card/${cardId}/delete`;
    document.body.appendChild(form);
    form.submit();
}

function toggleFavorite(setId, cardId, button) {
    event.stopPropagation();
    
    const originalContent = button.innerHTML;
    button.innerHTML = '<svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>';
    button.disabled = true;
    
    fetch(`/card/${setId}/${cardId}/toggle-favorite`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.favorite) {
                button.innerHTML = '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>';
            } else {
                button.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg>';
            }
            
            showNotification(data.message, 'success');
        } else {
            button.innerHTML = originalContent;
            showNotification(data.message || 'Error updating favorite status', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerHTML = originalContent;
        showNotification('Error updating favorite status', 'error');
    })
    .finally(() => {
        button.disabled = false;
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center">
            <span class="flex-1">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('studyModeBtn')) {
        window.flashcardStudy = new FlashcardStudyMode();
    }
}); 