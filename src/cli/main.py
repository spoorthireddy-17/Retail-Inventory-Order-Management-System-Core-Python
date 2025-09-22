# src/cli/main.py
import argparse
import json
from src.services.product_service import product_service
from src.services.customer_service import customer_service
from src.services.order_service import order_service
from src.services.payment_service import payment_service
from src.services.report_service import report_service
from src.dao.product_dao import product_dao
from src.dao.customer_dao import customer_dao

# Instantiate services and DAOs
product_svc = product_service()
product_dao_inst = product_dao()
customer_dao_inst = customer_dao()
customer_svc = customer_service()
order_svc = order_service()
payment_svc = payment_service()
report_svc = report_service()

# ======================== PRODUCT CMDs ========================
def cmd_product_add(args):
    try:
        p = product_svc.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_dao_inst.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))

# ======================== CUSTOMER CMDs ========================
def cmd_customer_add(args):
    try:
        c = customer_dao_inst.create_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    cs = customer_dao_inst.list_customers(limit=100)
    print(json.dumps(cs, indent=2, default=str))

def cmd_customer_delete(args):
    try:
        deleted = customer_svc.delete_customer(args.cust_id)
        print("Deleted customer:")
        print(json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ======================== ORDER CMDs ========================
def cmd_order_create(args):
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_svc.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_list(args):
    try:
        orders = order_svc.list_orders_by_customer(args.customer)
        print(json.dumps(orders, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_svc.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ======================== PAYMENT CMDs ========================
def cmd_payment_create(args):
    try:
        p = payment_svc.create_pending_payment(args.order, args.amount)
        print("Payment created:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_process(args):
    try:
        p = payment_svc.process_payment(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        p = payment_svc.refund_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ======================== REPORT CMDs ========================
def cmd_report_top_products(args):
    data = report_svc.top_selling_products()
    print(json.dumps(data, indent=2))

def cmd_report_revenue(args):
    revenue = report_svc.total_revenue_last_month()
    print(f"Total Revenue Last Month: {revenue}")

def cmd_report_orders_per_customer(args):
    data = report_svc.orders_per_customer()
    print(json.dumps(data, indent=2))

def cmd_report_frequent_customers(args):
    data = report_svc.frequent_customers()
    print(json.dumps(data, indent=2))

# ======================== BUILD PARSER ========================
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # --- Product ---
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")

    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # --- Customer ---
    pcust = sub.add_parser("customer", help="customer commands")
    pcust_sub = pcust.add_subparsers(dest="action")

    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    deletec = pcust_sub.add_parser("delete")
    deletec.add_argument("--cust_id", type=int, required=True)
    deletec.set_defaults(func=cmd_customer_delete)

    # --- Order ---
    porder = sub.add_parser("order", help="order commands")
    porder_sub = porder.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)

    listo = porder_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    # --- Payment ---
    ppayment = sub.add_parser("payment", help="payment commands")
    ppayment_sub = ppayment.add_subparsers(dest="action")

    createp = ppayment_sub.add_parser("create")
    createp.add_argument("--order", type=int, required=True)
    createp.add_argument("--amount", type=float, required=True)
    createp.set_defaults(func=cmd_payment_create)

    processp = ppayment_sub.add_parser("process")
    processp.add_argument("--order", type=int, required=True)
    processp.add_argument("--method", required=True, choices=["Cash", "Card", "UPI"])
    processp.set_defaults(func=cmd_payment_process)

    refundp = ppayment_sub.add_parser("refund")
    refundp.add_argument("--order", type=int, required=True)
    refundp.set_defaults(func=cmd_payment_refund)

    # --- Reports ---
    preport = sub.add_parser("report", help="report commands")
    preport_sub = preport.add_subparsers(dest="action")

    tprod = preport_sub.add_parser("top_products")
    tprod.set_defaults(func=cmd_report_top_products)

    revenue = preport_sub.add_parser("revenue_last_month")
    revenue.set_defaults(func=cmd_report_revenue)

    orders_cust = preport_sub.add_parser("orders_per_customer")
    orders_cust.set_defaults(func=cmd_report_orders_per_customer)

    freq_cust = preport_sub.add_parser("frequent_customers")
    freq_cust.set_defaults(func=cmd_report_frequent_customers)

    return parser

# ======================== MAIN ========================
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
