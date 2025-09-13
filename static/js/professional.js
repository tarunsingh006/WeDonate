// Professional Medical Platform JavaScript - Enhanced Edition
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeAnimations();
    initializeForms();
    initializeButtons();
    initializeTooltips();
    initializeScrollEffects();
    initializeProfessionalComponents();
    initializeLoadingStates();
    initializeMicroInteractions();
    initializeNotificationSystem();
    initializeAdvancedScrollEffects();
});

// Navigation functionality
function initializeNavigation() {
    const navbar = document.querySelector('.navbar-professional');
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && targetId.length > 1) {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Initialize animations
function initializeAnimations() {
    // Animate elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe professional cards and forms
    document.querySelectorAll('.professional-card, .professional-form, .professional-table').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Form functionality
function initializeForms() {
    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitButton = form.querySelector('button[type="submit"]');
        
        form.addEventListener('submit', function(e) {
            if (submitButton) {
                // Add loading state
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<div class="loading-spinner"></div>Processing...';
                submitButton.disabled = true;
                
                // Reset button after 3 seconds if no redirect
                setTimeout(() => {
                    if (submitButton) {
                        submitButton.innerHTML = originalText;
                        submitButton.disabled = false;
                    }
                }, 3000);
            }
        });
        
        // Real-time validation feedback
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', validateInput);
            input.addEventListener('input', clearValidationErrors);
        });
    });
    
    // Password confirmation validation
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    if (passwordInputs.length >= 2) {
        const password = passwordInputs[0];
        const confirmPassword = passwordInputs[1];
        
        confirmPassword.addEventListener('input', function() {
            validatePasswordMatch(password, confirmPassword);
        });
    }
}

// Input validation function
function validateInput(event) {
    const input = event.target;
    const isValid = input.checkValidity();
    
    // Remove existing validation classes
    input.classList.remove('is-valid', 'is-invalid');
    
    // Add appropriate validation class
    if (input.value.trim() !== '') {
        input.classList.add(isValid ? 'is-valid' : 'is-invalid');
        
        // Show/hide validation feedback
        showValidationFeedback(input, isValid);
    }
}

// Clear validation errors
function clearValidationErrors(event) {
    const input = event.target;
    if (input.classList.contains('is-invalid')) {
        input.classList.remove('is-invalid');
        hideValidationFeedback(input);
    }
}

// Password match validation
function validatePasswordMatch(password, confirmPassword) {
    const isMatch = password.value === confirmPassword.value;
    const isEmpty = confirmPassword.value.trim() === '';
    
    confirmPassword.classList.remove('is-valid', 'is-invalid');
    
    if (!isEmpty) {
        confirmPassword.classList.add(isMatch ? 'is-valid' : 'is-invalid');
        
        let feedback = confirmPassword.parentNode.querySelector('.validation-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'validation-feedback';
            confirmPassword.parentNode.appendChild(feedback);
        }
        
        if (isMatch) {
            feedback.textContent = '✓ Passwords match';
            feedback.style.color = 'var(--success)';
        } else {
            feedback.textContent = '✗ Passwords do not match';
            feedback.style.color = 'var(--danger)';
        }
        feedback.style.display = 'block';
    }
}

// Show validation feedback
function showValidationFeedback(input, isValid) {
    let feedback = input.parentNode.querySelector('.validation-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'validation-feedback';
        feedback.style.fontSize = '0.875rem';
        feedback.style.marginTop = '0.25rem';
        input.parentNode.appendChild(feedback);
    }
    
    if (isValid) {
        feedback.textContent = '✓ Looks good!';
        feedback.style.color = 'var(--success)';
    } else {
        feedback.textContent = input.validationMessage || 'Please provide a valid input.';
        feedback.style.color = 'var(--danger)';
    }
    feedback.style.display = 'block';
}

