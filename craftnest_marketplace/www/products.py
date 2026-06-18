import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    # Get filters from query string
    category = frappe.form_dict.get('category')
    artisan = frappe.form_dict.get('artisan')
    search = frappe.form_dict.get('q')
    min_price = frappe.form_dict.get('min_price')
    max_price = frappe.form_dict.get('max_price')
    sort_by = frappe.form_dict.get('sort') or 'creation'
    
    # Build filters
    filters = {"status": "Published", "published": 1}
    
    if category:
        filters["category"] = category
        context.category = frappe.get_doc("Product Category", category)
    
    if artisan:
        filters["artisan"] = artisan
        context.artisan = frappe.get_doc("Artisan Profile", artisan)
    
    if search:
        filters["product_name"] = ["like", f"%{search}%"]
        context.search = search
    
    if min_price:
        filters["price"] = [">=", float(min_price)]
    
    if max_price:
        if "price" in filters:
            filters["price"][1] = [">=", float(min_price)]
        filters["price"] = ["<=", float(max_price)]
    
    # Get sorting
    order_by = "creation desc"
    if sort_by == "price_low":
        order_by = "price asc"
    elif sort_by == "price_high":
        order_by = "price desc"
    elif sort_by == "rating":
        order_by = "average_rating desc"
    elif sort_by == "popular":
        order_by = "total_sales desc"
    
    # Get products
    context.products = frappe.get_all(
        "Craft Product",
        filters=filters,
        fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating", "artisan", "stock_status"],
        order_by=order_by,
        limit=24
    )
    
    # Get categories for filter
    context.categories = frappe.get_all(
        "Product Category",
        filters={"published": 1, "is_active": 1},
        fields=["name", "category_name", "route", "product_count"]
    )
    
    # Get artisans for filter
    context.artisans = frappe.get_all(
        "Artisan Profile",
        filters={"status": "Active"},
        fields=["name", "artisan_name", "profile_image", "rating"],
        limit=20
    )
    
    return context
