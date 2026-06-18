// CraftNest Marketplace - Main JavaScript

// ===== Cart Functions =====
function addToCart(productId, event) {
    if (event) event.preventDefault();
    
    var quantity = 1;
    var qtyInput = document.getElementById('quantity');
    if (qtyInput) {
        quantity = parseInt(qtyInput.value) || 1;
    }
    
    frappe.call({
        method: 'craftnest_marketplace.api.cart.add_to_cart',
        args: {
            product: productId,
            qty: quantity
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                updateCartCount();
                frappe.msgprint({
                    title: __('Added to Cart'),
                    indicator: 'green',
                    message: __('Item added to your cart!')
                });
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: r.message ? r.message.message : __('Failed to add item to cart')
                });
            }
        }
    });
}

function removeFromCart(productId) {
    frappe.call({
        method: 'craftnest_marketplace.api.cart.remove_from_cart',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                location.reload();
            }
        }
    });
}

function updateCartItem(productId, delta, directValue) {
    var qty;
    if (directValue !== undefined) {
        qty = parseInt(directValue);
    } else {
        var input = event.target.parentElement.querySelector('input');
        qty = parseInt(input.value) + delta;
    }
    
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
                location.reload();
            }
        }
    });
}

function clearCart() {
    if (confirm('Are you sure you want to clear your cart?')) {
        frappe.call({
            method: 'craftnest_marketplace.api.cart.clear_cart',
            callback: function(r) {
                if (r.message && r.message.success) {
                    location.reload();
                }
            }
        });
    }
}

function updateCartCount() {
    frappe.call({
        method: 'craftnest_marketplace.api.cart.get_cart_count',
        callback: function(r) {
            var count = r.message || 0;
            var badges = document.querySelectorAll('#cart-count');
            badges.forEach(function(badge) {
                badge.textContent = count;
            });
        }
    });
}

// ===== Wishlist Functions =====
function addToWishlist(productId, event) {
    if (event) event.preventDefault();
    
    frappe.call({
        method: 'craftnest_marketplace.api.wishlist.add_to_wishlist',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                updateWishlistCount();
                frappe.msgprint({
                    title: __('Added to Wishlist'),
                    indicator: 'green',
                    message: __('Item added to your wishlist!')
                });
            } else if (r.message && r.message.message === 'login_required') {
                window.location.href = '/login?redirect=/products';
            }
        }
    });
}

function removeFromWishlist(productId) {
    frappe.call({
        method: 'craftnest_marketplace.api.wishlist.remove_from_wishlist',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                location.reload();
            }
        }
    });
}

function moveToWishlist(productId) {
    frappe.call({
        method: 'craftnest_marketplace.api.wishlist.add_to_wishlist',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                removeFromCart(productId);
            }
        }
    });
}

function updateWishlistCount() {
    frappe.call({
        method: 'craftnest_marketplace.api.wishlist.get_wishlist_count',
        callback: function(r) {
            var count = r.message || 0;
            var badges = document.querySelectorAll('#wishlist-count');
            badges.forEach(function(badge) {
                badge.textContent = count;
            });
        }
    });
}

// ===== Quick View =====
function quickView(productId, event) {
    if (event) event.preventDefault();
    
    frappe.call({
        method: 'craftnest_marketplace.api.product.get_product_details',
        args: {
            product: productId
        },
        callback: function(r) {
            if (r.message) {
                showQuickViewModal(r.message);
            }
        }
    });
}

function showQuickViewModal(product) {
    var modalHtml = `
    <div class="modal fade" id="quickViewModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${product.product_name}</h5>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6">
                            <img src="${product.main_image || '/assets/craftnest_marketplace/images/placeholder.png'}" 
                                 class="img-fluid" alt="${product.product_name}">
                        </div>
                        <div class="col-md-6">
                            <p class="text-muted">${product.category}</p>
                            <h3>₹${product.sale_price || product.price}</h3>
                            <p>${product.description}</p>
                            <div class="mt-3">
                                <button class="btn btn-primary" onclick="addToCart('${product.name}')">
                                    Add to Cart
                                </button>
                                <button class="btn btn-outline-secondary" onclick="addToWishlist('${product.name}')">
                                    Add to Wishlist
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Remove existing modal if any
    var existingModal = document.getElementById('quickViewModal');
    if (existingModal) existingModal.remove();
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    $('#quickViewModal').modal('show');
}

// ===== Order Functions =====
function placeOrder() {
    var address = document.querySelector('input[name="address"]:checked');
    var paymentMethod = document.querySelector('input[name="payment_method"]:checked');
    
    if (!address) {
        frappe.msgprint(__('Please select a shipping address'));
        return;
    }
    
    if (!paymentMethod) {
        frappe.msgprint(__('Please select a payment method'));
        return;
    }
    
    frappe.call({
        method: 'craftnest_marketplace.api.checkout.place_order',
        args: {
            address: address.value,
            payment_method: paymentMethod.value
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint({
                    title: __('Order Placed'),
                    indicator: 'green',
                    message: __('Your order has been placed successfully! Order ID: ') + r.message.order_id
                });
                setTimeout(function() {
                    window.location.href = '/my-account/orders';
                }, 2000);
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: r.message ? r.message.message : __('Failed to place order')
                });
            }
        }
    });
}

// ===== Initialize on Page Load =====
frappe.ready(function() {
    // Update cart count
    if (document.querySelector('#cart-count')) {
        updateCartCount();
    }
    
    // Update wishlist count
    if (document.querySelector('#wishlist-count')) {
        updateWishlistCount();
    }
    
    // Product page - increment view count
    var productName = document.querySelector('[data-product-name]');
    if (productName) {
        frappe.call({
            method: 'craftnest_marketplace.product_management.doctype.craft_product.craft_product.increment_view_count',
            args: {
                product: productName.dataset.productName
            }
        });
    }
});
