// CraftNest Product Category Form Controller

frappe.ui.form.on('Product Category', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View on Website'), function() {
                if (frm.doc.route) {
                    window.open('/products/' + frm.doc.route, '_blank');
                } else {
                    frappe.msgprint(__('Category not published'));
                }
            });
            
            frm.add_custom_button(__('View Products'), function() {
                frappe.set_route('List', 'Craft Product', {
                    'category': frm.doc.name
                });
            });
        }
    },
    
    category_name: function(frm) {
        if (frm.doc.category_name && !frm.doc.route) {
            frm.call({
                method: 'frappe.utils.slugify',
                args: {
                    'string': frm.doc.category_name
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('route', r.message);
                    }
                }
            });
        }
    }
});
