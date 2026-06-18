# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class Wishlist(Document):
    def validate(self):
        self.set_customer_name()
    
    def set_customer_name(self):
        if self.customer and not self.customer_name:
            self.customer_name = frappe.db.get_value("Customer Profile", self.customer, "customer_name")
    
    def add_item(self, product):
        """Add a product to wishlist"""
        if self.has_item(product):
            frappe.throw(_("Product already in wishlist"))
        
        self.append("items", {
            "product": product
        })
        self.save()
    
    def remove_item(self, product):
        """Remove a product from wishlist"""
        for item in self.items:
            if item.product == product:
                self.remove(item)
                self.save()
                return True
        return False
    
    def has_item(self, product):
        """Check if product is in wishlist"""
        return any(item.product == product for item in self.items)


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Customer" in frappe.get_roles(user):
        customer = frappe.db.get_value("Customer Profile", {"user": user}, "name")
        if customer:
            return f"`tabWishlist`.customer = '{customer}'"
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if "CraftNest Customer" in frappe.get_roles(user):
        customer = frappe.db.get_value("Customer Profile", {"user": user}, "name")
        if customer and doc.customer == customer:
            return True
    
    return False


@frappe.whitelist()
def add_to_wishlist(customer, product):
    """Add product to customer's wishlist"""
    if not frappe.db.exists("Wishlist", {"customer": customer}):
        wishlist = frappe.get_doc({
            "doctype": "Wishlist",
            "customer": customer,
            "wishlist_name": "My Wishlist"
        })
        wishlist.insert()
    else:
        wishlist = frappe.get_doc("Wishlist", {"customer": customer})
    
    wishlist.add_item(product)
    return True


@frappe.whitelist()
def remove_from_wishlist(customer, product):
    """Remove product from customer's wishlist"""
    if frappe.db.exists("Wishlist", {"customer": customer}):
        wishlist = frappe.get_doc("Wishlist", {"customer": customer})
        return wishlist.remove_item(product)
    return False
