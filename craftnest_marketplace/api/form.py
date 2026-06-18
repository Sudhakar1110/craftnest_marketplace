# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe.desk.form.load import getdoc as original_getdoc


@frappe.whitelisted_method
def getdoc(doctype, name, user=None):
    """Override frappe.desk.form.load.getdoc to add CraftNest-specific data"""
    doc = original_getdoc(doctype, name, user=user)

    # Add custom CraftNest data for relevant doctypes
    if doctype == "Craft Order":
        _enrich_craft_order(doc)

    return doc


def _enrich_craft_order(doc):
    """Add artisan details to craft order doc"""
    try:
        from frappe.desk.form.load import run_method
        # Custom enrichment logic can be added here
        pass
    except Exception:
        pass
