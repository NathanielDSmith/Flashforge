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

// Favorite toggle function
function toggleFavorite(setId, cardId, button) {
    // Prevent event propagation to avoid triggering flip
    event.stopPropagation();
    
    // Show loading state
    const originalClass = button.className;
    const originalSvg = button.querySelector('svg');
    const originalSvgClass = originalSvg.className;
    
    // Show loading spinner
    button.innerHTML = `
        <svg class="w-5 h-5 animate-spin text-gray-400" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    `;
    
    // Make API call
    fetch(`/card/${setId}/${cardId}/toggle-favorite`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update button appearance based on new favorite status
            if (data.favorite) {
                button.className = 'favorite-btn absolute top-2 right-2 text-yellow-500 hover:text-yellow-600 transition-colors z-20';
                button.innerHTML = `
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                `;
            } else {
                button.className = 'favorite-btn absolute top-2 right-2 text-gray-400 hover:text-yellow-600 transition-colors z-20';
                button.innerHTML = `
                    <svg class="w-5 h-5 fill-none stroke-current" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                `;
            }
            
            // Show success message
            showNotification(data.message, 'success');
            
            // Update favorites count on home page if it exists
            const favoritesLink = document.querySelector('a[href="/favorites"]');
            if (favoritesLink) {
                const currentText = favoritesLink.textContent;
                const match = currentText.match(/Favorites \((\d+)\)/);
                if (match) {
                    const currentCount = parseInt(match[1]);
                    const newCount = data.favorite ? currentCount + 1 : currentCount - 1;
                    favoritesLink.innerHTML = `
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        Favorites (${newCount})
                    `;
                }
            }
        } else {
            // Show error message
            showNotification(data.message, 'error');
            // Restore original button state
            button.className = originalClass;
            button.innerHTML = `<svg class="${originalSvgClass}" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating favorite status', 'error');
        // Restore original button state
        button.className = originalClass;
        button.innerHTML = `<svg class="${originalSvgClass}" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>`;
    });
}

// Notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on a page with flashcards
    if (document.querySelector('.flip-card')) {
        window.flashcardStudy = new FlashcardStudyMode();
    }
}); 