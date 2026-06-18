# CraftNest Marketplace - Cart API

import frappe
from frappe import _
from frappe.utils import flt


@frappe.whitelist()
def add_to_cart(product, qty=1):
    """Add item to cart"""
    if frappe.session.user == "Guest":
        return {"success": False, "message": "login_required"}
    
    try:
        # Get product details
        product_doc = frappe.get_doc("Craft Product", product)
        
        if product_doc.stock_quantity < qty:
            return {"success": False, "message": "Insufficient stock"}
        
        # Get or create cart from session
        cart = get_or_create_cart()
        
        # Add/update item
        if product in cart:
            cart[product]["qty"] += qty
        else:
            cart[product] = {
                "qty": qty,
                "price": product_doc.sale_price or product_doc.price,
                "name": product_doc.product_name
            }
        
        # Save cart
        save_cart(cart)
        
        return {
            "success": True,
            "message": "Item added to cart",
            "cart_count": len(cart)
        }
    except Exception as e:
        frappe.log_error(str(e))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def remove_from_cart(product):
    """Remove item from cart"""
    if frappe.session.user == "Guest":
        return {"success": False, "message": "login_required"}
    
    try:
        cart = get_cart()
        
        if product in cart:
            del cart[product]
            save_cart(cart)
        
        return {
            "success": True,
            "message": "Item removed from cart",
            "cart": get_cart_with_totals()
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_cart_item(product, qty):
    """Update item quantity in cart"""
    if frappe.session.user == "Guest":
        return {"success": False, "message": "login_required"}
    
    try:
        cart = get_cart()
        
        if qty <= 0:
            del cart[product]
        else:
            # Check stock
            product_doc = frappe.get_doc("Craft Product", product)
            if product_doc.stock_quantity < qty:
                return {"success": False, "message": "Insufficient stock"}
            
            cart[product] = {
                "qty": qty,
                "price": product_doc.sale_price or product_doc.price,
                "name": product_doc.product_name
            }
        
        save_cart(cart)
        
        return {
            "success": True,
            "message": "Cart updated",
            "cart": get_cart_with_totals()
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def clear_cart():
    """Clear entire cart"""
    if frappe.session.user == "Guest":
        return {"success": False, "message": "login_required"}
    
    try:
        save_cart({})
        
        return {
            "success": True,
            "message": "Cart cleared",
            "cart": {"items": {}, "subtotal": 0, "tax": 0, "shipping": 0, "total": 0}
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_cart():
    """Get current cart"""
    cart_data = frappe.session.get("craftnest_cart") or {}
    return cart_data


@frappe.whitelist()
def get_cart_with_totals():
    """Get cart with calculated totals"""
    cart = get_cart()
    
    subtotal = sum([item["qty"] * item["price"] for item in cart.values()])
    tax = subtotal * 0.18
    shipping = 50 if subtotal < 500 else 0
    total = subtotal + tax + shipping
    
    return {
        "items": cart,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "total": total
    }


@frappe.whitelist()
def get_cart_count():
    """Get number of items in cart"""
    cart = get_cart()
    return sum([item.get("qty", 0) for item in cart.values()])


def get_or_create_cart():
    """Get or create cart for current session"""
    return frappe.session.get("craftnest_cart") or {}


def save_cart(cart):
    """Save cart to session"""
    frappe.session["craftnest_cart"] = cart
