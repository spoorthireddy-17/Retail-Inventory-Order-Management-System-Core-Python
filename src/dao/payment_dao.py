# src/dao/payment_dao.py
from typing import Dict, Optional
from datetime import datetime
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        self._sb = get_supabase()
        self.table_name = "payments"

    # Create a new pending payment
    def create_payment(self, order_id: int, amount: float) -> Dict:
        payload = {
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING"
        }
        resp = self._sb.table(self.table_name).insert(payload).execute()
        return resp.data[0] if resp.data else None

    # Update payment status and optionally method & paid_at


    def update_payment(self, payment_id: int, status: str, method: str | None = None) -> Dict:
        payload = {"status": status}
        if method:
            payload["method"] = method
        if status == "PAID":
            payload["paid_at"] = datetime.now().isoformat()
        resp = self._sb.table(self.table_name).update(payload).eq("payment_id", payment_id).execute()
        resp2 = self._sb.table(self.table_name).select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp2.data[0] if resp2.data else None


    # Fetch payment by order_id
    def get_payment_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table(self.table_name).select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    # List all payments
    def list_payments(self, limit: int = 100) -> list[Dict]:
        resp = self._sb.table(self.table_name).select("*").order("payment_id", desc=False).limit(limit).execute()
        return resp.data or []
