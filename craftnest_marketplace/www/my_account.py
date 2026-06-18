import frappe
from frappe import _


def get_context(context):
    context.no_cache = 1
    
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to view your account"), frappe.PermissionError)
    
    # Get customer profile
    customer = frappe.get_doc("Customer Profile", {"email": frappe.session.user})
    context.customer = customer
    
    # Get recent orders
    context.recent_orders = frappe.get_all(
        "Craft Order",
        filters={"customer": frappe.session.user, "docstatus": 1},
        fields=["name", "order_date", "total_amount", "status", "payment_status"],
        order_by="creation desc",
        limit=5
    )
    
    # Get wishlist items
    wishlist = frappe.get_doc("Wishlist", {"customer": customer.name})
    if wishlist:
        context.wishlist_items = frappe.get_all(
            "Wishlist Item",
            filters={"parent": wishlist.name},
            fields=["product", "product_name", "price"],
            limit=5
        )
    
    return context
