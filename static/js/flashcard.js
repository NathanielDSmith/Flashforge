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
        this.shuffleEnabled = false;
        this.scores = {};
        this._touch = {};
        this._keyHandler = this._handleKeydown.bind(this);
        this._boundTouchStart = this._onTouchStart.bind(this);
        this._boundTouchEnd   = this._onTouchEnd.bind(this);
    }

    _handleKeydown(e) {
        if (!this.studyMode) return;
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch (e.key) {
            case ' ':
            case 'Enter':
                e.preventDefault();
                document.getElementById('studyCard').classList.toggle('flipped');
                break;
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                this.nextCard();
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                this.previousCard();
                break;
            case 'Escape':
                this.exitStudyMode();
                break;
        }
    }

    _onTouchStart(e) {
        const t = e.changedTouches[0];
        this._touch = { x: t.clientX, y: t.clientY, time: Date.now() };
    }

    _onTouchEnd(e) {
        const t = e.changedTouches[0];
        const dx = t.clientX - this._touch.x;
        const dy = t.clientY - this._touch.y;
        const dt = Date.now() - this._touch.time;
        const absDx = Math.abs(dx);
        const absDy = Math.abs(dy);

        if (absDx < 10 && absDy < 10 && dt < 300) {
            const studyCard = document.getElementById('studyCard');
            if (studyCard) studyCard.classList.toggle('flipped');
            return;
        }

        if (absDx > 50 && absDx > absDy) {
            if (dx < 0) {
                this.nextCard();
            } else {
                this.previousCard();
            }
        }
    }

    _bindSwipe() {
        const el = document.getElementById('studyCardContainer');
        if (!el) return;
        el.addEventListener('touchstart', this._boundTouchStart, { passive: true });
        el.addEventListener('touchend',   this._boundTouchEnd,   { passive: true });
    }

    _unbindSwipe() {
        const el = document.getElementById('studyCardContainer');
        if (!el) return;
        el.removeEventListener('touchstart', this._boundTouchStart);
        el.removeEventListener('touchend',   this._boundTouchEnd);
    }

    toggleShuffle() {
        this.shuffleEnabled = !this.shuffleEnabled;
        const btn = document.getElementById('shuffleBtn');
        if (btn) {
            btn.classList.toggle('shuffle-toggle--on', this.shuffleEnabled);
            btn.setAttribute('aria-pressed', this.shuffleEnabled);
        }
    }

    _shuffle(arr) {
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
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

    enterStudyMode(deck) {
        if (this.cardData.length === 0) return;

        this.studyMode = true;
        this.currentCardIndex = 0;
        this.activeDeck = this.shuffleEnabled ? this._shuffle(this.cardData) : this.cardData.slice();
        this.scores = {};

        document.getElementById('normalMode').classList.add('hidden');
        document.getElementById('studyMode').classList.remove('hidden');
        document.getElementById('studyResults').classList.add('hidden');
        document.getElementById('studyCardContainer').classList.remove('hidden');

        this.loadStudyCard();
        this.updateStudyButton();
        this.showStudyControls();
        document.addEventListener('keydown', this._keyHandler);
        this._bindSwipe();
    }

    exitStudyMode() {
        this.studyMode = false;

        document.getElementById('normalMode').classList.remove('hidden');
        document.getElementById('studyMode').classList.add('hidden');

        this.updateStudyButton();
        this.hideStudyControls();
        document.removeEventListener('keydown', this._keyHandler);
        this._unbindSwipe();
    }

    loadStudyCard() {
        const deck = this.activeDeck || this.cardData;
        const card = deck[this.currentCardIndex];
        document.getElementById('studyQuestion').textContent = card.question;
        document.getElementById('studyAnswer').textContent = card.answer;

        const studyCard = document.getElementById('studyCard');
        studyCard.classList.remove('flipped');

        this.updateProgressBar();
    }

    updateProgressBar() {
        const total = this.cardData.length;
        const current = this.currentCardIndex + 1;
        const pct = Math.round((current / total) * 100);

        const bar     = document.getElementById('studyProgressBar');
        const label   = document.getElementById('progressLabel');
        const percent = document.getElementById('progressPercent');

        if (bar)     bar.style.width = pct + '%';
        if (label)   label.textContent = `Card ${current} of ${total}`;
        if (percent) percent.textContent = pct + '%';
    }

    scoreCard(result) {
        const deck = this.activeDeck || this.cardData;
        const card = deck[this.currentCardIndex];
        this.scores[card.id] = result;

        if (this.currentCardIndex < deck.length - 1) {
            this.currentCardIndex++;
            this.loadStudyCard();
            this.updateStudyButton();
        } else {
            this.showResults();
        }
    }

    showResults() {
        const deck = this.activeDeck || this.cardData;
        const gotIt = Object.values(this.scores).filter(s => s === 'got-it').length;
        const learning = deck.length - gotIt;

        document.getElementById('studyCardContainer').classList.add('hidden');
        document.getElementById('studyResults').classList.remove('hidden');
        document.getElementById('gotItCount').textContent = gotIt;
        document.getElementById('learningCount').textContent = learning;

        const retryBtn = document.getElementById('retryMissedBtn');
        retryBtn.style.display = learning > 0 ? '' : 'none';

        this.hideStudyControls();

        if (typeof window.currentSetId !== 'undefined') {
            try {
                localStorage.setItem('ff-score-' + window.currentSetId, JSON.stringify({
                    got: gotIt,
                    total: this.cardData.length,
                    date: new Date().toISOString()
                }));
            } catch (_) {}
        }
    }

    restartAll() {
        this.activeDeck = this.cardData.slice();
        this.scores = {};
        this.currentCardIndex = 0;
        document.getElementById('studyResults').classList.add('hidden');
        document.getElementById('studyCardContainer').classList.remove('hidden');
        this.loadStudyCard();
        this.updateStudyButton();
        this.showStudyControls();
    }

    restartWithMissed() {
        const missed = (this.activeDeck || this.cardData).filter(c => this.scores[c.id] !== 'got-it');
        if (missed.length === 0) return;
        this.activeDeck = missed;
        this.scores = {};
        this.currentCardIndex = 0;
        document.getElementById('studyResults').classList.add('hidden');
        document.getElementById('studyCardContainer').classList.remove('hidden');
        this.loadStudyCard();
        this.updateStudyButton();
        this.showStudyControls();
    }

    showStudyControls() {
        let controls = document.getElementById('studyControls');
        if (!controls) {
            controls = document.createElement('div');
            controls.id = 'studyControls';
            controls.className = 'study-controls';
            controls.innerHTML = `
                <button onclick="window.flashcardStudy.previousCard()" class="btn btn-secondary">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                    Prev
                </button>
                <button onclick="window.flashcardStudy.nextCard()" class="btn">
                    Next
                    <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                </button>
                <div class="keyboard-hints">
                    <span><kbd>Space</kbd> flip</span>
                    <span><kbd>←</kbd><kbd>→</kbd> navigate</span>
                    <span><kbd>Esc</kbd> exit</span>
                </div>
            `;
            document.body.appendChild(controls);
        }
        controls.style.display = 'flex';
    }

    hideStudyControls() {
        const controls = document.getElementById('studyControls');
        if (controls) controls.style.display = 'none';
    }

    nextCard() {
        const deck = this.activeDeck || this.cardData;
        if (this.currentCardIndex < deck.length - 1) {
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
            const deck = this.activeDeck || this.cardData;
            button.innerHTML = `
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
                Exit Study Mode (${this.currentCardIndex + 1}/${deck.length})
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
    if (window.flashcardStudy) window.flashcardStudy.flipCardBack(button);
}

function flipStudyCard() {
    if (window.flashcardStudy) window.flashcardStudy.flipStudyCard();
}

function flipStudyCardBack() {
    if (window.flashcardStudy) window.flashcardStudy.flipStudyCardBack();
}

function toggleStudyMode() {
    if (window.flashcardStudy) window.flashcardStudy.toggleStudyMode();
}

function nextCard() {
    if (window.flashcardStudy) window.flashcardStudy.nextCard();
}

function previousCard() {
    if (window.flashcardStudy) window.flashcardStudy.previousCard();
}

function deleteCard(event, setId, cardId) {
    event.stopPropagation();

    if (!confirm('Are you sure you want to delete this card?')) return;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/set/${setId}/card/${cardId}/delete`;
    document.body.appendChild(form);
    form.submit();
}

function toggleFavorite(setId, cardId, button) {
    
    const originalContent = button.innerHTML;
    button.innerHTML = '<svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>';
    button.disabled = true;

    fetch(`/card/${setId}/${cardId}/toggle-favorite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
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
    .catch(() => {
        button.innerHTML = originalContent;
        showNotification('Error updating favorite status', 'error');
    })
    .finally(() => {
        button.disabled = false;
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `toast fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error'   ? 'bg-red-500 text-white'   :
        'bg-blue-500 text-white'
    }`;
    
    const row = document.createElement('div');
    row.className = 'flex items-center';

    const text = document.createElement('span');
    text.className = 'flex-1';
    text.textContent = message;

    const closeBtn = document.createElement('button');
    closeBtn.className = 'ml-2 text-white hover:text-gray-200';
    closeBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
    closeBtn.addEventListener('click', () => notification.remove());

    row.appendChild(text);
    row.appendChild(closeBtn);
    notification.appendChild(row);
    
    document.body.appendChild(notification);

    setTimeout(() => {
        if (!notification.parentElement) return;
        notification.classList.add('toast-out');
        notification.addEventListener('animationend', () => notification.remove(), { once: true });
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('studyModeBtn')) {
        window.flashcardStudy = new FlashcardStudyMode();
    }

    document.querySelectorAll('.card').forEach(function(card) {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width)  * 100;
            const y = ((e.clientY - rect.top)  / rect.height) * 100;
            card.style.setProperty('--mx', x + '%');
            card.style.setProperty('--my', y + '%');
        });
    });
});
