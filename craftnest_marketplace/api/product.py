# CraftNest Marketplace - Product API

import frappe
from frappe import _


@frappe.whitelist()
def get_product_details(product):
    """Get detailed product information"""
    try:
        product_doc = frappe.get_doc("Craft Product", product)
        
        # Get artisan info
        artisan = None
        if product_doc.artisan:
            artisan_doc = frappe.get_doc("Artisan Profile", product_doc.artisan)
            artisan = {
                "name": artisan_doc.name,
                "artisan_name": artisan_doc.artisan_name,
                "profile_image": artisan_doc.profile_image,
                "rating": artisan_doc.rating
            }
        
        # Get gallery images
        gallery = []
        if product_doc.image_gallery:
            gallery = [item.image for item in product_doc.image_gallery if item.image]
        
        # Get related products
        related = frappe.get_all(
            "Craft Product",
            filters={
                "category": product_doc.category,
                "name": ["!=", product],
                "status": "Published"
            },
            fields=["name", "product_name", "main_image", "price", "sale_price"],
            limit=4
        )
        
        return {
            "name": product_doc.name,
            "product_name": product_doc.product_name,
            "description": product_doc.description,
            "specifications": product_doc.specifications,
            "main_image": product_doc.main_image,
            "gallery": gallery,
            "price": product_doc.price,
            "sale_price": product_doc.sale_price,
            "stock_quantity": product_doc.stock_quantity,
            "stock_status": product_doc.stock_status,
            "category": product_doc.category,
            "artisan": artisan,
            "processing_time_days": product_doc.processing_time_days,
            "free_shipping": product_doc.free_shipping,
            "return_policy": product_doc.return_policy,
            "care_instructions": product_doc.care_instructions,
            "average_rating": product_doc.average_rating,
            "total_reviews": product_doc.total_reviews,
            "related_products": related
        }
    except Exception as e:
        frappe.log_error(str(e))
        return None


@frappe.whitelist()
def search_products(query, category=None, min_price=None, max_price=None, limit=20):
    """Search products"""
    filters = {
        "status": "Published",
        "published": 1
    }
    
    if category:
        filters["category"] = category
    
    if min_price:
        filters["price"] = [">=", flt(min_price)]
    
    if max_price:
        filters["price"] = ["<=", flt(max_price)]
    
    if query:
        filters["product_name"] = ["like", f"%{query}%"]
    
    products = frappe.get_all(
        "Craft Product",
        filters=filters,
        fields=["name", "product_name", "main_image", "price", "sale_price", "average_rating"],
        limit=limit
    )
    
    return products


@frappe.whitelist()
def get_featured_products(limit=8):
    """Get featured products"""
    products = frappe.get_all(
        "Craft Product",
        filters={"featured": 1, "status": "Published", "published": 1},
        fields=["name", "product_name", "main_image", "price", "sale_price", "average_rating"],
        limit=limit
    )
    return products


@frappe.whitelist()
def get_new_arrivals(limit=8):
    """Get new arrival products"""
    products = frappe.get_all(
        "Craft Product",
        filters={"status": "Published", "published": 1},
        fields=["name", "product_name", "main_image", "price", "sale_price"],
        order_by="creation desc",
        limit=limit
    )
    return products


@frappe.whitelist()
def get_categories():
    """Get all product categories"""
    categories = frappe.get_all(
        "Product Category",
        filters={"published": 1, "is_active": 1},
        fields=["name", "category_name", "category_image", "route"]
    )
    return categories
