// CraftNest Customer Profile List

frappe.listview_settings['Customer Profile'] = {
    add_fields: ['loyalty_tier', 'total_orders', 'total_spent', 'newsletter_subscribed'],
    get_indicator: function(doc) {
        if (doc.loyalty_tier === 'Platinum') {
            return [__('Platinum'), 'purple', 'loyalty_tier,=,' + doc.loyalty_tier];
        } else if (doc.loyalty_tier === 'Gold') {
            return [__('Gold'), 'yellow', 'loyalty_tier,=,' + doc.loyalty_tier];
        } else if (doc.loyalty_tier === 'Silver') {
            return [__('Silver'), 'gray', 'loyalty_tier,=,' + doc.loyalty_tier];
        } else {
            return [__('Bronze'), 'orange', 'loyalty_tier,=,' + doc.loyalty_tier];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Customer'), function() {
            frappe.new_doc('Customer Profile');
        });
    }
};
