from models.models import Product, Movement, Stock

def test_product_creation():
    product = Product(
        id="1",
        name="Test Product",
        description="This is a test product.",
        category="Category A",
        price=19.99,
        sku="SKU001"
    )
    assert product.name == "Test Product"
    assert product.price == 19.99

def test_movements_creation():
    movement = Movement(
        id = 1,
        product_id = "pd1",
        source_store_id = "str1",
        target_store_id = "str2",
        quantity = 10,
        type = "TRANSFER"
    )
    assert movement.product_id == "pd1"
    assert movement.quantity == 10

def test_stock_creation():
    stock = Stock(
        id = 1,
        product_id = "pd1",
        store_id = "str1",
        quantity = 100,
        min_stock = 10,
    )
    assert stock.product_id == "pd1"
    assert stock.quantity == 100
