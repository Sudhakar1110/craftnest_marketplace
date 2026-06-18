# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe


def get_featured_products():
    """Get published products for the website homepage"""
    try:
        return frappe.get_all(
            "Craft Product",
            filters={"status": "Published"},
            fields=["name", "product_name", "price", "sale_price", "route", "image"],
            limit=8
        )
    except Exception as e:
        frappe.log_error(f"Error in get_featured_products: {e}")
        return []


def get_product_categories():
    """Get product categories for the website navigation"""
    try:
        return frappe.get_all(
            "Product Category",
            filters={"is_active": 1},
            fields=["name", "category_name"],
            order_by="category_name asc"
        )
    except Exception as e:
        frappe.log_error(f"Error in get_product_categories: {e}")
        return []


def get_cart_count():
    """Get current cart count for the user"""
    try:
        from frappe.utils.shopping_cart import get_cart_count as frappe_cart_count
        return frappe_cart_count()
    except Exception as e:
        frappe.log_error(f"Error in get_cart_count: {e}")
    return 0
