import pytest
from main import create_app
from models.base import db
from models.models import Product, Movement, Stock

class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = True

@pytest.fixture
def test_client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_get_products(test_client):
    response = test_client.get('/api/products/')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_create_product(test_client):
    new_product = {
        "id": "1",
        "name": "Product 1",
        "description": "Test product",
        "category": "Category A",
        "price": 10.99,
        "sku": "SKU001"
    }
    response = test_client.post('/api/products/', json=new_product)
    assert response.status_code == 201
    assert response.json['name'] == "Product 1"

def test_update_product(test_client):
    new_product = {
        "id": "1",
        "name": "Product 1",
        "description": "Test product",
        "category": "Category A",
        "price": 10.99,
        "sku": "SKU001"
    }
    test_client.post('/api/products/', json=new_product)
    updated_product = {
        "name": "Updated Product 1",
        "description": "Updated description",
        "category": "Category B",
        "price": 12.99,
        "sku": "SKU002"
    }
    response = test_client.put('/api/products/1', json=updated_product)
    assert response.status_code == 200
    assert response.json['name'] == "Updated Product 1"

def test_delete_product(test_client):
    new_product = {
        "id": "1",
        "name": "Product 1",
        "description": "Test product",
        "category": "Category A",
        "price": 10.99,
        "sku": "SKU001"
    }
    test_client.post('/api/products/', json=new_product)
    response = test_client.delete('/api/products/1')
    assert response.status_code == 204
