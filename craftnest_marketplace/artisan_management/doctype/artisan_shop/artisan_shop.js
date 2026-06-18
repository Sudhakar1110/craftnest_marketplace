// CraftNest Artisan Shop Form Controller

frappe.ui.form.on('Artisan Shop', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Shop'), function() {
                if (frm.doc.slug) {
                    window.open('/shop/' + frm.doc.slug, '_blank');
                } else {
                    frappe.msgprint(__('Shop not published yet'));
                }
            });
            
            frm.add_custom_button(__('View Products'), function() {
                frappe.set_route('List', 'Craft Product', {
                    'artisan': frm.doc.artisan
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
    
    shop_name: function(frm) {
        if (frm.doc.shop_name && !frm.doc.slug) {
            frm.call({
                method: 'frappe.utils.slugify',
                args: {
                    'string': frm.doc.shop_name,
                    'reference_doctype': frm.doc.doctype,
                    'reference_name': frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('slug', r.message);
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
    }
});
