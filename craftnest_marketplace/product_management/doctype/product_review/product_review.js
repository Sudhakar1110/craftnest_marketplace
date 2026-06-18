// CraftNest Product Review Form Controller

frappe.ui.form.on('Product Review', {
    refresh: function(frm) {
        if (frm.doc.status === 'Approved') {
            frm.add_custom_button(__('View Product'), function() {
                frappe.set_route('Form', 'Craft Product', frm.doc.product);
            });
        }
    },
    
    customer: function(frm) {
        if (frm.doc.customer) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    'doctype': 'Customer',
                    'name': frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('customer_name', r.message.customer_name);
                    }
                }
            });
        }
    },
    
    status: function(frm) {
        if (frm.doc.status === 'Approved' && frm.is_dirty()) {
            frappe.msgprint(__('Saving this review will update the product and artisan ratings'));
        }
    }
});
