from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os
import login

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

# --- Add to cart ---
def add_to_cart(product):
    print("Added to cart:", product["name"])

# --- Products Page ---
def products_page(category):
    root = Toplevel()
    root.geometry("1000x672")
    root.title(f"{category} Products")

    bg = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bg_label = Label(root, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0)

    title = Label(root, text=f"{category} Products", font=("Arial", 22, "bold"), bg="white")
    title.pack(pady=10)

    top_frame = Frame(root, bg="white")
    top_frame.pack(pady=10)

    search_entry = Entry(top_frame, font=("Arial", 14), width=30)
    search_entry.pack(side=LEFT, padx=5)

    Button(top_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=lambda: do_search()).pack(side=LEFT, padx=5)

    sort_frame = Frame(root, bg="white")
    sort_frame.pack(pady=5)

    Button(sort_frame, text="Sort Name ↑", command=lambda: do_sort("name", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Name ↓", command=lambda: do_sort("name", False)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↑", command=lambda: do_sort("price", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↓", command=lambda: do_sort("price", False)).pack(side=LEFT, padx=5)

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

    def display_products(prod_list):
        for widget in product_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for product in prod_list:
            card = Frame(product_frame, bg="white", bd=2, relief="groove", width=250, height=180)
            card.grid(row=row, column=col, padx=20, pady=20)

            Label(card, text=product["name"], font=("Arial", 14, "bold"), bg="white").pack(pady=5)
            Label(card, text=f"Price: ${product['price']}", font=("Arial", 12), bg="white").pack()
            Label(card, text=f"Stock: {product['stock']}", font=("Arial", 10), bg="white", fg="gray").pack()

            Button(card, text="Add to Cart", bg="#2196F3", fg="white",
                   command=lambda p=product: add_to_cart(p)).pack(pady=8)

            col += 1
            if col == 5:
                col = 0
                row += 1

    def do_search():
        query = search_entry.get().strip()
        if query:
            results = binary_search_partial(products, query)
            display_products(results)
        else:
            display_products(products)

    def do_sort(key, ascending=True):
        nonlocal products
        if ascending:
            products = quicksort_asc(products, key)
        else:
            products = quicksort_desc(products, key)
        display_products(products)

    products = load_products(category)
    display_products(products)

    root.mainloop()

# ---------------- ADMIN FUNCTIONS ----------------
def add_product_form(parent):
    form = Toplevel(parent)
    form.title("Add Product")
    form.geometry("400x300")

    Label(form, text="Name:").pack(pady=5)
    name_entry = Entry(form, width=30)
    name_entry.pack()

    Label(form, text="Category:").pack(pady=5)
    cat_entry = Entry(form, width=30)
    cat_entry.pack()

    Label(form, text="Price:").pack(pady=5)
    price_entry = Entry(form, width=30)
    price_entry.pack()

    Label(form, text="Stock:").pack(pady=5)
    stock_entry = Entry(form, width=30)
    stock_entry.pack()

    def save_product():
        name = name_entry.get().strip()
        cat = cat_entry.get().strip()
        try:
            price = float(price_entry.get())
            stock = int(stock_entry.get())
        except:
            messagebox.showerror("Error", "Invalid price or stock!")
            return

        if not name or not cat:
            messagebox.showerror("Error", "Name and Category required!")
            return

        products = load_all_products()
        products.append({"name": name, "category": cat, "price": price, "stock": stock})
        save_all_products(products)
        messagebox.showinfo("Success", "Product added successfully!")
        form.destroy()

    Button(form, text="Save", bg="#4CAF50", fg="white", command=save_product).pack(pady=15)

def update_product_form(parent):
    form = Toplevel(parent)
    form.title("Update Product")
    form.geometry("400x300")

    Label(form, text="Enter Product Name:").pack(pady=5)
    search_entry = Entry(form, width=30)
    search_entry.pack()

    def search_product():
        name = search_entry.get().strip().lower()
        products = load_all_products()
        for p in products:
            if p["name"].lower() == name:
                show_update_fields(p, products, form)
                return
        messagebox.showerror("Error", "Product not found!")

    Button(form, text="Search", bg="#2196F3", fg="white", command=search_product).pack(pady=10)

def show_update_fields(product, products, form):
    Label(form, text=f"Updating {product['name']}", font=("Arial", 12, "bold")).pack(pady=5)

    Label(form, text="New Price:").pack(pady=5)
    price_entry = Entry(form, width=30)
    price_entry.insert(0, str(product["price"]))
    price_entry.pack()

    Label(form, text="New Stock:").pack(pady=5)
    stock_entry = Entry(form, width=30)
    stock_entry.insert(0, str(product["stock"]))
    stock_entry.pack()

    def save_update():
        try:
            product["price"] = float(price_entry.get())
            product["stock"] = int(stock_entry.get())
        except:
            messagebox.showerror("Error", "Invalid price or stock!")
            return

        save_all_products(products)
        messagebox.showinfo("Success", "Product updated!")
        form.destroy()

    Button(form, text="Save Update", bg="#4CAF50", fg="white", command=save_update).pack(pady=10)

def discount_form(parent):
    form = Toplevel(parent)
    form.title("Apply Discount")
    form.geometry("400x250")

    Label(form, text="Category:").pack(pady=5)
    cat_entry = Entry(form, width=30)
    cat_entry.pack()

    Label(form, text="Discount %:").pack(pady=5)
    discount_entry = Entry(form, width=30)
    discount_entry.pack()

    def apply_discount():
        try:
            discount = float(discount_entry.get())
        except:
            messagebox.showerror("Error", "Invalid discount value!")
            return

        cat = cat_entry.get().strip().lower()
        products = load_all_products()
        updated = False

        for p in products:
            if p["category"].lower() == cat:
                p["price"] = round(p["price"] * (1 - discount / 100), 2)
                updated = True

        if updated:
            save_all_products(products)
            messagebox.showinfo("Success", f"Discount applied to {cat}!")
            form.destroy()
        else:
            messagebox.showerror("Error", "Category not found!")

    Button(form, text="Apply", bg="#FF9800", fg="white", command=apply_discount).pack(pady=15)

# --- Admin Dashboard ---
def admin_dashboard():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Admin Dashboard")

    bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bgLabel = Label(root, image=bgImage)
    bgLabel.image = bgImage
    bgLabel.place(x=0, y=0)

    Label(root, text="Admin Dashboard", font=("Arial", 26, "bold"), bg="white").pack(pady=20)

    Button(root, text="Manage Categories", font=("Arial", 16), bg="#4CAF50", fg="white", width=20,
           command=categories_page).pack(pady=10)

    Button(root, text="Add Product", font=("Arial", 16), bg="#2196F3", fg="white", width=20,
           command=lambda: add_product_form(root)).pack(pady=10)

    Button(root, text="Update Product", font=("Arial", 16), bg="#FF9800", fg="white", width=20,
           command=lambda: update_product_form(root)).pack(pady=10)

    Button(root, text="Apply Discounts", font=("Arial", 16), bg="#9C27B0", fg="white", width=20,
           command=lambda: discount_form(root)).pack(pady=10)

    root.mainloop()

# --- Categories Page ---
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

def categories_page():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Categories")

    bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bgLabel = Label(root, image=bgImage)
    bgLabel.image = bgImage
    bgLabel.place(x=0, y=0)

    categories = load_categories()
    positions = [(30,30), (1050,30), (30,500), (1050,500)]

    for i, cat in enumerate(categories[:4]):
        btn = Button(
            root,
            text=cat,
            font=("Arial", 18, "bold"),
            width=12,
            height=5,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            cursor="hand2",
            command=lambda c=cat: products_page(c)
        )
        btn.place(x=positions[i][0], y=positions[i][1])

    root.mainloop()

# --- MAIN PROGRAM ---
if __name__ == "__main__":
    user_type = login.login_page()
    if user_type == "admin":
        admin_dashboard()
    elif user_type == "user":
        categories_page()
