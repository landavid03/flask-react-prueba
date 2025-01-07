from .test_routes import test_client


def test_inventory_transfer(test_client):
    # Setup: Add products and inventory
    product = {
        "id": "1",
        "name": "Product 1",
        "description": "Test product",
        "category": "Category A",
        "price": 10.99,
        "sku": "SKU001"
    }
    test_client.post('/api/products/', json=product)

    stock = {
        "product_id": 1,
        "store_id": 1,
        "quantity": 10,
        "min_stock": 100
    }
    test_client.post('/api/stock', json=stock)

    transfer_data = {
        "product_id": 1,
        "source_store_id": "1",
        "target_store_id": "2",
        "quantity": 5
    }
    response = test_client.post('/api/inventory/transfer', json=transfer_data)
    assert response.status_code == 200
    assert "success" in response.json["message"]
