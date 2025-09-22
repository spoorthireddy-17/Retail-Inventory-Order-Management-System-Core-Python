# src/dao/order_dao.py
from typing import List, Dict, Optional
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        self._sb = get_supabase()

    # ---------------- Create order ----------------
    def create_order(self, cust_id: int, items: List[Dict], total_amount: float) -> Dict:
        # Insert order
        order_payload = {
            "cust_id": cust_id,           # changed from customer_id
            "total_amount": total_amount,
            "status": "PLACED"
        }
        resp_order = self._sb.table("orders").insert(order_payload).execute()
        order = resp_order.data[0]

        # Insert order_items
        for item in items:
            item_payload = {
                "order_id": order["order_id"],
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]
            }
            self._sb.table("order_items").insert(item_payload).execute()

        return order

    # ---------------- List orders by customer ----------------
    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        resp = self._sb.table("orders").select("*").eq("cust_id", cust_id).execute()
        return resp.data or []

    # ---------------- Get order details ----------------
    def get_order_details(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        order = resp.data[0] if resp.data else None
        if not order:
            return None
        # Fetch items
        items_resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        order["items"] = items_resp.data or []
        return order

    # ---------------- Cancel order ----------------
    def cancel_order(self, order_id: int) -> Optional[Dict]:
        order = self.get_order_details(order_id)
        if not order:
            return None
        if order["status"] != "PLACED":
            raise Exception("Order cannot be cancelled")
        # Update order status
        self._sb.table("orders").update({"status": "CANCELLED"}).eq("order_id", order_id).execute()
        return self.get_order_details(order_id)
    