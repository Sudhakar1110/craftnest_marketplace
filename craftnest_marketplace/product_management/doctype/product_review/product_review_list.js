// CraftNest Product Review List

frappe.listview_settings['Product Review'] = {
    add_fields: ['status', 'product', 'customer', 'rating', 'review_date', 'verified_purchase'],
    get_indicator: function(doc) {
        if (doc.status === 'Approved') {
            return [__('Approved'), 'green', 'status,=,' + doc.status];
        } else if (doc.status === 'Pending') {
            return [__('Pending'), 'orange', 'status,=,' + doc.status];
        } else if (doc.status === 'Rejected') {
            return [__('Rejected'), 'red', 'status,=,' + doc.status];
        } else {
            return [__('Spam'), 'gray', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Pending Reviews'), function() {
            frappe.set_route('List', 'Product Review', {
                'status': 'Pending'
            });
        });
        
        listview.page.add_action_item(__('Approved Reviews'), function() {
            frappe.set_route('List', 'Product Review', {
                'status': 'Approved'
            });
        });
    }
};
