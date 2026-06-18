# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class ProductReview(Document):
    def validate(self):
        self.set_customer_name()
    
    def set_customer_name(self):
        if self.customer and not self.customer_name:
            self.customer_name = frappe.db.get_value("Customer", self.customer, "customer_name")
    
    def after_insert(self):
        """Update product rating when new review is added"""
        self.update_product_rating()
    
    def on_update(self):
        """Update product rating when review status changes"""
        if self.has_value_changed("status"):
            self.update_product_rating()
    
    def update_product_rating(self):
        """Calculate and update average rating for the product"""
        if self.status == "Approved":
            product = frappe.get_doc("Craft Product", self.product)
            
            # Get all approved reviews
            reviews = frappe.get_all(
                "Product Review",
                filters={"product": self.product, "status": "Approved"},
                fields=["rating"]
            )
            
            if reviews:
                total_rating = sum([r.rating for r in reviews])
                avg_rating = total_rating / len(reviews)
                
                product.average_rating = round(avg_rating, 2)
                product.total_reviews = len(reviews)
                product.save(ignore_permissions=True)
                
                # Also update artisan rating
                self.update_artisan_rating(product.artisan)
    
    def update_artisan_rating(self, artisan):
        """Update artisan's average rating"""
        if artisan:
            artisan_doc = frappe.get_doc("Artisan Profile", artisan)
            
            avg_rating = frappe.db.sql("""
                SELECT AVG(pr.rating) as avg_rating
                FROM `tabProduct Review` pr
                INNER JOIN `tabCraft Product` cp ON pr.product = cp.name
                WHERE cp.artisan = %s
                AND pr.status = 'Approved'
            """, (artisan,))
            
            if avg_rating and avg_rating[0][0]:
                artisan_doc.rating = round(avg_rating[0][0], 2)
                artisan_doc.save(ignore_permissions=True)


@frappe.whitelist()
def mark_helpful(review):
    """Mark review as helpful"""
    frappe.db.sql("""
        UPDATE `tabProduct Review`
        SET helpful_count = helpful_count + 1
        WHERE name = %s
    """, (review,))
    frappe.db.commit()
    return True


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Customer" in frappe.get_roles(user):
        return f"`tabProduct Review`.customer = '{user}'"
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if "CraftNest Customer" in frappe.get_roles(user):
        if doc.customer == user:
            return True
    
    if ptype == "read" and doc.status == "Approved":
        return True
    
    return False
