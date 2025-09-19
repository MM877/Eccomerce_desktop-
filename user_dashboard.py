from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import login
from cart import add_to_cart, cart_page  # import cart system

# --- Utility: Load and Save products ---
def load_all_products():
    if os.path.exists("products.json"):
        with open("products.json", "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_all_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

# --- Load products by category ---
def load_products(category):
    with open("products.json", "r") as f:
        data = json.load(f)
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

# --- Sorting Functions ---
def quicksort_asc(products, key):
    if len(products) <= 1:
        return products
    pivot = products[0]
    less = [x for x in products[1:] if x[key] <= pivot[key]]
    greater = [x for x in products[1:] if x[key] > pivot[key]]
    return quicksort_asc(less, key) + [pivot] + quicksort_asc(greater, key)

def quicksort_desc(products, key):
    if len(products) <= 1:
        return products
    pivot = products[0]
    greater = [x for x in products[1:] if x[key] >= pivot[key]]
    less = [x for x in products[1:] if x[key] < pivot[key]]
    return quicksort_desc(greater, key) + [pivot] + quicksort_desc(less, key)

# --- Products Page with Enhanced Features ---
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

    Button(search_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=lambda: do_search()).pack(side=LEFT, padx=5)

    # Sorting buttons
    sort_frame = Frame(root, bg="white")
    sort_frame.pack(pady=5)

    Button(sort_frame, text="Sort Name ↑", font=("Arial", 10), bg="#607D8B", fg="white",
           command=lambda: do_sort("name", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Name ↓", font=("Arial", 10), bg="#607D8B", fg="white",
           command=lambda: do_sort("name", False)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↑", font=("Arial", 10), bg="#607D8B", fg="white",
           command=lambda: do_sort("price", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↓", font=("Arial", 10), bg="#607D8B", fg="white",
           command=lambda: do_sort("price", False)).pack(side=LEFT, padx=5)

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
            if col == 4:  # 4 products per row for better layout
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

    # --- Sort logic ---
    def do_sort(key, ascending=True):
        nonlocal products
        current_query = search_entry.get().strip()
        
        # If there's a search query, sort the filtered results
        if current_query:
            current_products = binary_search_partial(load_products(category), current_query)
        else:
            current_products = load_products(category)
            
        if ascending:
            sorted_products = quicksort_asc(current_products, key)
        else:
            sorted_products = quicksort_desc(current_products, key)
        
        display_products(sorted_products)

    # Display all products initially
    display_products(products)

    root.mainloop()



# --- Load categories ---
def load_categories():
    if os.path.exists("products.json"):
        with open("products.json", "r") as f:
            try:
                data = json.load(f)
                categories = list({item["category"] for item in data})
                return categories
            except:
                return []
    return []

# --- Categories Page ---
def categories_page():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Product Categories")

    try:
        bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
        bgLabel = Label(root, image=bgImage)
        bgLabel.image = bgImage
        bgLabel.place(x=0, y=0)
    except:
        root.configure(bg="#f0f0f0")

    # Title
    title_frame = Frame(root, bg="white", bd=2, relief="raised")
    title_frame.pack(pady=30, fill=X, padx=50)
    Label(title_frame, text="Product Categories", font=("Arial", 26, "bold"), bg="white", fg="#333").pack(pady=15)

    categories = load_categories()
    
    if not categories:
        Label(root, text="No categories found. Please add some products first.", 
              font=("Arial", 16), bg="white", fg="red").pack(pady=50)
        return

    # Create a frame for category buttons
    cat_frame = Frame(root, bg="white", bd=2, relief="raised")
    cat_frame.pack(pady=30, padx=100, fill=BOTH, expand=True)

    # Position categories in a grid
    row, col = 0, 0
    for i, cat in enumerate(categories):
        btn = Button(
            cat_frame,
            text=cat,
            font=("Arial", 18, "bold"),
            width=15,
            height=3,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            cursor="hand2",
            command=lambda c=cat: products_page(c)
        )
        btn.grid(row=row, column=col, padx=20, pady=20)
        
        col += 1
        if col == 3:  # 3 categories per row
            col = 0
            row += 1

    root.mainloop()

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    user_type = login.login_page()
    if user_type == "admin":
        admin_dashboard()
    elif user_type == "user":
        categories_page()