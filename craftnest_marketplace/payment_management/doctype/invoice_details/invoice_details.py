# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import flt


class InvoiceDetails(Document):
    def validate(self):
        self.set_customer_details()
        self.calculate_totals()
    
    def set_customer_details(self):
        """Set customer name and email from customer"""
        if self.customer and not self.customer_name:
            customer = frappe.get_doc("Customer", self.customer)
            self.customer_name = customer.customer_name
            self.customer_email = customer.email_id
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        self.subtotal = sum([flt(item.amount) for item in self.items])
        
        # Calculate CGST and SGST (9% each = 18% total GST)
        self.cgst_amount = flt(self.subtotal) * 0.09
        self.sgst_amount = flt(self.subtotal) * 0.09
        self.igst_amount = 0  # IGST if applicable
        
        self.total_tax = self.cgst_amount + self.sgst_amount + self.igst_amount
        self.total_amount = self.subtotal + self.total_tax
        
        # Calculate due amount
        self.due_amount = self.total_amount - self.paid_amount
    
    def update_payment_status(self):
        """Update payment status based on paid amount"""
        if self.paid_amount >= self.total_amount:
            self.payment_status = "Paid"
            self.status = "Paid"
        elif self.paid_amount > 0:
            self.payment_status = "Partially Paid"
        else:
            self.payment_status = "Pending"


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    return None


def has_permission(doc, ptype, user):
    if "CraftNest Administrator" in frappe.get_roles(user):
        return True
    
    return False
