// CraftNest Craft Order List

frappe.listview_settings['Craft Order'] = {
    add_fields: ['status', 'payment_status', 'workflow_state', 'customer', 'total_amount', 'order_date'],
    get_indicator: function(doc) {
        if (doc.status === 'Delivered' && doc.payment_status === 'Paid') {
            return [__('Completed'), 'green', 'status,=,' + doc.status + '|payment_status,=,' + doc.payment_status];
        } else if (doc.status === 'Cancelled') {
            return [__('Cancelled'), 'red', 'status,=,' + doc.status];
        } else if (doc.status === 'Shipped') {
            return [__('Shipped'), 'blue', 'status,=,' + doc.status];
        } else if (doc.status === 'Processing') {
            return [__('Processing'), 'orange', 'status,=,' + doc.status];
        } else if (doc.payment_status === 'Pending') {
            return [__('Payment Pending'), 'yellow', 'payment_status,=,' + doc.payment_status];
        } else {
            return [__(doc.status), 'gray', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Pending Orders'), function() {
            frappe.set_route('List', 'Craft Order', {
                'status': 'Pending'
            });
        });
        
        listview.page.add_action_item(__('Recent Orders'), function() {
            frappe.route_options = {
                "order_date": ["between", frappe.datetime.add_days(frappe.datetime.now_date(), -7), frappe.datetime.now_date()]
            };
            frappe.route_options = {};
            frappe.set_route('List', 'Craft Order');
        });
    }
};
