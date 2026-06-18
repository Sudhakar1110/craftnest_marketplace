import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    # Featured Products
    context.featured_products = frappe.get_all(
        "Craft Product",
        filters={"featured": 1, "status": "Published", "published": 1},
        fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating"],
        limit=8
    )
    
    # Categories
    context.categories = frappe.get_all(
        "Product Category",
        filters={"published": 1, "is_active": 1},
        fields=["name", "category_name", "route", "category_image"],
        limit=6
    )
    
    # New Arrivals
    context.new_arrivals = frappe.get_all(
        "Craft Product",
        filters={"status": "Published", "published": 1},
        fields=["name", "product_name", "route", "main_image", "price", "sale_price"],
        order_by="creation desc",
        limit=8
    )
    
    # Best Sellers
    context.best_sellers = frappe.get_all(
        "Craft Product",
        filters={"status": "Published", "published": 1},
        fields=["name", "product_name", "route", "main_image", "price", "sale_price", "total_sales"],
        order_by="total_sales desc",
        limit=8
    )
    
    # Testimonials
    context.testimonials = frappe.get_all(
        "Product Review",
        filters={"status": "Approved"},
        fields=["customer_name", "rating", "review_text", "product"],
        order_by="creation desc",
        limit=6
    )
    
    return context
