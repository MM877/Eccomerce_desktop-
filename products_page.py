from tkinter import *
from PIL import Image, ImageTk
import json

# --- Load products by category ---
def load_products(category):
    with open("products.json", "r") as f:
        data = json.load(f)  # this is a list
        # filter items by category field
        return [item for item in data if item["category"] == category]

# --- Add to cart function ---
def add_to_cart(product):
    print("Added to cart:", product["name"])

# --- Products Page ---
def products_page(category):
    root = Toplevel()
    root.geometry("1320x672")
    root.title(f"{category} Products")

    # Background
    bg = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bg_label = Label(root, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0)

    # Title
    title = Label(root, text=f"{category} Products", font=("Arial", 22, "bold"), bg="white")
    title.pack(pady=10)

    # Search bar (UI only)
    search_frame = Frame(root, bg="white")
    search_frame.pack(pady=10)

    search_entry = Entry(search_frame, font=("Arial", 14), width=40)
    search_entry.pack(side=LEFT, padx=5)

    Button(search_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=LEFT, padx=5)

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

    # Show products in cards
    row = 0
    col = 0
    for product in products:
        card = Frame(product_frame, bg="white", bd=2, relief="groove", width=250, height=180)
        card.grid(row=row, column=col, padx=20, pady=20)

        Label(card, text=product["name"], font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        Label(card, text=f"Price: ${product['price']}", font=("Arial", 12), bg="white").pack()
        Label(card, text=f"Stock: {product['stock']}", font=("Arial", 10), bg="white", fg="gray").pack()
        
        Button(card, text="Add to Cart", bg="#2196F3", fg="white",
               command=lambda p=product: add_to_cart(p)).pack(pady=8)

        col += 1
        if col == 3:  # 3 products per row
            col = 0
            row += 1

    root.mainloop()
