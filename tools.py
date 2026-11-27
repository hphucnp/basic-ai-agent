inventory = {
    "iphone-16-pro": 15,
    "macbook-pro": 5,
    "airpods-pro": 0,
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
    }
]


def check_inventory(product_id: str) -> dict:
    return {
        "product_id": product_id,
        "quantity": inventory.get(product_id, 0),
    }

def get_product_price(product_id: str) -> float:
    return 999.99  # Placeholder price - replace with actual price lookup logic