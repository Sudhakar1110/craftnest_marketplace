# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import flt, nowdate, add_days


class CraftOrder(Document):
    def validate(self):
        self.validate_items()
        self.set_customer_name()
        self.calculate_totals()
    
    def validate_items(self):
        if not self.items:
            frappe.throw(_("Order must have at least one item"))
        
        for item in self.items:
            if not item.product:
                frappe.throw(_("Product is required for all items"))
            if item.quantity <= 0:
                frappe.throw(_("Quantity must be greater than 0"))
    
    def set_customer_name(self):
        if self.customer and not self.customer_name:
            self.customer_name = frappe.db.get_value("Customer", self.customer, "customer_name")
    
    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum([flt(item.amount) for item in self.items])
        
        # Calculate tax (18% GST)
        self.tax_amount = flt(self.subtotal) * 0.18
        
        # Calculate total
        self.total_amount = flt(self.subtotal) + flt(self.shipping_charges) + flt(self.tax_amount)
    
    def on_submit(self):
        self.update_stock()
        self.create_sales_order()
        self.send_order_confirmation()
        self.update_customer_statistics()
    
    def on_cancel(self):
        self.reverse_stock()
        self.cancel_sales_order()
    
    def update_stock(self):
        """Update product stock when order is placed"""
        for item in self.items:
            product = frappe.get_doc("Craft Product", item.product)
            product.stock_quantity -= item.quantity
            product.total_sales += item.quantity
            product.save(ignore_permissions=True)
            
            # Update artisan statistics
            self.update_artisan_sales(product.artisan, item.amount)
    
    def reverse_stock(self):
        """Reverse stock when order is cancelled"""
        for item in self.items:
            product = frappe.get_doc("Craft Product", item.product)
            product.stock_quantity += item.quantity
            product.total_sales -= item.quantity
            product.save(ignore_permissions=True)
    
    def update_artisan_sales(self, artisan, amount):
        """Update artisan's total sales"""
        if artisan:
            artisan_doc = frappe.get_doc("Artisan Profile", artisan)
            artisan_doc.total_sales = flt(artisan_doc.total_sales) + flt(amount)
            artisan_doc.save(ignore_permissions=True)
    
    def create_sales_order(self):
        """Create ERPNext Sales Order"""
        try:
            items = []
            for item in self.items:
                product = frappe.get_doc("Craft Product", item.product)
                items.append({
                    "item_code": product.item_code or product.sku,
                    "item_name": product.product_name,
                    "qty": item.quantity,
                    "rate": item.rate,
                    "amount": item.amount
                })
            
            so = frappe.get_doc({
                "doctype": "Sales Order",
                "customer": self.customer,
                "order_type": "Sales",
                "transaction_date": self.order_date,
                "delivery_date": add_days(self.order_date, 7),
                "craft_order": self.name,
                "items": items
            })
            so.insert(ignore_permissions=True)
            so.submit()
            self.sales_order = so.name
            self.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Error creating Sales Order: {str(e)}")
    
    def cancel_sales_order(self):
        """Cancel related Sales Order"""
        if self.sales_order:
            try:
                so = frappe.get_doc("Sales Order", self.sales_order)
                if so.docstatus == 1:
                    so.cancel()
            except Exception as e:
                frappe.log_error(f"Error cancelling Sales Order: {str(e)}")
    
    def send_order_confirmation(self):
        """Send order confirmation email"""
        try:
            frappe.sendmail(
                recipients=self.customer,
                subject=_("Order Confirmation - {0}").format(self.name),
                message=self.get_order_email_template()
            )
        except Exception as e:
            frappe.log_error(f"Error sending order confirmation: {str(e)}")
    
    def get_order_email_template(self):
        """Generate order confirmation email template"""
        items_html = ""
        for item in self.items:
            items_html += f"""
            <tr>
                <td>{item.product_name}</td>
                <td>{item.quantity}</td>
                <td>₹{item.rate}</td>
                <td>₹{item.amount}</td>
            </tr>
            """
        
        return f"""
        <h2>Thank you for your order!</h2>
        <p>Order ID: {self.name}</p>
        <p>Order Date: {self.order_date}</p>
        
        <h3>Order Items:</h3>
        <table>
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Rate</th>
                <th>Amount</th>
            </tr>
            {items_html}
        </table>
        
        <h3>Order Total: ₹{self.total_amount}</h3>
        
        <p>We will notify you when your order ships.</p>
        """
    
    def update_customer_statistics(self):
        """Update customer order statistics"""
        try:
            if self.customer:
                customer_profile = frappe.get_doc("Customer Profile", {"email": self.customer})
                if customer_profile:
                    customer_profile.update_statistics()
        except Exception:
            pass


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Customer" in frappe.get_roles(user):
        return f"`tabCraft Order`.customer = '{user}'"
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    if doc.customer == user:
        return True
    
    return False
