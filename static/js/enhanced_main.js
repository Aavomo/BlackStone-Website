// Enhanced JavaScript for Blackstone EG & Partners Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initializeHeader();
    initializeScrollReveal();
    initializeBackToTop();
    initializeMobileMenu();
    initializeFormEnhancements();
    initializeLoadingScreen();
    initializeSmoothScrolling();
    initializePortfolioFilters();
    initializeBlogFeatures();
    initializeAnalytics();
    
    // Initialize page-specific features
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        initializeHomePage();
    }
});

// Header scroll effect and navigation
function initializeHeader() {
    const header = document.getElementById('header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove scrolled class
        if (scrollTop > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Hide/show header on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Active navigation highlighting
    const navLinks = document.querySelectorAll('.nav a');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath || 
            (currentPath === '/' && link.getAttribute('href') === '/')) {
            link.classList.add('active');
        }
    });
}

// Scroll reveal animations
function initializeScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // Add staggered animation for grids
                if (entry.target.classList.contains('services-grid') || 
                    entry.target.classList.contains('portfolio-grid') ||
                    entry.target.classList.contains('blog-grid')) {
                    animateGridItems(entry.target);
                }
            }
        });
    }, observerOptions);

    // Observe all scroll-reveal elements
    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);
    });
}

// Animate grid items with stagger effect
function animateGridItems(container) {
    const items = container.children;
    Array.from(items).forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Back to top button
function initializeBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Mobile menu functionality
function initializeMobileMenu() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const nav = document.getElementById('nav');
    
    if (mobileToggle && nav) {
        mobileToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
            mobileToggle.classList.toggle('active');
            
            // Animate hamburger menu
            const spans = mobileToggle.querySelectorAll('span');
            spans.forEach((span, index) => {
                span.style.transform = nav.classList.contains('active') 
                    ? `rotate(${index === 0 ? '45' : index === 1 ? '0' : '-45'}deg) translate(${index === 1 ? '100%' : '0'}, ${index === 0 ? '6px' : index === 2 ? '-6px' : '0'})`
                    : 'none';
                span.style.opacity = nav.classList.contains('active') && index === 1 ? '0' : '1';
            });
        });
        
        // Close menu when clicking on links
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('active');
                mobileToggle.classList.remove('active');
            });
        });
    }
}

// Enhanced form functionality
function initializeFormEnhancements() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearErrors);
        });
        
        // Enhanced form submission
        form.addEventListener('submit', handleFormSubmission);
    });
}

// Field validation
function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    const fieldName = field.name;
    
    // Remove existing errors
    clearFieldErrors(field);
    
    // Validation rules
    const validationRules = {
        name: {
            required: true,
            minLength: 2,
            pattern: /^[a-zA-Z\s]+$/
        },
        email: {
            required: true,
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        },
        phone: {
            pattern: /^[\+]?[0-9\s\-\(\)]+$/
        },
        message: {
            required: true,
            minLength: 10
        }
    };
    
    const rules = validationRules[fieldName];
    if (!rules) return;
    
    const errors = [];
    
    // Required validation
    if (rules.required && !value) {
        errors.push(`${capitalizeFirst(fieldName)} is required`);
    }
    
    // Pattern validation
    if (value && rules.pattern && !rules.pattern.test(value)) {
        if (fieldName === 'email') {
            errors.push('Please enter a valid email address');
        } else if (fieldName === 'phone') {
            errors.push('Please enter a valid phone number');
        } else if (fieldName === 'name') {
            errors.push('Name should only contain letters and spaces');
        }
    }
    
    // Length validation
    if (value && rules.minLength && value.length < rules.minLength) {
        errors.push(`${capitalizeFirst(fieldName)} must be at least ${rules.minLength} characters`);
    }
    
    // Show errors
    if (errors.length > 0) {
        showFieldErrors(field, errors);
    }
}

// Clear field errors
function clearFieldErrors(field) {
    field.classList.remove('error');
    const errorDiv = field.parentNode.querySelector('.form-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Show field errors
function showFieldErrors(field, errors) {
    field.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = errors[0];
    field.parentNode.appendChild(errorDiv);
}

// Clear errors on input
function clearErrors(event) {
    const field = event.target;
    if (field.classList.contains('error') && field.value.trim()) {
        clearFieldErrors(field);
    }
}

// Enhanced form submission
function handleFormSubmission(event) {
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    // Validate all fields before submission
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let hasErrors = false;
    
    inputs.forEach(input => {
        validateField({ target: input });
        if (input.classList.contains('error')) {
            hasErrors = true;
        }
    });
    
    if (hasErrors) {
        event.preventDefault();
        showMessage('Please correct the errors before submitting', 'error');
        return;
    }
    
    // Show loading state
    if (submitBtn && btnText && btnLoader) {
        submitBtn.disabled = true;
        btnText.style.opacity = '0';
        btnLoader.style.display = 'block';
        
        // Track form submission
        if (typeof gtag !== 'undefined') {
            gtag('event', 'form_submit', {
                'event_category': 'Contact',
                'event_label': form.id || 'Contact Form'
            });
        }
    }
}

// Show messages
function showMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at top of page
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(messageDiv, main.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.remove();
            }
        }, 5000);
    }
}

// Loading screen
function initializeLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    
    if (loadingScreen) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                setTimeout(() => {
                    loadingScreen.remove();
                }, 500);
            }, 1000);
        });
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                const header = document.getElementById('header');
                const headerHeight = header ? header.offsetHeight : 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Portfolio filters
function initializePortfolioFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioCards = document.querySelectorAll('.portfolio-card');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const filter = btn.getAttribute('data-filter');
            
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Filter cards
            portfolioCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'scale(1)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
            
            // Track filter usage
            if (typeof gtag !== 'undefined') {
                gtag('event', 'portfolio_filter', {
                    'event_category': 'Portfolio',
                    'event_label': filter
                });
            }
        });
    });
}