// Hide validation feedback
function hideValidationFeedback(input) {
    const feedback = input.parentNode.querySelector('.validation-feedback');
    if (feedback) {
        feedback.style.display = 'none';
    }
}

// Button functionality
function initializeButtons() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', createRipple);
    });
    
    // Handle confirmation dialogs for dangerous actions
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(e) {
            const confirmMessage = this.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
            if (!confirm(confirmMessage)) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Create ripple effect
function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    circle.style.width = circle.style.height = diameter + 'px';
    circle.style.left = event.clientX - button.offsetLeft - radius + 'px';
    circle.style.top = event.clientY - button.offsetTop - radius + 'px';
    circle.classList.add('ripple');
    
    const ripple = button.querySelector('.ripple');
    if (ripple) {
        ripple.remove();
    }
    
    button.appendChild(circle);
    
    // Remove ripple after animation
    setTimeout(() => {
        circle.remove();
    }, 600);
}

// Initialize tooltips
function initializeTooltips() {
    // Simple tooltip implementation
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(event) {
    const element = event.target;
    const tooltipText = element.getAttribute('data-tooltip');
    
    if (tooltipText) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = tooltipText;
        tooltip.style.cssText = `
            position: absolute;
            background: var(--dark-gray);
            color: var(--white);
            padding: 0.5rem;
            border-radius: var(--border-radius);
            font-size: 0.875rem;
            z-index: 1000;
            white-space: nowrap;
            box-shadow: var(--shadow);
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
        
        element._tooltip = tooltip;
    }
}

function hideTooltip(event) {
    const element = event.target;
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// Scroll effects
function initializeScrollEffects() {
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Progress indicator
    createScrollProgressIndicator();
    
    // Back to top button
    createBackToTopButton();
}

// Create scroll progress indicator
function createScrollProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: var(--accent-teal);
        z-index: 1001;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

// Create back to top button
function createBackToTopButton() {
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        background: var(--primary-blue);
        color: var(--white);
        border: none;
        border-radius: 50%;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: var(--transition);
        z-index: 1000;
        box-shadow: var(--shadow);
    `;
    
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    });
}

// Table functionality
function initializeTables() {
    document.querySelectorAll('.professional-table').forEach(table => {
        // Add sorting functionality
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, this);
            });
        });
        
        // Add search functionality if search input exists
        const searchInput = table.querySelector('.table-search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                filterTable(table, this.value);
            });
        }
    });
}

// Sort table
function sortTable(table, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const column = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = header.classList.contains('sort-asc');
    
    // Clear all sort classes
    header.parentNode.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add appropriate sort class
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.children[column].textContent.trim();
        const bValue = b.children[column].textContent.trim();
        
        if (isAscending) {
            return bValue.localeCompare(aValue, undefined, { numeric: true });
        } else {
            return aValue.localeCompare(bValue, undefined, { numeric: true });
        }
    });
    
    // Append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Filter table
function filterTable(table, searchTerm) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Alert system
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alert-container') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto dismiss
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, duration);
    
    return alert;
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alert-container';
    container.style.cssText = `
        position: fixed;
        top: 100px;
        right: 1rem;
        z-index: 1050;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

function getAlertIcon(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Add ripple CSS
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .is-valid {
        border-color: var(--success) !important;
    }
    
    .is-invalid {
        border-color: var(--danger) !important;
    }
    
    .validation-feedback {
        display: none;
    }
    
    .alert {
        border-radius: var(--border-radius);
        border: none;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }
    
    .alert-success {
        background-color: rgba(16, 185, 129, 0.1);
        color: var(--success);
        border-left: 4px solid var(--success);
    }
    
    .alert-danger {
        background-color: rgba(239, 68, 68, 0.1);
        color: var(--danger);
        border-left: 4px solid var(--danger);
    }
    
    .alert-warning {
        background-color: rgba(245, 158, 11, 0.1);
        color: var(--warning);
        border-left: 4px solid var(--warning);
    }
    
    .alert-info {
        background-color: rgba(59, 130, 246, 0.1);
        color: var(--info);
        border-left: 4px solid var(--info);
    }
    
    .btn-close {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        margin-left: auto;
    }
`;
document.head.appendChild(rippleStyle);

