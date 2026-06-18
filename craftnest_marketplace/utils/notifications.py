# CraftNest Marketplace - Notifications Utility

import frappe
from frappe import _


def notify_order_confirmed(doc, method):
    """Send notification when order is confirmed"""
    try:
        frappe.sendmail(
            recipients=doc.customer,
            subject=_("Order Confirmed - {0}").format(doc.name),
            message=get_order_confirmed_template(doc)
        )
    except Exception as e:
        frappe.log_error(f"Error sending order confirmation: {str(e)}")


def notify_order_shipped(order_name, tracking_number=None, carrier=None):
    """Send notification when order is shipped"""
    try:
        order = frappe.get_doc("Craft Order", order_name)
        
        frappe.sendmail(
            recipients=order.customer,
            subject=_("Your order {0} has been shipped").format(order.name),
            message=get_order_shipped_template(order, tracking_number, carrier)
        )
    except Exception as e:
        frappe.log_error(f"Error sending shipping notification: {str(e)}")


def notify_order_delivered(order_name):
    """Send notification when order is delivered"""
    try:
        order = frappe.get_doc("Craft Order", order_name)
        
        frappe.sendmail(
            recipients=order.customer,
            subject=_("Your order {0} has been delivered").format(order.name),
            message=get_order_delivered_template(order)
        )
    except Exception as e:
        frappe.log_error(f"Error sending delivery notification: {str(e)}")


def notify_low_stock(product_name):
    """Send notification when product stock is low"""
    try:
        product = frappe.get_doc("Craft Product", product_name)
        
        if product.artisan:
            artisan = frappe.get_doc("Artisan Profile", product.artisan)
            
            frappe.sendmail(
                recipients=artisan.email,
                subject=_("Low Stock Alert - {0}").format(product.product_name),
                message=get_low_stock_template(product, artisan)
            )
    except Exception as e:
        frappe.log_error(f"Error sending low stock notification: {str(e)}")


def notify_new_review(product_name, review_data):
    """Send notification when new review is added"""
    try:
        product = frappe.get_doc("Craft Product", product_name)
        
        if product.artisan:
            artisan = frappe.get_doc("Artisan Profile", product.artisan)
            
            frappe.sendmail(
                recipients=artisan.email,
                subject=_("New Review - {0}").format(product.product_name),
                message=get_new_review_template(product, review_data, artisan)
            )
    except Exception as e:
        frappe.log_error(f"Error sending review notification: {str(e)}")


# Email Templates
def get_order_confirmed_template(order):
    return f"""
    <h2>Order Confirmed!</h2>
    <p>Thank you for your order, {order.customer_name}.</p>
    <p><strong>Order ID:</strong> {order.name}</p>
    <p><strong>Order Date:</strong> {order.order_date}</p>
    <p><strong>Total Amount:</strong> ₹{order.total_amount}</p>
    
    <h3>Order Items:</h3>
    <table>
        <tr>
            <th>Product</th>
            <th>Quantity</th>
            <th>Rate</th>
            <th>Amount</th>
        </tr>
        {"".join([f"<tr><td>{item.product_name}</td><td>{item.quantity}</td><td>₹{item.rate}</td><td>₹{item.amount}</td></tr>" for item in order.items])}
    </table>
    
    <p>We will notify you when your order ships.</p>
    """


def get_order_shipped_template(order, tracking_number, carrier):
    tracking_html = f"<p><strong>Tracking Number:</strong> {tracking_number}</p>" if tracking_number else ""
    carrier_html = f"<p><strong>Carrier:</strong> {carrier}</p>" if carrier else ""
    
    return f"""
    <h2>Your order is on its way!</h2>
    <p>Great news! Your order {order.name} has been shipped.</p>
    {tracking_html}
    {carrier_html}
    <p><strong>Expected Delivery:</strong> {order.estimated_delivery or 'Within 5-7 business days'}</p>
    
    <p>Track your package using the tracking number above.</p>
    """


def get_order_delivered_template(order):
    return f"""
    <h2>Your order has been delivered!</h2>
    <p>We hope you love your handcrafted items.</p>
    <p><strong>Order ID:</strong> {order.name}</p>
    <p><strong>Delivered on:</strong> {frappe.utils.today()}</p>
    
    <p>Please take a moment to leave a review for your purchase. Your feedback helps other customers!</p>
    <a href="/review/{order.name}">Write a Review</a>
    """


def get_low_stock_template(product, artisan):
    return f"""
    <h2>Low Stock Alert</h2>
    <p>Dear {artisan.artisan_name},</p>
    <p>The following product is running low on stock:</p>
    
    <h3>{product.product_name}</h3>
    <p><strong>Current Stock:</strong> {product.stock_quantity}</p>
    <p><strong>Low Stock Threshold:</strong> {product.low_stock_threshold}</p>
    
    <p>Please update your stock to avoid missing sales.</p>
    <a href="/app/craft-product/{product.name}">Update Stock</a>
    """


def get_new_review_template(product, review_data, artisan):
    return f"""
    <h2>New Review Received</h2>
    <p>Dear {artisan.artisan_name},</p>
    <p>You have received a new review for {product.product_name}:</p>
    
    <p><strong>Rating:</strong> {'⭐' * review_data.get('rating', 0)}</p>
    <p><strong>Customer:</strong> {review_data.get('customer_name', 'Anonymous')}</p>
    <p><strong>Review:</strong> {review_data.get('review_text', '')}</p>
    
    <p>Thank you for maintaining quality products!</p>
    """
