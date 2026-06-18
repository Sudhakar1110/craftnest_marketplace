# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class ArtisanProfile(Document):
    def validate(self):
        self.validate_email()
        self.create_user_if_not_exists()
    
    def validate_email(self):
        if self.email:
            if frappe.db.exists("Artisan Profile", {"email": self.email, "name": ["!=", self.name]}):
                frappe.throw(_("Email {0} already exists").format(self.email))
    
    def create_user_if_not_exists(self):
        if self.email and not self.user:
            if not frappe.db.exists("User", self.email):
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": self.email,
                    "first_name": self.artisan_name,
                    "send_welcome_email": 0,
                    "user_type": "Website User"
                })
                user.add_roles("CraftNest Artisan")
                user.insert(ignore_permissions=True)
                self.user = user.name
            else:
                self.user = self.email
    
    def update_statistics(self):
        """Update total products and sales statistics"""
        total_products = frappe.db.count("Craft Product", {"artisan": self.name})
        total_sales = frappe.db.sql("""
            SELECT SUM(oi.amount) as total
            FROM `tabOrder Item` oi
            INNER JOIN `tabCraft Order` co ON oi.parent = co.name
            WHERE co.docstatus = 1
            AND oi.product IN (
                SELECT name FROM `tabCraft Product` WHERE artisan = %s
            )
        """, (self.name,))
        
        self.total_products = total_products
        self.total_sales = total_sales[0][0] or 0 if total_sales else 0
        self.save(ignore_permissions=True)
    
    def update_rating(self):
        """Calculate and update average rating from reviews"""
        avg_rating = frappe.db.sql("""
            SELECT AVG(rating) as avg_rating
            FROM `tabProduct Review` pr
            INNER JOIN `tabCraft Product` cp ON pr.product = cp.name
            WHERE cp.artisan = %s
            AND pr.status = 'Approved'
        """, (self.name,))
        
        if avg_rating and avg_rating[0][0]:
            self.rating = round(avg_rating[0][0], 2)
            self.save(ignore_permissions=True)


@frappe.whitelist()
def create_user(artisan):
    """Create user for artisan"""
    doc = frappe.get_doc("Artisan Profile", artisan)
    if not doc.user and doc.email:
        if not frappe.db.exists("User", doc.email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": doc.email,
                "first_name": doc.artisan_name,
                "send_welcome_email": 1,
                "user_type": "Website User"
            })
            user.add_roles("CraftNest Artisan")
            user.insert(ignore_permissions=True)
            doc.user = user.name
            doc.save(ignore_permissions=True)
            return True
    return False


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    return f"(`tabArtisan Profile`.user = '{user}' or `tabArtisan Profile`.email = '{user}')"


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if doc.user == user or doc.email == user:
        return True
    
    return False
