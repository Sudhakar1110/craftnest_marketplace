// CraftNest Artisan Verification List

frappe.listview_settings['Artisan Verification'] = {
    add_fields: ['workflow_state', 'artisan', 'verification_type', 'submission_date'],
    get_indicator: function(doc) {
        var states = {
            'Draft': ['Draft', 'gray'],
            'Pending Review': ['Pending Review', 'orange'],
            'Documents Verified': ['Documents Verified', 'blue'],
            'Approved': ['Approved', 'green'],
            'Rejected': ['Rejected', 'red']
        };
        
        var state = states[doc.workflow_state] || ['Unknown', 'gray'];
        return [__(state[0]), state[1], 'workflow_state,=,' + doc.workflow_state];
    },
    onload: function(listview) {
        listview.page.add_action_item(__('Pending Verifications'), function() {
            frappe.call({
                method: 'craftnest_marketplace.artisan_management.doctype.artisan_verification.artisan_verification.get_pending_verifications',
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        frappe.msgprint(__('{0} pending verifications found').format(r.message.length));
                    } else {
                        frappe.msgprint(__('No pending verifications'));
                    }
                }
            });
        });
    }
};
