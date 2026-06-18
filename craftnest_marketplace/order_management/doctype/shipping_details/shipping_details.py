# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class ShippingDetails(Document):
    def validate(self):
        if self.status == "Delivered" and not self.delivered_date:
            self.delivered_date = frappe.utils.today()
    
    def update_order_status(self):
        """Update related order status based on shipping status"""
        if self.order:
            order = frappe.get_doc("Craft Order", self.order)
            
            if self.status == "Shipped":
                order.status = "Shipped"
                order.tracking_number = self.tracking_number
                order.carrier = self.carrier
                order.estimated_delivery = self.estimated_delivery
            elif self.status == "Delivered":
                order.status = "Delivered"
            
            order.save(ignore_permissions=True)
    
    def on_update(self):
        self.update_order_status()
    
    def send_shipping_notification(self):
        """Send shipping notification to customer"""
        if self.order:
            order = frappe.get_doc("Craft Order", self.order)
            frappe.sendmail(
                recipients=order.customer,
                subject=_("Your order {0} has been shipped").format(order.name),
                message=self.get_shipping_email_template()
            )
    
    def get_shipping_email_template(self):
        """Generate shipping notification email template"""
        return f"""
        <h2>Your order is on its way!</h2>
        <p>Order ID: {self.order}</p>
        <p>Carrier: {self.carrier}</p>
        <p>Tracking Number: {self.tracking_number}</p>
        {f"<p>Track your package: <a href='{self.tracking_url}'>{self.tracking_url}</a></p>" if self.tracking_url else ""}
        <p>Estimated Delivery: {self.estimated_delivery}</p>
        """


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Delivery Staff" in frappe.get_roles(user):
        return None
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if "CraftNest Delivery Staff" in frappe.get_roles(user):
        return True
    
    return False
