// CraftNest Customer Address List

frappe.listview_settings['Customer Address'] = {
    add_fields: ['customer', 'address_type', 'is_default_shipping', 'city', 'state'],
    get_indicator: function(doc) {
        if (doc.is_default_shipping) {
            return [__('Default'), 'green', 'is_default_shipping,=,1'];
        } else {
            return [__(doc.address_type || 'Other'), 'gray', 'address_type,=,' + doc.address_type];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Address'), function() {
            frappe.new_doc('Customer Address');
        });
    }
};
