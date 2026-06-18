// CraftNest Payment Transaction List

frappe.listview_settings['Payment Transaction'] = {
    add_fields: ['status', 'order', 'payment_method', 'amount', 'payment_date', 'customer'],
    get_indicator: function(doc) {
        if (doc.status === 'Completed') {
            return [__('Completed'), 'green', 'status,=,' + doc.status];
        } else if (doc.status === 'Pending') {
            return [__('Pending'), 'orange', 'status,=,' + doc.status];
        } else if (doc.status === 'Failed' || doc.status === 'Cancelled') {
            return [__(doc.status), 'red', 'status,=,' + doc.status];
        } else if (doc.status === 'Refunded') {
            return [__('Refunded'), 'gray', 'status,=,' + doc.status];
        } else if (doc.status === 'Partially Refunded') {
            return [__('Partial Refund'), 'yellow', 'status,=,' + doc.status];
        } else {
            return [__(doc.status), 'blue', 'status,=,' + doc.status];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Pending Payments'), function() {
            frappe.set_route('List', 'Payment Transaction', {
                'status': 'Pending'
            });
        });
        
        listview.page.add_action_item(__('Completed Today'), function() {
            var today = frappe.datetime.now_date();
            frappe.route_options = {
                "payment_date": ["between", today, today]
            };
            frappe.set_route('List', 'Payment Transaction');
        });
    }
};
