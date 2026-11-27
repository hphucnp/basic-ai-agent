inventory = {
    "iphone-16-pro": 15,
    "macbook-pro": 5,
    "airpods-pro": 0,
}

orders = {
    "12345": {
        "status": "shipped",
        "tracking_id": "TRACK001"
    }
}

shipments = {
    "TRACK001": {
        "status": "in_transit",
        "estimated_delivery": "2026-11-29",
    }
}

tools = [
    {
        "type": "function",
        "name": "check_inventory",
        "description": "Check available stock for a product.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID in lowercase kebab-case",
                }
            },
            "required": ["product_id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_order",
        "description": "Retrieve order information by order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "track_shipment",
        "description": "Track shipment using its tracking ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_id": {"type": "string"}
            },
            "required": ["tracking_id"],
            "additionalProperties": False,
        },
    },
]


def check_inventory(product_id: str) -> dict:
    return {
        "product_id": product_id,
        "quantity": inventory.get(product_id, 0),
    }

def get_order(order_id: str) -> dict:
    return orders.get(
        order_id,
        {"error": "Order not found"},
    )


def track_shipment(tracking_id: str) -> dict:
    return shipments.get(
        tracking_id,
        {"error": "Shipment not found"},
    )
    
tool_registry = {
    "check_inventory": check_inventory,
    "get_order": get_order,
    "track_shipment": track_shipment,
}