// CraftNest Craft Product List

frappe.listview_settings['Craft Product'] = {
    add_fields: ['status', 'published', 'stock_status', 'artisan', 'category', 'price', 'sale_price', 'stock_quantity', 'average_rating'],
    get_indicator: function(doc) {
        if (doc.status === 'Published' && doc.published) {
            if (doc.stock_status === 'In Stock') {
                return [__('Active'), 'green', 'status,=,' + doc.status + '|stock_status,=,' + doc.stock_status];
            } else if (doc.stock_status === 'Low Stock') {
                return [__('Low Stock'), 'orange', 'status,=,' + doc.status + '|stock_status,=,' + doc.stock_status];
            } else {
                return [__('Out of Stock'), 'red', 'status,=,' + doc.status];
            }
        } else if (doc.status === 'Draft') {
            return [__('Draft'), 'gray', 'status,=,' + doc.status];
        } else if (doc.status === 'Discontinued') {
            return [__('Discontinued'), 'darkgray', 'status,=,' + doc.status];
        } else {
            return [__(doc.status), 'blue', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Product'), function() {
            frappe.new_doc('Craft Product');
        });
        
        listview.page.add_action_item(__('Low Stock Products'), function() {
            frappe.set_route('List', 'Craft Product', {
                'stock_status': 'Low Stock'
            });
        });
        
        listview.page.add_action_item(__('Featured Products'), function() {
            frappe.set_route('List', 'Craft Product', {
                'featured': 1
            });
        });
    }
};
