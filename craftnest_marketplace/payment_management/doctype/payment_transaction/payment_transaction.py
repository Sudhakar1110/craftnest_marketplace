# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt, now_datetime


class PaymentTransaction(Document):
    def validate(self):
        self.calculate_net_amount()
        self.set_transaction_id()
    
    def calculate_net_amount(self):
        """Calculate net amount after transaction fee"""
        self.net_amount = flt(self.amount) - flt(self.transaction_fee)
    
    def set_transaction_id(self):
        """Generate unique transaction ID"""
        if not self.transaction_id:
            self.transaction_id = f"TXN-{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}-{frappe.utils.random_string(4)}"
    
    def on_submit(self):
        self.update_order_payment_status()
        self.send_payment_confirmation()
    
    def update_order_payment_status(self):
        """Update order payment status"""
        if self.order and self.status == "Completed":
            order = frappe.get_doc("Craft Order", self.order)
            order.payment_status = "Paid"
            order.save(ignore_permissions=True)
    
    def send_payment_confirmation(self):
        """Send payment confirmation email"""
        if self.status == "Completed":
            try:
                frappe.sendmail(
                    recipients=self.customer,
                    subject=_("Payment Confirmation - {0}").format(self.name),
                    message=self.get_payment_email_template()
                )
            except Exception as e:
                frappe.log_error(f"Error sending payment confirmation: {str(e)}")
    
    def get_payment_email_template(self):
        """Generate payment confirmation email template"""
        return f"""
        <h2>Payment Received!</h2>
        <p>Thank you for your payment.</p>
        <p><strong>Transaction ID:</strong> {self.transaction_id}</p>
        <p><strong>Order ID:</strong> {self.order}</p>
        <p><strong>Amount:</strong> ₹{self.amount}</p>
        <p><strong>Payment Method:</strong> {self.payment_method}</p>
        <p><strong>Payment Date:</strong> {self.payment_date}</p>
        
        <p>We will process your order shortly.</p>
        """
    
    def process_refund(self, amount, reason):
        """Process refund for this transaction"""
        if self.status != "Completed":
            frappe.throw(_("Can only refund completed transactions"))
        
        refund_amount = flt(amount) or self.amount
        
        if refund_amount > self.amount:
            frappe.throw(_("Refund amount cannot exceed transaction amount"))
        
        if refund_amount == self.amount:
            self.status = "Refunded"
        else:
            self.status = "Partially Refunded"
        
        self.refund_amount = refund_amount
        self.refund_date = now_datetime()
        self.refund_reason = reason
        self.save(ignore_permissions=True)
        
        # Update order payment status
        if self.order:
            order = frappe.get_doc("Craft Order", self.order)
            if self.status == "Refunded":
                order.payment_status = "Refunded"
            else:
                order.payment_status = "Partially Refunded"
            order.save(ignore_permissions=True)


@frappe.whitelist()
def create_payment(order, payment_method, amount, gateway_response=None):
    """Create a new payment transaction"""
    order_doc = frappe.get_doc("Craft Order", order)
    
    payment = frappe.get_doc({
        "doctype": "Payment Transaction",
        "order": order,
        "customer": order_doc.customer,
        "payment_method": payment_method,
        "amount": flt(amount),
        "status": "Completed",
        "gateway_response": gateway_response
    })
    payment.insert(ignore_permissions=True)
    
    return payment


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    return False
