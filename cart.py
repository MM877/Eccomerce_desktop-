from tkinter import *
import json

# --- Global Cart List ---
cart_items = []  # each element will be a dict {"id":.., "name":.., "price":.., "qty":..}

# --- Add product to cart ---
def add_to_cart(product):
    # check if product already in cart
    for item in cart_items:
        if item["id"] == product["id"]:
            item["qty"] += 1
            return
    # else add new
    cart_items.append({
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "qty": 1
    })

# --- Remove product from cart ---
def remove_from_cart(product_id):
    for item in cart_items:
        if item["id"] == product_id:
            cart_items.remove(item)
            break

# --- Cart Page ---
def cart_page():
    root = Toplevel()
    root.geometry("800x600")
    root.title("🛒 Your Cart")

    Label(root, text="Shopping Cart", font=("Arial", 20, "bold")).pack(pady=10)

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # List cart items
    total_price = 0
    row = 0
    for item in cart_items:
        Label(frame, text=item["name"], font=("Arial", 14)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        Label(frame, text=f"${item['price']}", font=("Arial", 14)).grid(row=row, column=1, padx=10, pady=5)
        Label(frame, text=f"Qty: {item['qty']}", font=("Arial", 14)).grid(row=row, column=2, padx=10, pady=5)

        Button(frame, text="Remove", bg="red", fg="white",
               command=lambda pid=item["id"]: [remove_from_cart(pid), root.destroy(), cart_page()]).grid(row=row, column=3, padx=10, pady=5)

        total_price += item["price"] * item["qty"]
        row += 1

    # Total
    Label(root, text=f"Total: ${total_price:.2f}", font=("Arial", 18, "bold")).pack(pady=10)

    Button(root, text="Checkout", font=("Arial", 14), bg="green", fg="white").pack(pady=5)

    root.mainloop()
