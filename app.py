from flask import Flask, render_template, request, jsonify
import json
import re
import os

app = Flask(__name__)


# =========================
# LOAD DATA
# =========================

def load_orders():
    with open("data/orders.json", "r") as file:
        return json.load(file)


def load_customers():
    with open("data/customers.json", "r") as file:
        return json.load(file)


def load_billing():
    with open("data/billing.json", "r") as file:
        return json.load(file)


def load_faqs():
    with open("data/faq.json", "r") as file:
        return json.load(file)


# =========================
# ORDER FUNCTIONS
# =========================

def get_order(order_id):

    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            return order

    return None


def get_orders_by_customer(customer_id):

    orders = load_orders()

    return [
        order
        for order in orders
        if order["customer_id"] == customer_id
    ]


def get_latest_order(customer_id):

    orders = get_orders_by_customer(customer_id)

    if not orders:
        return None

    orders.sort(
        key=lambda order: order["order_date"],
        reverse=True
    )

    return orders[0]


# =========================
# CUSTOMER FUNCTIONS
# =========================

def get_customer(customer_id):

    customers = load_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return None


# =========================
# BILLING FUNCTIONS
# =========================

def get_billing(customer_id):

    billing_records = load_billing()

    for record in billing_records:
        if record["customer_id"] == customer_id:
            return record

    return None


# =========================
# FAQ FUNCTIONS
# =========================

def find_faq(message):

    faqs = load_faqs()

    message = message.lower()

    for faq in faqs:

        keywords = faq["question"].lower().split()

        if any(word in message for word in keywords):
            return faq["answer"]

    return None


# =========================
# EXTRACTION FUNCTIONS
# =========================

def extract_order_id(message):

    match = re.search(r"ORD\d+", message.upper())

    if match:
        return match.group()

    return None


def extract_customer_id(message):

    match = re.search(r"C\d+", message.upper())

    if match:
        return match.group()

    return None


# =========================
# ROUTES
# =========================

def get_dashboard_stats():

    customers = load_customers()
    orders = load_orders()
    faqs = load_faqs()
    billing = load_billing()

    open_balances = sum(
        1
        for record in billing
        if record["outstanding_balance"] > 0
    )

    return {
        "customers": len(customers),
        "orders": len(orders),
        "faqs": len(faqs),
        "open_balances": open_balances
    }
    
@app.route("/")
def home():

    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        stats=stats
    )

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    message = user_message.lower()

    order_id = extract_order_id(user_message)
    customer_id = extract_customer_id(user_message)

    # =========================
    # ORDER LOOKUP
    # =========================

    if order_id:

        order = get_order(order_id)

        if order:

            response = (
                f"📦 Order Details\n\n"
                f"Order ID: {order['order_id']}\n"
                f"Status: {order['status']}\n"
                f"Order Date: {order['order_date']}\n"
                f"Estimated Delivery: {order['estimated_delivery']}"
            )

        else:

            response = (
                f"❌ I couldn't find order {order_id}."
            )

    # =========================
    # LATEST ORDER
    # =========================

    elif "latest order" in message and customer_id:

        latest = get_latest_order(customer_id)

        if latest:

            response = (
                f"📦 Latest Order\n\n"
                f"Order ID: {latest['order_id']}\n"
                f"Status: {latest['status']}\n"
                f"Order Date: {latest['order_date']}\n"
                f"Estimated Delivery: {latest['estimated_delivery']}"
            )

        else:
            response = "No orders found for that customer."

    # =========================
    # ORDER HISTORY
    # =========================

    elif "orders" in message and customer_id:

        orders = get_orders_by_customer(customer_id)

        if not orders:
            response = "No orders found."

        else:

            response = "📦 Order History\n\n"

            for order in orders:
                response += (
                    f"{order['order_id']} - "
                    f"{order['status']}\n"
                )

    # =========================
    # CUSTOMER LOOKUP
    # =========================

    elif "customer" in message and customer_id:

        customer = get_customer(customer_id)

        if customer:

            response = (
                f"👤 Customer Information\n\n"
                f"Name: {customer['name']}\n"
                f"Customer ID: {customer['customer_id']}"
            )

        else:

            response = "Customer not found."

    # =========================
    # BILLING LOOKUP
    # =========================

    elif any(word in message for word in [
        "billing",
        "balance",
        "payment"
    ]) and customer_id:

        bill = get_billing(customer_id)

        if bill:

            response = (
                f"💳 Billing Summary\n\n"
                f"Customer ID: {bill['customer_id']}\n"
                f"Outstanding Balance: "
                f"${bill['outstanding_balance']}\n"
                f"Last Payment Date: "
                f"{bill['last_payment_date']}"
            )

        else:

            response = (
                "No billing information found."
            )

    # =========================
    # BILLING HELP
    # =========================

    elif any(word in message for word in [
        "billing",
        "balance",
        "invoice",
        "payment",
        "charge"
    ]):

        response = (
            "💳 Billing Help\n\n"
            "Examples:\n"
            "• balance C001\n"
            "• billing C001"
        )

    # =========================
    # ORDER HELP
    # =========================

    elif any(word in message for word in [
        "order",
        "track",
        "delivery",
        "status"
    ]):

        response = (
            "📦 To track an order, provide an Order ID.\n\n"
            "Example:\n"
            "Check ORD102"
        )

    # =========================
    # REFUNDS
    # =========================

    elif any(word in message for word in [
        "refund",
        "return",
        "money back"
    ]):

        response = (
            "↩️ Refund requests can be submitted "
            "within 30 days of delivery."
        )

    # =========================
    # HELP
    # =========================

    elif any(word in message for word in [
        "help",
        "support",
        "assist"
    ]):

        response = (
            "🤖 Nova Support Assistant\n\n"
            "I can help with:\n\n"
            "• Order Tracking\n"
            "• Customer Lookup\n"
            "• Order History\n"
            "• Latest Orders\n"
            "• Billing Questions\n"
            "• Refund Requests\n\n"
            "Try:\n"
            "• ORD102\n"
            "• customer C001\n"
            "• latest order C001\n"
            "• orders C001\n"
            "• balance C001"
        )

    # =========================
    # GREETINGS
    # =========================

    elif any(word in message for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon"
    ]):

        response = (
            "👋 Welcome to Nova Services!\n\n"
            "How can I help you today?"
        )

    # =========================
    # FAQ LOOKUP
    # =========================

    else:

        faq_answer = find_faq(message)

        if faq_answer:

            response = faq_answer

        else:

            response = (
                "🤔 I couldn't understand that request.\n\n"
                "Try:\n"
                "• ORD102\n"
                "• customer C001\n"
                "• latest order C001\n"
                "• orders C001\n"
                "• balance C001\n"
                "• refund policy"
            )

    return jsonify({
        "response": response
    })


@app.route("/test")
def test():
    return {
        "status": "Nova Assistant Running ✅"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)