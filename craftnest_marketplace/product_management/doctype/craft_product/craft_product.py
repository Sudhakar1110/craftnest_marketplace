# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import cint, flt
from frappe import _


class CraftProduct(WebsiteGenerator):
    def validate(self):
        self.calculate_discount()
        self.update_stock_status()
        self.generate_sku()
    
    def before_save(self):
        if self.status == "Published" and not self.published:
            self.published = 1
        self.update_artisan_product_count()
    
    def on_update(self):
        self.sync_with_item()
        if self.has_value_changed("published"):
            self.update_website()
    
    def calculate_discount(self):
        if self.sale_price and self.price:
            self.discount_percentage = ((self.price - self.sale_price) / self.price) * 100
        else:
            self.discount_percentage = 0
    
    def update_stock_status(self):
        if self.stock_quantity == 0:
            self.stock_status = "Out of Stock"
            self.status = "Out of Stock"
        elif self.stock_quantity <= self.low_stock_threshold:
            self.stock_status = "Low Stock"
        else:
            self.stock_status = "In Stock"
    
    def generate_sku(self):
        if not self.sku:
            category_code = "".join([c[0].upper() for c in (self.category or "").split() if c])[:3] or "GEN"
            artisan_code = "".join([c[0].upper() for c in (self.artisan or "").split() if c])[:2] or "AR"
            number = str(frappe.db.count("Craft Product") + 1).zfill(4)
            self.sku = f"{category_code}{artisan_code}{number}"
    
    def update_artisan_product_count(self):
        """Update artisan's total products count"""
        if self.artisan:
            frappe.db.sql("""
                UPDATE `tabArtisan Profile`
                SET total_products = (
                    SELECT COUNT(*) FROM `tabCraft Product`
                    WHERE artisan = %s AND status = 'Published'
                )
                WHERE name = %s
            """, (self.artisan, self.artisan))
    
    def sync_with_item(self):
        """Sync product with ERPNext Item"""
        try:
            if not self.item_code:
                # Create new Item
                item = frappe.get_doc({
                    "doctype": "Item",
                    "item_code": self.sku or self.name,
                    "item_name": self.product_name,
                    "item_group": "Products",
                    "stock_uom": "Nos",
                    "is_stock_item": 1,
                    "include_item_in_manufacturing": 0,
                    "is_craft_product": 1,
                    "craft_artisan": self.artisan,
                    "craft_material": self.material,
                    "description": frappe.utils.strip_html_tags(self.description or "")[:140]
                })
                item.insert(ignore_permissions=True)
                self.item_code = item.name
            else:
                # Update existing Item
                item = frappe.get_doc("Item", self.item_code)
                item.item_name = self.product_name
                if self.sale_price:
                    item.standard_rate = self.sale_price
                item.description = frappe.utils.strip_html_tags(self.description or "")[:140]
                item.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Error syncing item: {str(e)}")
    
    def update_website(self):
        """Update website cache"""
        if self.published:
            frappe.publish_realtime("website_theme")
    
    def get_context(self, context):
        context.no_cache = 1
        
        # Increment view count
        if frappe.session.user != "Guest":
            self.increment_view_count()
        
        # Product details
        context.product = self
        
        # Get artisan details
        if self.artisan:
            context.artisan_details = frappe.get_doc("Artisan Profile", self.artisan)
        
        # Related products (same category)
        context.related_products = frappe.get_all(
            "Craft Product",
            filters={
                "category": self.category,
                "name": ["!=", self.name],
                "status": "Published",
                "published": 1
            },
            fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating"],
            limit=4
        )
        
        # Reviews
        context.reviews = frappe.get_all(
            "Product Review",
            filters={"product": self.name, "status": "Approved"},
            fields=["customer_name", "rating", "review_title", "review_text", "creation"],
            order_by="creation desc",
            limit=10
        )
        
        # Gallery images
        if self.image_gallery:
            context.gallery_images = [item.image for item in self.image_gallery if item.image]
        
        return context
    
    def increment_view_count(self):
        """Increment product view count"""
        frappe.db.sql("""
            UPDATE `tabCraft Product`
            SET total_views = total_views + 1
            WHERE name = %s
        """, (self.name,))
        frappe.db.commit()


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Artisan" in frappe.get_roles(user):
        return f"""(`tabCraft Product`.artisan in (
            SELECT name FROM `tabArtisan Profile` WHERE user = '{user}'
        ))"""
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if "CraftNest Artisan" in frappe.get_roles(user):
        artisan = frappe.db.get_value("Artisan Profile", {"user": user}, "name")
        if artisan and doc.artisan == artisan:
            return True
    
    if ptype == "read" and doc.published:
        return True
    
    return False


@frappe.whitelist()
def increment_view_count(product):
    frappe.db.sql("""
        UPDATE `tabCraft Product`
        SET total_views = total_views + 1
        WHERE name = %s
    """, product)
    frappe.db.commit()
