// CraftNest Wishlist Form Controller

frappe.ui.form.on('Wishlist', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View on Website'), function() {
                frappe.set_route('Form', 'Wishlist', frm.doc.name);
            });
        }
    }
});

// Wishlist item row events
frappe.ui.form.on('Wishlist Item', {
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
                        frappe.model.set_value(cdt, cdn, 'price', r.message.price);
                    }
                }
            });
        }
    }
});
