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
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "fieldname": "customer_name",
            "label": _("Name"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "total_orders",
            "label": _("Total Orders"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "total_spent",
            "label": _("Total Spent"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "average_order_value",
            "label": _("Avg Order Value"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "loyalty_points",
            "label": _("Loyalty Points"),
            "fieldtype": "Int",
            "width": 100
        },
        {
            "fieldname": "loyalty_tier",
            "label": _("Loyalty Tier"),
            "fieldtype": "Data",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters.get("loyalty_tier"):
        conditions.append(f"loyalty_tier = '{filters['loyalty_tier']}'")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT
            cu.name as customer,
            cu.customer_name,
            COUNT(co.name) as total_orders,
            SUM(co.total_amount) as total_spent,
            AVG(co.total_amount) as average_order_value,
            cu.loyalty_points,
            cu.loyalty_tier
        FROM
            `tabCustomer Profile` cu
            LEFT JOIN `tabCraft Order` co ON cu.email = co.customer AND co.docstatus = 1
        {where_clause}
        GROUP BY
            cu.name, cu.customer_name, cu.loyalty_points, cu.loyalty_tier
        ORDER BY
            total_spent DESC
    """
    
    return frappe.db.sql(query, as_dict=1)
