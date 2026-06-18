// CraftNest Artisan Profile Form Controller

frappe.ui.form.on('Artisan Profile', {
    refresh: function(frm) {
        // Create User button
        if (frm.doc.email && !frm.doc.user) {
            frm.add_custom_button(__('Create User'), function() {
                frappe.call({
                    method: 'craftnest_marketplace.artisan_management.doctype.artisan_profile.artisan_profile.create_user',
                    args: {
                        artisan: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__('User created successfully'));
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('User already exists or email not provided'));
                        }
                    }
                });
            });
        }
        
        // View Products button
        if (frm.doc.name && !frm.is_new()) {
            frm.add_custom_button(__('View Products'), function() {
                frappe.set_route('List', 'Craft Product', {
                    'artisan': frm.doc.name
                });
            });
            
            frm.add_custom_button(__('View Shop'), function() {
                frappe.set_route('Form', 'Artisan Shop', {
                    'artisan': frm.doc.name
                });
            });
        }
        
        // Update Statistics button
        if (!frm.is_new()) {
            frm.add_custom_button(__('Update Statistics'), function() {
                frm.call('update_statistics').then(() => {
                    frappe.msgprint(__('Statistics updated successfully'));
                    frm.reload_doc();
                });
            });
        }
    },
    
    email: function(frm) {
        // Auto-suggest username from email
        if (frm.doc.email && !frm.doc.user) {
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
