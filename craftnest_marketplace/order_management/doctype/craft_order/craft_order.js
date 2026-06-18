// CraftNest Craft Order Form Controller

frappe.ui.form.on('Craft Order', {
    refresh: function(frm) {
        // View related documents
        if (!frm.is_new()) {
            if (frm.doc.sales_order) {
                frm.add_custom_button(__('View Sales Order'), function() {
                    frappe.set_route('Form', 'Sales Order', frm.doc.sales_order);
                });
            }
            
            if (frm.doc.shipping_details) {
                frm.add_custom_button(__('View Shipping Details'), function() {
                    frappe.set_route('Form', 'Shipping Details', frm.doc.shipping_details);
                });
            }
            
            // Print buttons
            frm.add_custom_button(__('Print Order'), function() {
                frappe.ui.print.print();
            });
        }
    },
    
    items_on_form_rendered: function(frm, cdt, cdn) {
        // Item row rendered
    }
});

// Calculate totals when items change
frappe.ui.form.on('Order Item', {
    quantity: function(frm, cdt, cdn) {
        calculate_item_amount(frappe.get_doc(cdt, cdn));
        frm.refresh_field('items');
        calculate_order_totals(frm);
    },
    
    rate: function(frm, cdt, cdn) {
        calculate_item_amount(frappe.get_doc(cdt, cdn));
        frm.refresh_field('items');
        calculate_order_totals(frm);
    },
    
    product: function(frm, cdt, cdn) {
        var item = frappe.get_doc(cdt, cdn);
        if (item.product) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    'doctype': 'Craft Product',
                    'name': item.product
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, 'product_name', r.message.product_name);
                        frappe.model.set_value(cdt, cdn, 'rate', r.message.sale_price || r.message.price);
                        calculate_item_amount(item);
                        frm.refresh_field('items');
                        calculate_order_totals(frm);
                    }
                }
            });
        }
    },
    
    remove: function(frm) {
        calculate_order_totals(frm);
    }
});

function calculate_item_amount(item) {
    if (item.quantity && item.rate) {
        frappe.model.set_value(item.doctype, item.name, 'amount', item.quantity * item.rate);
    }
}

function calculate_order_totals(frm) {
    var subtotal = 0;
    frm.doc.items.forEach(function(item) {
        if (item.amount) {
            subtotal += item.amount;
        }
    });
    
    frm.set_value('subtotal', subtotal);
    frm.set_value('tax_amount', subtotal * 0.18);
    frm.set_value('total_amount', subtotal + (frm.doc.shipping_charges || 0) + (subtotal * 0.18));
}
