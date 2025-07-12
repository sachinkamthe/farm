// Main JavaScript functionality for Farm Fresh Products

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are needed
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize cart functionality
    initializeCartFunctionality();
    
    // Initialize search functionality
    initializeSearchFunctionality();
    
    // Initialize admin functionality
    initializeAdminFunctionality();
    
    // Add smooth scrolling to anchor links
    initializeSmoothScrolling();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Contact form specific validation
    const contactForm = document.querySelector('#contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            const email = contactForm.querySelector('#email');
            const name = contactForm.querySelector('#name');
            const message = contactForm.querySelector('#message');
            
            let isValid = true;
            
            // Name validation
            if (name.value.trim().length < 2) {
                showFieldError(name, 'Name must be at least 2 characters long');
                isValid = false;
            } else {
                clearFieldError(name);
            }
            
            // Email validation
            if (!isValidEmail(email.value)) {
                showFieldError(email, 'Please enter a valid email address');
                isValid = false;
            } else {
                clearFieldError(email);
            }
            
            // Message validation
            if (message.value.trim().length < 10) {
                showFieldError(message, 'Message must be at least 10 characters long');
                isValid = false;
            } else {
                clearFieldError(message);
            }
            
            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    }
}

// Cart functionality
function initializeCartFunctionality() {
    // Cart quantity update buttons
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            const productId = this.dataset.productId;
            const quantityInput = document.querySelector(`#quantity-${productId}`);
            
            if (quantityInput) {
                let currentQuantity = parseInt(quantityInput.value);
                
                if (action === 'increase') {
                    currentQuantity += 1;
                } else if (action === 'decrease' && currentQuantity > 1) {
                    currentQuantity -= 1;
                }
                
                quantityInput.value = currentQuantity;
                updateCartItem(productId, currentQuantity);
            }
        });
    });
    
    // Add to cart buttons with loading state
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const originalText = this.innerHTML;
            this.innerHTML = '<i data-feather="loader" class="me-2"></i>Adding...';
            this.disabled = true;
            
            // Re-enable button after a short delay (simulating processing)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
                feather.replace(); // Re-initialize feather icons
            }, 1000);
        });
    });
}

// Search functionality
function initializeSearchFunctionality() {
    const searchInput = document.querySelector('#searchInput');
    const searchForm = document.querySelector('#searchForm');
    
    if (searchInput) {
        // Add search suggestions/autocomplete functionality
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    // In a real application, you might fetch search suggestions here
                    console.log('Searching for:', query);
                }, 300);
            }
        });
        
        // Handle search form submission
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                const query = searchInput.value.trim();
                if (query.length < 2) {
                    e.preventDefault();
                    showAlert('Please enter at least 2 characters to search', 'warning');
                }
            });
        }
    }
    
    // Category filter buttons
    const categoryButtons = document.querySelectorAll('.category-filter-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active state
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter products (in a real application, this might make an AJAX request)
            const category = this.dataset.category;
            filterProductsByCategory(category);
        });
    });
}

// Admin functionality
function initializeAdminFunctionality() {
    // Product form validation in admin
    const productForms = document.querySelectorAll('.product-form');
    productForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const name = form.querySelector('[name="name"]');
            const price = form.querySelector('[name="price"]');
            const description = form.querySelector('[name="description"]');
            
            let isValid = true;
            
            if (name.value.trim().length < 2) {
                showFieldError(name, 'Product name must be at least 2 characters');
                isValid = false;
            }
            
            if (parseFloat(price.value) <= 0) {
                showFieldError(price, 'Price must be greater than 0');
                isValid = false;
            }
            
            if (description.value.trim().length < 10) {
                showFieldError(description, 'Description must be at least 10 characters');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}

// Smooth scrolling
function initializeSmoothScrolling() {
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.alert-container') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove alert after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'alert-container';
    document.body.insertBefore(container, document.body.firstChild);
    return container;
}

function updateCartItem(productId, quantity) {
    // In a real application, this would make an AJAX request
    console.log(`Updating cart item ${productId} to quantity ${quantity}`);
    
    // Update the URL to reflect the change
    const updateUrl = `/update_cart/${productId}?quantity=${quantity}`;
    window.location.href = updateUrl;
}

function filterProductsByCategory(category) {
    // In a real application, this might filter products client-side or make an AJAX request
    console.log(`Filtering products by category: ${category}`);
    
    const products = document.querySelectorAll('.product-card');
    products.forEach(card => {
        const productCategory = card.dataset.category;
        
        if (category === 'all' || productCategory === category) {
            card.style.display = 'block';
            card.classList.add('fade-in');
        } else {
            card.style.display = 'none';
        }
    });
}

// Image loading error handling
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Replace broken images with a placeholder
            this.src = 'https://via.placeholder.com/300x200/228B22/FFFFFF?text=No+Image';
            this.alt = 'Image not available';
        });
    });
});

// Shopping cart persistence (using localStorage)
function saveCartToStorage() {
    const cartData = getCartData();
    localStorage.setItem('farmFreshCart', JSON.stringify(cartData));
}

function loadCartFromStorage() {
    const savedCart = localStorage.getItem('farmFreshCart');
    if (savedCart) {
        try {
            return JSON.parse(savedCart);
        } catch (e) {
            console.error('Error loading cart from storage:', e);
        }
    }
    return {};
}

function getCartData() {
    // This would extract current cart data from the page
    const cartItems = document.querySelectorAll('.cart-item');
    const cart = {};
    
    cartItems.forEach(item => {
        const productId = item.dataset.productId;
        const quantity = item.querySelector('.quantity-input').value;
        cart[productId] = { quantity: parseInt(quantity) };
    });
    
    return cart;
}

// Performance optimization: Lazy loading for images
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// Call lazy loading initialization
document.addEventListener('DOMContentLoaded', initializeLazyLoading);
