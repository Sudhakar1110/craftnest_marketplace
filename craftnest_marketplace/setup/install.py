# CraftNest Marketplace - Installation Script

import frappe
from frappe import _


def before_install():
    """Run before app installation"""
    frappe.publish_realtime("installation_progress", {"progress": 10, "message": "Starting installation..."})


def after_install():
    """Run after app installation"""
    frappe.publish_realtime("installation_progress", {"progress": 30, "message": "Creating roles..."})
    create_roles()
    
    frappe.publish_realtime("installation_progress", {"progress": 50, "message": "Setting up defaults..."})
    setup_defaults()
    
    frappe.publish_realtime("installation_progress", {"progress": 70, "message": "Creating demo data..."})
    create_demo_data()
    
    frappe.publish_realtime("installation_progress", {"progress": 100, "message": "Installation complete!"})
    
    frappe.publish_realtime("installation_complete", {"message": "CraftNest Marketplace installed successfully!"})


def create_roles():
    """Create custom roles for CraftNest"""
    roles = [
        {
            "role_name": "CraftNest Administrator",
            "role_name": "CraftNest Administrator",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Full access to CraftNest Marketplace"
        },
        {
            "role_name": "CraftNest Artisan",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Access for artisan sellers"
        },
        {
            "role_name": "CraftNest Customer",
            "desk_access": 0,
            "is_custom": 1,
            "description": "Customer access for CraftNest"
        },
        {
            "role_name": "CraftNest Delivery Staff",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Delivery staff access"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "desk_access": role_data.get("desk_access", 0),
                "is_custom": role_data.get("is_custom", 1),
                "description": role_data.get("description", "")
            })
            role.insert(ignore_permissions=True)
            frappe.publish_realtime("installation_progress", {"message": f"Created role: {role_data['role_name']}"})


def setup_defaults():
    """Setup default settings and configurations"""
    # Create default product categories
    categories = [
        {"category_name": "Pottery & Ceramics", "description": "Handcrafted pottery and ceramic items"},
        {"category_name": "Textiles & Embroidery", "description": "Handwoven textiles and embroidery"},
        {"category_name": "Jewelry", "description": "Handmade jewelry and accessories"},
        {"category_name": "Woodwork", "description": "Handcrafted wooden items"},
        {"category_name": "Metal Crafts", "description": "Metal artwork and crafts"},
        {"category_name": "Painting & Art", "description": "Paintings and artistic creations"},
        {"category_name": "Glasswork", "description": "Handcrafted glass items"},
        {"category_name": "Leather Goods", "description": "Handmade leather products"},
        {"category_name": "Paper Crafts", "description": "Handmade paper products"},
        {"category_name": "Home Decor", "description": "Handcrafted home decor items"}
    ]
    
    for cat in categories:
        if not frappe.db.exists("Product Category", {"category_name": cat["category_name"]}):
            category = frappe.get_doc({
                "doctype": "Product Category",
                "category_name": cat["category_name"],
                "description": cat["description"],
                "published": 1,
                "is_active": 1
            })
            category.insert(ignore_permissions=True)
            frappe.publish_realtime("installation_progress", {"message": f"Created category: {cat['category_name']}"})


def create_demo_data():
    """Create demo data for testing"""
    # Create demo artisan
    if not frappe.db.exists("Artisan Profile", {"email": "demo_artisan@craftnest.com"}):
        demo_artisan = frappe.get_doc({
            "doctype": "Artisan Profile",
            "artisan_name": "Demo Artisan",
            "email": "demo_artisan@craftnest.com",
            "phone": "+919876543210",
            "bio": "I am a passionate artisan with over 10 years of experience in creating unique handcrafted items.",
            "specialization": "Pottery, Ceramics, Home Decor",
            "experience_years": 10,
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "status": "Active",
            "verified": 1
        })
        demo_artisan.insert(ignore_permissions=True)
        
        # Create demo shop
        demo_shop = frappe.get_doc({
            "doctype": "Artisan Shop",
            "shop_name": "Demo Artisan Shop",
            "slug": "demo-artisan-shop",
            "artisan": demo_artisan.name,
            "shop_description": "Welcome to our demo shop featuring handcrafted pottery and ceramic items.",
            "location": "Mumbai, Maharashtra",
            "status": "Active"
        })
        demo_shop.insert(ignore_permissions=True)
        
        # Create demo products
        for i in range(1, 5):
            product = frappe.get_doc({
                "doctype": "Craft Product",
                "product_name": f"Demo Product {i}",
                "artisan": demo_artisan.name,
                "category": frappe.db.get_value("Product Category", {"category_name": "Pottery & Ceramics"}, "name"),
                "price": 500 + (i * 100),
                "sale_price": 450 + (i * 90) if i % 2 == 0 else None,
                "stock_quantity": 10 + i,
                "status": "Published",
                "published": 1,
                "description": f"This is demo product {i} created during installation.",
                "material": "Clay",
                "processing_time_days": 5,
                "shipping_available": 1
            })
            product.insert(ignore_permissions=True)
            
            frappe.publish_realtime("installation_progress", {"message": f"Created demo product: {product.product_name}"})


def after_app_install(app_name):
    """Hook called after app installation"""
    if app_name == "craftnest_marketplace":
        after_install()


def after_uninstall():
    """Hook called after app uninstall"""
    frappe.publish_realtime("uninstallation_complete", {"message": "CraftNest Marketplace uninstalled!"})
