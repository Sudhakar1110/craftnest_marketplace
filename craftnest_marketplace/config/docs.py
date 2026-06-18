from frappe import _


def get_data():
    return [
        {
            "doctype": "DocType",
            "label": _("Artisan Profile"),
            "name": "Artisan Profile",
            "description": "Manage artisan profiles, bank details, and verification status."
        },
        {
            "doctype": "DocType",
            "label": _("Craft Product"),
            "name": "Craft Product",
            "description": "Manage craft products with pricing, inventory, and shipping details."
        },
        {
            "doctype": "DocType",
            "label": _("Craft Order"),
            "name": "Craft Order",
            "description": "Track and manage customer orders for craft products."
        },
        {
            "doctype": "DocType",
            "label": _("Payment Transaction"),
            "name": "Payment Transaction",
            "description": "Record and manage payment transactions."
        },
        {
            "doctype": "DocType",
            "label": _("Customer Profile"),
            "name": "Customer Profile",
            "description": "Manage customer profiles and preferences."
        }
    ]
