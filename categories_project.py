from tkinter import *
from PIL import Image, ImageTk
import json, os

# --- Load products by category ---
def load_products(category):
    with open("products.json", "r") as f:
        data = json.load(f)  # this is a list
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

# --- Sorting Functions (Quicksort) ---
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

# --- Add to cart function ---
def add_to_cart(product):
    print("Added to cart:", product["name"])

# --- Products Page ---
def products_page(category):
    root = Toplevel()
    root.geometry("1000x672")
    root.title(f"{category} Products")

    # Background
    bg = ImageTk.PhotoImage(Image.open("cat.png").resize((1320, 672)))
    bg_label = Label(root, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0)

    # Title
    title = Label(root, text=f"{category} Products", font=("Arial", 22, "bold"), bg="white")
    title.pack(pady=10)

    # Search + Sorting frame
    top_frame = Frame(root, bg="white")
    top_frame.pack(pady=10)

    search_entry = Entry(top_frame, font=("Arial", 14), width=30)
    search_entry.pack(side=LEFT, padx=5)

    Button(top_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white",
           command=lambda: do_search()).pack(side=LEFT, padx=5)

    # --- Sorting Buttons ---
    sort_frame = Frame(root, bg="white")
    sort_frame.pack(pady=5)

    Button(sort_frame, text="Sort Name ↑", command=lambda: do_sort("name", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Name ↓", command=lambda: do_sort("name", False)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↑", command=lambda: do_sort("price", True)).pack(side=LEFT, padx=5)
    Button(sort_frame, text="Sort Price ↓", command=lambda: do_sort("price", False)).pack(side=LEFT, padx=5)

    # --- Scrollable Canvas ---
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

    # --- Function to display products ---
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

    # --- Search logic ---
    def do_search():
        query = search_entry.get().strip()
        if query:
            results = binary_search_partial(products, query)
            display_products(results)
        else:
            display_products(products)

    # --- Sorting logic ---
    def do_sort(key, ascending=True):
        nonlocal products
        if ascending:
            products = quicksort_asc(products, key)
        else:
            products = quicksort_desc(products, key)
        display_products(products)

    # Load products initially
    products = load_products(category)
    display_products(products)

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

if __name__ == "__main__":
    categories_page()
