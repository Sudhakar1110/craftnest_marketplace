# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class CustomerProfile(Document):
    def validate(self):
        self.generate_customer_code()
        self.validate_email()
        self.create_user_if_not_exists()
    
    def generate_customer_code(self):
        if not self.customer_code:
            year = frappe.utils.now_datetime().year
            count = frappe.db.count("Customer Profile") + 1
            self.customer_code = f"CN-{year}-{str(count).zfill(5)}"
    
    def validate_email(self):
        if self.email:
            if frappe.db.exists("Customer Profile", {"email": self.email, "name": ["!=", self.name]}):
                frappe.throw(_("Email {0} already exists").format(self.email))
    
    def create_user_if_not_exists(self):
        if self.email and not self.user:
            if not frappe.db.exists("User", self.email):
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": self.email,
                    "first_name": self.customer_name,
                    "send_welcome_email": 0,
                    "user_type": "Website User"
                })
                user.add_roles("CraftNest Customer")
                user.insert(ignore_permissions=True)
                self.user = user.name
            else:
                self.user = self.email
    
    def update_statistics(self):
        """Update customer statistics from orders"""
        orders = frappe.get_all(
            "Craft Order",
            filters={"customer": self.email, "docstatus": 1},
            fields=["name", "total_amount"]
        )
        
        self.total_orders = len(orders)
        self.total_spent = sum([o.total_amount for o in orders]) if orders else 0
        self.average_order_value = self.total_spent / self.total_orders if self.total_orders > 0 else 0
        
        # Update loyalty tier based on total spent
        self.update_loyalty_tier()
        
        # Calculate loyalty points (1 point per 10 spent)
        self.loyalty_points = int(self.total_spent / 10)
        
        self.save(ignore_permissions=True)
    
    def update_loyalty_tier(self):
        """Update loyalty tier based on total spent"""
        if self.total_spent >= 50000:
            self.loyalty_tier = "Platinum"
        elif self.total_spent >= 25000:
            self.loyalty_tier = "Gold"
        elif self.total_spent >= 10000:
            self.loyalty_tier = "Silver"
        else:
            self.loyalty_tier = "Bronze"


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Customer" in frappe.get_roles(user):
        return f"(`tabCustomer Profile`.user = '{user}' or `tabCustomer Profile`.email = '{user}')"
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if doc.user == user or doc.email == user:
        return True
    
    return False
