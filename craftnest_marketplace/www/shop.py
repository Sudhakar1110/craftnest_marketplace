import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    # Get shop slug from route
    slug = frappe.request.path.strip('/').split('/')[-1]
    
    # Get shop
    try:
        shop = frappe.get_doc("Artisan Shop", {"slug": slug})
    except:
        frappe.throw(_("Shop not found"), frappe.DoesNotExistError)
    
    context.shop = shop
    
    # Get artisan details
    if shop.artisan:
        context.artisan = frappe.get_doc("Artisan Profile", shop.artisan)
    
    # Get shop products
    context.products = frappe.get_all(
        "Craft Product",
        filters={"artisan": shop.artisan, "status": "Published", "published": 1},
        fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating", "stock_status"],
        limit=24
    )
    
    return context