// Initialize table functionality
document.addEventListener('DOMContentLoaded', initializeTables);

// Professional Components Initialization
function initializeProfessionalComponents() {
    // Initialize floating labels
    initializeFloatingLabels();
    
    // Initialize glass panels
    initializeGlassPanels();
    
    // Initialize card stacks
    initializeCardStacks();
    
    // Initialize professional badges
    initializeProfessionalBadges();
}

// Floating Labels Implementation
function initializeFloatingLabels() {
    const floatingLabels = document.querySelectorAll('.floating-label');
    
    floatingLabels.forEach(container => {
        const input = container.querySelector('input');
        const label = container.querySelector('label');
        
        if (input && label) {
            // Check if input has value on load
            if (input.value.trim() !== '') {
                label.classList.add('active');
            }
            
            input.addEventListener('focus', () => {
                label.classList.add('active');
                input.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                if (input.value.trim() === '') {
                    label.classList.remove('active');
                }
                input.parentElement.classList.remove('focused');
            });
        }
    });
}

// Glass Panels Enhancement
function initializeGlassPanels() {
    const glassPanels = document.querySelectorAll('.glass-panel');
    
    glassPanels.forEach(panel => {
        // Add hover effect with mouse tracking
        panel.addEventListener('mousemove', (e) => {
            const rect = panel.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            panel.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        panel.addEventListener('mouseleave', () => {
            panel.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
    });
}

// Card Stack Animation
function initializeCardStacks() {
    const cardStacks = document.querySelectorAll('.card-stack');
    
    cardStacks.forEach(stack => {
        const cards = stack.querySelectorAll('.card');
        
        stack.addEventListener('mouseenter', () => {
            cards.forEach((card, index) => {
                const delay = index * 100;
                setTimeout(() => {
                    card.style.transform = `translateY(-${index * 8}px) translateZ(${index * 20}px) rotateX(${index * 2}deg)`;
                }, delay);
            });
        });
        
        stack.addEventListener('mouseleave', () => {
            cards.forEach((card, index) => {
                const delay = index * 50;
                setTimeout(() => {
                    card.style.transform = 'translateY(0px) translateZ(0px) rotateX(0deg)';
                }, delay);
            });
        });
    });
}

// Professional Badge Animation
function initializeProfessionalBadges() {
    const badges = document.querySelectorAll('.professional-badge');
    
    badges.forEach(badge => {
        badge.addEventListener('mouseenter', () => {
            badge.style.transform = 'scale(1.05) translateY(-2px)';
            badge.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.3)';
        });
        
        badge.addEventListener('mouseleave', () => {
            badge.style.transform = 'scale(1) translateY(0px)';
            badge.style.boxShadow = 'none';
        });
    });
}

// Loading States Implementation
function initializeLoadingStates() {
    // Enhanced button loading states
    const loadingButtons = document.querySelectorAll('[data-loading]');
    
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                showButtonLoading(this);
            }
        });
    });
}

function showButtonLoading(button) {
    const originalText = button.innerHTML;
    const loadingText = button.dataset.loading || 'Loading...';
    
    button.classList.add('loading');
    button.disabled = true;
    button.innerHTML = `
        <span class="loading-spinner"></span>
        <span class="loading-text">${loadingText}</span>
    `;
    
    // Auto-reset after 3 seconds if no manual reset
    setTimeout(() => {
        if (button.classList.contains('loading')) {
            hideButtonLoading(button, originalText);
        }
    }, 3000);
}

function hideButtonLoading(button, originalText) {
    button.classList.remove('loading');
    button.disabled = false;
    button.innerHTML = originalText;
}

