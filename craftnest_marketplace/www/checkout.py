import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to checkout"), frappe.PermissionError)
    
    # Get cart
    cart = frappe.get_site_config().get("cart", {})
    
    if not cart:
        frappe.redirect_to("/products")
    
    cart_items = []
    subtotal = 0
    
    for product_id, item in cart.items():
        try:
            product = frappe.get_doc("Craft Product", product_id)
            item_total = (product.sale_price or product.price) * item.get("qty", 1)
            subtotal += item_total
            
            cart_items.append({
                "product": product,
                "qty": item.get("qty", 1),
                "price": product.sale_price or product.price,
                "total": item_total
            })
        except:
            pass
    
    context.cart_items = cart_items
    context.subtotal = subtotal
    context.tax = subtotal * 0.18
    context.shipping = 50 if subtotal < 500 else 0
    context.total = context.subtotal + context.tax + context.shipping
    
    # Get customer addresses
    context.addresses = frappe.get_all(
        "Address",
        filters={"email_id": frappe.session.user},
        fields=["name", "address_type", "address_line1", "city", "state", "pincode", "country"]
    )
    
    return context
