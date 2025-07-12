from app import app

class Product:
    def __init__(self, id, name, category, price, description, image_url=None, in_stock=True, quantity=0):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.image_url = image_url or f'https://via.placeholder.com/300x200/228B22/FFFFFF?text={name.replace(" ", "+")}'
        self.in_stock = in_stock
        self.quantity = quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'in_stock': self.in_stock,
            'quantity': self.quantity
        }

def get_products():
    """Get all products from in-memory storage"""
    return app.config['PRODUCTS']

def get_product_by_id(product_id):
    """Get a single product by ID"""
    products = get_products()
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def get_products_by_category(category):
    """Get products filtered by category"""
    products = get_products()
    if category == 'all':
        return products
    return [product for product in products if product['category'].lower() == category.lower()]

def add_product(product_data):
    """Add a new product to in-memory storage"""
    products = get_products()
    product_data['id'] = app.config['NEXT_PRODUCT_ID']
    products.append(product_data)
    app.config['NEXT_PRODUCT_ID'] += 1
    return product_data

def update_product(product_id, product_data):
    """Update an existing product"""
    products = get_products()
    for i, product in enumerate(products):
        if product['id'] == product_id:
            product_data['id'] = product_id
            products[i] = product_data
            return product_data
    return None

def delete_product(product_id):
    """Delete a product by ID"""
    products = get_products()
    for i, product in enumerate(products):
        if product['id'] == product_id:
            return products.pop(i)
    return None

def search_products(query):
    """Search products by name or description"""
    products = get_products()
    query = query.lower()
    return [product for product in products 
            if query in product['name'].lower() or query in product['description'].lower()]
