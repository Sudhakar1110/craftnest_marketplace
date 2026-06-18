# CraftNest Marketplace - Validators Utility

import frappe
from frappe import _


def validate_artisan_registration(data):
    """Validate artisan registration data"""
    errors = []
    
    if not data.get("artisan_name"):
        errors.append(_("Artisan name is required"))
    
    if not data.get("email"):
        errors.append(_("Email is required"))
    elif not is_valid_email(data["email"]):
        errors.append(_("Invalid email format"))
    elif frappe.db.exists("Artisan Profile", {"email": data["email"]}):
        errors.append(_("Email already registered"))
    
    if not data.get("phone"):
        errors.append(_("Phone number is required"))
    elif not is_valid_phone(data["phone"]):
        errors.append(_("Invalid phone number format"))
    
    return errors


def validate_product_listing(data):
    """Validate product listing data"""
    errors = []
    
    if not data.get("product_name"):
        errors.append(_("Product name is required"))
    
    if not data.get("category"):
        errors.append(_("Category is required"))
    elif not frappe.db.exists("Product Category", data["category"]):
        errors.append(_("Invalid category"))
    
    if not data.get("price"):
        errors.append(_("Price is required"))
    elif flt(data["price"]) <= 0:
        errors.append(_("Price must be greater than 0"))
    
    if data.get("sale_price") and flt(data["sale_price"]) >= flt(data.get("price", 0)):
        errors.append(_("Sale price must be less than regular price"))
    
    if data.get("stock_quantity") and data.get("stock_quantity") < 0:
        errors.append(_("Stock quantity cannot be negative"))
    
    return errors


def validate_order_items(items):
    """Validate order items"""
    errors = []
    
    if not items:
        errors.append(_("Order must have at least one item"))
        return errors
    
    for idx, item in enumerate(items, 1):
        if not item.get("product"):
            errors.append(_("Item {0}: Product is required").format(idx))
        elif not frappe.db.exists("Craft Product", item["product"]):
            errors.append(_("Item {0}: Invalid product").format(idx))
        
        if not item.get("quantity") or item["quantity"] <= 0:
            errors.append(_("Item {0}: Quantity must be greater than 0").format(idx))
        
        if not item.get("rate") or item["rate"] <= 0:
            errors.append(_("Item {0}: Rate must be greater than 0").format(idx))
    
    return errors


def validate_review(review_data):
    """Validate product review"""
    errors = []
    
    if not review_data.get("rating") or review_data["rating"] < 1 or review_data["rating"] > 5:
        errors.append(_("Rating must be between 1 and 5"))
    
    if not review_data.get("review_text") or len(review_data["review_text"]) < 10:
        errors.append(_("Review text must be at least 10 characters"))
    
    return errors


def is_valid_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone):
    """Validate phone number format"""
    import re
    # Indian phone number format
    pattern = r'^[6-9]\d{9}$'
    clean_phone = ''.join(filter(str.isdigit, phone))
    return bool(re.match(pattern, clean_phone))


def is_valid_pincode(pincode):
    """Validate Indian pincode"""
    import re
    pattern = r'^[1-9]\d{5}$'
    return bool(re.match(pattern, str(pincode)))
