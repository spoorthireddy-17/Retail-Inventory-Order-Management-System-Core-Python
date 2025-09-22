# src/services/customer_service.py
from src.dao.customer_dao import customer_dao
from src.dao.order_dao import OrderDAO  # import OrderDAO
from typing import Dict, List

class CustomerError(Exception):
    pass

class customer_service:
    def __init__(self):
        self.customer_dao = customer_dao()
        self.order_dao = OrderDAO()  # <-- This was missing

    def add_customer(self, name, email, phone, city=None):
        if not name.strip():
            raise CustomerError("Name is required")
        if not email.strip() or "@" not in email:
            raise CustomerError("Invalid email")
        existing = self.customer_dao.get_customer_by_email(email)
        if existing:
            raise CustomerError("Email already exists")
        return self.customer_dao.create_customer(name, email, phone, city)

    def delete_customer(self, cust_id: int) -> Dict:
        # Check customer exists
        c = self.customer_dao.get_customer_by_id(cust_id)
        if not c:
            raise CustomerError("Customer not found")

        # Check if customer has orders
        orders = self.order_dao.list_orders_by_customer(cust_id)
        if orders:
            raise CustomerError("Cannot delete customer: orders exist")

        # Safe to delete
        try:
            return self.customer_dao.delete_customer(cust_id)
        except Exception as e:
            raise CustomerError(str(e))

    def list_customers(self, limit: int = 100, city: str | None = None) -> List[Dict]:
        return self.customer_dao.list_customers(limit, city)
