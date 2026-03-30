// Studio Event Portal Logic
console.log("🚀 Studio Experience System Online");

// Modal Management
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('fade-in');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Global Notification System
function showNotif(message, type = 'success') {
    const notif = document.createElement('div');
    notif.className = `notif fade-in`;
    notif.style = `
        position: fixed; bottom: 2rem; right: 2rem; 
        background: #000; color: #fff; padding: 1.5rem 3rem; 
        font-weight: 800; font-size: 0.75rem; letter-spacing: 0.1em;
        text-transform: uppercase; z-index: 10000;
    `;
    notif.innerHTML = message;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.style.opacity = '0';
        notif.style.transition = '0.5s';
        setTimeout(() => notif.remove(), 500);
    }, 3000);
}

// Dynamic UI Helpers
function updateProgressBar(filled, total) {
    const percent = Math.round((filled / total) * 100);
    return `
        <div class="progress-container" style="background:var(--paper); height:4px; margin-bottom:1rem;">
            <div class="progress-bar" style="width: ${percent}%; height:100%; background:var(--coral);"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.7rem; font-weight:850; color:var(--black); letter-spacing:0.05em;">
            <span style="opacity:0.4;">STATUS</span>
            <span>${filled}/${total} BOOKED</span>
        </div>
    `;
}
