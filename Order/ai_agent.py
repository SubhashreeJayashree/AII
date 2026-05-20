import os
import requests
import google.generativeai as genai

# =========================
# 1. CONFIGURE GEMINI
# =========================
setx GOOGLE_API_KEY "AIzaSyAa53RpNHlU9kjyIuKOzIjnoP-GNDaYQLs"

GOOGLE_API_KEY = os.getenv("AIzaSyAa53RpNHlU9kjyIuKOzIjnoP-GNDaYQLs")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set")

genai.configure(api_key=GOOGLE_API_KEY)

API_URL = "http://127.0.0.1:8000/place-order/"


# =========================
# 2. FUNCTION THE AI CAN CALL
# =========================

def place_order(item_name: str, quantity: int):
    """
    Place an order in the system.

    Args:
        item_name: Name of the item
        quantity: Quantity to order
    """
    response = requests.post(
        API_URL,
        json={
            "item_name": item_name,
            "quantity": quantity
        },
        timeout=10
    )

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to place order"
        }

    data = response.json()

    return {
        "status": "success",
        "order_id": data["id"],
        "message": f"Order placed for {quantity} x {item_name}"
    }


# =========================
# 3. LOAD MODEL WITH TOOLS
# =========================

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[place_order]
)

chat = model.start_chat(enable_automatic_function_calling=True)


# =========================
# 4. TEST PROMPT
# =========================

response = chat.send_message(
    "Please order 3 blue water bottles"
)

print("AI Response:")
print(response.text)
