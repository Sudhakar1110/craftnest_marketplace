// CraftNest Artisan Profile List

frappe.listview_settings['Artisan Profile'] = {
    add_fields: ['status', 'verified', 'total_products', 'total_sales', 'rating'],
    get_indicator: function(doc) {
        if (doc.status === 'Active' && doc.verified) {
            return [__('Active & Verified'), 'green', 'status,=,' + doc.status + '|verified,=,1'];
        } else if (doc.status === 'Active') {
            return [__('Active'), 'blue', 'status,=,' + doc.status];
        } else if (doc.status === 'Pending') {
            return [__('Pending'), 'orange', 'status,=,' + doc.status];
        } else if (doc.status === 'Suspended') {
            return [__('Suspended'), 'red', 'status,=,' + doc.status];
        } else {
            return [__('Inactive'), 'gray', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Artisan'), function() {
            frappe.new_doc('Artisan Profile');
        });
    }
};
