from .base import db
import datetime


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    store_id = db.Column(db.String(100), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    min_stock = db.Column(db.Integer, nullable=False)


class Movement(db.Model):
    __tablename__ = 'movements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    source_store_id = db.Column(db.String(100), nullable=True)
    target_store_id = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    type = db.Column(db.Enum('IN', 'OUT', 'TRANSFER', name='movement_type'), nullable=False)

