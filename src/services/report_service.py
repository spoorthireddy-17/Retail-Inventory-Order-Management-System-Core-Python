from src.config import get_supabase

class report_service:
    def __init__(self):
        self._sb = get_supabase()

    # 1️⃣ Top 5 selling products
    def top_selling_products(self):
        resp = self._sb.rpc("top_selling_products").execute()
        return resp.data or []

    # 2️⃣ Total revenue in last month
    def total_revenue_last_month(self):
        resp = self._sb.rpc("revenue_last_month").execute()
        return resp.data[0]["revenue"] if resp.data else 0

    # 3️⃣ Total orders placed by each customer
    def orders_per_customer(self):
        resp = self._sb.rpc("orders_per_customer").execute()
        return resp.data or []

    # 4️⃣ Customers who placed more than 2 orders
    def frequent_customers(self):
        resp = self._sb.rpc("frequent_customers").execute()
        return resp.data or []
