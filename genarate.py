import json
import random

# --- Settings ---
NUM_PRODUCTS = 600
NUM_CATEGORIES = 30

# Define realistic categories
categories = [
    "HomeAppliances", "Electronics", "Fashion", "Books", "Sports", "Gaming",
    "Toys", "Furniture", "Beauty", "Groceries", "Stationery", "Jewelry",
    "Automotive", "Health", "Music", "Shoes", "Clothing", "Tools", "Garden",
    "Office", "Pets", "Cameras", "Watches", "Luggage", "Fitness", "Lighting",
    "Baby", "Kitchen", "Outdoors", "Accessories"
]

# Sample product names for variety
sample_products = [
    "Laptop", "Smartphone", "Headphones", "Camera", "Shoes", "Watch", "Backpack",
    "Keyboard", "Mouse", "Monitor", "Tablet", "Charger", "Speaker", "T-Shirt",
    "Jacket", "Jeans", "Sunglasses", "Book", "Perfume", "Ring", "Toy Car",
    "Sofa", "Desk Lamp", "Microwave", "Refrigerator", "Washing Machine",
    "Air Conditioner", "Bicycle", "Gaming Console", "Printer"
]

# Sample brands
brands = [
    "Samsung", "Apple", "Sony", "LG", "Nike", "Adidas", "Dell", "HP",
    "Microsoft", "Asus", "Lenovo", "Puma", "Zara", "Fossil", "Panasonic",
    "Nikon", "Canon", "Philips", "Bosch", "Rolex"
]

products = []

for i in range(NUM_PRODUCTS):
    category = random.choice(categories)
    name = random.choice(sample_products) + f" {i+1}"
    price = round(random.uniform(5, 5000), 2)  # between $5 and $5000
    brand = random.choice(brands)
    year = random.randint(2018, 2025)
    description = f"High-quality {name.lower()} from {brand}, perfect for everyday use."
    stock = random.randint(1, 100)

    product = {
        "id": i + 1,
        "category": category,
        "name": name,
        "price": price,
        "brand": brand,
        "year": year,
        "description": description,
        "stock": stock
    }
    products.append(product)

# Save to products.json
with open("products.json", "w") as f:
    json.dump(products, f, indent=4)

print(f"✅ Generated {NUM_PRODUCTS} products across {NUM_CATEGORIES} categories into products.json")
