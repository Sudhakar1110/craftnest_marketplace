// CraftNest Artisan Verification Form Controller

frappe.ui.form.on('Artisan Verification', {
    refresh: function(frm) {
        // Show current status
        if (frm.doc.workflow_state) {
            frappe.call({
                method: 'frappe.translate.get_dict',
                args: {
                    'doctype': 'Artisan Verification'
                },
                callback: function(r) {
                    // Status is shown via workflow_state field
                }
            });
        }
    },
    
    verification_type: function(frm) {
        // Show/hide fields based on verification type
        update_field_visibility(frm);
    }
});

function update_field_visibility(frm) {
    if (frm.doc.verification_type === 'Basic') {
        frm.toggle_display('business_verification', false);
        frm.toggle_display('additional_documents', false);
    } else if (frm.doc.verification_type === 'Complete') {
        frm.toggle_display('business_verification', false);
        frm.toggle_display('additional_documents', true);
    } else if (frm.doc.verification_type === 'Enterprise') {
        frm.toggle_display('business_verification', true);
        frm.toggle_display('additional_documents', true);
    }
}
