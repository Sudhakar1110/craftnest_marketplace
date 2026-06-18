from . import __version__ as app_version


app_name = "craftnest_marketplace"
app_title = "CraftNest Marketplace"
app_publisher = "CraftNest"
app_description = "Art & Craft Marketplace for Artisans and Customers"
app_email = "info@craftnest.com"
app_license = "MIT"


# Includes in <head>
# ------------------
app_include_css = "/assets/craftnest_marketplace/css/craftnest.css"
app_include_js = "/assets/craftnest_marketplace/js/craftnest.js"


# include js, css files in header of web template
web_include_css = "/assets/craftnest_marketplace/css/craftnest.css"
web_include_js = "/assets/craftnest_marketplace/js/shopping_cart.js"


# Home Pages
# ----------
home_page = "home"


# website user home page (by Role)
role_home_page = {
    "CraftNest Customer": "my-account",
    "CraftNest Artisan": "seller-dashboard"
}


# Generators
# ----------
website_generators = ["Craft Product"]


# Installation
# ------------
before_install = "craftnest_marketplace.setup.install.before_install"
after_install = "craftnest_marketplace.setup.install.after_install"


# Uninstallation
# --------------
before_uninstall = "craftnest_marketplace.setup.uninstall.before_uninstall"


# Desk Notifications
# ------------------
notification_config = "craftnest_marketplace.notifications.get_notification_config"


# Permissions
# -----------
permission_query_conditions = {
    "Craft Product": "craftnest_marketplace.product_management.doctype.craft_product.craft_product.get_permission_query_conditions",
    "Craft Order": "craftnest_marketplace.order_management.doctype.craft_order.craft_order.get_permission_query_conditions"
}


has_permission = {
    "Craft Product": "craftnest_marketplace.product_management.doctype.craft_product.craft_product.has_permission",
    "Craft Order": "craftnest_marketplace.order_management.doctype.craft_order.craft_order.has_permission"
}


# Document Events
# ---------------
doc_events = {
    "Craft Order": {
        "on_submit": "craftnest_marketplace.order_management.doctype.craft_order.craft_order.create_sales_order",
        "on_cancel": "craftnest_marketplace.order_management.doctype.craft_order.craft_order.cancel_sales_order"
    },
    "Craft Product": {
        "validate": "craftnest_marketplace.product_management.doctype.craft_product.craft_product.sync_with_item",
        "on_update": "craftnest_marketplace.product_management.doctype.craft_product.craft_product.update_website"
    },
    "Sales Order": {
        "on_submit": "craftnest_marketplace.utils.notifications.notify_order_confirmed"
    }
}


# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "craftnest_marketplace.tasks.send_low_stock_alerts",
        "craftnest_marketplace.tasks.update_product_rankings"
    ],
    "weekly": [
        "craftnest_marketplace.tasks.send_seller_performance_summary"
    ],
    "monthly": [
        "craftnest_marketplace.tasks.generate_monthly_sales_report"
    ]
}


# Fixtures
# --------
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "CraftNest Administrator",
        "CraftNest Artisan",
        "CraftNest Customer",
        "CraftNest Delivery Staff"
    ]]]},
    {"dt": "Custom Field", "filters": [["module", "=", "CraftNest Marketplace"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "CraftNest Marketplace"]]},
    {"dt": "Workflow"},
    {"dt": "Workflow State"},
    {"dt": "Workflow Action Master"},
    {"dt": "Notification", "filters": [["module", "=", "CraftNest Marketplace"]]},
    {"dt": "Quick List", "filters": [["name", "in", [
        "Recent Artisans", "Recent Products", "Recent Customers",
        "Recent Wishlists", "Pending Orders", "Recent Transactions",
        "Pending Verifications"
    ]]]}
]


# Jinja
# -----
jinja = {
    "methods": [
        "craftnest_marketplace.utils.jinja.get_featured_products",
        "craftnest_marketplace.utils.jinja.get_product_categories",
        "craftnest_marketplace.utils.jinja.get_cart_count"
    ],
    "filters": []
}


# Authentication and authorization
# -----------------------------------
auth_hooks = [
    "craftnest_marketplace.auth.validate"
]


# Translation
# --------------------------------
translatable_doctypes = {
    "Craft Product": ["product_name", "description"],
    "Product Category": ["category_name", "description"]
}
