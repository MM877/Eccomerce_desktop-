import json
import random

# Categories with some brands/authors
CATEGORIES = {
    "Electronics": ["Samsung", "Apple", "Sony", "Dell", "HP"],
    "Clothing": ["Nike", "Adidas", "Puma", "Zara", "H&M"],
    "Books": ["J.K. Rowling", "George Orwell", "J.D. Salinger", "Agatha Christie"],
    "Home": ["Ikea", "Philips", "LG", "Panasonic"],
    "Sports": ["Wilson", "Spalding", "Yonex", "Decathlon"]
}

# Example names
NAMES = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Camera"],
    "Clothing": ["Shirt", "Jacket", "Shoes", "Watch", "Backpack"],
    "Books": ["Harry Potter", "1984", "The Catcher in the Rye", "Murder on the Orient Express"],
    "Home": ["Chair", "Table", "Lamp", "Sofa", "Bed"],
    "Sports": ["Football", "Tennis Racket", "Basketball", "Gloves", "Bicycle"]
}

# Example descriptions
DESCRIPTIONS = [
    "High quality and durable.",
    "Best-selling product.",
    "Customer favorite choice.",
    "Limited edition item.",
    "Comfortable and stylish."
]

def generate_products(num=120):
    products = []
    for i in range(1, num + 1):
        category = random.choice(list(CATEGORIES.keys()))
        name = random.choice(NAMES[category])
        brand = random.choice(CATEGORIES[category])
        price = round(random.uniform(5, 2000), 2)
        year = random.randint(1990, 2024)
        stock = random.randint(1, 100)
        description = random.choice(DESCRIPTIONS)

        products.append({
            "id": i,
            "category": category,
            "name": name,
            "price": price,
            "brand": brand,
            "year": year,
            "description": description,
            "stock": stock
        })
    return products

if __name__ == "__main__":
    data = generate_products(120)
    with open("products.json", "w") as f:
        json.dump(data, f, indent=4)
    print("✅ products.json generated with detailed 120 random products")
