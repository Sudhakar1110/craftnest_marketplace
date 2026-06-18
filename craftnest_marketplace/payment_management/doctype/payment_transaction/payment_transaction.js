// CraftNest Payment Transaction Form Controller

frappe.ui.form.on('Payment Transaction', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            if (frm.doc.order) {
                frm.add_custom_button(__('View Order'), function() {
                    frappe.set_route('Form', 'Craft Order', frm.doc.order);
                });
            }
            
            if (frm.doc.status === 'Completed') {
                frm.add_custom_button(__('Process Refund'), function() {
                    show_refund_dialog(frm);
                });
            }
        }
    },
    
    amount: function(frm) {
        frm.call({
            method: 'calculate_net_amount',
            doc: frm.doc,
            callback: function() {
                frm.refresh_fields();
            }
        });
    },
    
    transaction_fee: function(frm) {
        frm.call({
            method: 'calculate_net_amount',
            doc: frm.doc,
            callback: function() {
                frm.refresh_fields();
            }
        });
    }
});

function show_refund_dialog(frm) {
    var dialog = new frappe.ui.Dialog({
        title: __('Process Refund'),
        fields: [
            {
                fieldtype: 'Currency',
                fieldname: 'refund_amount',
                label: __('Refund Amount'),
                options: 'INR',
                default: frm.doc.amount,
                reqd: 1
            },
            {
                fieldtype: 'Small Text',
                fieldname: 'refund_reason',
                label: __('Reason for Refund'),
                reqd: 1
            }
        ],
        primary_action: function() {
            var values = dialog.get_values();
            frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    'doctype': 'Payment Transaction',
                    'name': frm.doc.name,
                    'fieldname': {
                        'refund_amount': values.refund_amount,
                        'refund_reason': values.refund_reason,
                        'status': values.refund_amount == frm.doc.amount ? 'Refunded' : 'Partially Refunded'
                    }
                },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Refund processed successfully'));
                        frm.reload_doc();
                    }
                }
            });
            dialog.hide();
        }
    });
    dialog.show();
}
