// CraftNest Craft Product Form Controller

frappe.ui.form.on('Craft Product', {
    refresh: function(frm) {
        // View on Website
        if (!frm.is_new() && frm.doc.published) {
            frm.add_custom_button(__('View on Website'), function() {
                if (frm.doc.route) {
                    window.open('/products/' + frm.doc.route, '_blank');
                } else {
                    window.open('/products/' + frm.doc.name, '_blank');
                }
            });
        }
        
        // Sync with Item
        frm.add_custom_button(__('Sync with Item'), function() {
            frappe.call({
                method: 'craftnest_marketplace.product_management.doctype.craft_product.craft_product.sync_with_item',
                args: {
                    product: frm.doc.name
                },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Product synced with Item'));
                        frm.reload_doc();
                    }
                }
            });
        });
    },
    
    price: function(frm) {
        calculate_discount(frm);
    },
    
    sale_price: function(frm) {
        calculate_discount(frm);
    },
    
    stock_quantity: function(frm) {
        update_stock_status(frm);
    },
    
    low_stock_threshold: function(frm) {
        update_stock_status(frm);
    },
    
    category: function(frm) {
        if (frm.doc.category) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    'doctype': 'Product Category',
                    'name': frm.doc.category
                },
                callback: function(r) {
                    if (r.message && !frm.doc.sku) {
                        // SKU is auto-generated in Python
                    }
                }
            });
        }
    },
    
    artisan: function(frm) {
        if (frm.doc.artisan) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    'doctype': 'Artisan Profile',
                    'name': frm.doc.artisan
                },
                callback: function(r) {
                    if (r.message) {
                        if (r.message.status !== 'Active') {
                            frappe.msgprint(__('Warning: Artisan is not active'));
                        }
                    }
                }
            });
        }
    },
    
    status: function(frm) {
        if (frm.doc.status === 'Published') {
            frm.set_value('published', 1);
        }
    }
});

function calculate_discount(frm) {
    if (frm.doc.sale_price && frm.doc.price) {
        var discount = ((frm.doc.price - frm.doc.sale_price) / frm.doc.price) * 100;
        frm.set_value('discount_percentage', discount.toFixed(2));
    }
}

function update_stock_status(frm) {
    if (frm.doc.stock_quantity === 0) {
        frm.set_value('stock_status', 'Out of Stock');
    } else if (frm.doc.stock_quantity <= frm.doc.low_stock_threshold) {
        frm.set_value('stock_status', 'Low Stock');
    } else {
        frm.set_value('stock_status', 'In Stock');
    }
}

// Quick Add to Cart (for website)
frappe.provide('craftnest');

craftnest.add_to_cart = function(product, quantity) {
    return frappe.call({
        method: 'craftnest_marketplace.api.cart.add_to_cart',
        args: {
            product: product,
            quantity: quantity || 1
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.msgprint(__('Added to cart!'));
                update_cart_badge();
            } else if (r.message && r.message.error) {
                frappe.msgprint(r.message.error, __('Error'));
            }
        }
    });
};

function update_cart_badge() {
    frappe.call({
        method: 'craftnest_marketplace.utils.jinja.get_cart_count',
        callback: function(r) {
            var badge = document.querySelector('.cart-badge');
            if (badge && r.message) {
                badge.textContent = r.message;
            }
        }
    });
}
