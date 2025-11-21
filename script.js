// State
let currentMode = 'jokes'; // 'jokes' or 'pickup'
let currentLang = 'en'; // 'en' or 'id'
let currentContentId = null;
let historyIds = []; // Keep track of last few IDs to avoid repetition

// DOM Elements
const displayEl = document.getElementById('display-text');
const generateBtn = document.getElementById('generate-btn');
const copyBtn = document.getElementById('copy-btn');
const modeJokesBtn = document.getElementById('mode-jokes');
const modePickupBtn = document.getElementById('mode-pickup');
const langEnBtn = document.getElementById('lang-en');
const langIdBtn = document.getElementById('lang-id');
const mascotImg = document.getElementById('mascot-img');
const ratingContainer = document.getElementById('rating-container');
const ratingText = document.getElementById('rating-text');
const stars = document.querySelectorAll('.star');

// Modal Elements
const modal = document.getElementById('submit-modal');
const openModalBtn = document.getElementById('open-submit-modal');
const closeModalBtn = document.querySelector('.close-modal');
const submitForm = document.getElementById('submit-form');

// Functions
async function updateDisplay() {
    // Loading state
    displayEl.classList.remove('fade-in');
    displayEl.style.opacity = '0.5';
    ratingContainer.style.display = 'none';
    resetStars();

    resetStars();

    try {
        // Pass history IDs to exclude
        const excludeStr = historyIds.join(',');
        const response = await fetch(`/api/random?type=${currentMode}&lang=${currentLang}&exclude=${excludeStr}`);
        const data = await response.json();

        if (data.error) {
            displayEl.textContent = "Oops! No jokes found.";
        } else {
            currentContentId = data.id;
            displayEl.textContent = data.text;

            // Update history
            historyIds.push(currentContentId);
            if (historyIds.length > 5) {
                historyIds.shift(); // Keep only last 5
            }

            // Show rating info if available
            if (data.rating_count > 0) {
                ratingText.textContent = `Rated ${data.average_rating.toFixed(1)}/5 (${data.rating_count} votes)`;
            } else {
                ratingText.textContent = "Be the first to rate this!";
            }
            ratingContainer.style.display = 'flex';
        }
    } catch (error) {
        console.error('Error fetching content:', error);
        displayEl.textContent = "Error connecting to the fun factory.";
    }

    // Restore UI
    displayEl.style.opacity = '1';
    displayEl.classList.add('fade-in');
}

function setMode(mode) {
    currentMode = mode;

    if (mode === 'jokes') {
        modeJokesBtn.classList.add('active');
        modePickupBtn.classList.remove('active');
        document.documentElement.style.setProperty('--primary-gradient', 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)');
    } else {
        modePickupBtn.classList.add('active');
        modeJokesBtn.classList.remove('active');
        document.documentElement.style.setProperty('--primary-gradient', 'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)');
    }

    updateDisplay();
    updateMascot();
}

function setLanguage(lang) {
    currentLang = lang;

    if (lang === 'en') {
        langEnBtn.classList.add('active');
        langIdBtn.classList.remove('active');
    } else {
        langIdBtn.classList.add('active');
        langEnBtn.classList.remove('active');
    }

    updateDisplay();
}

function updateMascot() {
    if (currentMode === 'jokes') {
        mascotImg.src = 'dad-mascot.png';
    } else {
        mascotImg.src = 'pickup-mascot.png';
    }
}

function copyToClipboard() {
    const text = displayEl.textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Visual feedback
        const originalIcon = copyBtn.innerHTML;
        copyBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        copyBtn.style.background = 'rgba(34, 197, 94, 0.2)';
        copyBtn.style.color = '#4ade80';

        setTimeout(() => {
            copyBtn.innerHTML = originalIcon;
            copyBtn.style.background = '';
            copyBtn.style.color = '';
        }, 2000);
    });
}

// Rating Logic
function resetStars() {
    stars.forEach(star => star.classList.remove('active'));
}

async function submitRating(score) {
    if (!currentContentId) return;

    // Optimistic UI update
    stars.forEach(star => {
        if (parseInt(star.dataset.value) <= score) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });

    try {
        const response = await fetch('/api/rate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentContentId, score: score })
        });

        if (response.ok) {
            ratingText.textContent = "Thanks for rating!";
        }
    } catch (error) {
        console.error('Error submitting rating:', error);
    }
}

// Modal Logic
function openModal() {
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
}

async function handleSubmission(e) {
    e.preventDefault();

    const type = document.getElementById('submit-type').value;
    const lang = document.getElementById('submit-lang').value;
    const text = document.getElementById('submit-text').value;

    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type, lang, text })
        });

        if (response.ok) {
            alert("Thanks! Your submission has been sent for approval.");
            closeModal();
            e.target.reset();
        } else {
            alert("Something went wrong. Please try again.");
        }
    } catch (error) {
        console.error('Error submitting:', error);
        alert("Error submitting. Please check your connection.");
    }
}

// Event Listeners
generateBtn.addEventListener('click', updateDisplay);
copyBtn.addEventListener('click', copyToClipboard);

modeJokesBtn.addEventListener('click', () => setMode('jokes'));
modePickupBtn.addEventListener('click', () => setMode('pickup'));

langEnBtn.addEventListener('click', () => setLanguage('en'));
langIdBtn.addEventListener('click', () => setLanguage('id'));

stars.forEach(star => {
    star.addEventListener('click', () => submitRating(parseInt(star.dataset.value)));
});

openModalBtn.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);
window.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});
submitForm.addEventListener('submit', handleSubmission);

// Initialize
updateDisplay();

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed', err));
    });
}
