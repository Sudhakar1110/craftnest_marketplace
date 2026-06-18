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
            "width": 250
        },
        {
            "fieldname": "artisan",
            "label": _("Artisan"),
            "fieldtype": "Link",
            "options": "Artisan Profile",
            "width": 150
        },
        {
            "fieldname": "total_sales",
            "label": _("Units Sold"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "average_rating",
            "label": _("Avg Rating"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters.get("from_date"):
        conditions.append(f"co.order_date >= '{filters['from_date']}'")
    
    if filters.get("to_date"):
        conditions.append(f"co.order_date <= '{filters['to_date']}'")
    
    if filters.get("artisan"):
        conditions.append(f"cp.artisan = '{filters['artisan']}'")
    
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT
            cp.name as product_name,
            cp.artisan,
            SUM(oi.quantity) as total_sales,
            SUM(oi.amount) as revenue,
            cp.average_rating
        FROM
            `tabCraft Product` cp
            INNER JOIN `tabOrder Item` oi ON cp.name = oi.product
            INNER JOIN `tabCraft Order` co ON oi.parent = co.name
        WHERE
            co.docstatus = 1
            {where_clause}
        GROUP BY
            cp.name, cp.artisan, cp.average_rating
        ORDER BY
            total_sales DESC
        LIMIT 20
    """
    
    return frappe.db.sql(query, as_dict=1)
