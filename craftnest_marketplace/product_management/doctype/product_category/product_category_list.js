// CraftNest Product Category List

frappe.listview_settings['Product Category'] = {
    add_fields: ['is_active', 'published', 'product_count', 'parent_category'],
    get_indicator: function(doc) {
        if (doc.published && doc.is_active) {
            return [__('Active'), 'green', 'published,=,1|is_active,=,1'];
        } else if (doc.published) {
            return [__('Published'), 'blue', 'published,=,1'];
        } else if (doc.is_active) {
            return [__('Inactive'), 'orange', 'is_active,=,1'];
        } else {
            return [__('Disabled'), 'gray', 'is_active,=,0'];
        }
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Create Category'), function() {
            frappe.new_doc('Product Category');
        });
    }
};
