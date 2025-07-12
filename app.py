import os
import logging
from flask import Flask

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
# For local development, either:
# Option A: Set environment variable SESSION_SECRET
# Option B: Use a hardcoded key for development:
app.secret_key = "your-secret-key-here-change-for-production"

# In-memory storage for products and data
app.config['PRODUCTS'] = []
app.config['CATEGORIES'] = ['Fruits', 'Vegetables', 'Other']
app.config['NEXT_PRODUCT_ID'] = 1

# Initialize with some sample products for demonstration
def init_sample_products():
    sample_products = [
        {
            'id': 1,
            'name': 'Fresh Apples',
            'category': 'Fruits',
            'price': 300.0,
            'description': 'Crisp and sweet locally grown apples, perfect for snacking or baking.',
            'image_url': 'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=300&h=200&fit=crop&crop=center',
            'in_stock': True,
            'quantity': 50
        },
        {
            'id': 2,
            'name': 'Organic Carrots',
            'category': 'Vegetables',
            'price': 100.0,
            'description': 'Fresh organic carrots harvested from our sustainable farm.',
            'image_url': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=200&fit=crop&crop=center',
            'in_stock': True,
            'quantity': 30
        },
        {
            'id': 3,
            'name': 'Farm Fresh Eggs',
            'category': 'Other',
            'price': 10.0,
            'description': 'Free-range eggs from happy hens, rich in flavor and nutrition.',
            'image_url': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=300&h=200&fit=crop&crop=center',
            'in_stock': True,
            'quantity': 25
        },
        {
            'id': 4,
            'name': 'Sweet Strawberries',
            'category': 'Fruits',
            'price': 50.0,
            'description': 'Juicy, sweet strawberries picked fresh from our fields.',
            'image_url': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=300&h=200&fit=crop&crop=center',
            'in_stock': True,
            'quantity': 20
        },
        {
            'id': 5,
            'name': 'Green Lettuce',
            'category': 'Vegetables',
            'price': 20,
            'description': 'Crisp, fresh lettuce perfect for salads and sandwiches.',
            'image_url': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=300&h=200&fit=crop&crop=center',
            'in_stock': True,
            'quantity': 40
        }
    ]
    
    app.config['PRODUCTS'] = sample_products
    app.config['NEXT_PRODUCT_ID'] = len(sample_products) + 1

# Initialize sample products
init_sample_products()

# Import routes after app is created
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