// Blog features
function initializeBlogFeatures() {
    // Share buttons functionality
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const url = btn.getAttribute('href');
            
            if (url.includes('mailto:')) {
                window.location.href = url;
            } else {
                window.open(url, 'share', 'width=600,height=400');
            }
            
            // Track social sharing
            if (typeof gtag !== 'undefined') {
                const platform = btn.classList.contains('twitter') ? 'Twitter' : 
                               btn.classList.contains('linkedin') ? 'LinkedIn' : 
                               btn.classList.contains('facebook') ? 'Facebook' : 'Email';
                
                gtag('event', 'share', {
                    'event_category': 'Social',
                    'event_label': platform
                });
            }
        });
    });
    
    // Newsletter subscription
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = newsletterForm.querySelector('input[type="email"]').value;
            
            if (validateEmail(email)) {
                showMessage('Thank you for subscribing! We\'ll keep you updated.', 'success');
                newsletterForm.reset();
                
                // Track newsletter signup
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'newsletter_signup', {
                        'event_category': 'Marketing',
                        'event_label': 'Newsletter'
                    });
                }
            } else {
                showMessage('Please enter a valid email address.', 'error');
            }
        });
    }
}

// Home page specific features
function initializeHomePage() {
    // Counter animations (handled in template)
    
    // Service card hover effects
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-15px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Portfolio card hover effects
    const portfolioCards = document.querySelectorAll('.portfolio-card');
    portfolioCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const overlay = card.querySelector('.portfolio-overlay');
            if (overlay) {
                overlay.style.opacity = '1';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const overlay = card.querySelector('.portfolio-overlay');
            if (overlay) {
                overlay.style.opacity = '0';
            }
        });
    });
}

// Analytics initialization
function initializeAnalytics() {
    // Track page views
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            page_title: document.title,
            page_location: window.location.href
        });
    }
    
    // Track scroll depth
    let maxScroll = 0;
    const trackingThresholds = [25, 50, 75, 100];
    
    window.addEventListener('scroll', () => {
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            
            trackingThresholds.forEach(threshold => {
                if (scrollPercent >= threshold && maxScroll >= threshold) {
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'scroll', {
                            'event_category': 'Engagement',
                            'event_label': `${threshold}%`,
                            'value': threshold
                        });
                    }
                    
                    // Remove threshold to avoid duplicate tracking
                    const index = trackingThresholds.indexOf(threshold);
                    if (index > -1) {
                        trackingThresholds.splice(index, 1);
                    }
                }
            });
        }
    });
    
    // Track time on page
    let startTime = Date.now();
    let timeThresholds = [30, 60, 180, 300]; // seconds
    
    setInterval(() => {
        const timeOnPage = Math.floor((Date.now() - startTime) / 1000);
        
        timeThresholds.forEach(threshold => {
            if (timeOnPage >= threshold) {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'timing_complete', {
                        'event_category': 'Engagement',
                        'event_label': `${threshold}s on page`,
                        'value': threshold
                    });
                }
                
                // Remove threshold to avoid duplicate tracking
                const index = timeThresholds.indexOf(threshold);
                if (index > -1) {
                    timeThresholds.splice(index, 1);
                }
            }
        });
    }, 10000); // Check every 10 seconds
    
    // Track outbound links
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        if (!link.href.includes(window.location.hostname)) {
            link.addEventListener('click', () => {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        'event_category': 'Outbound Link',
                        'event_label': link.href
                    });
                }
            });
        }
    });
    
    // Track file downloads
    document.querySelectorAll('a[href*=".pdf"], a[href*=".doc"], a[href*=".zip"]').forEach(link => {
        link.addEventListener('click', () => {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'file_download', {
                    'event_category': 'Downloads',
                    'event_label': link.href.split('/').pop()
                });
            }
        });
    });
}

// Utility functions
function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function validateEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

function debounce(func, wait) {
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

// Performance optimization
function optimizeImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Error handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
    
    // Track JavaScript errors
    if (typeof gtag !== 'undefined') {
        gtag('event', 'exception', {
            'description': e.error.toString(),
            'fatal': false
        });
    }
});

// Browser compatibility checks
function checkBrowserSupport() {
    const unsupportedFeatures = [];
    
    if (!window.fetch) unsupportedFeatures.push('Fetch API');
    if (!window.IntersectionObserver) unsupportedFeatures.push('Intersection Observer');
    if (!CSS.supports('backdrop-filter', 'blur(20px)')) unsupportedFeatures.push('Backdrop Filter');
    
    if (unsupportedFeatures.length > 0) {
        console.warn('Unsupported features detected:', unsupportedFeatures);
        
        // Provide fallbacks
        if (!window.IntersectionObserver) {
            // Fallback: Show all scroll-reveal elements immediately
            document.querySelectorAll('.scroll-reveal').forEach(el => {
                el.classList.add('revealed');
            });
        }
    }
}

// Initialize browser compatibility checks
checkBrowserSupport();

// Performance monitoring
const perfObserver = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (entry.entryType === 'navigation') {
            // Track page load performance
            if (typeof gtag !== 'undefined') {
                gtag('event', 'timing_complete', {
                    'name': 'page_load_time',
                    'value': Math.round(entry.loadEventEnd - entry.fetchStart)
                });
            }
        }
    }
});

if ('PerformanceObserver' in window) {
    perfObserver.observe({ entryTypes: ['navigation'] });
}

// Service Worker registration for PWA (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export functions for global use
window.BlackstoneEG = {
    showMessage,
    validateEmail,
    debounce,
    initializeScrollReveal,
    optimizeImages
};