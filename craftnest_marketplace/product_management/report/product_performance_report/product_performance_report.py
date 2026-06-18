# Copyright (c) 2026, CraftNest and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "product_name",
            "label": _("Product"),
            "fieldtype": "Link",
            "options": "Craft Product",
            "width": 200
        },
        {
            "fieldname": "artisan",
            "label": _("Artisan"),
            "fieldtype": "Link",
            "options": "Artisan Profile",
            "width": 150
        },
        {
            "fieldname": "category",
            "label": _("Category"),
            "fieldtype": "Link",
            "options": "Product Category",
            "width": 120
        },
        {
            "fieldname": "price",
            "label": _("Price"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_views",
            "label": _("Views"),
            "fieldtype": "Int",
            "width": 80
        },
        {
            "fieldname": "total_sales",
            "label": _("Units Sold"),
            "fieldtype": "Int",
            "width": 80
        },
        {
            "fieldname": "total_revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "average_rating",
            "label": _("Rating"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 80
        },
        {
            "fieldname": "stock_quantity",
            "label": _("Stock"),
            "fieldtype": "Int",
            "width": 80
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters.get("category"):
        conditions.append(f"category = '{filters['category']}'")
    
    if filters.get("artisan"):
        conditions.append(f"artisan = '{filters['artisan']}'")
    
    if filters.get("status"):
        conditions.append(f"status = '{filters['status']}'")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT
            name as product_name,
            artisan,
            category,
            price,
            total_views,
            total_sales,
            (total_sales * price) as total_revenue,
            average_rating,
            stock_quantity,
            status
        FROM
            `tabCraft Product`
        {where_clause}
        ORDER BY
            total_sales DESC
    """
    
    return frappe.db.sql(query, as_dict=1)
