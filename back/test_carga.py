from locust import HttpUser, TaskSet, task, between


class ProductTasks(TaskSet):

    @task(1)
    def get_products(self):
        self.client.get("/api/products")

    # @task(1)
    # def create_product(self):
    #     self.client.post(
    #         "/api/products",
    #         json={
    #             "name": "Test Product",
    #             "description": "A test product",
    #             "category": "Test Category",
    #             "price": 99.99,
    #             "sku": "TEST123"
    #         },
    #     )
    # @task(1)
    # def create_stock(self):
    #     self.client.post(
    #         "/api/stock",
    #         json={
    #                 "product_id": 1,
    #                 "store_id": 1,
    #                 "quantity": 10,
    #                 "min_stock": 100
    #             },
    #     )
    #
    # @task(1)
    # def transfer_inventory(self):
    #     self.client.post(
    #         "/api/inventory/transfer",
    #         json={
    #             "product_id": "1",
    #             "source_store_id": "1",
    #             "target_store_id": "2",
    #             "quantity": 1
    #         },
    #     )


class WebsiteUser(HttpUser):
    tasks = [ProductTasks]
    wait_time = between(1, 2)
