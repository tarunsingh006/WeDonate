/**
 * Accessibility Enhancement Script for WeDonate Platform
 * Provides keyboard navigation, screen reader support, and focus management
 */

(function() {
    'use strict';

    // Initialize accessibility features when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        initializeAccessibility();
    });

    function initializeAccessibility() {
        setupKeyboardNavigation();
        setupFocusManagement();
        setupFormValidation();
        setupScreenReaderAnnouncements();
        setupSkipLinks();
        setupReducedMotion();
    }

    /**
     * Enhanced keyboard navigation
     */
    function setupKeyboardNavigation() {
        // Escape key to close modals/dropdowns
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAllModals();
                closeAllDropdowns();
            }
        });

        // Arrow key navigation for menus
        const menuItems = document.querySelectorAll('[role="menubar"] [role="menuitem"]');
        menuItems.forEach((item, index) => {
            item.addEventListener('keydown', function(e) {
                switch(e.key) {
                    case 'ArrowRight':
                    case 'ArrowDown':
                        e.preventDefault();
                        focusNextMenuItem(menuItems, index);
                        break;
                    case 'ArrowLeft':
                    case 'ArrowUp':
                        e.preventDefault();
                        focusPreviousMenuItem(menuItems, index);
                        break;
                    case 'Home':
                        e.preventDefault();
                        menuItems[0].focus();
                        break;
                    case 'End':
                        e.preventDefault();
                        menuItems[menuItems.length - 1].focus();
                        break;
                }
            });
        });

        // Tab trapping for modals
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                const modal = document.querySelector('.modal:not([style*="display: none"])');
                if (modal) {
                    trapFocus(e, modal);
                }
            }
        });
    }

    /**
     * Focus management utilities
     */
    function setupFocusManagement() {
        // Store focus before opening modals
        let lastFocusedElement = null;

        // Modal focus management
        const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', function() {
                lastFocusedElement = this;
            });
        });

        // Return focus when modal closes
        document.addEventListener('hidden.bs.modal', function() {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
                lastFocusedElement = null;
            }
        });

        // Focus first focusable element when modal opens
        document.addEventListener('shown.bs.modal', function(e) {
            const modal = e.target;
            const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (firstFocusable) {
                firstFocusable.focus();
            }
        });
    }

    /**
     * Enhanced form validation with accessibility
     */
    function setupFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                // Real-time validation feedback
                input.addEventListener('blur', function() {
                    validateField(this);
                });

                input.addEventListener('input', function() {
                    if (this.getAttribute('aria-invalid') === 'true') {
                        validateField(this);
                    }
                });
            });

            // Form submission validation
            form.addEventListener('submit', function(e) {
                let isValid = true;
                let firstInvalidField = null;

                inputs.forEach(input => {
                    if (!validateField(input)) {
                        isValid = false;
                        if (!firstInvalidField) {
                            firstInvalidField = input;
                        }
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    firstInvalidField.focus();
                    announceToScreenReader('Form has errors. Please check the highlighted fields.');
                }
            });
        });
    }

    /**
     * Validate individual form field
     */
    function validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        const type = field.type;
        let isValid = true;
        let errorMessage = '';

        // Remove existing error message
        removeErrorMessage(field);

        // Required field validation
        if (isRequired && !value) {
            isValid = false;
            errorMessage = `${getFieldLabel(field)} is required.`;
        }

        // Email validation
        if (type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }

        // Password validation
        if (type === 'password' && value && field.hasAttribute('pattern')) {
            const pattern = new RegExp(field.getAttribute('pattern'));
            if (!pattern.test(value)) {
                isValid = false;
                errorMessage = field.getAttribute('title') || 'Password does not meet requirements.';
            }
        }

        // Phone validation
        if (type === 'tel' && value && !isValidPhone(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number.';
        }

        // Update field state
        field.setAttribute('aria-invalid', !isValid);
        
        if (!isValid) {
            showErrorMessage(field, errorMessage);
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }

        return isValid;
    }

    /**
     * Screen reader announcements
     */
    function setupScreenReaderAnnouncements() {
        // Create live region for announcements
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.id = 'live-region';
        document.body.appendChild(liveRegion);

        // Announce page changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    const addedNode = mutation.addedNodes[0];
                    if (addedNode.nodeType === Node.ELEMENT_NODE) {
                        const heading = addedNode.querySelector('h1, h2, h3');
                        if (heading) {
                            announceToScreenReader(`Page updated: ${heading.textContent}`);
                        }
                    }
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Skip links functionality
     */
    function setupSkipLinks() {
        const skipLinks = document.querySelectorAll('.skip-link');
        
        skipLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                
                if (target) {
                    target.focus();
                    target.scrollIntoView({ behavior: 'smooth' });
                    announceToScreenReader(`Skipped to ${target.textContent || targetId}`);
                }
            });
        });
    }

    /**
     * Reduced motion support
     */
    function setupReducedMotion() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            // Disable animations
            const style = document.createElement('style');
            style.textContent = `
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }
            `;
            document.head.appendChild(style);
        }
    }

    // Utility functions
    function focusNextMenuItem(items, currentIndex) {
        const nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex].focus();
    }

    function focusPreviousMenuItem(items, currentIndex) {
        const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
        items[prevIndex].focus();
    }

    function trapFocus(e, container) {
        const focusableElements = container.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    }

    function closeAllModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }

    function closeAllDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }

    function announceToScreenReader(message) {
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    function getFieldLabel(field) {
        const label = document.querySelector(`label[for="${field.id}"]`);
        return label ? label.textContent.replace(/\s*\*\s*$/, '').trim() : field.name || 'Field';
    }

    function showErrorMessage(field, message) {
        const errorId = `${field.id}-error`;
        let errorElement = document.getElementById(errorId);
        
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = errorId;
            errorElement.className = 'error-message';
            errorElement.setAttribute('role', 'alert');
            field.parentNode.appendChild(errorElement);
            
            // Update aria-describedby
            const describedBy = field.getAttribute('aria-describedby') || '';
            field.setAttribute('aria-describedby', `${describedBy} ${errorId}`.trim());
        }
        
        errorElement.textContent = message;
    }

    function removeErrorMessage(field) {
        const errorId = `${field.id}-error`;
        const errorElement = document.getElementById(errorId);
        
        if (errorElement) {
            errorElement.remove();
            
            // Update aria-describedby
            const describedBy = field.getAttribute('aria-describedby') || '';
            const newDescribedBy = describedBy.replace(errorId, '').trim();
            if (newDescribedBy) {
                field.setAttribute('aria-describedby', newDescribedBy);
            } else {
                field.removeAttribute('aria-describedby');
            }
        }
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhone(phone) {
        const phoneRegex = /^[0-9]{10}$/;
        return phoneRegex.test(phone.replace(/\D/g, ''));
    }

    // Enhanced login form accessibility
    function setupLoginFormAccessibility() {
        // Add ARIA labels and descriptions for login forms
        const loginForms = document.querySelectorAll('form[action*="login"]');
        
        loginForms.forEach(form => {
            // Add form landmark
            form.setAttribute('role', 'form');
            form.setAttribute('aria-label', 'Login form');
            
            // Enhance password toggle buttons
            const passwordToggles = form.querySelectorAll('.professional-toggle-password');
            passwordToggles.forEach(toggle => {
                toggle.setAttribute('aria-label', 'Toggle password visibility');
                toggle.setAttribute('aria-pressed', 'false');
                
                toggle.addEventListener('click', function() {
                    const pressed = this.getAttribute('aria-pressed') === 'true';
                    this.setAttribute('aria-pressed', !pressed);
                    
                    const passwordField = this.previousElementSibling;
                    const isVisible = passwordField.type === 'text';
                    
                    announceToScreenReader(
                        isVisible ? 'Password is now visible' : 'Password is now hidden'
                    );
                });
            });
            
            // Add live region for form errors
            const errorContainer = document.createElement('div');
            errorContainer.setAttribute('aria-live', 'polite');
            errorContainer.setAttribute('aria-atomic', 'true');
            errorContainer.className = 'sr-only';
            errorContainer.id = 'form-errors';
            form.insertBefore(errorContainer, form.firstChild);
            
            // Enhanced error announcements
            const alerts = form.querySelectorAll('.alert');
            alerts.forEach(alert => {
                alert.setAttribute('role', 'alert');
                alert.setAttribute('aria-atomic', 'true');
            });
        });
    }
    
    // Professional card accessibility
    function setupProfessionalCardAccessibility() {
        const professionalCards = document.querySelectorAll('.professional-card, .professional-feature-card');
        
        professionalCards.forEach(card => {
            // Add keyboard navigation
            const actionButtons = card.querySelectorAll('a, button');
            if (actionButtons.length === 0) {
                card.setAttribute('tabindex', '0');
                card.setAttribute('role', 'article');
            }
            
            // Add focus indicators
            card.addEventListener('focus', function() {
                this.style.outline = '3px solid #667eea';
                this.style.outlineOffset = '2px';
            });
            
            card.addEventListener('blur', function() {
                this.style.outline = 'none';
            });
        });
    }
    
    // Initialize enhanced accessibility features
    document.addEventListener('DOMContentLoaded', function() {
        setupLoginFormAccessibility();
        setupProfessionalCardAccessibility();
    });
    
    // Export functions for global use
    window.WeDonateAccessibility = {
        announceToScreenReader,
        validateField,
        trapFocus,
        setupLoginFormAccessibility,
        setupProfessionalCardAccessibility
    };

})();