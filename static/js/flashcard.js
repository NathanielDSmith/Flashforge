// Flashcard Study Mode Management
class FlashcardStudyMode {
    constructor() {
        this.studyMode = false;
        this.currentCardIndex = 0;
        this.cardData = [];
        this.init();
    }

    init() {
        // Initialize card data from the page
        this.loadCardData();
    }

    loadCardData() {
        // This will be populated by the template
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
        
        // Hide normal mode, show study mode
        document.getElementById('normalMode').classList.add('hidden');
        document.getElementById('studyMode').classList.remove('hidden');
        
        // Load first card
        this.loadStudyCard();
        
        // Update button
        this.updateStudyButton();
        
        // Show navigation controls
        this.showStudyControls();
    }

    exitStudyMode() {
        this.studyMode = false;
        
        // Show normal mode, hide study mode
        document.getElementById('normalMode').classList.remove('hidden');
        document.getElementById('studyMode').classList.add('hidden');
        
        // Update button
        this.updateStudyButton();
        
        // Hide navigation controls
        this.hideStudyControls();
    }

    loadStudyCard() {
        const card = this.cardData[this.currentCardIndex];
        document.getElementById('studyQuestion').textContent = card.question;
        document.getElementById('studyAnswer').textContent = card.answer;
        
        // Reset card to front
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

// Global flashcard functions for backward compatibility
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

// Card deletion function
function deleteCard(setId, cardId, button) {
    // Prevent event propagation to avoid triggering flip
    event.stopPropagation();
    
    // Show confirmation dialog
    if (!confirm('Are you sure you want to delete this card?')) {
        return;
    }
    
    // Create and submit form programmatically
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/set/${setId}/card/${cardId}/delete`;
    
    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrf_token';
        csrfInput.value = csrfToken.getAttribute('content');
        form.appendChild(csrfInput);
    }
    
    document.body.appendChild(form);
    form.submit();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on a page with flashcards
    if (document.querySelector('.flip-card')) {
        window.flashcardStudy = new FlashcardStudyMode();
    }
}); 