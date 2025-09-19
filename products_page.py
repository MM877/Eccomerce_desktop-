from tkinter import *
from PIL import Image, ImageTk
import json
from tkinter import messagebox 
from cart import add_to_cart, cart_page   # import cart system

# --- Load products by category ---
def load_products(category):
    with open("products.json", "r") as f:
        data = json.load(f)  # this is a list
        # filter items by category field
        return [item for item in data if item["category"] == category]

# --- Binary Search with Partial Match ---
def binary_search_partial(products, query):
    products_sorted = sorted(products, key=lambda x: x["name"].lower())
    query = query.lower()
    results = []

    low, high = 0, len(products_sorted) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_name = products_sorted[mid]["name"].lower()

        if query in mid_name:
            left = mid
            while left >= 0 and query in products_sorted[left]["name"].lower():
                results.append(products_sorted[left])
                left -= 1
            right = mid + 1
            while right < len(products_sorted) and query in products_sorted[right]["name"].lower():
                results.append(products_sorted[right])
                right += 1
            break
        elif mid_name < query:
            low = mid + 1
        else:
            high = mid - 1

    return results

# --- Products Page ---
def products_page(category):
    root = Toplevel()
    root.geometry("1320x672")
    root.title(f"{category} Products")

    # Background
    try:
        bg = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
        bg_label = Label(root, image=bg)
        bg_label.image = bg
        bg_label.place(x=0, y=0)
    except:
        root.configure(bg="#f0f0f0")  # fallback color if image not found

    # Title + Cart Button
    top_frame = Frame(root, bg="white")
    top_frame.pack(pady=10, fill=X)

    Label(top_frame, text=f"{category} Products", font=("Arial", 22, "bold"), bg="white").pack(side=LEFT, padx=20)
    Button(top_frame, text="🛒 Cart", font=("Arial", 14), bg="orange", fg="white",
           command=cart_page).pack(side=RIGHT, padx=20)

    # Search bar
    search_frame = Frame(root, bg="white")
    search_frame.pack(pady=10)

    search_entry = Entry(search_frame, font=("Arial", 14), width=40)
    search_entry.pack(side=LEFT, padx=5)

    # Scrollable Canvas
    canvas = Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=10)

    scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    product_frame = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=product_frame, anchor="nw")

    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    product_frame.bind("<Configure>", update_scroll)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Load products
    products = load_products(category)

    # --- Function to handle add to cart with message ---
    def handle_add_to_cart(product):
        add_to_cart(product)   # This calls the function from cart.py
        messagebox.showinfo("Cart", f"✅ {product['name']} added to cart!")

    # --- Function to display products ---
    def display_products(prod_list):
        # Clear existing products
        for widget in product_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for product in prod_list:
            card = Frame(product_frame, bg="white", bd=2, relief="groove", width=250, height=200)
            card.grid(row=row, column=col, padx=20, pady=20)
            card.grid_propagate(False)  # Maintain fixed size

            Label(card, text=product["name"], font=("Arial", 14, "bold"), bg="white").pack(pady=5)
            Label(card, text=f"Price: ${product['price']}", font=("Arial", 12), bg="white").pack()
            Label(card, text=f"Stock: {product['stock']}", font=("Arial", 10), bg="white", fg="gray").pack()

            Button(card, text="Add to Cart", bg="#2196F3", fg="white",
                   command=lambda p=product: handle_add_to_cart(p)).pack(pady=8)

            col += 1
            if col == 3:  # 3 products per row
                col = 0
                row += 1

        # Update scroll region
        product_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # --- Search logic ---
    def do_search():
        query = search_entry.get().strip()
        if query:
            results = binary_search_partial(products, query)
            display_products(results)
        else:
            display_products(products)

    # Add search button functionality
    Button(search_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=do_search).pack(side=LEFT, padx=5)

    # Display all products initially
    display_products(products)

    root.mainloop()