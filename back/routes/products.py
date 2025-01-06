from flask import Blueprint, request, jsonify
from models.models import Product, db
from flask_cors import cross_origin
from sqlalchemy.exc import SQLAlchemyError
from logger import logger
product_blueprint = Blueprint('products', __name__)



@product_blueprint.route('/', methods=['GET'])
def get_products():
    logger.info("Get Products")
    category = request.args.get('category')
    price = request.args.get('price')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))

    query = Product.query

    if category:
        query = query.filter(Product.category == category)
    if price:
        query = query.filter(Product.price <= float(price))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    result = {
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'category': product.category,
                'price': product.price,
                'sku': product.sku
            } for product in pagination.items
        ],
        'pagination': {
            'current_page': pagination.page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'per_page': pagination.per_page
        }
    }
    return jsonify(result)

@product_blueprint.route('/<id>', methods=['GET'])
def get_product(id):
    logger.info("Get Products By Id")
    product = Product.query.get(id)
    if not product:
        logger.error("Product not found")
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category': product.category,
        'price': product.price,
        'sku': product.sku
    })

@product_blueprint.route('/', methods=['POST'])

def create_product():
    data = request.json
    logger.info("Create Product", payload=data)

    if not all(k in data for k in ('name', 'category', 'price', 'sku')):
        logger.error("Missing required fields")
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            category=data['category'],
            price=data['price'],
            sku=data['sku']
        )
        db.session.add(new_product)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    logger.info("Create Product successfully", payload=data)
    return jsonify({'message': 'Product created successfully', 'id': new_product.id,
                    'name': new_product.name}), 201

@product_blueprint.route('/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    logger.info("Update Product", payload=data)
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    try:

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.price = data.get('price', product.price)
        product.sku = data.get('sku', product.sku)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(e)
        return jsonify({'error': str(e)}), 500

    logger.info('Product updated successfully')
    return jsonify({'message': 'Product updated successfully','name': product.name})

@product_blueprint.route('/<id>', methods=['DELETE'])
def delete_product(id):
    logger.info(f"Delete product ${id}")

    product = Product.query.get(id)
    if not product:
        logger.error('Product not found')
        return jsonify({'error': 'Product not found'}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(e)
        return jsonify({'error': str(e)}), 500

    logger.info('Product deleted successfully')
    return jsonify({'message': 'Product deleted successfully'}),204
