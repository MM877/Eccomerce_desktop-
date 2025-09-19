from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os
import login
from user_dashboard import products_page, load_all_products, save_all_products

# ---------------- ADMIN FUNCTIONS ----------------
def add_product_form(parent):
    form = Toplevel(parent)
    form.title("Add Product")
    form.geometry("400x350")
    form.configure(bg="white")

    Label(form, text="Add New Product", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    Label(form, text="Name:", bg="white").pack(pady=5)
    name_entry = Entry(form, width=30, font=("Arial", 12))
    name_entry.pack()

    Label(form, text="Category:", bg="white").pack(pady=5)
    cat_entry = Entry(form, width=30, font=("Arial", 12))
    cat_entry.pack()

    Label(form, text="Price:", bg="white").pack(pady=5)
    price_entry = Entry(form, width=30, font=("Arial", 12))
    price_entry.pack()

    Label(form, text="Stock:", bg="white").pack(pady=5)
    stock_entry = Entry(form, width=30, font=("Arial", 12))
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

    Button(form, text="Save Product", bg="#4CAF50", fg="white", font=("Arial", 12),
           command=save_product).pack(pady=15)

def update_product_form(parent):
    form = Toplevel(parent)
    form.title("Update Product")
    form.geometry("400x400")
    form.configure(bg="white")

    Label(form, text="Update Product", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    Label(form, text="Enter Product Name:", bg="white").pack(pady=5)
    search_entry = Entry(form, width=30, font=("Arial", 12))
    search_entry.pack()

    def search_product():
        name = search_entry.get().strip().lower()
        products = load_all_products()
        for i, p in enumerate(products):
            if p["name"].lower() == name:
                show_update_fields(p, products, i, form)
                return
        messagebox.showerror("Error", "Product not found!")

    Button(form, text="Search Product", bg="#2196F3", fg="white", font=("Arial", 12),
           command=search_product).pack(pady=10)

def show_update_fields(product, products, index, form):
    # Clear previous widgets if any
    for widget in form.winfo_children()[4:]:  # Keep first 4 widgets
        widget.destroy()

    Label(form, text=f"Updating: {product['name']}", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

    Label(form, text="New Price:", bg="white").pack(pady=5)
    price_entry = Entry(form, width=30, font=("Arial", 12))
    price_entry.insert(0, str(product["price"]))
    price_entry.pack()

    Label(form, text="New Stock:", bg="white").pack(pady=5)
    stock_entry = Entry(form, width=30, font=("Arial", 12))
    stock_entry.insert(0, str(product["stock"]))
    stock_entry.pack()

    def save_update():
        try:
            products[index]["price"] = float(price_entry.get())
            products[index]["stock"] = int(stock_entry.get())
        except:
            messagebox.showerror("Error", "Invalid price or stock!")
            return

        save_all_products(products)
        messagebox.showinfo("Success", "Product updated successfully!")
        form.destroy()

    Button(form, text="Save Changes", bg="#4CAF50", fg="white", font=("Arial", 12),
           command=save_update).pack(pady=15)

def discount_form(parent):
    form = Toplevel(parent)
    form.title("Apply Discount")
    form.geometry("400x300")
    form.configure(bg="white")

    Label(form, text="Apply Discount", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    Label(form, text="Category:", bg="white").pack(pady=5)
    cat_entry = Entry(form, width=30, font=("Arial", 12))
    cat_entry.pack()

    Label(form, text="Discount %:", bg="white").pack(pady=5)
    discount_entry = Entry(form, width=30, font=("Arial", 12))
    discount_entry.pack()

    def apply_discount():
        try:
            discount = float(discount_entry.get())
            if discount < 0 or discount > 100:
                raise ValueError("Discount must be between 0 and 100")
        except:
            messagebox.showerror("Error", "Invalid discount value! Enter a number between 0-100")
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
            messagebox.showinfo("Success", f"{discount}% discount applied to {cat} category!")
            form.destroy()
        else:
            messagebox.showerror("Error", "Category not found!")

    Button(form, text="Apply Discount", bg="#FF9800", fg="white", font=("Arial", 12),
           command=apply_discount).pack(pady=15)

# --- Admin Dashboard ---
def admin_dashboard():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Admin Dashboard")

    try:
        bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
        bgLabel = Label(root, image=bgImage)
        bgLabel.image = bgImage
        bgLabel.place(x=0, y=0)
    except:
        root.configure(bg="#f0f0f0")

    # Title
    title_frame = Frame(root, bg="white", bd=2, relief="raised")
    title_frame.pack(pady=30, padx=50, fill=X)
    Label(title_frame, text="Admin Dashboard", font=("Arial", 26, "bold"), bg="white", fg="#333").pack(pady=15)

    # Button frame
    button_frame = Frame(root, bg="white", bd=2, relief="raised")
    button_frame.pack(pady=20, padx=100)

    Button(button_frame, text="Manage Categories", font=("Arial", 16), bg="#4CAF50", fg="white", width=25, height=2,
           command=categories_page).pack(pady=10)

    Button(button_frame, text="Add Product", font=("Arial", 16), bg="#2196F3", fg="white", width=25, height=2,
           command=lambda: add_product_form(root)).pack(pady=10)

    Button(button_frame, text="Update Product", font=("Arial", 16), bg="#FF9800", fg="white", width=25, height=2,
           command=lambda: update_product_form(root)).pack(pady=10)

    Button(button_frame, text="Apply Discounts", font=("Arial", 16), bg="#9C27B0", fg="white", width=25, height=2,
           command=lambda: discount_form(root)).pack(pady=10)

    Button(button_frame, text="Logout", font=("Arial", 16), bg="#F44336", fg="white", width=25, height=2,
           command=root.destroy).pack(pady=10)

    root.mainloop()
# --- Admin Dashboard ---
def admin_dashboard():
    root = Tk()
    root.geometry("1320x672")
    root.resizable(0, 0)
    root.title("Admin Dashboard")

    try:
        bgImage = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
        bgLabel = Label(root, image=bgImage)
        bgLabel.image = bgImage
        bgLabel.place(x=0, y=0)
    except:
        root.configure(bg="#f0f0f0")

    # Title
    title_frame = Frame(root, bg="white", bd=2, relief="raised")
    title_frame.pack(pady=30, padx=50, fill=X)
    Label(title_frame, text="Admin Dashboard", font=("Arial", 26, "bold"), bg="white", fg="#333").pack(pady=15)

    # Button frame
    button_frame = Frame(root, bg="white", bd=2, relief="raised")
    button_frame.pack(pady=20, padx=100)

    Button(button_frame, text="Manage Categories", font=("Arial", 16), bg="#4CAF50", fg="white", width=25, height=2,
           command=categories_page).pack(pady=10)

    Button(button_frame, text="Add Product", font=("Arial", 16), bg="#2196F3", fg="white", width=25, height=2,
           command=lambda: add_product_form(root)).pack(pady=10)

    Button(button_frame, text="Update Product", font=("Arial", 16), bg="#FF9800", fg="white", width=25, height=2,
           command=lambda: update_product_form(root)).pack(pady=10)

    Button(button_frame, text="Apply Discounts", font=("Arial", 16), bg="#9C27B0", fg="white", width=25, height=2,
           command=lambda: discount_form(root)).pack(pady=10)

    Button(button_frame, text="Logout", font=("Arial", 16), bg="#F44336", fg="white", width=25, height=2,
           command=root.destroy).pack(pady=10)

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