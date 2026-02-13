/**
 * AstroGuy AI - Optimized Main JavaScript
 * Performance-focused frontend interactions
 */

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize stars with reduced count for performance
    initStars();
    
    // Hide loading screen after 1.5 seconds (reduced from 2)
    setTimeout(() => {
        const loadingScreen = document.getElementById('loadingScreen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
    }, 1500);
});

// ==================== OPTIMIZED STARS BACKGROUND ====================

function initStars() {
    const container = document.getElementById('starsBg');
    if (!container) return;
    
    // Use DocumentFragment for batch DOM insertion
    const fragment = document.createDocumentFragment();
    
    // Reduced star count for better performance (50 instead of 100)
    for (let i = 0; i < 50; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        
        // Only 20% of stars twinkle (reduces animation load)
        if (Math.random() < 0.2) {
            star.classList.add('twinkle');
            star.style.animationDelay = (Math.random() * 4) + 's';
        }
        
        fragment.appendChild(star);
    }
    
    container.appendChild(fragment);
    
    // Reduced shooting star frequency (every 8s instead of 5s)
    setInterval(createShootingStar, 8000);
}

function createShootingStar() {
    const container = document.getElementById('starsBg');
    if (!container) return;
    
    const shootingStar = document.createElement('div');
    shootingStar.className = 'shooting-star';
    shootingStar.style.top = Math.random() * 40 + '%';
    shootingStar.style.left = Math.random() * 40 + '%';
    
    // Use CSS animation instead of JS animation
    shootingStar.style.animation = 'shoot 2.5s linear forwards';
    
    container.appendChild(shootingStar);
    
    setTimeout(() => {
        if (shootingStar.parentNode) {
            shootingStar.remove();
        }
    }, 2500);
}

// Add shooting star animation to stylesheet dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shoot {
        0% { transform: translateX(-100px) translateY(100px); opacity: 1; }
        100% { transform: translateX(300px) translateY(-100px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// ==================== MOBILE MENU ====================

function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// ==================== LANGUAGE TOGGLE ====================

async function toggleLanguage() {
    try {
        const response = await fetch('/api/toggle-language', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.location.reload();
        }
    } catch (error) {
        console.error('Error toggling language:', error);
        showAlert('Error changing language', 'error');
    }
}

// ==================== ALERT SYSTEM ====================

let alertTimeout = null;

function showAlert(message, type = 'info') {
    // Clear existing timeout
    if (alertTimeout) {
        clearTimeout(alertTimeout);
    }
    
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = 'alert';
    alert.innerHTML = `
        <div class="alert-title">${type === 'error' ? '⚠️ Error' : '✨ Info'}</div>
        <div class="alert-message">${message}</div>
    `;
    
    document.body.appendChild(alert);
    
    // Auto-remove after 3 seconds
    alertTimeout = setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 3000);
}

// ==================== UTILITY FUNCTIONS ====================

function formatDate(date, locale = 'en-US') {
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return date.toLocaleDateString(locale, options);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== FORM VALIDATION ====================

function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#ef4444';
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// ==================== PERFORMANCE: INTERSECTION OBSERVER ====================

// Lazy load elements when they come into view
const lazyObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            lazyObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.lazy-load').forEach(el => {
    lazyObserver.observe(el);
});

// ==================== DEBOUNCE & THROTTLE UTILITIES ====================

function debounce(func, wait = 100) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit = 100) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ==================== KEYBOARD SHORTCUTS ====================

document.addEventListener('keydown', (e) => {
    // Press 'Escape' to close mobile menu
    if (e.key === 'Escape') {
        const navLinks = document.getElementById('navLinks');
        if (navLinks) {
            navLinks.classList.remove('active');
        }
    }
});

// ==================== CONSOLE EASTER EGG ====================

console.log('%c🌟 AstroGuy AI 🌟', 'font-size: 20px; font-weight: bold; color: #FFD700;');
console.log('%cOptimized Vedic Astrology', 'font-size: 12px; color: #6B46C1;');
