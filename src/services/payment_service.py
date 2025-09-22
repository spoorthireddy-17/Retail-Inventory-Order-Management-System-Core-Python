# src/services/payment_service.py
from src.dao.payment_dao import PaymentDAO
from src.dao.order_dao import OrderDAO

class PaymentError(Exception):
    pass

class payment_service:
    def __init__(self):
        self.payment_dao = PaymentDAO()
        self.order_dao = OrderDAO()  # assuming you have order_dao implemented

    # Create a pending payment for a new order
    def create_pending_payment(self, order_id: int, amount: float):
        return self.payment_dao.create_payment(order_id, amount)

    # Process payment (mark PAID) and update order status to COMPLETED
    def process_payment(self, order_id: int, method: str):
        payment = self.payment_dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment["status"] != "PENDING":
            raise PaymentError("Payment already processed")
        
        updated_payment = self.payment_dao.update_payment(payment["payment_id"], "PAID", method)
        # Update order status
        self.order_dao._sb.table("orders").update({"status": "COMPLETED"}).eq("order_id", order_id).execute()
        return updated_payment

    # Refund payment (mark REFUNDED) if order is cancelled
    def refund_payment(self, order_id: int):
        payment = self.payment_dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment["status"] != "PAID":
            raise PaymentError("Cannot refund non-paid payment")
        
        return self.payment_dao.update_payment(payment["payment_id"], "REFUNDED")
