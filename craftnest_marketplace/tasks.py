# CraftNest Marketplace - Scheduled Tasks

import frappe
from frappe import _


def send_low_stock_alerts():
    """Send low stock alerts to artisans daily"""
    low_stock_products = frappe.get_all(
        "Craft Product",
        filters={
            "stock_status": ["in", ["Low Stock", "Out of Stock"]],
            "status": "Published"
        },
        fields=["name", "product_name", "stock_quantity", "low_stock_threshold", "artisan"]
    )
    
    for product in low_stock_products:
        try:
            from craftnest_marketplace.utils.notifications import notify_low_stock
            notify_low_stock(product.name)
        except Exception as e:
            frappe.log_error(f"Error sending low stock alert for {product.name}: {str(e)}")


def update_product_rankings():
    """Update product rankings daily"""
    # Update best sellers based on total sales
    products = frappe.get_all(
        "Craft Product",
        filters={"status": "Published"},
        fields=["name", "total_sales"]
    )
    
    # Sort by total sales and update rankings
    sorted_products = sorted(products, key=lambda x: x.total_sales or 0, reverse=True)
    
    for idx, product in enumerate(sorted_products[:100], 1):
        try:
            frappe.db.set_value("Craft Product", product.name, "ranking", idx)
        except Exception as e:
            frappe.log_error(f"Error updating ranking for {product.name}: {str(e)}")


def send_seller_performance_summary():
    """Send weekly performance summary to sellers"""
    # Get all active artisans
    artisans = frappe.get_all(
        "Artisan Profile",
        filters={"status": "Active"},
        fields=["name", "artisan_name", "email", "total_sales"]
    )
    
    for artisan in artisans:
        try:
            # Get artisan's orders for the week
            from datetime import datetime, timedelta
            week_ago = frappe.utils.add_days(frappe.utils.today(), -7)
            
            weekly_orders = frappe.db.sql("""
                SELECT DISTINCT co.name
                FROM `tabCraft Order` co
                INNER JOIN `tabOrder Item` oi ON oi.parent = co.name
                WHERE co.docstatus = 1
                    AND oi.artisan = %s
                    AND co.order_date >= %s
            """, (artisan.name, week_ago), as_dict=1)
            
            weekly_sales = len(weekly_orders)
            
            # Send email if there are orders
            if weekly_sales > 0:
                frappe.sendmail(
                    recipients=artisan.email,
                    subject=_("Your Weekly Performance Summary"),
                    message=f"""
                    <h2>Weekly Performance Summary</h2>
                    <p>Dear {artisan.artisan_name},</p>
                    <p>Here's your weekly performance summary:</p>
                    <ul>
                        <li>New Orders: {weekly_sales}</li>
                        <li>Total Sales (All Time): ₹{artisan.total_sales or 0}</li>
                    </ul>
                    <p>Keep up the great work!</p>
                    """
                )
        except Exception as e:
            frappe.log_error(f"Error sending performance summary to {artisan.email}: {str(e)}")


def generate_monthly_sales_report():
    """Generate and store monthly sales report"""
    from datetime import datetime
    from calendar import monthrange
    
    today = frappe.utils.today()
    month_start = today[:7] + "-01"
    
    # Calculate month end
    year, month = int(today[:4]), int(today[5:7])
    _, last_day = monthrange(year, month)
    month_end = f"{year}-{month:02d}-{last_day:02d}"
    
    # Get monthly orders
    monthly_orders = frappe.get_all(
        "Craft Order",
        filters={
            "docstatus": 1,
            "order_date": ["between", month_start, month_end]
        },
        fields=["name", "total_amount", "status"]
    )
    
    total_sales = sum([o.total_amount for o in monthly_orders])
    total_orders = len(monthly_orders)
    
    # Store report
    report = frappe.get_doc({
        "doctype": "Monthly Sales Report",
        "report_month": f"{year}-{month:02d}",
        "total_orders": total_orders,
        "total_sales": total_sales,
        "average_order_value": total_sales / total_orders if total_orders > 0 else 0
    })
    report.insert(ignore_permissions=True)
