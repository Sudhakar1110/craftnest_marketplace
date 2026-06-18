# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class CustomerAddress(Document):
    def validate(self):
        self.validate_default_address()
    
    def validate_default_address(self):
        """Ensure only one default shipping address per customer"""
        if self.is_default_shipping:
            existing = frappe.get_all(
                "Customer Address",
                filters={
                    "customer": self.customer,
                    "is_default_shipping": 1,
                    "name": ["!=", self.name]
                }
            )
            if existing:
                frappe.throw(_("Customer already has a default shipping address. Please unset it first."))
    
    def on_trash(self):
        """Update orders if this was the default address"""
        if self.is_default_shipping:
            frappe.db.sql("""
                UPDATE `tabCraft Order`
                SET shipping_address = NULL
                WHERE shipping_address = %s
            """, (self.name,))


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Customer" in frappe.get_roles(user):
        customer = frappe.db.get_value("Customer Profile", {"user": user}, "name")
        if customer:
            return f"`tabCustomer Address`.customer = '{customer}'"
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if "CraftNest Customer" in frappe.get_roles(user):
        customer = frappe.db.get_value("Customer Profile", {"user": user}, "name")
        if customer and doc.customer == customer:
            return True
    
    return False
