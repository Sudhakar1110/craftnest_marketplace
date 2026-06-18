from frappe import _


def get_data():
    return [
        {
            "module_name": "CraftNest Dashboard",
            "category": "Modules",
            "label": _("CraftNest Dashboard"),
            "color": "#FF6B6B",
            "icon": "octicon octicon-home",
            "type": "module",
            "description": "Dashboard and Analytics"
        },
        {
            "module_name": "Artisan Management",
            "category": "Modules",
            "label": _("Artisan Management"),
            "color": "#4ECDC4",
            "icon": "octicon octicon-organization",
            "type": "module",
            "description": "Manage Artisans and Shops"
        },
        {
            "module_name": "Product Management",
            "category": "Modules",
            "label": _("Product Management"),
            "color": "#95E1D3",
            "icon": "octicon octicon-package",
            "type": "module",
            "description": "Manage Craft Products"
        },
        {
            "module_name": "Customer Management",
            "category": "Modules",
            "label": _("Customer Management"),
            "color": "#FFE66D",
            "icon": "octicon octicon-people",
            "type": "module",
            "description": "Manage Customers"
        },
        {
            "module_name": "Order Management",
            "category": "Modules",
            "label": _("Order Management"),
            "color": "#A8DADC",
            "icon": "octicon octicon-checklist",
            "type": "module",
            "description": "Manage Orders and Shipping"
        },
        {
            "module_name": "Payment Management",
            "category": "Modules",
            "label": _("Payment Management"),
            "color": "#F4A261",
            "icon": "octicon octicon-credit-card",
            "type": "module",
            "description": "Manage Payments and Invoices"
        }
    ]
