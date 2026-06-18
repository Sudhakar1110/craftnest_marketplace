// CraftNest Artisan Shop List

frappe.listview_settings['Artisan Shop'] = {
    add_fields: ['status', 'published', 'total_products', 'total_sales', 'artisan'],
    get_indicator: function(doc) {
        if (doc.published && doc.status === 'Active') {
            return [__('Live'), 'green', 'published,=,1|status,=,' + doc.status];
        } else if (doc.published) {
            return [__('Published'), 'blue', 'published,=,1'];
        } else if (doc.status === 'Active') {
            return [__('Inactive'), 'orange', 'status,=,' + doc.status];
        } else if (doc.status === 'Suspended') {
            return [__('Suspended'), 'red', 'status,=,' + doc.status];
        } else {
            return [__('Draft'), 'gray', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Shop'), function() {
            frappe.new_doc('Artisan Shop');
        });
    }
};
