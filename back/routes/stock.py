from flask import Blueprint, request, jsonify
from models.models import Stock, Movement, db
from sqlalchemy.exc import SQLAlchemyError
from logger import logger

stock_blueprint = Blueprint('stock', __name__)


@stock_blueprint.route('/stores/<store_id>/inventory', methods=['GET'])
def get_inventory(store_id):
    logger.info("Get Inventory")
    inventory = Stock.query.filter_by(store_id=store_id).all()
    result = [
        {
            'id': item.id,
            'product_id': item.product_id,
            'store_id': item.store_id,
            'quantity': item.quantity,
            'min_stock': item.min_stock
        } for item in inventory
    ]
    logger.info("Get Invetory Done")
    return jsonify(result)


@stock_blueprint.route('/stock', methods=['POST'])
def create_stock():
    data = request.json
    logger.info("Create Stock", payload=data)
    if not all(k in data for k in ('product_id', 'store_id', 'quantity', 'min_stock')):
        logger.error('Missing required fields')
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_product = Stock(
            product_id=data['product_id'],
            store_id=data['store_id'],
            quantity=data['quantity'],
            min_stock=data['min_stock']
        )
        db.session.add(new_product)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f'Error: {e}')
        return jsonify({'error': str(e)}), 500

    logger.info('Stock added successfully')
    return jsonify({'message': 'Stock added successfully'}), 201


@stock_blueprint.route('/inventory/transfer', methods=['POST'])
def transfer_inventory():
    data = request.json
    logger.info('Transfer Inventory', payload=data)
    source_stock = Stock.query.filter_by(
        store_id=data['source_store_id'],
        product_id=data['product_id']
    ).first()
    quantity = int(data['quantity'])
    if not source_stock or source_stock.quantity < quantity:
        logger.error('Insufficient stock')
        return jsonify({'error': 'Insufficient stock'}), 400

    target_stock = Stock.query.filter_by(
        store_id=data['target_store_id'],
        product_id=data['product_id']
    ).first()
    try:

        if not target_stock:
            target_stock = Stock(
                product_id=data['product_id'],
                store_id=data['target_store_id'],
                quantity=0,
                min_stock=0
            )
            db.session.add(target_stock)

        source_stock.quantity -= quantity
        target_stock.quantity += quantity

        movement = Movement(
            product_id=data['product_id'],
            source_store_id=data['source_store_id'],
            target_store_id=data['target_store_id'],
            quantity=quantity,
            type='TRANSFER'
        )

        db.session.add(movement)
        db.session.commit()
        logger.info('Transfer completed successfully')
        return jsonify({'message': 'Transfer completed successfully'})
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f'Error: {e}')
        return jsonify({'error': str(e)}), 500


@stock_blueprint.route('/inventory/alerts', methods=['GET'])
def inventory_alerts():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))
    logger.info('Inventory Alerts')
    low_stock_items = Stock.query.filter(Stock.quantity < Stock.min_stock)
    pagination = low_stock_items.paginate(page=page, per_page=per_page, error_out=False)

    result = {
        'products': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'store_id': item.store_id,
                'quantity': item.quantity,
                'min_stock': item.min_stock
            } for item in low_stock_items
        ],
        'pagination': {
            'current_page': pagination.page,
            'total_pages': pagination.pages,
            'total_items': pagination.total,
            'per_page': pagination.per_page
        }

    }
    logger.info('Alerts Sucessful')
    return jsonify(result)
