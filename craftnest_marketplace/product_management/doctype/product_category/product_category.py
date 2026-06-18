# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import cint
from frappe import _


class ProductCategory(Document):
    def validate(self):
        self.validate_parent_category()
        self.generate_route()
        self.update_product_count()
    
    def validate_parent_category(self):
        if self.parent_category:
            if self.parent_category == self.name:
                frappe.throw(_("Category cannot be its own parent"))
            
            parent = frappe.get_doc("Product Category", self.parent_category)
            if parent.parent_category:
                frappe.throw(_("Cannot create nested categories more than 2 levels deep"))
    
    def generate_route(self):
        if not self.route and self.category_name:
            self.route = frappe.utils.slugify(self.category_name)
    
    def update_product_count(self):
        self.product_count = frappe.db.count("Craft Product", {
            "category": self.name,
            "status": "Published"
        })
    
    def get_context(self, context):
        context.no_cache = 1
        context.category = self
        
        # Get products in this category
        context.products = frappe.get_all(
            "Craft Product",
            filters={"category": self.name, "status": "Published", "published": 1},
            fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating", "artisan"],
            limit=24
        )
        
        # Get subcategories
        context.subcategories = frappe.get_all(
            "Product Category",
            filters={"parent_category": self.name, "is_active": 1, "published": 1},
            fields=["name", "category_name", "route", "category_image", "product_count"]
        )
        
        # Get parent category info
        if self.parent_category:
            context.parent_category = frappe.get_doc("Product Category", self.parent_category)
        
        return context


@frappe.whitelist()
def get_category_tree():
    """Get category tree structure"""
    categories = frappe.get_all(
        "Product Category",
        filters={"is_active": 1},
        fields=["name", "category_name", "parent_category", "route", "category_image"],
        order_by="category_name"
    )
    
    tree = {}
    for cat in categories:
        if cat.parent_category:
            if cat.parent_category not in tree:
                tree[cat.parent_category] = {"children": []}
            tree[cat.parent_category]["children"].append(cat)
        else:
            tree[cat.name] = {"category": cat, "children": []}
    
    return tree


def get_permission_query_conditions(user):
    return None


def has_permission(doc, ptype, user):
    return True
