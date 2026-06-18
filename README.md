# CraftNest Marketplace

Art & Craft Marketplace for Artisans and Customers built on Frappe Framework v15.

## Features

- **Artisan Management**: Complete profile management, verification system, and shop creation
- **Product Management**: Rich product listings with categories, galleries, reviews, and ratings
- **Customer Management**: Customer profiles, addresses, wishlists, and loyalty program
- **Order Management**: Complete order workflow from cart to delivery
- **Payment Management**: Multiple payment methods, invoices, and refunds
- **Dashboard**: Real-time analytics with charts and reports

## Installation

```bash
# Get the app
bench get-app craftnest_marketplace https://github.com/Sudhakar1110/craftnest_marketplace.git

# Install on site
bench --site your-site.local install-app craftnest_marketplace

# Run migrations
bench --site your-site.local migrate

# Clear cache and restart
bench --site your-site.local clear-cache
bench restart
```

## Modules

1. **CraftNest Dashboard** - Analytics and overview
2. **Artisan Management** - Manage artisans and shops
3. **Product Management** - Manage craft products
4. **Customer Management** - Manage customers
5. **Order Management** - Manage orders and shipping
6. **Payment Management** - Manage payments and invoices

## Roles

- **CraftNest Administrator** - Full access
- **CraftNest Artisan** - Seller access
- **CraftNest Customer** - Buyer access
- **CraftNest Delivery Staff** - Delivery management

## Reports

- Sales Report
- Product Performance Report
- Top Selling Products
- Customer Order Report

## License

MIT License

## Support

For support, please contact support@craftnest.com
