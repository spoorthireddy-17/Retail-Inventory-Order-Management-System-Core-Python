# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase
 
class customer_dao:
    def __init__(self):
        self._sb=get_supabase()
    def create_customer(self,name: str, email: str, phone: str | None = None, city: str | None = None) -> Optional[Dict]:
        """
        Insert a customer and return the inserted row (two-step: insert then select by unique email).
        """
        payload = {"name": name, "email": email}
        if phone is not None:
            payload["phone"] = phone
        if city is not None:
            payload["city"] = city
    
        # Insert (no select chaining)
        self._sb.table("customers").insert(payload).execute()
    
        # Fetch inserted row by unique column (email)
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None
    def get_customer_by_id(self,cust_id: int) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    def get_customer_by_email(self,email: str) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None
    def get_customer_by_city(self,city: str) -> List[Dict]:
        resp = self._sb.table("customers").select("*").eq("city", city).execute()
        return resp.data or []
    def update_customer(self,phone: str, fields: Dict) -> Optional[Dict]:
        """
        Update and then return the updated row (two-step).
        """
        self._sb.table("customers").update(fields).eq("phone", phone).execute()
        resp = self._sb.table("customers").select("*").eq("phone", phone).limit(1).execute()
        return resp.data[0] if resp.data else None
    # Only showing delete_customer (rest unchanged)
    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        # Check if customer has any orders
        resp_orders = self._sb.table("orders").select("*").eq("cust_id", cust_id).limit(1).execute()
        if resp_orders.data:
            raise Exception("Cannot delete customer: they have existing orders.")

        # fetch row before delete (so we can return it)
        resp_before = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None

        # Delete customer
        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return row


    def list_customers(self,limit: int = 100, city: str | None = None) -> List[Dict]:
        q = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []