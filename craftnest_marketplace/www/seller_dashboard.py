import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to view your seller dashboard"), frappe.PermissionError)
    
    # Get artisan profile
    artisan = frappe.get_doc("Artisan Profile", {"email": frappe.session.user})
    context.artisan = artisan
    
    # Get shop
    shop = frappe.get_doc("Artisan Shop", {"artisan": artisan.name})
    context.shop = shop
    
    # Get products
    context.products = frappe.get_all(
        "Craft Product",
        filters={"artisan": artisan.name},
        fields=["name", "product_name", "status", "price", "stock_quantity", "total_sales", "average_rating"],
        order_by="creation desc",
        limit=10
    )
    
    # Get recent orders
    context.recent_orders = frappe.get_all(
        "Craft Order co",
        filters={"co.docstatus": 1},
        fields=["co.name", "co.order_date", "co.total_amount", "co.status", "oi.product_name"],
        filters={"oi.artisan": artisan.name},
        order_by="co.creation desc",
        limit=5
    )
    
    # Statistics
    context.total_products = len(context.products)
    context.total_sales = artisan.total_sales or 0
    
    return context
