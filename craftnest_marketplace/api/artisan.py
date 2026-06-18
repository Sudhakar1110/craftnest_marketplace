# CraftNest Marketplace - Artisan API

import frappe
from frappe import _


@frappe.whitelist()
def get_artisan_details(artisan):
    """Get artisan profile details"""
    try:
        artisan_doc = frappe.get_doc("Artisan Profile", artisan)
        
        # Get shop
        shop = None
        shop_docs = frappe.get_all(
            "Artisan Shop",
            filters={"artisan": artisan, "status": "Active"},
            fields=["name", "shop_name", "slug", "shop_logo", "shop_banner"]
        )
        if shop_docs:
            shop = shop_docs[0]
        
        # Get products
        products = frappe.get_all(
            "Craft Product",
            filters={"artisan": artisan, "status": "Published", "published": 1},
            fields=["name", "product_name", "main_image", "price", "sale_price", "average_rating"],
            limit=20
        )
        
        return {
            "name": artisan_doc.name,
            "artisan_name": artisan_doc.artisan_name,
            "email": artisan_doc.email,
            "profile_image": artisan_doc.profile_image,
            "bio": artisan_doc.bio,
            "specialization": artisan_doc.specialization,
            "experience_years": artisan_doc.experience_years,
            "rating": artisan_doc.rating,
            "verified": artisan_doc.verified,
            "city": artisan_doc.city,
            "state": artisan_doc.state,
            "country": artisan_doc.country,
            "total_products": artisan_doc.total_products,
            "total_sales": artisan_doc.total_sales,
            "shop": shop,
            "products": products
        }
    except Exception as e:
        frappe.log_error(str(e))
        return None


@frappe.whitelist()
def get_shop_details(slug):
    """Get shop details by slug"""
    try:
        shop = frappe.get_doc("Artisan Shop", {"slug": slug})
        
        # Get artisan
        artisan = None
        if shop.artisan:
            artisan_doc = frappe.get_doc("Artisan Profile", shop.artisan)
            artisan = {
                "name": artisan_doc.name,
                "artisan_name": artisan_doc.artisan_name,
                "profile_image": artisan_doc.profile_image,
                "bio": artisan_doc.bio,
                "rating": artisan_doc.rating,
                "verified": artisan_doc.verified
            }
        
        # Get products
        products = frappe.get_all(
            "Craft Product",
            filters={"artisan": shop.artisan, "status": "Published", "published": 1},
            fields=["name", "product_name", "main_image", "price", "sale_price", "average_rating", "stock_status"]
        )
        
        return {
            "shop": {
                "name": shop.name,
                "shop_name": shop.shop_name,
                "slug": shop.slug,
                "shop_logo": shop.shop_logo,
                "shop_banner": shop.shop_banner,
                "shop_description": shop.shop_description,
                "location": shop.location
            },
            "artisan": artisan,
            "products": products,
            "total_products": len(products)
        }
    except Exception as e:
        frappe.log_error(str(e))
        return None


@frappe.whitelist()
def register_artisan(data):
    """Register new artisan"""
    try:
        # Validate required fields
        required = ["artisan_name", "email"]
        for field in required:
            if not data.get(field):
                return {"success": False, "message": f"{field} is required"}
        
        # Check if email exists
        if frappe.db.exists("Artisan Profile", {"email": data["email"]}):
            return {"success": False, "message": "Email already registered"}
        
        # Create artisan profile
        artisan = frappe.get_doc({
            "doctype": "Artisan Profile",
            "artisan_name": data["artisan_name"],
            "email": data["email"],
            "phone": data.get("phone"),
            "bio": data.get("bio"),
            "specialization": data.get("specialization"),
            "status": "Pending"
        })
        artisan.insert(ignore_permissions=True)
        
        return {
            "success": True,
            "message": "Artisan registered successfully",
            "artisan_id": artisan.name
        }
    except Exception as e:
        frappe.log_error(str(e))
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_top_artisans(limit=10):
    """Get top rated artisans"""
    artisans = frappe.get_all(
        "Artisan Profile",
        filters={"status": "Active"},
        fields=["name", "artisan_name", "profile_image", "rating", "total_sales", "city"],
        order_by="rating desc",
        limit=limit
    )
    return artisans
