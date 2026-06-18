// CraftNest Shipping Details List

frappe.listview_settings['Shipping Details'] = {
    add_fields: ['status', 'order', 'carrier', 'tracking_number', 'shipped_date', 'estimated_delivery'],
    get_indicator: function(doc) {
        if (doc.status === 'Delivered') {
            return [__('Delivered'), 'green', 'status,=,' + doc.status];
        } else if (doc.status === 'Shipped' || doc.status === 'In Transit') {
            return [__('In Transit'), 'blue', 'status,=,' + doc.status];
        } else if (doc.status === 'Out for Delivery') {
            return [__('Out for Delivery'), 'orange', 'status,=,' + doc.status];
        } else if (doc.status === 'Pending' || doc.status === 'Packed') {
            return [__('Processing'), 'yellow', 'status,=,' + doc.status];
        } else if (doc.status === 'Failed Delivery' || doc.status === 'Returned') {
            return [__('Issue'), 'red', 'status,=,' + doc.status];
        } else {
            return [__(doc.status), 'gray', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Pending Shipments'), function() {
            frappe.set_route('List', 'Shipping Details', {
                'status': ['in', ['Pending', 'Packed']]
            });
        });
    }
};
