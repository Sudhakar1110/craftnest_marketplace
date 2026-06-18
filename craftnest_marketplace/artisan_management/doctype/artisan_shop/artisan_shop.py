# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import cint
from frappe import _


class ArtisanShop(Document):
    def validate(self):
        self.validate_artisan()
        self.generate_slug()
    
    def generate_slug(self):
        if not self.slug and self.shop_name:
            self.slug = frappe.utils.slugify(self.shop_name)
    
    def validate_artisan(self):
        if self.artisan:
            artisan = frappe.get_doc("Artisan Profile", self.artisan)
            if artisan.status != "Active":
                frappe.throw(_("Cannot create shop. Artisan {0} is not active").format(self.artisan))
            
            # Check if shop already exists for this artisan
            if frappe.db.exists("Artisan Shop", {"artisan": self.artisan, "name": ["!=", self.name]}):
                frappe.throw(_("Shop already exists for this artisan"))
    
    def update_statistics(self):
        """Update shop statistics"""
        self.total_products = frappe.db.count("Craft Product", {"artisan": self.artisan, "status": "Published"})
        
        total_sales_data = frappe.db.sql("""
            SELECT SUM(oi.amount) as total
            FROM `tabOrder Item` oi
            INNER JOIN `tabCraft Order` co ON oi.parent = co.name
            WHERE co.docstatus = 1
            AND oi.product IN (
                SELECT name FROM `tabCraft Product` WHERE artisan = %s
            )
        """, (self.artisan,))
        
        self.total_sales = total_sales_data[0][0] if total_sales_data and total_sales_data[0][0] else 0
        self.save(ignore_permissions=True)
    
    def get_context(self, context):
        context.no_cache = 1
        context.shop = self
        
        # Get artisan details
        context.artisan = frappe.get_doc("Artisan Profile", self.artisan)
        
        # Get shop products
        context.products = frappe.get_all(
            "Craft Product",
            filters={"artisan": self.artisan, "status": "Published", "published": 1},
            fields=["name", "product_name", "route", "main_image", "price", "sale_price", "average_rating", "stock_status"],
            limit=20
        )
        
        # Get shop reviews
        context.reviews = frappe.db.sql("""
            SELECT pr.*, cp.product_name
            FROM `tabProduct Review` pr
            INNER JOIN `tabCraft Product` cp ON pr.product = cp.name
            WHERE cp.artisan = %s
            AND pr.status = 'Approved'
            ORDER BY pr.creation DESC
            LIMIT 10
        """, (self.artisan,), as_dict=1)
        
        return context


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Artisan" in frappe.get_roles(user):
        return f"""(`tabArtisan Shop`.artisan in (
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
