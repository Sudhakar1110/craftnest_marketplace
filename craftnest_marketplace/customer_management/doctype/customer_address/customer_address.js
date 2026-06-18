// CraftNest Customer Address Form Controller

frappe.ui.form.on('Customer Address', {
    refresh: function(frm) {
        if (frm.doc.is_default_shipping) {
            frappe.msgprint(__('This is the default shipping address'));
        }
    },
    
    is_default_shipping: function(frm) {
        if (frm.doc.is_default_shipping) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    'doctype': 'Customer Address',
                    'filters': {
                        'customer': frm.doc.customer,
                        'is_default_shipping': 1,
                        'name': ['!=', frm.doc.name]
                    },
                    'limit_page_length': 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        frappe.confirm(
                            __('Customer already has a default shipping address. Do you want to set this as the new default?'),
                            function() {
                                // User confirmed, proceed
                            },
                            function() {
                                frm.set_value('is_default_shipping', 0);
                            }
                        );
                    }
                }
            });
        }
    }
});
