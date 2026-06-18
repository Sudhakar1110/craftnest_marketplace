// CraftNest Customer Profile Form Controller

frappe.ui.form.on('Customer Profile', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Orders'), function() {
                frappe.set_route('List', 'Craft Order', {
                    'customer': frm.doc.email
                });
            });
            
            frm.add_custom_button(__('View Wishlist'), function() {
                frappe.set_route('List', 'Wishlist', {
                    'customer': frm.doc.name
                });
            });
            
            frm.add_custom_button(__('Update Statistics'), function() {
                frm.call('update_statistics').then(() => {
                    frappe.msgprint(__('Statistics updated successfully'));
                    frm.reload_doc();
                });
            });
        }
    },
    
    email: function(frm) {
        if (frm.doc.email && !frm.doc.customer_code) {
            frappe.call({
                method: 'frappe.client.exists',
                args: {
                    'doctype': 'User',
                    'name': frm.doc.email
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__('User already exists with this email'));
                    }
                }
            });
        }
    }
});
