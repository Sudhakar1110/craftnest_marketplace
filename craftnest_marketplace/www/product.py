import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    # Get product name from route
    product_name = frappe.form_dict.get('name') or frappe.request.path.strip('/').split('/')[-1]
    
    # Get product
    try:
        product = frappe.get_doc("Craft Product", product_name)
    except:
        product = frappe.get_doc("Craft Product", {"route": product_name})
    
    context.product = product
    
    # Get artisan details
    if product.artisan:
        context.artisan = frappe.get_doc("Artisan Profile", product.artisan)
        
        # Get artisan shop
        shop = frappe.get_all(
            "Artisan Shop",
            filters={"artisan": product.artisan, "status": "Active"},
            fields=["name", "shop_name", "slug", "shop_logo"]
        )
        if shop:
            context.shop = shop[0]
    
    # Get category
    if product.category:
        context.category = frappe.get_doc("Product Category", product.category)
    
    # Related products
    context.related_products = frappe.get_all(
        "Craft Product",
        filters={
            "category": product.category,
            "name": ["!=", product.name],
            "status": "Published",
            "published": 1
        },
        fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating"],
        limit=4
    )
    
    # Reviews
    context.reviews = frappe.get_all(
        "Product Review",
        filters={"product": product.name, "status": "Approved"},
        fields=["customer_name", "rating", "review_title", "review_text", "creation"],
        order_by="creation desc",
        limit=10
    )
    
    # Gallery images
    if product.image_gallery:
        context.gallery_images = [item.image for item in product.image_gallery if item.image]
    
    return context
