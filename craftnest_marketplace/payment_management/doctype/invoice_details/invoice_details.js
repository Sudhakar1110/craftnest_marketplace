// CraftNest Invoice Details Form Controller

frappe.ui.form.on('Invoice Details', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            if (frm.doc.order) {
                frm.add_custom_button(__('View Order'), function() {
                    frappe.set_route('Form', 'Craft Order', frm.doc.order);
                });
            }
            
            frm.add_custom_button(__('Print Invoice'), function() {
                frappe.ui.print.print();
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
                        frm.set_value('customer_email', r.message.email_id);
                    }
                }
            });
        }
    }
});
