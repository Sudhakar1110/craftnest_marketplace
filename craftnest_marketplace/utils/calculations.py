# CraftNest Marketplace - Calculations Utility

import frappe
from frappe.utils import flt


def calculate_product_price(price, sale_price=None, discount_percentage=None):
    """Calculate product price with discount"""
    if sale_price:
        discount = ((flt(price) - flt(sale_price)) / flt(price)) * 100 if price > 0 else 0
        return {
            "price": flt(price),
            "sale_price": flt(sale_price),
            "discount_percentage": flt(discount)
        }
    elif discount_percentage:
        sale_price = flt(price) * (1 - flt(discount_percentage) / 100)
        return {
            "price": flt(price),
            "sale_price": flt(sale_price),
            "discount_percentage": flt(discount_percentage)
        }
    else:
        return {
            "price": flt(price),
            "sale_price": None,
            "discount_percentage": 0
        }


def calculate_order_totals(items, shipping_charges=0):
    """Calculate order totals including tax"""
    subtotal = sum([flt(item.amount) for item in items])
    tax_amount = subtotal * 0.18  # 18% GST
    total = subtotal + flt(shipping_charges) + tax_amount
    
    return {
        "subtotal": flt(subtotal),
        "tax_amount": flt(tax_amount),
        "shipping_charges": flt(shipping_charges),
        "total": flt(total)
    }


def calculate_shipping_cost(subtotal, weight=0, location=None):
    """Calculate shipping cost"""
    # Free shipping above 500
    if subtotal >= 500:
        return 0
    
    # Base shipping
    base_cost = 50
    
    # Weight based cost (if applicable)
    if weight > 0.5:
        base_cost += (weight - 0.5) * 20
    
    return base_cost


def calculate_artisan_commission(amount, commission_rate=0.85):
    """Calculate artisan commission (default 85%)"""
    commission = flt(amount) * commission_rate
    platform_fee = flt(amount) - commission
    
    return {
        "artisan_amount": commission,
        "platform_fee": platform_fee,
        "commission_rate": commission_rate
    }


def calculate_loyalty_points(amount):
    """Calculate loyalty points for purchase"""
    # 1 point per 10 rupees spent
    points = int(flt(amount) / 10)
    return points


def calculate_average_rating(reviews):
    """Calculate average rating from reviews"""
    if not reviews:
        return 0
    
    total = sum([r.rating for r in reviews])
    return flt(total / len(reviews), precision=2)
