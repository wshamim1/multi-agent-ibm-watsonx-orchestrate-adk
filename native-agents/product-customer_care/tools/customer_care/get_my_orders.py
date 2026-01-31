from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_my_orders():
    """
    Retrieve detailed information about your recent orders including order status, dates,
    amounts, shipping information, and items included in each order.

    Returns:
      A list of dictionaries, each containing details about a specific order:
              - 'orderId': Unique identifier for the order
              - 'orderDate': Date when the order was placed
              - 'orderStatus': Current status of the order (e.g., 'Delivered', 'Shipped', 'Processing', 'Cancelled')
              - 'deliveryDate': Expected or actual delivery date
              - 'totalAmount': Total order amount including tax and shipping
              - 'shippingAddress': Delivery address for the order
              - 'trackingNumber': Shipping tracking number (if available)
              - 'items': List of items in the order, each with:
                  - 'productId': Product identifier
                  - 'name': Product name
                  - 'quantity': Number of items ordered
                  - 'price': Price per item
    """
    orders_data = [
        {
            "orderId": "ORD1234567",
            "orderDate": "2025-01-15",
            "orderStatus": "Delivered",
            "deliveryDate": "2025-01-20",
            "totalAmount": 159.98,
            "shippingAddress": "123 Main St, Boston, MA 02101",
            "trackingNumber": "TRK9876543210",
            "items": [
                {"productId": "ELEC001", "name": "Wireless Bluetooth Headphones", "quantity": 2, "price": 79.99}
            ]
        },
        {
            "orderId": "ORD7654321",
            "orderDate": "2025-01-25",
            "orderStatus": "Shipped",
            "deliveryDate": "2025-02-02",
            "totalAmount": 349.98,
            "shippingAddress": "123 Main St, Boston, MA 02101",
            "trackingNumber": "TRK1234567890",
            "items": [
                {"productId": "ELEC002", "name": "Smart Watch Pro", "quantity": 1, "price": 299.99},
                {"productId": "SPORT001", "name": "Yoga Mat with Carrying Strap", "quantity": 1, "price": 34.99}
            ]
        },
        {
            "orderId": "ORD9876543",
            "orderDate": "2025-01-28",
            "orderStatus": "Processing",
            "deliveryDate": "2025-02-05",
            "totalAmount": 149.99,
            "shippingAddress": "123 Main St, Boston, MA 02101",
            "trackingNumber": None,
            "items": [
                {"productId": "HOME001", "name": "Stainless Steel Cookware Set", "quantity": 1, "price": 149.99}
            ]
        },
        {
            "orderId": "ORD5555555",
            "orderDate": "2025-01-10",
            "orderStatus": "Cancelled",
            "deliveryDate": None,
            "totalAmount": 0.00,
            "shippingAddress": "123 Main St, Boston, MA 02101",
            "trackingNumber": None,
            "cancellationReason": "Customer requested cancellation",
            "items": [
                {"productId": "BOOK001", "name": "The Art of Programming", "quantity": 2, "price": 49.99}
            ]
        }
    ]

    return orders_data