// Micro-interactions
function initializeMicroInteractions() {
    // Scale on hover elements
    const scaleElements = document.querySelectorAll('.scale-on-hover');
    scaleElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'scale(1)';
        });
    });
    
    // Tilt on hover elements
    const tiltElements = document.querySelectorAll('.tilt-on-hover');
    tiltElements.forEach(element => {
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const mouseX = e.clientX - centerX;
            const mouseY = e.clientY - centerY;
            
            const rotateX = (mouseY / (rect.height / 2)) * 10;
            const rotateY = (mouseX / (rect.width / 2)) * 10;
            
            element.style.transform = `perspective(1000px) rotateX(${-rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
        });
    });
    
    // Floating elements
    initializeFloatingElements();
}

function initializeFloatingElements() {
    const floatingElements = document.querySelectorAll('.floating-element');
    
    floatingElements.forEach((element, index) => {
        // Random floating animation
        const duration = 3000 + (index * 500);
        const distance = 10 + (index * 5);
        
        setInterval(() => {
            element.style.transform = `translateY(-${distance}px)`;
            setTimeout(() => {
                element.style.transform = 'translateY(0px)';
            }, duration / 2);
        }, duration);
    });
}

// Advanced Notification System
function initializeNotificationSystem() {
    // Create notification container if it doesn't exist
    if (!document.getElementById('notification-container')) {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 1000;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }
}

// Enhanced Toast Notifications
function showToastNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    const toast = document.createElement('div');
    
    toast.className = `toast-notification ${type}`;
    toast.style.pointerEvents = 'auto';
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <div class="toast-content" style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="${icons[type]}" style="font-size: 1.25rem;"></i>
            <div class="toast-message" style="flex: 1;">${message}</div>
            <button class="toast-close" style="background: none; border: none; cursor: pointer; opacity: 0.7;" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="toast-progress" style="height: 3px; background: currentColor; opacity: 0.3; margin-top: 0.75rem; border-radius: 2px; transform-origin: left; animation: toast-progress ${duration}ms linear;"></div>
    `;
    
    container.appendChild(toast);
    
    // Trigger show animation
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    
    // Auto remove
    setTimeout(() => {
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, duration);
    
    return toast;
}

// Advanced Scroll Effects
function initializeAdvancedScrollEffects() {
    // Parallax scrolling for hero elements
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
    
    // Staggered fade-in animations
    const staggerElements = document.querySelectorAll('.stagger-animation');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    staggerElements.forEach(element => {
        observer.observe(element);
    });
}

// Professional Form Enhancement
function enhanceProfessionalForms() {
    const forms = document.querySelectorAll('.form-3d');
    
    forms.forEach(form => {
        // Add focus ring effects
        const inputs = form.querySelectorAll('.form-control-3d');
        
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                form.classList.add('form-focused');
            });
            
            input.addEventListener('blur', () => {
                if (!form.querySelector('.form-control-3d:focus')) {
                    form.classList.remove('form-focused');
                }
            });
        });
    });
}

// Add CSS for new animations
const enhancedStyles = document.createElement('style');
enhancedStyles.textContent = `
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes toast-progress {
        from { transform: scaleX(1); }
        to { transform: scaleX(0); }
    }
    
    .form-focused {
        box-shadow: 
            0 25px 50px -12px rgba(102, 126, 234, 0.25),
            0 8px 20px -8px rgba(102, 126, 234, 0.15) !important;
    }
    
    .floating-label.focused label {
        color: #667eea !important;
        transform: translateY(-1.5rem) scale(0.875) !important;
    }
`;
document.head.appendChild(enhancedStyles);

// Export enhanced functions for external use
window.ProfessionalPlatform = {
    showAlert,
    showToastNotification,
    validateInput,
    sortTable,
    filterTable,
    showButtonLoading,
    hideButtonLoading,
    enhanceProfessionalForms
};
