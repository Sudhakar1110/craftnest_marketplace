// CraftNest Shipping Details Form Controller

frappe.ui.form.on('Shipping Details', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.order) {
            frm.add_custom_button(__('View Order'), function() {
                frappe.set_route('Form', 'Craft Order', frm.doc.order);
            });
        }
        
        if (frm.doc.tracking_number && frm.doc.tracking_url) {
            frm.add_custom_button(__('Track Shipment'), function() {
                window.open(frm.doc.tracking_url, '_blank');
            });
        }
    },
    
    status: function(frm) {
        if (frm.doc.status === 'Shipped' && !frm.doc.shipped_date) {
            frm.set_value('shipped_date', frappe.datetime.now_date());
        } else if (frm.doc.status === 'Delivered') {
            frm.set_value('delivered_date', frappe.datetime.now_date());
        }
    },
    
    carrier: function(frm) {
        if (frm.doc.carrier) {
            // Auto-generate tracking URL based on carrier
            var carrier = frm.doc.carrier.toLowerCase();
            if (carrier.includes('dhl')) {
                frm.set_value('tracking_url', 'https://www.dhl.com/track?tracking-id=' + (frm.doc.tracking_number || ''));
            } else if (carrier.includes('fedex')) {
                frm.set_value('tracking_url', 'https://www.fedex.com/fedextrack/?trknbr=' + (frm.doc.tracking_number || ''));
            } else if (carrier.includes('ups')) {
                frm.set_value('tracking_url', 'https://www.ups.com/track?tracknum=' + (frm.doc.tracking_number || ''));
            } else if (carrier.includes('india post') || carrier.includes('speed post')) {
                frm.set_value('tracking_url', 'https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx?trackingno=' + (frm.doc.tracking_number || ''));
            }
        }
    }
});
