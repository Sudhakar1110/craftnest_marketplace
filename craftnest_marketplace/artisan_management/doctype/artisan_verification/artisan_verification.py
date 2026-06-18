# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class ArtisanVerification(Document):
    def validate(self):
        self.validate_artisan()
        self.validate_documents()
    
    def validate_artisan(self):
        if self.artisan:
            artisan = frappe.get_doc("Artisan Profile", self.artisan)
            if artisan.verified:
                frappe.throw(_("Artisan {0} is already verified").format(self.artisan))
    
    def validate_documents(self):
        if self.verification_type == "Complete":
            if not self.id_document:
                frappe.throw(_("ID Document is required for Complete verification"))
            if not self.address_proof:
                frappe.throw(_("Address Proof is required for Complete verification"))
        elif self.verification_type == "Enterprise":
            if not self.id_document:
                frappe.throw(_("ID Document is required for Enterprise verification"))
            if not self.business_license:
                frappe.throw(_("Business License is required for Enterprise verification"))
            if not self.tax_certificate:
                frappe.throw(_("Tax Certificate is required for Enterprise verification"))
    
    def on_update(self):
        if self.workflow_state == "Approved":
            self.approve_artisan()
        elif self.workflow_state == "Rejected":
            self.reject_artisan()
    
    def approve_artisan(self):
        """Mark artisan as verified"""
        if self.artisan:
            artisan = frappe.get_doc("Artisan Profile", self.artisan)
            artisan.verified = 1
            artisan.status = "Active"
            artisan.save(ignore_permissions=True)
            
            frappe.msgprint(_("Artisan {0} has been verified successfully").format(self.artisan))
    
    def reject_artisan(self):
        """Log rejection reason"""
        if self.artisan and self.rejection_reason:
            frappe.msgprint(_("Verification rejected for {0}. Reason: {1}").format(
                self.artisan, self.rejection_reason))


@frappe.whitelist()
def get_pending_verifications():
    """Get all pending artisan verifications"""
    return frappe.get_all(
        "Artisan Verification",
        filters={"workflow_state": ["in", ["Pending Review", "Documents Verified"]]},
        fields=["name", "artisan", "verification_type", "submission_date", "workflow_state"],
        order_by="submission_date asc"
    )


def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    
    if "CraftNest Administrator" in frappe.get_roles(user):
        return None
    
    if "CraftNest Artisan" in frappe.get_roles(user):
        return f"""(`tabArtisan Verification`.artisan in (
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
    
    return False
