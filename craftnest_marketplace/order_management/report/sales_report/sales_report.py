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
            "fieldname": "order_id",
            "label": _("Order ID"),
            "fieldtype": "Link",
            "options": "Craft Order",
            "width": 150
        },
        {
            "fieldname": "order_date",
            "label": _("Order Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "fieldname": "product",
            "label": _("Product"),
            "fieldtype": "Data",
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
            "fieldname": "quantity",
            "label": _("Quantity"),
            "fieldtype": "Int",
            "width": 80
        },
        {
            "fieldname": "amount",
            "label": _("Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "payment_status",
            "label": _("Payment"),
            "fieldtype": "Data",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters.get("from_date"):
        conditions.append(f"co.order_date >= '{filters['from_date']}'")
    
    if filters.get("to_date"):
        conditions.append(f"co.order_date <= '{filters['to_date']}'")
    
    if filters.get("customer"):
        conditions.append(f"co.customer = '{filters['customer']}'")
    
    if filters.get("artisan"):
        conditions.append(f"cp.artisan = '{filters['artisan']}'")
    
    if filters.get("status"):
        conditions.append(f"co.status = '{filters['status']}'")
    
    where_clause = " AND " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT
            co.name as order_id,
            co.order_date,
            co.customer,
            cp.product_name as product,
            cp.artisan,
            oi.quantity,
            oi.amount,
            co.status,
            co.payment_status
        FROM
            `tabCraft Order` co
            INNER JOIN `tabOrder Item` oi ON co.name = oi.parent
            INNER JOIN `tabCraft Product` cp ON oi.product = cp.name
        WHERE
            co.docstatus = 1
            {where_clause}
        ORDER BY
            co.order_date DESC
    """
    
    return frappe.db.sql(query, as_dict=1)
