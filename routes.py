from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app
import models

@app.route('/')
def index():
    """Home page with featured products"""
    products = models.get_products()
    featured_products = products[:6]  # Show first 6 products as featured
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    """Products page with category filtering and search"""
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '')
    
    if search_query:
        products = models.search_products(search_query)
    else:
        products = models.get_products_by_category(category)
    
    categories = app.config['CATEGORIES']
    return render_template('products.html', products=products, categories=categories, 
                         current_category=category, search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = models.get_product_by_id(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to cart"""
    product = models.get_product_by_id(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products'))
    
    if not product['in_stock'] or product['quantity'] <= 0:
        flash('Product is out of stock.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'product_id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'image_url': product['image_url']
        }
    
    session['cart'] = cart
    flash(f'{product["name"]} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for item in cart.values():
        subtotal = item['price'] * item['quantity']
        cart_items.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'image_url': item['image_url']
        })
        total += subtotal
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:product_id>')
def update_cart(product_id):
    """Update cart item quantity"""
    quantity = request.args.get('quantity', type=int)
    
    if 'cart' not in session:
        flash('Cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if quantity <= 0:
            del cart[product_id_str]
            flash('Item removed from cart.', 'info')
        else:
            cart[product_id_str]['quantity'] = quantity
            flash('Cart updated.', 'success')
        
        session['cart'] = cart
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    if 'cart' not in session:
        flash('Cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        session['cart'] = cart
        flash('Item removed from cart.', 'info')
    
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    flash('Cart cleared.', 'info')
    return redirect(url_for('cart'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form for orders and inquiries"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        order_type = request.form.get('order_type')
        
        # Basic validation
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html')
        
        # In a real application, you would send an email or save to database
        flash('Thank you for your message! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/admin')
def admin():
    """Admin dashboard"""
    total_products = len(models.get_products())
    categories = app.config['CATEGORIES']
    
    # Calculate products per category
    category_counts = {}
    for category in categories:
        category_counts[category] = len(models.get_products_by_category(category))
    
    return render_template('admin.html', total_products=total_products, 
                         category_counts=category_counts)

@app.route('/admin/products')
def admin_products():
    """Admin products management"""
    products = models.get_products()
    categories = app.config['CATEGORIES']
    return render_template('admin_products.html', products=products, categories=categories)

@app.route('/admin/add_product', methods=['POST'])
def admin_add_product():
    """Add new product via admin"""
    try:
        product_data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price')),
            'description': request.form.get('description'),
            'image_url': request.form.get('image_url') or None,
            'in_stock': request.form.get('in_stock') == 'on',
            'quantity': int(request.form.get('quantity', 0))
        }
        
        # Basic validation
        if not product_data['name'] or not product_data['category'] or product_data['price'] <= 0:
            flash('Please fill in all required fields with valid values.', 'error')
            return redirect(url_for('admin_products'))
        
        models.add_product(product_data)
        flash('Product added successfully!', 'success')
        
    except ValueError:
        flash('Invalid price or quantity value.', 'error')
    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'error')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def admin_edit_product(product_id):
    """Edit existing product via admin"""
    try:
        product_data = {
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'price': float(request.form.get('price')),
            'description': request.form.get('description'),
            'image_url': request.form.get('image_url') or None,
            'in_stock': request.form.get('in_stock') == 'on',
            'quantity': int(request.form.get('quantity', 0))
        }
        
        # Basic validation
        if not product_data['name'] or not product_data['category'] or product_data['price'] <= 0:
            flash('Please fill in all required fields with valid values.', 'error')
            return redirect(url_for('admin_products'))
        
        updated_product = models.update_product(product_id, product_data)
        if updated_product:
            flash('Product updated successfully!', 'success')
        else:
            flash('Product not found.', 'error')
        
    except ValueError:
        flash('Invalid price or quantity value.', 'error')
    except Exception as e:
        flash(f'Error updating product: {str(e)}', 'error')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/delete_product/<int:product_id>')
def admin_delete_product(product_id):
    """Delete product via admin"""
    deleted_product = models.delete_product(product_id)
    if deleted_product:
        flash('Product deleted successfully!', 'success')
    else:
        flash('Product not found.', 'error')
    
    return redirect(url_for('admin_products'))

# Context processor to make cart item count available in all templates
@app.context_processor
def cart_context():
    cart = session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': cart_count}

