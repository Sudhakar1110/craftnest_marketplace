# CraftNest Marketplace - Uninstallation Script

import frappe


def before_uninstall():
    """Run before app uninstallation"""
    frappe.publish_realtime("uninstallation_progress", {"progress": 10, "message": "Starting uninstallation..."})


def after_uninstall():
    """Run after app uninstallation"""
    frappe.publish_realtime("uninstallation_progress", {"progress": 50, "message": "Cleaning up data..."})
    cleanup_data()
    
    frappe.publish_realtime("uninstallation_progress", {"progress": 100, "message": "Uninstallation complete!"})
    
    frappe.publish_realtime("uninstallation_complete", {"message": "CraftNest Marketplace uninstalled successfully!"})


def cleanup_data():
    """Clean up custom data created by the app"""
    # Note: This is a safety measure - actual cleanup happens via cascade delete
    # when the app is uninstalled
    
    # Clear any cached data
    frappe.clear_cache()
    
    frappe.publish_realtime("uninstallation_progress", {"message": "Cleanup complete!"})
