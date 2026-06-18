# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import flt


class OrderItem(Document):
    def validate(self):
        self.calculate_amount()
        self.set_product_details()
    
    def calculate_amount(self):
        """Calculate item amount"""
        self.amount = flt(self.quantity) * flt(self.rate)
    
    def set_product_details(self):
        """Set product name and artisan from product"""
        if self.product and not self.product_name:
            product = frappe.get_doc("Craft Product", self.product)
            self.product_name = product.product_name
            self.artisan = product.artisan
