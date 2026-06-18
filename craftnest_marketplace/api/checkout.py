# CraftNest Marketplace - Checkout API

import frappe
from frappe import _
from frappe.utils import flt, nowdate, add_days
from craftnest_marketplace.api.cart import get_cart, save_cart, get_cart_with_totals


@frappe.whitelist()
def place_order(address, payment_method):
    """Place order"""
    if frappe.session.user == "Guest":
        return {"success": False, "message": "login_required"}
    
    try:
        cart = get_cart()
        
        if not cart:
            return {"success": False, "message": "Cart is empty"}
        
        # Get cart totals
        cart_totals = get_cart_with_totals()
        
        # Create order
        order_items = []
        for product_id, item in cart.items():
            product = frappe.get_doc("Craft Product", product_id)
            order_items.append({
                "product": product_id,
                "product_name": product.product_name,
                "artisan": product.artisan,
                "quantity": item["qty"],
                "rate": item["price"],
                "amount": item["qty"] * item["price"]
            })
        
        order = frappe.get_doc({
            "doctype": "Craft Order",
            "customer": frappe.session.user,
            "customer_name": frappe.db.get_value("Customer", frappe.session.user, "customer_name"),
            "order_date": nowdate(),
            "status": "Pending",
            "payment_status": "Pending",
            "items": order_items,
            "subtotal": cart_totals["subtotal"],
            "shipping_charges": cart_totals["shipping"],
            "tax_amount": cart_totals["tax"],
            "total_amount": cart_totals["total"],
            "shipping_address": address
        })
        order.insert(ignore_permissions=True)
        
        # Clear cart
        save_cart({})
        
        # Process payment
        payment_status = "Pending"
        if payment_method == "cod":
            payment_status = "Pending"
        else:
            # For other payment methods, integrate with payment gateway
            payment_status = "Pending"  # Would be updated after payment confirmation
        
        order.payment_status = payment_status
        order.save(ignore_permissions=True)
        
        return {
            "success": True,
            "message": "Order placed successfully",
            "order_id": order.name
        }
    except Exception as e:
        frappe.log_error(str(e))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_available_addresses():
    """Get customer addresses"""
    if frappe.session.user == "Guest":
        return []
    
    addresses = frappe.get_all(
        "Address",
        filters={"email_id": frappe.session.user},
        fields=["name", "address_type", "address_line1", "city", "state", "pincode", "country"]
    )
    
    return addresses


@frappe.whitelist()
def calculate_shipping(address):
    """Calculate shipping based on address"""
    # Simple shipping calculation
    return {
        "standard": 50,
        "express": 100,
        "free_above": 500
    }
