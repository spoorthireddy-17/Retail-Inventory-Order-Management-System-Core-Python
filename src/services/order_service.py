# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.dao.product_dao import product_dao
from src.dao.customer_dao import customer_dao

class OrderError(Exception):
    pass

class order_service:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.product_dao = product_dao()
        self.customer_dao = customer_dao()

    # ---------------- Create order ----------------
    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        # Check customer exists
        customer = self.customer_dao.get_customer_by_id(cust_id)
        if not customer:
            raise OrderError(f"Customer {cust_id} not found")

        # Validate products and calculate total
        total = 0
        validated_items = []
        for item in items:
            prod = self.product_dao.get_product_by_id(item["prod_id"])
            if not prod:
                raise OrderError(f"Product {item['prod_id']} not found")
            if (prod.get("stock") or 0) < item["quantity"]:
                raise OrderError(f"Not enough stock for product {prod['name']}")
            total += prod["price"] * item["quantity"]
            validated_items.append({"prod_id": prod["prod_id"], "quantity": item["quantity"], "price": prod["price"]})

        # Deduct stock
        for item in validated_items:
            new_stock = self.product_dao.get_product_by_id(item["prod_id"])["stock"] - item["quantity"]
            self.product_dao.update_product(item["prod_id"], {"stock": new_stock})

        # Create order
        order = self.order_dao.create_order(cust_id, validated_items, total)
        return order

    # ---------------- Get order details ----------------
    def get_order_details(self, order_id: int) -> Dict:
        order = self.order_dao.get_order_details(order_id)
        if not order:
            raise OrderError("Order not found")
        return order

    # ---------------- Cancel order ----------------
    def cancel_order(self, order_id: int) -> Dict:
        order = self.order_dao.get_order_details(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Order cannot be cancelled")
        # Restore stock
        for item in order["items"]:
            prod = self.product_dao.get_product_by_id(item["prod_id"])
            new_stock = (prod.get("stock") or 0) + item["quantity"]
            self.product_dao.update_product(item["prod_id"], {"stock": new_stock})
        # Cancel order
        return self.order_dao.cancel_order(order_id)

    # ---------------- List all orders of a customer ----------------
    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        return self.order_dao.list_orders_by_customer(cust_id)
