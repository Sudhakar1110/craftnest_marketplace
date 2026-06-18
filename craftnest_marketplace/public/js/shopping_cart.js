// CraftNest Marketplace - Shopping Cart JavaScript

// Cart state management
var cartState = {
    items: {},
    subtotal: 0,
    tax: 0,
    shipping: 0,
    total: 0
};

// Initialize cart from server
function initCart() {
    frappe.call({
        method: 'craftnest_marketplace.api.cart.get_cart',
        callback: function(r) {
            if (r.message) {
                cartState = r.message;
                updateCartUI();
            }
        }
    });
}

// Update cart UI
function updateCartUI() {
    var cartCount = Object.keys(cartState.items).length;
    var cartCountElements = document.querySelectorAll('#cart-count');
    cartCountElements.forEach(function(el) {
        el.textContent = cartCount;
    });
}

// Add item to cart
function addToCart(productId, qty) {
    qty = qty || 1;
    
    frappe.call({
        method: 'craftnest_marketplace.api.cart.add_to_cart',
        args: {
            product: productId,
            qty: qty
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                cartState = r.message.cart;
                updateCartUI();
                showNotification('Item added to cart', 'success');
            } else {
                showNotification(r.message ? r.message.message : 'Error adding to cart', 'error');
            }
        }
    });
}

// Remove item from cart
function removeFromCart(productId) {
    frappe.call({
        method: 'craftnest_marketplace.api.cart.remove_from_cart',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                cartState = r.message.cart;
                updateCartUI();
                // Reload page to update cart display
                location.reload();
            }
        }
    });
}

// Update cart item quantity
function updateQuantity(productId, qty) {
    if (qty < 1) {
        removeFromCart(productId);
        return;
    }
    
    frappe.call({
        method: 'craftnest_marketplace.api.cart.update_cart_item',
        args: {
            product: productId,
            qty: qty
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                cartState = r.message.cart;
                updateCartUI();
                location.reload();
            }
        }
    });
}

// Clear entire cart
function clearCart() {
    if (!confirm('Are you sure you want to clear your cart?')) {
        return;
    }
    
    frappe.call({
        method: 'craftnest_marketplace.api.cart.clear_cart',
        callback: function(r) {
            if (r.message && r.message.success) {
                cartState = { items: {}, subtotal: 0, tax: 0, shipping: 0, total: 0 };
                updateCartUI();
                location.reload();
            }
        }
    });
}

// Get cart count
function getCartCount() {
    return Object.keys(cartState.items).length;
}

// Show notification
function showNotification(message, type) {
    type = type || 'info';
    var indicator = 'blue';
    if (type === 'success') indicator = 'green';
    if (type === 'error') indicator = 'red';
    if (type === 'warning') indicator = 'orange';
    
    frappe.msgprint({
        message: message,
        indicator: indicator
    });
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart
    initCart();
});
